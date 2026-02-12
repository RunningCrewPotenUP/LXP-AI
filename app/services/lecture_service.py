from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lecture import Lecture
from app.models.baai_lecture import BAAILecture
from app.models.dragonkue_lecture import DragonkueBAAILecture
from app.schemas.lecture import LectureCreate
from app.ai.models import SentenceEmbedder

class LectureService:
    def __init__(self, db: AsyncSession, embedder: SentenceEmbedder):
        self.db = db
        self.embedder = embedder

    async def create_lecture(self, lecture_in: LectureCreate) -> Lecture:
        new_lecture = Lecture(**lecture_in.model_dump())
        self.db.add(new_lecture)

        await self.db.flush()

        text_to_embed = f"{lecture_in.course_title} {lecture_in.section_title} {lecture_in.lecture_title} {lecture_in.script_content or ''}"
        vector = self.embedder.get_embedding(text_to_embed)

        lecture_vector = BAAILecture(
            lecture_id=new_lecture.id,
            vector=vector
        )
        self.db.add(lecture_vector)

        await self.db.commit()
        await self.db.refresh(new_lecture)

        return new_lecture

    async def generate_all_dragonkue_vectors(self, dragonkue_embedder: SentenceEmbedder):
        """모든 lecture 메타데이터로부터 dragonkue 벡터 생성"""
        # 모든 lecture 조회
        result = await self.db.execute(select(Lecture))
        lectures = result.scalars().all()

        generated_count = 0
        skipped_count = 0

        for lecture in lectures:
            # 이미 dragonkue 벡터가 존재하는지 확인
            existing_vector = await self.db.execute(
                select(DragonkueBAAILecture).where(DragonkueBAAILecture.lecture_id == lecture.id)
            )
            if existing_vector.scalar_one_or_none():
                skipped_count += 1
                continue

            # 텍스트 임베딩 생성
            text_to_embed = f"{lecture.course_title} {lecture.section_title} {lecture.lecture_title} {lecture.script_content or ''}"
            vector = dragonkue_embedder.get_embedding(text_to_embed)

            # DragonkueBAAILecture 레코드 생성
            lecture_vector = DragonkueBAAILecture(
                lecture_id=lecture.id,
                vector=vector
            )
            self.db.add(lecture_vector)
            generated_count += 1

        await self.db.commit()

        return {
            "total_lectures": len(lectures),
            "generated": generated_count,
            "skipped": skipped_count
        }