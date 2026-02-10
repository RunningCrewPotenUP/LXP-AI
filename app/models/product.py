from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
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
    embedding = Column(Vector(1536))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
