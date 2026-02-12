from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.ai.models import SentenceEmbedder
from app.api.v1 import products, lectures, ai_test, gemini_test

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading BGE-M3 models...")
    app.state.embedder = SentenceEmbedder()
    print("Loading Dragonkue BGE-M3-KO model...")
    app.state.dragonkue_embedder = SentenceEmbedder(model_name='dragonkue/BGE-m3-ko')
    yield
    del app.state.embedder
    del app.state.dragonkue_embedder

app = FastAPI(title="Running Crew API", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(lectures.router, prefix="/api/v1/lectures", tags=["Lectures"])
app.include_router(ai_test.router, prefix="/api/v1/ai-test", tags=["AI Test"])
app.include_router(gemini_test.router, prefix="/api/v1/gemini-test", tags=["Gemini Test"])