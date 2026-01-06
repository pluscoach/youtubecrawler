from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


# 요청 스키마
class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="YouTube 영상 URL")


# 콘텐츠 추천 스키마
class ContentIdea(BaseModel):
    target: str = Field(..., description="타겟 고객층")
    title_example: str = Field(..., description="제목 예시")
    direction: str = Field(..., description="활용 방향")


# 대본 방향 스키마
class ScriptDirection(BaseModel):
    intro: str = Field(..., description="도입")
    development: str = Field(..., description="전개")
    transition: str = Field(..., description="전환")
    conclusion: str = Field(..., description="마무리")


# 등장 인물 스키마
class Person(BaseModel):
    name: str = Field(..., description="이름")
    role: Optional[str] = Field(None, description="역할")
    related_links: Optional[List[str]] = Field(default_factory=list, description="관련 링크")


# 분석 결과 스키마
class AnalysisResult(BaseModel):
    id: Optional[str] = None
    video_id: str
    video_title: str
    video_url: str
    channel_name: str
    thumbnail_url: str
    transcript: Optional[str] = None
    summary: str = Field(..., description="영상 요약 (3~5줄)")
    key_message: str = Field(..., description="핵심 메시지 (한 문장)")
    key_points: List[str] = Field(..., description="키포인트 (3~5개)")
    quotes: List[str] = Field(..., description="인용할 만한 대사")
    people: List[Person] = Field(default_factory=list, description="등장 인물")
    content_ideas: List[ContentIdea] = Field(..., description="콘텐츠 추천")
    script_direction: ScriptDirection = Field(..., description="대본 방향")
    created_at: Optional[datetime] = None


# 응답 스키마
class AnalyzeResponse(BaseModel):
    success: bool
    data: Optional[AnalysisResult] = None
    error: Optional[str] = None


# 히스토리 아이템 스키마
class HistoryItem(BaseModel):
    id: str
    video_id: str
    video_title: str
    video_url: str
    channel_name: str
    thumbnail_url: str
    created_at: datetime


# 히스토리 목록 응답
class HistoryListResponse(BaseModel):
    success: bool
    data: List[HistoryItem] = Field(default_factory=list)
    total: int = 0
    error: Optional[str] = None
