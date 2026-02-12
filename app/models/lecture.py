from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, BigInteger, Enum, func
from sqlalchemy.orm import relationship
from app.db.base import Base
from .enums import DifficultyEnum

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lecture_id = Column(BigInteger, nullable=False)
    course_title = Column(String(255), nullable=False)
    course_description = Column(String(255))
    section_title = Column(String(255), nullable=False)
    lecture_title = Column(String(255), nullable=False)
    difficulty = Column(Enum(DifficultyEnum, name="difficulty"))
    script_content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    baai_vectors = relationship("BAAILecture", back_populates="lecture", cascade="all, delete-orphan")
    dragonkue_vectors = relationship("DragonkueBAAILecture", back_populates="lecture", cascade="all, delete-orphan")