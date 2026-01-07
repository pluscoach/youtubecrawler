from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    AnalyzeRequest, AnalyzeResponse, AnalysisResult,
    PerspectivesResponse, PerspectiveInfo, CriticalAnalysis,
    CriticalAnalyzeRequest, SuitabilityAnalysis, Quote,
    AdditionalAnalyzeRequest
)
from ..services.transcript import extract_video_id, get_transcript
from ..services.youtube_api import get_video_info
from ..services.claude import analyze_transcript, analyze_critical_v2
from ..services.perspectives import get_all_perspectives, get_perspective
from ..services.additional_analysis import analyze_additional
from ..services.cache import get_cached_analysis, set_cached_analysis
from ..database import save_analysis, get_analysis_by_id, update_analysis, get_analysis_by_video_id

router = APIRouter(prefix="/api", tags=["youtube"])


# suitability 데이터 정규화 헬퍼 함수 (None 값 처리)
def normalize_suitability_item(item):
    if not item or not isinstance(item, dict):
        return {"exists": False, "content": ""}
    return {
        "exists": item.get("exists", False) or False,
        "content": item.get("content") or ""
    }


def normalize_suitability_level(item):
    if not item or not isinstance(item, dict):
        return {"level": "중간", "reason": ""}
    return {
        "level": item.get("level") or "중간",
        "reason": item.get("reason") or ""
    }


def normalize_suitability(suitability_raw):
    """suitability_analysis 데이터 정규화"""
    if not suitability_raw or not isinstance(suitability_raw, dict):
        return None
    return {
        "feasibility_issue": normalize_suitability_item(suitability_raw.get("feasibility_issue")),
        "hidden_premise": normalize_suitability_item(suitability_raw.get("hidden_premise")),
        "criticism_point": normalize_suitability_item(suitability_raw.get("criticism_point")),
        "target_empathy": normalize_suitability_level(suitability_raw.get("target_empathy")),
        "source_availability": normalize_suitability_level(suitability_raw.get("source_availability")),
        "suitability_score": suitability_raw.get("suitability_score") or 3,
        "judgment": suitability_raw.get("judgment") or "보류",
        "usage_recommendation": suitability_raw.get("usage_recommendation") or "참고만",
        "unsuitable_reason": suitability_raw.get("unsuitable_reason")
    }


@router.get("/perspectives", response_model=PerspectivesResponse)
async def get_perspectives():
    """분석 관점 목록 조회"""
    try:
        perspectives = get_all_perspectives()
        return PerspectivesResponse(
            success=True,
            data=[PerspectiveInfo(**p) for p in perspectives]
        )
    except Exception as e:
        return PerspectivesResponse(
            success=False,
            error=f"관점 목록 조회 중 오류: {str(e)}"
        )


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest):
    """
    YouTube 영상 분석 API (1단계: 영상 분석 + 소재 적합성)

    1. URL에서 video_id 추출
    2. YouTube API로 영상 정보 가져오기
    3. 자막 추출
    4. Claude로 분석 (영상 분석 + 소재 적합성)
    5. DB 저장
    6. 결과 반환
    """
    try:
        # 1. video_id 추출
        video_id = extract_video_id(request.url)
        if not video_id:
            return AnalyzeResponse(
                success=False,
                error="유효하지 않은 YouTube URL입니다."
            )

        # 1-1. DB 캐시 확인 - 이미 분석된 영상이면 바로 반환
        existing = await get_analysis_by_video_id(video_id)
        if existing and existing.get('summary'):
            result = AnalysisResult(
                id=existing.get('id'),
                video_id=existing.get('video_id'),
                video_title=existing.get('video_title'),
                video_url=existing.get('video_url'),
                channel_name=existing.get('channel_name'),
                thumbnail_url=existing.get('thumbnail_url'),
                summary=existing.get('summary', ''),
                key_message=existing.get('key_message', ''),
                key_points=existing.get('key_points', []),
                quotes=existing.get('quotes', []),
                people=existing.get('people', []),
                investment_strategy=existing.get('investment_strategy', ''),
                source_tracking=existing.get('source_tracking', []),
                suitability_analysis=normalize_suitability(existing.get('suitability_analysis')),
                perspective=existing.get('perspective'),
                critical_analysis=existing.get('critical_analysis'),
                additional_analysis=existing.get('additional_analysis'),
                created_at=existing.get('created_at'),
            )
            return AnalyzeResponse(success=True, data=result, cached=True)

        # 2. 영상 정보 가져오기
        video_info = await get_video_info(video_id)
        if not video_info:
            return AnalyzeResponse(
                success=False,
                error="영상 정보를 가져올 수 없습니다."
            )

        # 3. 자막 추출
        transcript, error = await get_transcript(video_id)
        if error:
            return AnalyzeResponse(
                success=False,
                error=error
            )

        # 4. Claude로 1단계 분석 (영상 분석 + 소재 적합성)
        analysis, error = await analyze_transcript(transcript)
        if error:
            return AnalyzeResponse(
                success=False,
                error=error
            )

        # 새 프롬프트 응답 구조 파싱
        video_analysis = analysis.get('video_analysis', {})
        suitability = normalize_suitability(analysis.get('suitability_analysis', {}))

        # quotes 변환 (새 구조: {text, speaker})
        quotes_raw = video_analysis.get('quotes', [])
        quotes = []
        for q in quotes_raw:
            if isinstance(q, dict):
                quotes.append({"text": q.get('text', ''), "speaker": q.get('speaker', '')})
            elif isinstance(q, str):
                quotes.append({"text": q, "speaker": ""})

        # 5. DB 저장을 위한 데이터 구성
        analysis_data = {
            "video_id": video_id,
            "video_title": video_info['title'],
            "video_url": request.url,
            "channel_name": video_info['channel_name'],
            "thumbnail_url": video_info['thumbnail_url'],
            "transcript": transcript[:10000] if transcript else None,
            "summary": video_analysis.get('summary', ''),
            "key_message": video_analysis.get('key_message', ''),
            "key_points": video_analysis.get('key_points', []),
            "quotes": quotes,
            "people": video_analysis.get('people', []),
            "investment_strategy": video_analysis.get('investment_strategy', ''),
            "source_tracking": video_analysis.get('source_tracking', []),
            "suitability_analysis": suitability,
            # 비판적 분석은 버튼 클릭 시 별도 호출
            "perspective": None,
            "critical_analysis": None,
            "additional_analysis": None,
        }

        # DB 저장
        saved = await save_analysis(analysis_data)

        # 6. 결과 반환
        result = AnalysisResult(
            id=saved.get('id'),
            video_id=video_id,
            video_title=video_info['title'],
            video_url=request.url,
            channel_name=video_info['channel_name'],
            thumbnail_url=video_info['thumbnail_url'],
            summary=video_analysis.get('summary', ''),
            key_message=video_analysis.get('key_message', ''),
            key_points=video_analysis.get('key_points', []),
            quotes=quotes,
            people=video_analysis.get('people', []),
            investment_strategy=video_analysis.get('investment_strategy', ''),
            source_tracking=video_analysis.get('source_tracking', []),
            suitability_analysis=suitability if suitability else None,
            created_at=saved.get('created_at'),
        )

        return AnalyzeResponse(success=True, data=result)

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.get("/result/{analysis_id}", response_model=AnalyzeResponse)
async def get_result(analysis_id: str):
    """분석 결과 조회"""
    try:
        result = await get_analysis_by_id(analysis_id)

        if not result:
            return AnalyzeResponse(
                success=False,
                error="분석 결과를 찾을 수 없습니다."
            )

        analysis_result = AnalysisResult(
            id=result.get('id'),
            video_id=result.get('video_id'),
            video_title=result.get('video_title'),
            video_url=result.get('video_url'),
            channel_name=result.get('channel_name'),
            thumbnail_url=result.get('thumbnail_url'),
            summary=result.get('summary', ''),
            key_message=result.get('key_message', ''),
            key_points=result.get('key_points', []),
            quotes=result.get('quotes', []),
            people=result.get('people', []),
            investment_strategy=result.get('investment_strategy', ''),
            source_tracking=result.get('source_tracking', []),
            suitability_analysis=result.get('suitability_analysis'),
            perspective=result.get('perspective'),
            critical_analysis=result.get('critical_analysis'),
            additional_analysis=result.get('additional_analysis'),
            created_at=result.get('created_at'),
        )

        return AnalyzeResponse(success=True, data=analysis_result)

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze/critical", response_model=AnalyzeResponse)
async def analyze_critical_endpoint(request: CriticalAnalyzeRequest):
    """
    비판적 분석 API (2단계: 1단계 결과 기반)

    1. DB에서 1단계 분석 결과 조회
    2. 소재 적합성 체크 (부적합이면 분석 안함)
    3. Claude로 비판적 분석
    4. DB 업데이트
    5. 결과 반환
    """
    try:
        # 1. DB에서 1단계 분석 결과 조회
        existing = await get_analysis_by_id(request.analysis_id)
        if not existing:
            return AnalyzeResponse(
                success=False,
                error="분석 결과를 찾을 수 없습니다."
            )

        # 2. 소재 적합성 체크
        suitability = existing.get('suitability_analysis', {})
        if suitability and suitability.get('judgment') == '부적합':
            return AnalyzeResponse(
                success=False,
                error=f"이 영상은 비판적 분석에 적합하지 않습니다. 사유: {suitability.get('unsuitable_reason', '소재 부적합')}"
            )

        # 3. Claude로 비판적 분석 (1단계 결과 기반)
        critical_result, error = await analyze_critical_v2(
            perspective_id=request.perspective,
            summary=existing.get('summary', ''),
            key_message=existing.get('key_message', ''),
            key_points=existing.get('key_points', []),
            strategy=existing.get('investment_strategy', ''),
            quotes=existing.get('quotes', []),
            people=existing.get('people', []),
            source_tracking=existing.get('source_tracking', []),
            suitability_analysis=suitability
        )

        if error:
            return AnalyzeResponse(
                success=False,
                error=error
            )

        # 분석 결과에 에러가 있는 경우 (부적합 등)
        if critical_result and critical_result.get('error'):
            return AnalyzeResponse(
                success=False,
                error=critical_result.get('message', '비판적 분석을 수행할 수 없습니다.')
            )

        # 4. DB 업데이트
        update_data = {
            "perspective": request.perspective,
            "critical_analysis": critical_result
        }
        updated = await update_analysis(request.analysis_id, update_data)

        if not updated:
            return AnalyzeResponse(
                success=False,
                error="분석 결과 업데이트에 실패했습니다."
            )

        # 5. 결과 반환
        analysis_result = AnalysisResult(
            id=updated.get('id'),
            video_id=updated.get('video_id'),
            video_title=updated.get('video_title'),
            video_url=updated.get('video_url'),
            channel_name=updated.get('channel_name'),
            thumbnail_url=updated.get('thumbnail_url'),
            summary=updated.get('summary', ''),
            key_message=updated.get('key_message', ''),
            key_points=updated.get('key_points', []),
            quotes=updated.get('quotes', []),
            people=updated.get('people', []),
            investment_strategy=updated.get('investment_strategy', ''),
            source_tracking=updated.get('source_tracking', []),
            suitability_analysis=updated.get('suitability_analysis'),
            perspective=updated.get('perspective'),
            critical_analysis=updated.get('critical_analysis'),
            additional_analysis=updated.get('additional_analysis'),
            created_at=updated.get('created_at'),
        )

        return AnalyzeResponse(success=True, data=analysis_result)

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"비판적 분석 중 오류가 발생했습니다: {str(e)}"
        )


@router.post("/analyze/additional", response_model=AnalyzeResponse)
async def analyze_additional_endpoint(request: AdditionalAnalyzeRequest):
    """
    추가 분석 API (3단계: 1단계 + 2단계 결과 기반)

    1. DB에서 1단계 + 2단계 분석 결과 조회
    2. 비판적 분석 완료 여부 체크
    3. Claude로 추가 분석
    4. DB 업데이트
    5. 결과 반환
    """
    try:
        # 1. DB에서 기존 분석 결과 조회
        existing = await get_analysis_by_id(request.analysis_id)
        if not existing:
            return AnalyzeResponse(
                success=False,
                error="분석 결과를 찾을 수 없습니다."
            )

        # 2. 비판적 분석 완료 여부 체크
        critical_analysis = existing.get('critical_analysis')
        if not critical_analysis:
            return AnalyzeResponse(
                success=False,
                error="비판적 분석을 먼저 진행해주세요."
            )

        # 3. Claude로 추가 분석 (1단계 + 2단계 결과 기반)
        additional_result, error = await analyze_additional(
            summary=existing.get('summary', ''),
            key_message=existing.get('key_message', ''),
            key_points=existing.get('key_points', []),
            strategy=existing.get('investment_strategy', ''),
            quotes=existing.get('quotes', []),
            people=existing.get('people', []),
            source_tracking=existing.get('source_tracking', []),
            suitability_analysis=existing.get('suitability_analysis', {}),
            hidden_premises=critical_analysis.get('hidden_premises', []),
            realistic_contradictions=critical_analysis.get('realistic_contradictions', []),
            source_based_contradictions=critical_analysis.get('source_based_contradictions', []),
            hooking_points=critical_analysis.get('hooking_points', []),
            content_direction=critical_analysis.get('content_direction', [])
        )

        if error:
            return AnalyzeResponse(
                success=False,
                error=error
            )

        # 4. DB 업데이트
        update_data = {
            "additional_analysis": additional_result
        }
        updated = await update_analysis(request.analysis_id, update_data)

        if not updated:
            return AnalyzeResponse(
                success=False,
                error="추가 분석 결과 저장에 실패했습니다."
            )

        # 5. 결과 반환
        analysis_result = AnalysisResult(
            id=updated.get('id'),
            video_id=updated.get('video_id'),
            video_title=updated.get('video_title'),
            video_url=updated.get('video_url'),
            channel_name=updated.get('channel_name'),
            thumbnail_url=updated.get('thumbnail_url'),
            summary=updated.get('summary', ''),
            key_message=updated.get('key_message', ''),
            key_points=updated.get('key_points', []),
            quotes=updated.get('quotes', []),
            people=updated.get('people', []),
            investment_strategy=updated.get('investment_strategy', ''),
            source_tracking=updated.get('source_tracking', []),
            suitability_analysis=updated.get('suitability_analysis'),
            perspective=updated.get('perspective'),
            critical_analysis=updated.get('critical_analysis'),
            additional_analysis=updated.get('additional_analysis'),
            created_at=updated.get('created_at'),
        )

        return AnalyzeResponse(success=True, data=analysis_result)

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"추가 분석 중 오류가 발생했습니다: {str(e)}"
        )
