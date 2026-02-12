from sqlalchemy import Column, Integer, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base


class BAAILecture(Base):
    __tablename__ = "baai_lecture"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lecture_id = Column(Integer, ForeignKey("lectures.id", ondelete="CASCADE"), nullable=False)
    vector = Column(Vector(1024))
    created_at = Column(TIMESTAMP, server_default=func.now())

    lecture = relationship("Lecture", back_populates="baai_vectors")