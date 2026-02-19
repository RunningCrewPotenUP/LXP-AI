from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.recommendation import RecommendedProduct
from app.services.recommendation_service import RecommendationService

router = APIRouter()


@router.get(
    "/",
    response_model=list[RecommendedProduct],
    summary="강좌 기반 상품 추천",
    description="특정 강좌의 임베딩 벡터와 상품 임베딩 벡터 간 코사인 유사도를 계산하여, "
                "가장 연관도가 높은 상품을 추천합니다.",
    response_description="유사도 점수 내림차순으로 정렬된 추천 상품 목록",
)
async def get_recommendations(
    lecture_id: int = Query(description="추천 기준이 되는 강좌의 lecture_id"),
    limit: int = Query(default=5, description="반환할 추천 상품 수"),
    db: AsyncSession = Depends(get_db),
):
    service = RecommendationService(db)
    rows = await service.get_recommendations(lecture_id, limit)
    return [RecommendedProduct.model_validate(row) for row in rows]
