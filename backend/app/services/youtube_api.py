from googleapiclient.discovery import build
from typing import Optional, Dict
from ..config import get_settings

settings = get_settings()


def get_youtube_client():
    """YouTube API 클라이언트 생성"""
    return build('youtube', 'v3', developerKey=settings.youtube_api_key)


async def get_video_info(video_id: str) -> Optional[Dict]:
    """
    YouTube Data API로 영상 메타 정보 + 성과 데이터 가져오기

    Returns:
        Dict with video_id, title, channel_name, thumbnail_url,
        view_count, like_count, comment_count, subscriber_count, view_sub_ratio, published_at
    """
    try:
        youtube = get_youtube_client()

        # snippet + statistics 함께 요청
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        if not response.get('items'):
            return None

        item = response['items'][0]
        snippet = item['snippet']
        statistics = item.get('statistics', {})

        # 썸네일 URL (고화질 우선)
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('maxres', {}).get('url') or
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url', '')
        )

        # 채널 ID로 구독자 수 가져오기
        channel_id = snippet.get('channelId', '')
        subscriber_count = await get_channel_subscriber_count(youtube, channel_id)

        # 성과 데이터 파싱
        view_count = int(statistics.get('viewCount', 0))
        like_count = int(statistics.get('likeCount', 0))
        comment_count = int(statistics.get('commentCount', 0))

        # 조회수/구독자 비율 계산
        view_sub_ratio = None
        if subscriber_count and subscriber_count > 0:
            view_sub_ratio = round(view_count / subscriber_count, 2)

        return {
            'video_id': video_id,
            'title': snippet.get('title', ''),
            'channel_name': snippet.get('channelTitle', ''),
            'thumbnail_url': thumbnail_url,
            'description': snippet.get('description', ''),
            'published_at': snippet.get('publishedAt', ''),
            # 성과 데이터
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'subscriber_count': subscriber_count,
            'view_sub_ratio': view_sub_ratio,
        }

    except Exception as e:
        print(f"YouTube API 오류: {str(e)}")
        return None


async def get_channel_subscriber_count(youtube, channel_id: str) -> Optional[int]:
    """채널 구독자 수 가져오기"""
    if not channel_id:
        return None

    try:
        request = youtube.channels().list(
            part="statistics",
            id=channel_id
        )
        response = request.execute()

        if not response.get('items'):
            return None

        statistics = response['items'][0].get('statistics', {})
        subscriber_count = statistics.get('subscriberCount')

        if subscriber_count:
            return int(subscriber_count)
        return None

    except Exception as e:
        print(f"채널 정보 조회 오류: {str(e)}")
        return None
