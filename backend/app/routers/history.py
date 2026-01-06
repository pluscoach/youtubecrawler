from fastapi import APIRouter, Query
from ..models.schemas import HistoryListResponse, HistoryItem
from ..database import get_history, delete_analysis, get_history_count

router = APIRouter(prefix="/api", tags=["history"])


@router.get("/history", response_model=HistoryListResponse)
async def list_history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """분석 히스토리 목록 조회"""
    try:
        # 히스토리 조회
        history_data = await get_history(limit=limit, offset=offset)
        total = await get_history_count()

        # HistoryItem 리스트로 변환
        items = [
            HistoryItem(
                id=item['id'],
                video_id=item['video_id'],
                video_title=item['video_title'],
                video_url=item['video_url'],
                channel_name=item['channel_name'],
                thumbnail_url=item['thumbnail_url'],
                created_at=item['created_at'],
            )
            for item in history_data
        ]

        return HistoryListResponse(
            success=True,
            data=items,
            total=total
        )

    except Exception as e:
        return HistoryListResponse(
            success=False,
            error=f"히스토리 조회 중 오류가 발생했습니다: {str(e)}"
        )


@router.delete("/history/{analysis_id}")
async def remove_history(analysis_id: str):
    """분석 히스토리 삭제"""
    try:
        success = await delete_analysis(analysis_id)

        if success:
            return {"success": True, "message": "삭제되었습니다."}
        else:
            return {"success": False, "error": "삭제할 항목을 찾을 수 없습니다."}

    except Exception as e:
        return {"success": False, "error": f"삭제 중 오류가 발생했습니다: {str(e)}"}
