from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from app.models.enums import DifficultyEnum


class LectureCreate(BaseModel):
    """강좌 등록 요청 스키마"""

    lecture_id: int = Field(
        description="외부 시스템의 강의 고유 ID",
        examples=[5105],
    )
    course_title: str = Field(
        description="강좌(코스) 제목",
        examples=["대규모 트래픽에도 끄떡없는 고가용성 아키텍처"],
    )
    course_description: Optional[str] = Field(
        default=None,
        description="강좌(코스) 설명",
        examples=["넷플릭스처럼 장애 상황에서도 서비스가 멈추지 않는 비결"],
    )
    section_title: str = Field(
        description="섹션(챕터) 제목",
        examples=["카오스 엔지니어링"],
    )
    lecture_title: str = Field(
        description="개별 강의 제목",
        examples=["의도적으로 서버를 죽여라: 카오스 몽키 실습"],
    )
    difficulty: Optional[DifficultyEnum] = Field(
        default=None,
        description="강의 난이도 (JUNIOR / MIDDLE / SENIOR / EXPERT)",
        examples=["EXPERT"],
    )
    script_content: Optional[str] = Field(
        default=None,
        description="강의 스크립트(대본) 내용. 임베딩 벡터 생성에 활용됩니다.",
        examples=[
            "완벽한 인프라는 없습니다. 장애는 반드시 일어납니다. 그렇다면 차라리 미리 서버를 죽여보는 건 어떨까요? 도커 컨테이너를 무작위로 종료시키는 카오스 몽키 기법을 통해, 시스템이 스스로 자가 치유(Self-healing)하고 트래픽을 분산하는지 테스트해 보겠습니다. AWS 멀티 AZ 환경에서 데이터 손실 없이 서비스가 유지되는 마법 같은 과정을 직접 확인하세요."
        ],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "lecture_id": 5105,
                    "course_title": "대규모 트래픽에도 끄떡없는 고가용성 아키텍처",
                    "course_description": "넷플릭스처럼 장애 상황에서도 서비스가 멈추지 않는 비결",
                    "section_title": "카오스 엔지니어링",
                    "lecture_title": "의도적으로 서버를 죽여라: 카오스 몽키 실습",
                    "difficulty": "EXPERT",
                    "script_content": "완벽한 인프라는 없습니다. 장애는 반드시 일어납니다. 그렇다면 차라리 미리 서버를 죽여보는 건 어떨까요? 도커 컨테이너를 무작위로 종료시키는 카오스 몽키 기법을 통해, 시스템이 스스로 자가 치유(Self-healing)하고 트래픽을 분산하는지 테스트해 보겠습니다. AWS 멀티 AZ 환경에서 데이터 손실 없이 서비스가 유지되는 마법 같은 과정을 직접 확인하세요.",
                }
            ]
        }
    )


class LectureResponse(LectureCreate):
    """강좌 등록 응답 스키마"""

    id: int = Field(
        description="강좌 고유 ID (자동 생성)",
        examples=[1],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "lecture_id": 5105,
                    "course_title": "대규모 트래픽에도 끄떡없는 고가용성 아키텍처",
                    "course_description": "넷플릭스처럼 장애 상황에서도 서비스가 멈추지 않는 비결",
                    "section_title": "카오스 엔지니어링",
                    "lecture_title": "의도적으로 서버를 죽여라: 카오스 몽키 실습",
                    "difficulty": "EXPERT",
                    "script_content": "완벽한 인프라는 없습니다. 장애는 반드시 일어납니다. 그렇다면 차라리 미리 서버를 죽여보는 건 어떨까요? 도커 컨테이너를 무작위로 종료시키는 카오스 몽키 기법을 통해, 시스템이 스스로 자가 치유(Self-healing)하고 트래픽을 분산하는지 테스트해 보겠습니다. AWS 멀티 AZ 환경에서 데이터 손실 없이 서비스가 유지되는 마법 같은 과정을 직접 확인하세요.",
                }
            ]
        },
    )
