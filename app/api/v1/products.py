from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService
from app.api.dependencies import get_embedder

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