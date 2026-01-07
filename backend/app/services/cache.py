"""
분석 결과 캐싱 서비스
- 메모리 캐시로 동일 영상 재분석 방지
- 서버 재시작 시 캐시 초기화됨
"""

from typing import Optional, Dict

# 메모리 캐시
analysis_cache: Dict[str, Dict] = {}


def get_cache_key(video_id: str, analysis_type: str) -> str:
    """캐시 키 생성"""
    return f"{video_id}:{analysis_type}"


def get_cached_analysis(video_id: str, analysis_type: str) -> Optional[Dict]:
    """
    캐시된 분석 결과 조회

    Args:
        video_id: 유튜브 영상 ID
        analysis_type: 분석 유형 (stage1, stage2, stage3)

    Returns:
        캐시된 결과 또는 None
    """
    key = get_cache_key(video_id, analysis_type)
    return analysis_cache.get(key)


def set_cached_analysis(video_id: str, analysis_type: str, result: Dict) -> None:
    """
    분석 결과 캐시에 저장

    Args:
        video_id: 유튜브 영상 ID
        analysis_type: 분석 유형 (stage1, stage2, stage3)
        result: 분석 결과
    """
    key = get_cache_key(video_id, analysis_type)
    analysis_cache[key] = result


def clear_cache(video_id: str = None) -> None:
    """
    캐시 삭제

    Args:
        video_id: 특정 영상만 삭제 (None이면 전체 삭제)
    """
    global analysis_cache

    if video_id:
        keys_to_delete = [k for k in analysis_cache if k.startswith(video_id)]
        for k in keys_to_delete:
            del analysis_cache[k]
    else:
        analysis_cache.clear()


def get_cache_stats() -> Dict:
    """캐시 통계 조회"""
    return {
        "total_entries": len(analysis_cache),
        "video_ids": list(set(k.split(":")[0] for k in analysis_cache.keys()))
    }
