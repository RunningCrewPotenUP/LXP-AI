from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.models.enums import DifficultyEnum

class LectureCreate(BaseModel):
    lecture_id: int
    course_title: str
    course_description: Optional[str] = None
    section_title: str
    lecture_title: str
    difficulty: Optional[DifficultyEnum] = None
    script_content: Optional[str] = None

class LectureResponse(LectureCreate):
    id: int
    
    model_config = ConfigDict(from_attributes=True)