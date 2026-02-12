from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_embedder, get_dragonkue_embedder
from app.schemas.lecture import LectureCreate, LectureResponse
from app.services.lecture_service import LectureService

router = APIRouter()

@router.post("/", response_model=LectureResponse)
async def add_lecture(
    lecture_in: LectureCreate,
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder)
):
    service = LectureService(db, embedder)
    new_lecture = await service.create_lecture(lecture_in)

    return LectureResponse.model_validate(new_lecture)

@router.post("/generate-vectors")
async def generate_dragonkue_vectors(
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder),
    dragonkue_embedder = Depends(get_dragonkue_embedder)
):
    """모든 lecture 메타데이터로부터 dragonkue 벡터 생성"""
    service = LectureService(db, embedder)
    result = await service.generate_all_dragonkue_vectors(dragonkue_embedder)

    return {
        "message": "Dragonkue vectors generated successfully",
        "details": result
    }