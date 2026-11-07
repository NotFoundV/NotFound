from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class AnalyzeRequest(BaseModel):
    idea: str = Field(min_length=5, max_length=2000, description="창업 아이디어 설명")

    @field_validator("idea")
    @classmethod
    def strip_idea(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise ValueError("아이디어를 5자 이상 입력해 주세요.")
        return value


class ServiceAnalysis(BaseModel):
    name: str = Field(description="서비스 이름")
    url: str | None = Field(default=None, description="서비스 공식 웹사이트 주소. 모르면 null")
    summary: str = Field(description="서비스 한 줄 소개")
    business_model: str = Field(description="비즈니스 모델: 누구에게 어떤 가치를 어떤 방식으로 제공하는지")
    core_features: str = Field(description="핵심 기능: 사용자가 이 서비스를 쓰는 주된 이유가 되는 기능")
    revenue_model: str = Field(description="수익 구조: 구독, 수수료, 광고 등 실제로 돈을 버는 방식")
    differentiation: str = Field(description="차별점: 다른 유사 서비스와 구별되는 강점")


class AnalysisResult(BaseModel):
    services: list[ServiceAnalysis] = Field(description="유사 서비스 3~5개")
    insight: str = Field(description="사용자 아이디어가 파고들 수 있는 빈틈 인사이트 1~2문장")


class AnalysisRecord(AnalysisResult):
    id: int
    idea: str
    created_at: datetime


class HistoryItem(BaseModel):
    id: int
    idea: str
    created_at: datetime
    service_names: list[str]
