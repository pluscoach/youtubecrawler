from googleapiclient.discovery import build
from typing import Optional, Dict
from ..config import get_settings

settings = get_settings()


def get_youtube_client():
    """YouTube API 클라이언트 생성"""
    return build('youtube', 'v3', developerKey=settings.youtube_api_key)


async def get_video_info(video_id: str) -> Optional[Dict]:
    """
    YouTube Data API로 영상 메타 정보 가져오기

    Returns:
        Dict with video_id, title, channel_name, thumbnail_url
    """
    try:
        youtube = get_youtube_client()

        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        if not response.get('items'):
            return None

        item = response['items'][0]
        snippet = item['snippet']

        # 썸네일 URL (고화질 우선)
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url') or
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url', '')
        )

        return {
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'channel_name': snippet.get('channelTitle', ''),
            'thumbnail_url': thumbnail_url,
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
        }

    except Exception as e:
        print(f"YouTube API 오류: {str(e)}")
        return None
