from pydantic import BaseModel, Field
from typing import Optional, List

class LectureSummarizeRequest(BaseModel):
    lecture_id: int = Field(..., description="요약할 lecture의 ID")

class LectureSummarizeResponse(BaseModel):
    lecture_id: int
    course_title: str
    lecture_title: str
    summary_content: str
    vector_dimension: int
    message: str

class ProductSummarizeRequest(BaseModel):
    product_ids: Optional[List[int]] = Field(None, description="요약할 product ID 리스트 (비어있으면 모든 상품 처리)")
    delay_seconds: Optional[float] = Field(12.0, description="API 호출 간 지연 시간 (초), 기본값 12초 (분당 5회 제한)")
