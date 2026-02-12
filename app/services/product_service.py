from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.product import Product
from app.models.baai_product import BAAIProduct
from app.models.dragonkue_product import DragonkueBAAIProduct
from app.ai.models import SentenceEmbedder

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