from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lecture import Lecture
from app.models.product import Product


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_recommendations(self, lecture_id: int, limit: int) -> list:
        lecture_sub = (
            select(Lecture.embedding)
            .where(Lecture.lecture_id == lecture_id)
            .scalar_subquery()
        )

        similarity = (
            (1 - Product.embedding.cosine_distance(lecture_sub))
            .label("similarity_score")
        )

        stmt = (
            select(
                Product.name,
                Product.price,
                Product.image_url,
                Product.purchase_url,
                similarity,
            )
            .where(lecture_sub.isnot(None))
            .order_by(similarity.desc())
            .limit(limit)
        )

        result = await self.db.execute(stmt)
        return result.all()
