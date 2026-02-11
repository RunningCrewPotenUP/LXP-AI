from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.ai.models import SentenceEmbedder
from app.api.v1 import products, lectures

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading BGE-M3 model...")
    app.state.embedder = SentenceEmbedder()
    yield
    del app.state.embedder

app = FastAPI(title="Running Crew API", lifespan=lifespan)
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(lectures.router, prefix="/api/v1/lectures", tags=["Lectures"])