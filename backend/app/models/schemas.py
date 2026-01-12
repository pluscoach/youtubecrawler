from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from uuid import UUID


# 요청 스키마
class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="YouTube 영상 URL")
    perspective: str = Field(default="auto_trading", description="비판적 분석 관점")


# 비판적 분석 요청 스키마
class CriticalAnalyzeRequest(BaseModel):
    analysis_id: str = Field(..., description="1단계 분석 결과 ID")
    perspective: str = Field(default="auto_trading", description="비판적 분석 관점")


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


# 후킹 포인트 스키마 (새 구조)
class HookingPoint(BaseModel):
    point: Optional[str] = Field(None, description="후킹 포인트 (반전 요소 포함)")
    empathy_reason: Optional[str] = Field("", description="공감 이유")
    target: Optional[str] = Field("", description="타겟 (직장인/대학생/부업러 등)")
    level: Optional[int] = Field(None, description="후킹 레벨 (1~5)")


# 콘텐츠 방향 스키마 (새 구조 - 단계별)
class ContentDirectionStep(BaseModel):
    stage: Optional[str] = Field(None, description="단계 (후킹/모순지적/공감/해결암시)")
    example_script: Optional[str] = Field(None, description="예시 대사")
    intention: Optional[str] = Field(None, description="의도")


# 숨겨진 전제 스키마 (새 구조)
class HiddenPremise(BaseModel):
    premise: Optional[str] = Field(None, description="암묵적으로 가정하는 조건")
    why_problem: Optional[str] = Field(None, description="왜 비현실적인지 데이터로 증명")
    source: Optional[str] = Field(None, description="출처명")
    source_url: Optional[str] = Field(None, description="출처 URL")
    verified: Optional[bool] = Field(None, description="Tavily로 검증 여부")


# 현실적 모순 스키마 (새 구조)
class RealisticContradiction(BaseModel):
    strategy: Optional[str] = Field(None, description="영상에서 말한 전략")
    difficulty_reason: Optional[str] = Field(None, description="실행 어려운 이유")
    evidence_data: Optional[str] = Field(None, description="근거 데이터")
    source: Optional[str] = Field(None, description="출처명")
    source_url: Optional[str] = Field(None, description="출처 URL")
    verified: Optional[bool] = Field(None, description="Tavily로 검증 여부")


# 출처 기반 모순 분석 스키마 (새 구조)
class SourceBasedContradiction(BaseModel):
    original_claim: Optional[str] = Field(None, description="거장이 말한 원본 주장")
    original_source: Optional[str] = Field(None, description="원본 출처 (년도, 매체)")
    original_source_url: Optional[str] = Field(None, description="원본 출처 URL")
    counterexample: Optional[str] = Field(None, description="실제 데이터/사례로 반박")
    counterexample_source: Optional[str] = Field(None, description="반례 출처")
    counterexample_source_url: Optional[str] = Field(None, description="반례 출처 URL")
    hidden_condition: Optional[str] = Field(None, description="전략 성립에 필요한 숨겨진 조건")
    hidden_condition_source: Optional[str] = Field(None, description="조건 출처")
    hidden_condition_source_url: Optional[str] = Field(None, description="조건 출처 URL")
    conclusion: Optional[str] = Field(None, description="왜 일반인에게 적용 어려운지")


# 콘텐츠 방향 스키마 (기존 호환용 - deprecated)
class CriticalContentDirection(BaseModel):
    hook: str = Field(default="", description="후킹 예시 대사")
    contradiction: str = Field(default="", description="모순 지적 예시 대사")
    empathy: str = Field(default="", description="공감 예시 대사")
    solution_hint: str = Field(default="", description="해결 암시 예시 대사")


# 출처 추적 스키마
class SourceTracking(BaseModel):
    quote: Optional[str] = Field(None, description="인용 문장")
    source_title: Optional[str] = Field(None, description="출처 제목")
    source_type: Optional[str] = Field(None, description="출처 유형 (책/인터뷰 영상/기사/주주서한/논문/보고서/출처 확인 필요)")
    source_url: Optional[str] = Field(None, description="출처 URL")
    reliability: Optional[int] = Field(1, description="신뢰도 (1~5)")
    search_keywords: List[str] = Field(default_factory=list, description="검색 키워드 제안")


# 영상 구조 항목 스키마
class VideoStructureItem(BaseModel):
    order: int = Field(..., description="순서")
    element: str = Field(..., description="요소 (후킹/권위 인정/핵심 주장 등)")
    type: Optional[str] = Field(None, description="유형 (질문형/충격형 등)")
    description: str = Field(..., description="실행 방식")


# 자동화 관점 인사이트 스키마

# 구현 상세 스키마
class ImplementationDetail(BaseModel):
    condition: Optional[str] = Field(None, description="구체적 조건 (예: PER < 15, ROE > 15%)")
    tool: Optional[str] = Field(None, description="사용 도구 (예: 키움 HTS, Python FinanceDataReader)")
    backtest_result: Optional[str] = Field(None, description="백테스트 결과 (예: 2010-2024 연 12%, MDD 18%)")
    caution: Optional[str] = Field(None, description="주의사항/한계점")


# 개인 투자자 적용 사례 스키마
class IndividualCase(BaseModel):
    strategy: Optional[str] = Field(None, description="적용 전략")
    applier: Optional[str] = Field(None, description="적용자 (블로거 A, 유튜버 B 등)")
    period: Optional[str] = Field(None, description="적용 기간")
    result: Optional[str] = Field(None, description="결과")
    feedback: Optional[str] = Field(None, description="느낀 점/후기")
    source_link: Optional[str] = Field(None, description="출처 링크")


# 실행 가이드 단계 스키마
class ExecutionStep(BaseModel):
    step: int = Field(..., description="단계 번호")
    task: Optional[str] = Field(None, description="할 일")
    duration: Optional[str] = Field(None, description="소요 시간")
    difficulty: Optional[str] = Field(None, description="난이도 (쉬움/중간/어려움)")
    tool: Optional[str] = Field(None, description="필요 도구")


class ProblemSolutionItem(BaseModel):
    problem: Optional[str] = Field(None, description="문제점 (현실적 모순에서 추출)")
    human_difficulty: Optional[str] = Field(None, description="사람이 힘든 이유 (숨겨진 전제에서)")
    automation_solution: Optional[str] = Field(None, description="자동화 해결책")
    implementation: Optional[str] = Field(None, description="구현 방법 (지표, API, 코드 등)")
    # 구현 상세 추가
    implementation_detail: Optional[ImplementationDetail] = Field(None, description="구현 상세 정보")


class LifeExpansionExample(BaseModel):
    area: Optional[str] = Field(None, description="적용 영역")
    principle: Optional[str] = Field(None, description="투자에서 추출한 원리")
    application: Optional[str] = Field(None, description="구체적 적용 방법")


class LifeExpansion(BaseModel):
    applicable: bool = Field(default=False, description="적용 가능 여부")
    areas: List[str] = Field(default_factory=list, description="적용 가능 영역")
    examples: List[LifeExpansionExample] = Field(default_factory=list, description="구체적 예시")


# 보완 사례 스키마 (source_link 제거됨 - Gemini가 대본 작성 시 출처 검증)
class ImprovementCase(BaseModel):
    original_limitation: Optional[str] = Field(None, description="원본 한계점")
    improver: Optional[str] = Field(None, description="보완한 사람/연구")
    method: Optional[str] = Field(None, description="보완 방법")
    verified_result: Optional[str] = Field(None, description="검증된 결과")
    verification_period: Optional[str] = Field(None, description="검증 기간 (예: 1988-2009)")


# 차별화 포인트 스키마
class DifferentiationPoint(BaseModel):
    type: Optional[str] = Field(None, description="유형 (정량화 성공/감정 배제 성공/개인 적용 가능성)")
    summary: Optional[str] = Field(None, description="차별화 요약")
    quote_template: Optional[str] = Field(None, description="인용 템플릿 (예: 버핏은 이렇게 말했지만, [누구]는...)")


class AutomationInsight(BaseModel):
    video_type: Optional[str] = Field(None, description="영상 유형 (매매 기법/가치 투자/심리/리스크)")
    video_type_reason: Optional[str] = Field(None, description="유형 판단 이유")
    problem_solution_table: List[ProblemSolutionItem] = Field(default_factory=list, description="문제-해결책 테이블")
    core_insight: Optional[str] = Field(None, description="핵심 인사이트 한 문장")
    life_expansion: Optional[LifeExpansion] = Field(None, description="삶의 영역 확장 가능성")
    # 보완 사례 관련 필드
    improvement_cases: List[ImprovementCase] = Field(default_factory=list, description="실제 보완/업그레이드 사례")
    differentiation_points: List[DifferentiationPoint] = Field(default_factory=list, description="영상 차별화 포인트 (최소 3개)")
    improvement_search_failed: bool = Field(default=False, description="보완 사례 검색 실패 여부")
    suggested_search_keywords: List[str] = Field(default_factory=list, description="검색 키워드 제안")


# 모순 분석 출처 항목 스키마
class ContradictionSourceItem(BaseModel):
    content: str = Field(..., description="내용")
    source_title: str = Field(..., description="출처 제목")
    source_url: Optional[str] = Field(None, description="출처 URL")


# 모순 분석 결론 스키마
class ContradictionConclusion(BaseModel):
    content: str = Field(..., description="결론 내용")
    sources_summary: str = Field(..., description="출처 종합")


# 출처 기반 모순 분석 스키마
class ContradictionAnalysis(BaseModel):
    point: str = Field(..., description="비판 포인트")
    original_claim: ContradictionSourceItem = Field(..., description="원본 주장")
    counter_evidence: ContradictionSourceItem = Field(..., description="반례/팩트")
    hidden_condition: ContradictionSourceItem = Field(..., description="숨겨진 조건")
    conclusion: ContradictionConclusion = Field(..., description="결론")


# 비판적 분석 결과 스키마 (새 구조)
class CriticalAnalysis(BaseModel):
    perspective: str = Field(..., description="분석 관점 ID")
    perspective_name: str = Field(..., description="분석 관점 이름")
    # 새 구조 (Any로 기존 데이터 호환)
    hidden_premises: List[Any] = Field(default_factory=list, description="숨겨진 전제 (테이블 형식)")
    realistic_contradictions: List[Any] = Field(default_factory=list, description="현실적 모순 (테이블 형식)")
    source_based_contradictions: List[Any] = Field(default_factory=list, description="출처 기반 모순 분석")
    hooking_points: List[Any] = Field(default_factory=list, description="후킹 포인트")
    content_direction: Any = Field(default_factory=list, description="콘텐츠 방향 (단계별 또는 dict)")
    perspective_insights: List[str] = Field(default_factory=list, description="관점별 인사이트")
    # 자동화 관점 인사이트 (강화됨)
    auto_trading_connection: List[Any] = Field(default_factory=list, description="자동매매 연결 (기존)")
    automation_insight: Optional[Dict[str, Any]] = Field(None, description="자동화 관점 인사이트 (강화)")
    # 기존 호환 (deprecated)
    contradiction_analyses: List[Any] = Field(default_factory=list, description="출처 기반 모순 분석 (deprecated)")


# 소재 적합성 - 판단 항목 스키마
class SuitabilityItem(BaseModel):
    exists: bool = Field(default=False, description="해당 항목 존재 여부")
    content: Optional[str] = Field(default="", description="구체적 내용")


# 소재 적합성 - 레벨 항목 스키마
class SuitabilityLevelItem(BaseModel):
    level: str = Field(default="중간", description="높음/중간/낮음")
    reason: Optional[str] = Field(default="", description="이유")


# 소재 적합성 분석 스키마
class SuitabilityAnalysis(BaseModel):
    feasibility_issue: SuitabilityItem = Field(..., description="실현 가능성 이슈")
    hidden_premise: SuitabilityItem = Field(..., description="숨겨진 전제")
    criticism_point: SuitabilityItem = Field(..., description="비판 포인트")
    target_empathy: SuitabilityLevelItem = Field(..., description="타겟 공감 가능성")
    source_availability: SuitabilityLevelItem = Field(..., description="출처 활용 가능성")
    suitability_score: int = Field(..., ge=1, le=5, description="소재 적합도 (1~5)")
    judgment: str = Field(..., description="판단 (적합/보류/부적합)")
    usage_recommendation: str = Field(..., description="활용 추천 (메인 콘텐츠/숏폼/참고만/패스)")
    unsuitable_reason: Optional[str] = Field(None, description="부적합/보류 사유")


# 인용문 스키마 (새 구조)
class Quote(BaseModel):
    text: str = Field(..., description="인용 원문")
    speaker: Optional[str] = Field(None, description="발언자")


# 관점 정보 스키마
class PerspectiveInfo(BaseModel):
    id: str = Field(..., description="관점 ID")
    name: str = Field(..., description="관점 이름")
    description: str = Field(..., description="관점 설명")


# 관점 목록 응답
class PerspectivesResponse(BaseModel):
    success: bool
    data: List[PerspectiveInfo] = Field(default_factory=list)
    error: Optional[str] = None


# 분석 결과 스키마
class AnalysisResult(BaseModel):
    id: Optional[str] = None
    video_id: str
    video_title: str
    video_url: str
    channel_name: str
    thumbnail_url: str
    transcript: Optional[str] = None
    # 영상 성과 데이터
    view_count: Optional[int] = Field(None, description="조회수")
    like_count: Optional[int] = Field(None, description="좋아요 수")
    comment_count: Optional[int] = Field(None, description="댓글 수")
    subscriber_count: Optional[int] = Field(None, description="채널 구독자 수")
    view_sub_ratio: Optional[float] = Field(None, description="조회수/구독자 비율")
    published_at: Optional[str] = Field(None, description="업로드 일자")
    # 영상 구조 분석
    video_structure: List[Any] = Field(default_factory=list, description="영상 구조 분석")
    structure_summary: Optional[str] = Field(None, description="구조 요약 (예: 후킹→권위→주장→근거→CTA)")
    # 기본 영상 분석
    summary: str = Field(default="", description="영상 요약 (3~5줄)")
    key_message: str = Field(default="", description="핵심 메시지 (한 문장)")
    key_points: List[str] = Field(default_factory=list, description="키포인트 (3~5개)")
    quotes: List[Union[Quote, str]] = Field(default_factory=list, description="인용할 만한 대사")
    people: List[Person] = Field(default_factory=list, description="등장 인물")
    investment_strategy: Optional[str] = Field(None, description="거장의 전략 (투자법/철학)")
    # 출처 추적
    source_tracking: List[SourceTracking] = Field(default_factory=list, description="출처 및 원본 추적")
    # 소재 적합성 분석 (1단계)
    suitability_analysis: Optional[SuitabilityAnalysis] = Field(None, description="소재 적합성 판단")
    # 비판적 분석 (2단계 - 버튼 클릭 시)
    perspective: Optional[str] = Field(None, description="분석 관점 ID")
    critical_analysis: Optional[CriticalAnalysis] = Field(None, description="비판적 분석 결과")
    # 추가 분석 (3단계 - 버튼 클릭 시)
    additional_analysis: Optional[Dict[str, Any]] = Field(None, description="추가 분석 결과")
    # 기존 호환성 (사용 안함)
    content_ideas: List[ContentIdea] = Field(default_factory=list, description="콘텐츠 추천 (deprecated)")
    script_direction: Optional[ScriptDirection] = Field(None, description="대본 방향 (deprecated)")
    created_at: Optional[datetime] = None


# 응답 스키마
class AnalyzeResponse(BaseModel):
    success: bool
    data: Optional[AnalysisResult] = None
    error: Optional[str] = None
    cached: bool = False  # DB 캐시에서 가져온 경우 True


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


# ===== 추가 분석 스키마 (3단계) =====

# 추가 분석 요청 스키마
class AdditionalAnalyzeRequest(BaseModel):
    analysis_id: str = Field(..., description="1단계 분석 결과 ID")


# 썸네일 문구 추천
class ThumbnailSuggestion(BaseModel):
    type: str = Field(..., description="유형 (반전형/질문형/숫자형/권위형/공감형)")
    text: str = Field(..., description="문구 (10자 이내)")
    basis: str = Field(..., description="활용 근거")
    click_psychology: str = Field(..., description="클릭 유도 심리")


# 제목 후보 추천
class TitleSuggestion(BaseModel):
    pattern: str = Field(..., description="패턴 (권위 뒤집기/공감형/논쟁형/호기심형/숫자형)")
    title: str = Field(..., description="제목 (40자 이내)")
    basis: str = Field(..., description="활용 근거")
    target: str = Field(..., description="타겟")


# 영상 파트 정보
class VideoPart(BaseModel):
    part: str = Field(..., description="파트명")
    time_range: str = Field(..., description="시간대")
    content: str = Field(..., description="내용")


# 영상 길이 추천
class VideoLength(BaseModel):
    recommended_length: str = Field(..., description="추천 길이 (00분 00초)")
    format: str = Field(..., description="형식 (숏폼/미드폼/롱폼)")
    judgment_basis: str = Field(..., description="판단 근거")
    parts: List[VideoPart] = Field(default_factory=list, description="파트별 시간 배분")


# 대본 방향 (파트별)
class ScriptDirectionItem(BaseModel):
    part: str = Field(..., description="파트명")
    keypoint: str = Field(..., description="예시 문장")
    basis: str = Field(..., description="활용 근거")
    emotion: str = Field(..., description="시청자 감정 유도")


# 꿀팁
class BonusTip(BaseModel):
    topic: str = Field(..., description="주제")
    summary: str = Field(..., description="내용 요약")
    why_helpful: str = Field(..., description="왜 도움 되는지")
    source: str = Field(..., description="출처명")
    source_url: Optional[str] = Field(None, description="출처 링크")


# 인터뷰 클립
class InterviewClip(BaseModel):
    person: str = Field(..., description="인물명")
    video_title: str = Field(..., description="영상 제목")
    quote: str = Field(..., description="발언 내용")
    timestamp: str = Field(..., description="시간대")
    link: Optional[str] = Field(None, description="링크")


# 반례 증거 소스
class EvidenceSource(BaseModel):
    contradiction: str = Field(..., description="모순 내용")
    evidence: str = Field(..., description="증거 자료")
    source_type: str = Field(..., description="출처 유형")
    link: Optional[str] = Field(None, description="링크")


# B-roll 키워드
class BRollKeyword(BaseModel):
    scene: str = Field(..., description="장면 설명")
    keyword: str = Field(..., description="검색 키워드 (영문)")
    usage_part: str = Field(..., description="활용 파트")


# Veo3 프롬프트
class Veo3Prompt(BaseModel):
    scene: str = Field(..., description="장면 설명")
    prompt: str = Field(..., description="Veo3 프롬프트 (영문)")
    usage_part: str = Field(..., description="활용 파트")


# 영상 소스 추천
class VideoSourceRecommendation(BaseModel):
    interview_clips: List[InterviewClip] = Field(default_factory=list)
    evidence_sources: List[EvidenceSource] = Field(default_factory=list)
    broll_keywords: List[BRollKeyword] = Field(default_factory=list)
    veo3_prompts: List[Veo3Prompt] = Field(default_factory=list)


# 타겟 적합도
class TargetFit(BaseModel):
    target: str = Field(..., description="타겟")
    fit_level: int = Field(..., ge=1, le=5, description="적합도 (1~5)")
    reason: str = Field(..., description="이유")


# 논쟁 유발도
class ControversyPrediction(BaseModel):
    level: int = Field(..., ge=1, le=5, description="논쟁 유발도 (1~5)")
    expected_reactions: str = Field(..., description="예상 반응")


# 예상 댓글
class ExpectedComment(BaseModel):
    type: str = Field(..., description="유형 (긍정/부정/질문)")
    comment: str = Field(..., description="예상 댓글")


# 시리즈 확장
class SeriesExpansion(BaseModel):
    topic: str = Field(..., description="후속 영상 주제")
    connection: str = Field(..., description="연결 포인트")


# 콘텐츠 성과 예측
class PerformancePrediction(BaseModel):
    target_fits: List[TargetFit] = Field(default_factory=list)
    controversy: Optional[ControversyPrediction] = None
    expected_comments: List[ExpectedComment] = Field(default_factory=list)
    series_expansions: List[SeriesExpansion] = Field(default_factory=list)


# 멤버십 연결 타이밍
class MembershipTiming(BaseModel):
    timing: str = Field(..., description="추천 타이밍")
    video_position: str = Field(..., description="영상 위치")
    reason: str = Field(..., description="이유")


# 멤버십 연결 문맥
class MembershipContext(BaseModel):
    previous_line: str = Field(..., description="직전 대사")
    connection: str = Field(..., description="멤버십 연결 문구")


# 멤버십 티저
class MembershipTeaser(BaseModel):
    situation: str = Field(..., description="상황")
    teaser: str = Field(..., description="티저 문구")


# 멤버십 콘텐츠 제안
class MembershipContent(BaseModel):
    topic: str = Field(..., description="콘텐츠 주제")
    connection: str = Field(..., description="연결점")


# 멤버십 연결 포인트
class MembershipConnection(BaseModel):
    timings: List[MembershipTiming] = Field(default_factory=list)
    contexts: List[MembershipContext] = Field(default_factory=list)
    teasers: List[MembershipTeaser] = Field(default_factory=list)
    content_suggestions: List[MembershipContent] = Field(default_factory=list)


# 추가 분석 전체 결과
class AdditionalAnalysisResult(BaseModel):
    thumbnail_suggestions: List[ThumbnailSuggestion] = Field(default_factory=list)
    title_suggestions: List[TitleSuggestion] = Field(default_factory=list)
    video_length: Optional[VideoLength] = None
    script_directions: List[ScriptDirectionItem] = Field(default_factory=list)
    bonus_tip: Optional[BonusTip] = None
    video_sources: Optional[VideoSourceRecommendation] = None
    performance_prediction: Optional[PerformancePrediction] = None
    membership_connection: Optional[MembershipConnection] = None
