from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    brand = Column(String(100))
    price = Column(Integer, nullable=False)
    image_url = Column(Text)
    purchase_url = Column(Text)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # 관계 설정
    baai_vectors = relationship("BAAIProduct", back_populates="product", cascade="all, delete-orphan")
    dragonkue_vectors = relationship("DragonkueBAAIProduct", back_populates="product", cascade="all, delete-orphan")