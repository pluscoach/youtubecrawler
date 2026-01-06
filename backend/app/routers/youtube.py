from fastapi import APIRouter, HTTPException
from ..models.schemas import AnalyzeRequest, AnalyzeResponse, AnalysisResult
from ..services.transcript import extract_video_id, get_transcript
from ..services.youtube_api import get_video_info
from ..services.claude import analyze_transcript
from ..database import save_analysis, get_analysis_by_id

router = APIRouter(prefix="/api", tags=["youtube"])


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest):
    """
    YouTube 영상 분석 API

    1. URL에서 video_id 추출
    2. YouTube API로 영상 정보 가져오기
    3. 자막 추출
    4. Claude로 분석
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

        # 4. Claude로 분석
        analysis, error = await analyze_transcript(transcript)
        if error:
            return AnalyzeResponse(
                success=False,
                error=error
            )

        # 5. DB 저장을 위한 데이터 구성
        analysis_data = {
            "video_id": video_id,
            "video_title": video_info['title'],
            "video_url": request.url,
            "channel_name": video_info['channel_name'],
            "thumbnail_url": video_info['thumbnail_url'],
            "transcript": transcript[:10000] if transcript else None,  # 자막은 일부만 저장
            "summary": analysis.get('summary', ''),
            "key_message": analysis.get('key_message', ''),
            "key_points": analysis.get('key_points', []),
            "quotes": analysis.get('quotes', []),
            "people": analysis.get('people', []),
            "content_ideas": analysis.get('content_ideas', []),
            "script_direction": analysis.get('script_direction', {}),
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
            summary=analysis.get('summary', ''),
            key_message=analysis.get('key_message', ''),
            key_points=analysis.get('key_points', []),
            quotes=analysis.get('quotes', []),
            people=analysis.get('people', []),
            content_ideas=analysis.get('content_ideas', []),
            script_direction=analysis.get('script_direction', {}),
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
            content_ideas=result.get('content_ideas', []),
            script_direction=result.get('script_direction', {}),
            created_at=result.get('created_at'),
        )

        return AnalyzeResponse(success=True, data=analysis_result)

    except Exception as e:
        return AnalyzeResponse(
            success=False,
            error=f"조회 중 오류가 발생했습니다: {str(e)}"
        )
