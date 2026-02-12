from pydantic import BaseModel, Field
from typing import List, Literal

class EmbeddingTestRequest(BaseModel):
    text: str = Field(..., description="Text to generate embedding")
    model_type: Literal["baai", "dragonkue"] = Field(default="baai", description="Model type to use")

class BatchEmbeddingTestRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to generate embeddings")
    model_type: Literal["baai", "dragonkue"] = Field(default="baai", description="Model type to use")

class EmbeddingTestResponse(BaseModel):
    text: str
    model_type: str
    vector: List[float]
    vector_dimension: int

class BatchEmbeddingTestResponse(BaseModel):
    texts: List[str]
    model_type: str
    vectors: List[List[float]]
    vector_dimension: int
    count: int

class SimilarityTestRequest(BaseModel):
    text_a: str = Field(..., description="First text")
    text_b: str = Field(..., description="Second text")
    model_type: Literal["baai", "dragonkue"] = Field(default="baai", description="Model type to use")

class SimilarityTestResponse(BaseModel):
    text_a: str
    text_b: str
    model_type: str
    similarity_score: float
    vector_a: List[float]
    vector_b: List[float]
