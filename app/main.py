from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.ai.models import SentenceEmbedder

ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading BGE-M3 model...")
    ml_models["embedder"] = SentenceEmbedder()
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World with UV!"}

@app.post("/similarity")
async def check_similarity(sentences: list[str]):
    embedder = ml_models["embedder"]
    embeddings = embedder.get_embedding(sentences)
    
    if len(embeddings) >= 2:
        # 두 벡터 간의 유사도 계산
        dense_score = embedder.cal_score(embeddings[0], embeddings[1])

        return {
            "query": sentences[0],
            "target": sentences[1],
            "similarity_score": float(dense_score)
        }
    
    return {"message": "Need at least 2 sentences"}