from supabase import create_client, Client
from typing import Optional
from .config import get_settings

_supabase_client: Optional[Client] = None


def get_supabase() -> Client:
    global _supabase_client

    if _supabase_client is None:
        settings = get_settings()
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError("Supabase URL and Key must be set in environment variables")

        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )

    return _supabase_client


async def save_analysis(analysis_data: dict) -> dict:
    """분석 결과를 Supabase에 저장"""
    supabase = get_supabase()

    result = supabase.table("analyses").insert(analysis_data).execute()

    if result.data:
        return result.data[0]
    raise Exception("Failed to save analysis")


async def get_analysis_by_id(analysis_id: str) -> Optional[dict]:
    """ID로 분석 결과 조회"""
    supabase = get_supabase()

    result = supabase.table("analyses").select("*").eq("id", analysis_id).execute()

    if result.data:
        return result.data[0]
    return None


async def get_history(limit: int = 20, offset: int = 0) -> list:
    """분석 히스토리 조회"""
    supabase = get_supabase()

    result = supabase.table("analyses")\
        .select("id, video_id, video_title, video_url, channel_name, thumbnail_url, created_at")\
        .order("created_at", desc=True)\
        .range(offset, offset + limit - 1)\
        .execute()

    return result.data or []


async def delete_analysis(analysis_id: str) -> bool:
    """분석 결과 삭제"""
    supabase = get_supabase()

    result = supabase.table("analyses").delete().eq("id", analysis_id).execute()

    return len(result.data) > 0 if result.data else False


async def get_history_count() -> int:
    """히스토리 총 개수 조회"""
    supabase = get_supabase()

    result = supabase.table("analyses").select("id", count="exact").execute()

    return result.count or 0
