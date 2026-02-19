from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ProductCreate(BaseModel):
    """상품 등록 요청 스키마"""

    name: str = Field(
        description="상품명",
        examples=["NVIDIA RTX 5090 Ti 32GB (AI Edition)"],
    )
    brand: str = Field(
        description="브랜드명",
        examples=["NVIDIA"],
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
    description: str = Field(
        description="상품 상세 설명. 임베딩 벡터 생성에 활용됩니다.",
        examples=[
            "32GB의 VRAM으로 로컬에서 Llama-3 70B 모델이나 자율형 AI 에이전트를 끊김 없이 돌릴 수 있는 최고의 그래픽카드입니다. ReAct 프롬프팅 연산 속도를 극대화합니다."
        ],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "NVIDIA RTX 5090 Ti 32GB (AI Edition)",
                    "brand": "NVIDIA",
                    "price": 3450000,
                    "image_url": "https://img.example.com/rtx5090ti.jpg",
                    "purchase_url": "https://shop.example.com/p/5090ti",
                    "description": "32GB의 VRAM으로 로컬에서 Llama-3 70B 모델이나 자율형 AI 에이전트를 끊김 없이 돌릴 수 있는 최고의 그래픽카드입니다. ReAct 프롬프팅 연산 속도를 극대화합니다.",
                }
            ]
        }
    )


class ProductResponse(ProductCreate):
    """상품 등록 응답 스키마"""

    id: int = Field(
        description="상품 고유 ID (자동 생성)",
        examples=[1],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "NVIDIA RTX 5090 Ti 32GB (AI Edition)",
                    "brand": "NVIDIA",
                    "price": 3450000,
                    "image_url": "https://img.example.com/rtx5090ti.jpg",
                    "purchase_url": "https://shop.example.com/p/5090ti",
                    "description": "32GB의 VRAM으로 로컬에서 Llama-3 70B 모델이나 자율형 AI 에이전트를 끊김 없이 돌릴 수 있는 최고의 그래픽카드입니다. ReAct 프롬프팅 연산 속도를 극대화합니다.",
                }
            ]
        },
    )
