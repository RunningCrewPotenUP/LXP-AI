from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional
import time
import re
from app.core.config import settings

class LectureSummary(BaseModel):
    """Pydantic 모델로 Gemini 출력 제한"""
    summary: str = Field(
        ...,
        description="학습 대상, 핵심 기술, 실무 결과물 위주로 요약된 한 문장. 학습자가 이 강의를 듣고 나서 필요로 할 도구의 성격이 드러나야 함."
    )

class ProductSummary(BaseModel):
    """Pydantic 모델로 상품 요약 출력 제한"""
    summary: str = Field(
        ...,
        description="강의 학습자가 실습이나 심화 학습을 위해 왜 이 상품을 사야 하는지를 중심으로 동사나 학습 단계와 호응하는 단어를 사용한 한 문장 요약"
    )

class GeminiClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def summarize_lecture(
        self,
        course_title: str,
        course_description: Optional[str],
        section_title: str,
        lecture_title: str,
        difficulty: Optional[str],
        script_content: Optional[str]
    ) -> str:
        """
        강의 데이터를 Gemini LLM을 사용하여 요약

        Returns:
            str: 요약된 한 문장
        """
        # 강의 데이터 조합
        lecture_data = f"""
강좌명: {course_title}
강좌 설명: {course_description or 'N/A'}
섹션명: {section_title}
강의명: {lecture_title}
난이도: {difficulty or 'N/A'}
스크립트: {script_content or 'N/A'}
"""

        # 프롬프트 구성
        prompt = f"""
다음 강의 데이터를 학습 대상, 핵심 기술, 실무 결과물 위주로 요약해줘.
특히 상품과 매칭될 수 있도록 **'학습자가 이 강의를 듣고 나서 필요로 할 도구'**의 성격이 문맥에 드러나게 한 문장으로 요약해줘.

강의 데이터:
{lecture_data}

요약 (한 문장으로):
"""

        try:
            # 최신 Gemini 모델 사용 (gemini-2.5-flash)
            # 무료 버전에서 지원되지 않으면 gemini-1.5-flash로 폴백
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            summary = response.text.strip()

            # Pydantic 모델로 검증
            lecture_summary = LectureSummary(summary=summary)
            return lecture_summary.summary

        except Exception as e:
            # gemini-2.5-flash 실패 시 gemini-1.5-flash로 재시도
            if '404' in str(e) or 'NOT_FOUND' in str(e):
                try:
                    response = self.client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    summary = response.text.strip()
                    lecture_summary = LectureSummary(summary=summary)
                    return lecture_summary.summary
                except Exception as fallback_error:
                    raise Exception(f"Gemini API 호출 중 오류 발생: {str(fallback_error)}")
            raise Exception(f"Gemini API 호출 중 오류 발생: {str(e)}")

    def summarize_product(
        self,
        name: str,
        brand: Optional[str],
        description: Optional[str]
    ) -> str:
        """
        상품 데이터를 Gemini LLM을 사용하여 요약

        Returns:
            str: 요약된 한 문장
        """
        # 상품 데이터 조합
        product_data = f"""
상품명: {name}
브랜드: {brand or 'N/A'}
설명: {description or 'N/A'}
"""

        # 프롬프트 구성
        prompt = f"""
다음 상품 데이터를 요약할 때, **'강의 학습자가 실습이나 심화 학습을 위해 왜 이 상품을 사야 하는지'**를 중심으로 작성해줘.
**'동사(구축, 구현, 설정)'**나 **'학습 단계'**와 호응하는 단어를 사용해서 한 문장으로 요약해줘.

상품 데이터:
{product_data}

요약 (한 문장으로):
"""

        try:
            # 최신 Gemini 모델 사용 (gemini-2.5-flash)
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            summary = response.text.strip()

            # Pydantic 모델로 검증
            product_summary = ProductSummary(summary=summary)
            return product_summary.summary

        except Exception as e:
            # gemini-2.5-flash 실패 시 gemini-1.5-flash로 재시도
            if '404' in str(e) or 'NOT_FOUND' in str(e):
                try:
                    response = self.client.models.generate_content(
                        model='gemini-1.5-flash',
                        contents=prompt
                    )
                    summary = response.text.strip()
                    product_summary = ProductSummary(summary=summary)
                    return product_summary.summary
                except Exception as fallback_error:
                    raise Exception(f"Gemini API 호출 중 오류 발생: {str(fallback_error)}")
            raise Exception(f"Gemini API 호출 중 오류 발생: {str(e)}")

# 싱글톤 인스턴스 생성
def get_gemini_client() -> GeminiClient:
    """Gemini 클라이언트 인스턴스 반환"""
    return GeminiClient(api_key=settings.GEMINI_API_KEY)
