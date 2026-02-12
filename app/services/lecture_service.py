from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lecture import Lecture
from app.models.baai_lecture import BAAILecture
from app.models.dragonkue_lecture import DragonkueBAAILecture
from app.schemas.lecture import LectureCreate
from app.ai.models import SentenceEmbedder
from app.ai.gemini_client import GeminiClient

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

    async def summarize_and_embed_lecture(self, lecture_id: int, gemini_client: GeminiClient):
        """
        Gemini LLM으로 강의 요약 후 BAAI 모델로 임베딩하여 저장

        1. Lecture 메타데이터 조회
        2. Gemini LLM으로 요약
        3. 요약 결과를 summary_content에 저장
        4. summary_content를 BAAI 임베딩으로 변환
        5. baai_lecture 테이블의 vector에 저장
        """
        # 1. Lecture 조회
        result = await self.db.execute(
            select(Lecture).where(Lecture.id == lecture_id)
        )
        lecture = result.scalar_one_or_none()

        if not lecture:
            raise ValueError(f"Lecture with id {lecture_id} not found")

        # 2. Gemini LLM으로 요약
        summary = gemini_client.summarize_lecture(
            course_title=lecture.course_title,
            course_description=lecture.course_description,
            section_title=lecture.section_title,
            lecture_title=lecture.lecture_title,
            difficulty=lecture.difficulty.value if lecture.difficulty else None,
            script_content=lecture.script_content
        )

        # 3. BAAILecture 조회 또는 생성
        baai_result = await self.db.execute(
            select(BAAILecture).where(BAAILecture.lecture_id == lecture_id)
        )
        baai_lecture = baai_result.scalar_one_or_none()

        if not baai_lecture:
            # BAAILecture 레코드 생성
            baai_lecture = BAAILecture(lecture_id=lecture_id)
            self.db.add(baai_lecture)
            await self.db.flush()

        # 4. summary_content 저장
        baai_lecture.summary_content = summary

        # 5. BAAI 임베딩 생성 및 저장
        vector = self.embedder.get_embedding(summary)
        baai_lecture.vector = vector

        await self.db.commit()
        await self.db.refresh(baai_lecture)

        return {
            "lecture_id": lecture_id,
            "course_title": lecture.course_title,
            "lecture_title": lecture.lecture_title,
            "summary_content": summary,
            "vector_dimension": len(vector)
        }