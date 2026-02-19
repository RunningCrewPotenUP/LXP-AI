import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.ai.models import SentenceEmbedder
from app.api.v1 import products, lectures, recommendations

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading BGE-M3 model...")
    app.state.embedder = await asyncio.to_thread(SentenceEmbedder)
    print("Model loaded successfully!")
    yield
    del app.state.embedder

app = FastAPI(
    title="Running Crew API",
    summary="강의 기반 상품 추천 서비스",
    description="강의와 상품의 임베딩 벡터(BGE-M3)를 비교하여 연관 상품을 추천하는 API입니다.",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(lectures.router, prefix="/api/v1/lectures", tags=["Lectures"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])