from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from app.api.dependencies import get_embedder, get_dragonkue_embedder

router = APIRouter()

@router.post("/", response_model=ProductResponse)
async def add_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder)
):
    service = ProductService(db, embedder)
    new_product = await service.create_product(product_in)

    return ProductResponse.model_validate(new_product)

@router.post("/generate-vectors")
async def generate_dragonkue_vectors(
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder),
    dragonkue_embedder = Depends(get_dragonkue_embedder)
):
    """모든 product 메타데이터로부터 dragonkue 벡터 생성"""
    service = ProductService(db, embedder)
    result = await service.generate_all_dragonkue_vectors(dragonkue_embedder)

    return {
        "message": "Dragonkue vectors generated successfully",
        "details": result
    }