from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_embedder
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