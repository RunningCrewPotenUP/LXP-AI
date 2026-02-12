from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import asyncio
from app.models.product import Product
from app.models.baai_product import BAAIProduct
from app.models.dragonkue_product import DragonkueBAAIProduct
from app.ai.models import SentenceEmbedder
from app.ai.gemini_client import GeminiClient

class ProductService:
    def __init__(self, db: AsyncSession, embedder: SentenceEmbedder):
        self.db = db
        self.embedder = embedder

    async def create_product(self, product_data):
        new_product = Product(**product_data.dict())
        self.db.add(new_product)

        await self.db.flush()

        combined_text = f"{product_data.name} {product_data.description}"
        vector = self.embedder.get_embedding(combined_text)

        product_vector = BAAIProduct(
            product_id=new_product.id,
            vector=vector
        )
        self.db.add(product_vector)

        await self.db.commit()
        await self.db.refresh(new_product)
        return new_product

    async def generate_all_dragonkue_vectors(self, dragonkue_embedder: SentenceEmbedder):
        """모든 product 메타데이터로부터 dragonkue 벡터 생성"""
        # 모든 product 조회
        result = await self.db.execute(select(Product))
        products = result.scalars().all()

        generated_count = 0
        skipped_count = 0

        for product in products:
            # 이미 dragonkue 벡터가 존재하는지 확인
            existing_vector = await self.db.execute(
                select(DragonkueBAAIProduct).where(DragonkueBAAIProduct.product_id == product.id)
            )
            if existing_vector.scalar_one_or_none():
                skipped_count += 1
                continue

            # 텍스트 임베딩 생성
            combined_text = f"{product.name} {product.description}"
            vector = dragonkue_embedder.get_embedding(combined_text)

            # DragonkueBAAIProduct 레코드 생성
            product_vector = DragonkueBAAIProduct(
                product_id=product.id,
                vector=vector
            )
            self.db.add(product_vector)
            generated_count += 1

        await self.db.commit()

        return {
            "total_products": len(products),
            "generated": generated_count,
            "skipped": skipped_count
        }

    async def summarize_and_embed_all_products(
        self,
        gemini_client: GeminiClient,
        product_ids: Optional[List[int]] = None,
        delay_seconds: float = 12.0
    ):
        """
        상품에 대해 Gemini LLM으로 요약 후 BAAI 모델로 임베딩하여 저장

        1. Product 메타데이터 조회 (product_ids 지정 시 해당 ID만, 아니면 전체)
        2. 각 상품에 대해 Gemini LLM으로 요약
        3. 요약 결과를 summary_content에 저장
        4. summary_content를 BAAI 임베딩으로 변환
        5. baai_product 테이블의 vector에 저장

        Args:
            gemini_client: Gemini API 클라이언트
            product_ids: 처리할 product ID 리스트 (None이면 전체)
            delay_seconds: API 호출 간 지연 시간 (초), 기본 12초 (분당 5회 제한 대응)
        """
        # 1. Product 조회 (ID 지정 또는 전체)
        if product_ids:
            result = await self.db.execute(
                select(Product).where(Product.id.in_(product_ids))
            )
        else:
            result = await self.db.execute(select(Product))
        products = result.scalars().all()

        processed_count = 0
        skipped_count = 0
        error_count = 0
        errors = []

        for product in products:
            try:
                # ORM 객체에서 필요한 데이터를 즉시 추출 (greenlet 문제 방지)
                product_id = product.id
                product_name = product.name
                product_brand = product.brand
                product_description = product.description

                # 2. BAAIProduct 조회 또는 생성
                baai_result = await self.db.execute(
                    select(BAAIProduct).where(BAAIProduct.product_id == product_id)
                )
                baai_product = baai_result.scalar_one_or_none()

                # 이미 summary_content와 vector가 있으면 스킵
                if baai_product and baai_product.summary_content and baai_product.vector is not None:
                    skipped_count += 1
                    continue

                if not baai_product:
                    # BAAIProduct 레코드 생성
                    baai_product = BAAIProduct(product_id=product_id)
                    self.db.add(baai_product)

                # 3. Gemini LLM으로 요약
                summary = gemini_client.summarize_product(
                    name=product_name,
                    brand=product_brand,
                    description=product_description
                )

                # 4. summary_content 저장
                baai_product.summary_content = summary

                # 5. BAAI 임베딩 생성 및 저장
                vector = self.embedder.get_embedding(summary)
                baai_product.vector = vector

                # 각 상품마다 개별 commit (에러 발생 시 다른 상품에 영향 없도록)
                await self.db.commit()
                processed_count += 1

                # Rate limit 대응: API 호출 간 지연
                await asyncio.sleep(delay_seconds)

            except Exception as e:
                # 에러 발생 시 해당 트랜잭션만 롤백
                await self.db.rollback()
                error_count += 1
                errors.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "error": str(e)
                })
                # 에러가 발생해도 다음 상품 처리 계속
                continue

        return {
            "total_products": len(products),
            "processed": processed_count,
            "skipped": skipped_count,
            "errors": error_count,
            "error_details": errors
        }