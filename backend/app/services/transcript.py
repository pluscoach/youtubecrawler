import re
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional, Tuple


def extract_video_id(url: str) -> Optional[str]:
    """YouTube URL에서 video_id 추출"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/shorts\/([^&\n?#]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


async def get_transcript(video_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    YouTube 영상의 자막을 가져옴

    Returns:
        Tuple[Optional[str], Optional[str]]: (자막 텍스트, 에러 메시지)
    """
    try:
        api = YouTubeTranscriptApi()

        # 자막 가져오기
        transcript_data = api.fetch(video_id)

        # 자막 텍스트 추출 - 각 항목의 'text'만 추출해서 문자열로 합치기
        full_text = ' '.join([item['text'] for item in transcript_data.to_raw_data()])

        return full_text, None

    except Exception as e:
        return None, f"자막 추출 중 오류 발생: {str(e)}"
