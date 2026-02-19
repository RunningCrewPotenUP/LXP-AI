from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from app.api.dependencies import get_embedder

router = APIRouter()

@router.post(
    "/",
    response_model=ProductResponse,
    summary="상품 등록",
    description="새로운 상품을 등록합니다. 상품명과 설명을 기반으로 BGE-M3 임베딩 벡터를 자동 생성하여 저장합니다. "
                "생성된 벡터는 이후 강좌-상품 간 유사도 추천에 활용됩니다.",
    response_description="등록된 상품 정보",
)
async def add_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder)
):
    service = ProductService(db, embedder)
    new_product = await service.create_product(product_in)

    return ProductResponse.model_validate(new_product)
