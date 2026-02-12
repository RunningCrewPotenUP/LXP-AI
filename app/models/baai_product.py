from sqlalchemy import Column, Integer, TIMESTAMP, Text, func, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class BAAIProduct(Base):
    __tablename__ = "baai_product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    summary_content = Column(Text, nullable=True)
    vector = Column(Vector(1024))
    created_at = Column(TIMESTAMP, server_default=func.now())

    product = relationship("Product", back_populates="baai_vectors")