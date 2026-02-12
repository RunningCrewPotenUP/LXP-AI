import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lecture import Lecture
from app.schemas.lecture import LectureCreate
from app.ai.models import SentenceEmbedder

class LectureService:
    def __init__(self, db: AsyncSession, embedder: SentenceEmbedder):
        self.db = db
        self.embedder = embedder

    async def create_lecture(self, lecture_in: LectureCreate) -> Lecture:
        text_to_embed = f"{lecture_in.course_title} {lecture_in.section_title} {lecture_in.lecture_title} {lecture_in.script_content or ''}"
        vector = await asyncio.to_thread(self.embedder.get_embedding, text_to_embed)
        
        new_lecture = Lecture(
            **lecture_in.model_dump(),
            embedding=vector
        )

        self.db.add(new_lecture)
        await self.db.commit()
        await self.db.refresh(new_lecture)
        
        return new_lecture