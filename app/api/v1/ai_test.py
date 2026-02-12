from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import get_embedder, get_dragonkue_embedder
from app.schemas.ai_test import (
    EmbeddingTestRequest,
    EmbeddingTestResponse,
    BatchEmbeddingTestRequest,
    BatchEmbeddingTestResponse,
    SimilarityTestRequest,
    SimilarityTestResponse
)
from app.ai.models import SentenceEmbedder
import numpy as np

router = APIRouter()

def get_selected_embedder(model_type: str, baai_embedder: SentenceEmbedder, dragonkue_embedder: SentenceEmbedder):
    """모델 타입에 따라 적절한 embedder 반환"""
    if model_type == "baai":
        return baai_embedder
    elif model_type == "dragonkue":
        return dragonkue_embedder
    else:
        raise HTTPException(status_code=400, detail="Invalid model_type. Choose 'baai' or 'dragonkue'")

@router.post("/embedding", response_model=EmbeddingTestResponse)
async def test_single_embedding(
    request: EmbeddingTestRequest,
    baai_embedder: SentenceEmbedder = Depends(get_embedder),
    dragonkue_embedder: SentenceEmbedder = Depends(get_dragonkue_embedder)
):
    """
    단일 텍스트에 대한 임베딩 생성 테스트

    - **text**: 임베딩을 생성할 텍스트
    - **model_type**: 사용할 모델 타입 (baai 또는 dragonkue)
    """
    embedder = get_selected_embedder(request.model_type, baai_embedder, dragonkue_embedder)

    # 임베딩 생성
    vector = embedder.get_embedding(request.text)

    return EmbeddingTestResponse(
        text=request.text,
        model_type=request.model_type,
        vector=vector.tolist() if hasattr(vector, 'tolist') else list(vector),
        vector_dimension=len(vector)
    )

@router.post("/embeddings", response_model=BatchEmbeddingTestResponse)
async def test_batch_embeddings(
    request: BatchEmbeddingTestRequest,
    baai_embedder: SentenceEmbedder = Depends(get_embedder),
    dragonkue_embedder: SentenceEmbedder = Depends(get_dragonkue_embedder)
):
    """
    여러 텍스트에 대한 임베딩 배치 생성 테스트

    - **texts**: 임베딩을 생성할 텍스트 리스트
    - **model_type**: 사용할 모델 타입 (baai 또는 dragonkue)
    """
    embedder = get_selected_embedder(request.model_type, baai_embedder, dragonkue_embedder)

    # 배치 임베딩 생성
    vectors = embedder.get_embeddings(request.texts)

    # numpy array를 list로 변환
    vectors_list = [vec.tolist() if hasattr(vec, 'tolist') else list(vec) for vec in vectors]

    return BatchEmbeddingTestResponse(
        texts=request.texts,
        model_type=request.model_type,
        vectors=vectors_list,
        vector_dimension=len(vectors[0]),
        count=len(vectors)
    )

@router.post("/similarity", response_model=SimilarityTestResponse)
async def test_similarity(
    request: SimilarityTestRequest,
    baai_embedder: SentenceEmbedder = Depends(get_embedder),
    dragonkue_embedder: SentenceEmbedder = Depends(get_dragonkue_embedder)
):
    """
    두 텍스트 간의 유사도 계산 테스트

    - **text_a**: 첫 번째 텍스트
    - **text_b**: 두 번째 텍스트
    - **model_type**: 사용할 모델 타입 (baai 또는 dragonkue)
    """
    embedder = get_selected_embedder(request.model_type, baai_embedder, dragonkue_embedder)

    # 각 텍스트의 임베딩 생성
    vector_a = embedder.get_embedding(request.text_a)
    vector_b = embedder.get_embedding(request.text_b)

    # 유사도 계산 (내적)
    similarity_score = float(SentenceEmbedder.cal_score(vector_a, vector_b))

    return SimilarityTestResponse(
        text_a=request.text_a,
        text_b=request.text_b,
        model_type=request.model_type,
        similarity_score=similarity_score,
        vector_a=vector_a.tolist() if hasattr(vector_a, 'tolist') else list(vector_a),
        vector_b=vector_b.tolist() if hasattr(vector_b, 'tolist') else list(vector_b)
    )

@router.get("/models")
async def get_available_models():
    """
    사용 가능한 AI 모델 목록 반환
    """
    return {
        "models": [
            {
                "type": "baai",
                "name": "BAAI/bge-m3",
                "description": "BAAI BGE-M3 multilingual embedding model"
            },
            {
                "type": "dragonkue",
                "name": "dragonkue/BGE-m3-ko",
                "description": "Dragonkue Korean-optimized BGE-M3 model"
            }
        ]
    }
