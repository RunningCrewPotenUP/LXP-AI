from pydantic import BaseModel, ConfigDict, Field


class RecommendedProduct(BaseModel):
    """유사도 기반 추천 상품 응답 스키마"""

    name: str = Field(
        description="상품명",
        examples=["NVIDIA RTX 5090 Ti 32GB (AI Edition)"],
    )
    price: int = Field(
        description="상품 가격 (원)",
        examples=[3450000],
    )
    image_url: str = Field(
        description="상품 이미지 URL",
        examples=["https://img.example.com/rtx5090ti.jpg"],
    )
    purchase_url: str = Field(
        description="상품 구매 페이지 URL",
        examples=["https://shop.example.com/p/5090ti"],
    )
    similarity_score: float = Field(
        description="코사인 유사도 점수 (0~1)",
        examples=[0.87],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "NVIDIA RTX 5090 Ti 32GB (AI Edition)",
                    "price": 3450000,
                    "image_url": "https://img.example.com/rtx5090ti.jpg",
                    "purchase_url": "https://shop.example.com/p/5090ti",
                    "similarity_score": 0.87,
                }
            ]
        },
    )
