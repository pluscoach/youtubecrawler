from fastapi import APIRouter
from ..services.transcript import get_transcript, extract_video_id
from ..services.claude import analyze_transcript

router = APIRouter(prefix="/api", tags=["analyzer"])


@router.post("/analyze-only")
async def analyze_only(url: str):
    """
    자막만 분석 (DB 저장 없이)
    테스트/디버깅용 API
    """
    try:
        # video_id 추출
        video_id = extract_video_id(url)
        if not video_id:
            return {"success": False, "error": "유효하지 않은 YouTube URL입니다."}

        # 자막 추출
        transcript, error = await get_transcript(video_id)
        if error:
            return {"success": False, "error": error}

        # Claude로 분석
        analysis, error = await analyze_transcript(transcript)
        if error:
            return {"success": False, "error": error}

        return {
            "success": True,
            "video_id": video_id,
            "transcript_length": len(transcript),
            "analysis": analysis
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@router.get("/transcript/{video_id}")
async def get_video_transcript(video_id: str):
    """자막만 가져오기 (테스트/디버깅용)"""
    transcript, error = await get_transcript(video_id)

    if error:
        return {"success": False, "error": error}

    return {
        "success": True,
        "video_id": video_id,
        "transcript": transcript,
        "length": len(transcript)
    }
