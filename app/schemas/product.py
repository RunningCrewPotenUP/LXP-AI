from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    brand: str
    price: int
    image_url: str
    purchase_url: str
    description: str

class ProductResponse(ProductCreate):
    id: int
    class Config: 
        from_attributes = True