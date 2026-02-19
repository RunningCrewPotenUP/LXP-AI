from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_embedder
from app.schemas.lecture import LectureCreate, LectureResponse
from app.services.lecture_service import LectureService

router = APIRouter()

@router.post(
    "/",
    response_model=LectureResponse,
    summary="강좌 등록",
    description="새로운 강좌를 등록합니다. 강좌 제목, 섹션, 강의 제목, 스크립트를 기반으로 BGE-M3 임베딩 벡터를 자동 생성하여 저장합니다. "
                "생성된 벡터는 이후 강좌-상품 간 유사도 추천에 활용됩니다.",
    response_description="등록된 강좌 정보",
)
async def add_lecture(
    lecture_in: LectureCreate,
    db: AsyncSession = Depends(get_db),
    embedder = Depends(get_embedder)
):
    service = LectureService(db, embedder)
    new_lecture = await service.create_lecture(lecture_in)

    return LectureResponse.model_validate(new_lecture)
