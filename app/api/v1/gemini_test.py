from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.dependencies import get_embedder
from app.schemas.gemini_test import LectureSummarizeRequest, LectureSummarizeResponse, ProductSummarizeRequest
from app.services.lecture_service import LectureService
from app.services.product_service import ProductService
from app.ai.gemini_client import get_gemini_client, GeminiClient
from app.ai.models import SentenceEmbedder

router = APIRouter()

@router.post("/lecture/summarize-and-embed", response_model=LectureSummarizeResponse)
async def test_lecture_summarize_and_embed(
    request: LectureSummarizeRequest,
    db: AsyncSession = Depends(get_db),
    embedder: SentenceEmbedder = Depends(get_embedder),
    gemini_client: GeminiClient = Depends(get_gemini_client)
):
    """
    [테스트 API] Gemini LLM으로 강의 요약 후 BAAI 임베딩 생성 및 저장

    **프로세스:**
    1. lectures 테이블에서 강의 메타데이터 조회
    2. Gemini LLM으로 학습 대상, 핵심 기술, 실무 결과물 위주로 요약
    3. 요약 결과를 baai_lecture.summary_content에 저장
    4. summary_content를 BAAI 모델로 임베딩하여 벡터 생성
    5. baai_lecture.vector에 저장

    **프롬프트:**
    이 강의 데이터를 학습 대상, 핵심 기술, 실무 결과물 위주로 요약해줘.
    특히 상품과 매칭될 수 있도록 '학습자가 이 강의를 듣고 나서 필요로 할 도구'의 성격이 문맥에 드러나게 한 문장으로 요약해줘.

    **Parameters:**
    - **lecture_id**: 요약할 강의 ID

    **Returns:**
    - lecture_id: 강의 ID
    - course_title: 강좌명
    - lecture_title: 강의명
    - summary_content: Gemini가 생성한 요약 문장
    - vector_dimension: 생성된 벡터 차원
    - message: 성공 메시지
    """
    try:
        service = LectureService(db, embedder)
        result = await service.summarize_and_embed_lecture(request.lecture_id, gemini_client)

        return LectureSummarizeResponse(
            lecture_id=result["lecture_id"],
            course_title=result["course_title"],
            lecture_title=result["lecture_title"],
            summary_content=result["summary_content"],
            vector_dimension=result["vector_dimension"],
            message="Lecture summarized and embedded successfully"
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing lecture: {str(e)}")


@router.post("/products/summarize-and-embed-all")
async def test_all_products_summarize_and_embed(
    request: ProductSummarizeRequest,
    db: AsyncSession = Depends(get_db),
    embedder: SentenceEmbedder = Depends(get_embedder),
    gemini_client: GeminiClient = Depends(get_gemini_client)
):
    """
    [테스트 API] 상품에 대해 Gemini LLM으로 요약 후 BAAI 임베딩 생성 및 저장

    **프로세스:**
    1. products 테이블에서 상품 메타데이터 조회 (product_ids 지정 시 해당 ID만, 아니면 전체)
    2. 각 상품에 대해 Gemini LLM으로 학습자 중심 요약
    3. 요약 결과를 baai_product.summary_content에 저장
    4. summary_content를 BAAI 모델로 임베딩하여 벡터 생성
    5. baai_product.vector에 저장

    **프롬프트:**
    이 상품 데이터를 요약할 때, '강의 학습자가 실습이나 심화 학습을 위해 왜 이 상품을 사야 하는지'를 중심으로 작성해줘.
    '동사(구축, 구현, 설정)'나 '학습 단계'와 호응하는 단어를 사용해서 한 문장으로 요약해줘.

    **Parameters:**
    - product_ids: 처리할 product ID 리스트 (비어있으면 모든 상품 처리)
    - delay_seconds: API 호출 간 지연 시간 (초), 기본값 12초 (분당 5회 제한 대응)

    **Returns:**
    - total_products: 조회된 상품 수
    - processed: 처리된 상품 수
    - skipped: 이미 처리된 상품 수 (스킵)
    - errors: 에러 발생 수
    - error_details: 에러 상세 내역

    **예시:**
    ```json
    {
      "product_ids": [9, 10, 11],
      "delay_seconds": 12.0
    }
    ```
    """
    try:
        service = ProductService(db, embedder)
        result = await service.summarize_and_embed_all_products(
            gemini_client=gemini_client,
            product_ids=request.product_ids,
            delay_seconds=request.delay_seconds
        )

        return {
            "message": "Products summarized and embedded successfully",
            "details": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing products: {str(e)}")
