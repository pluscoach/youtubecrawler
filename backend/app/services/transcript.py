import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
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
        # 한국어 자막 우선 시도
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript = None

        # 한국어 자막 찾기
        try:
            transcript = transcript_list.find_transcript(['ko'])
        except NoTranscriptFound:
            pass

        # 한국어 없으면 영어 시도
        if transcript is None:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                pass

        # 둘 다 없으면 자동 생성 자막 시도
        if transcript is None:
            try:
                transcript = transcript_list.find_generated_transcript(['ko', 'en'])
            except NoTranscriptFound:
                pass

        if transcript is None:
            return None, "자막을 찾을 수 없습니다."

        # 자막 텍스트 추출
        transcript_data = transcript.fetch()
        full_text = " ".join([entry['text'] for entry in transcript_data])

        return full_text, None

    except TranscriptsDisabled:
        return None, "이 영상은 자막이 비활성화되어 있습니다."
    except VideoUnavailable:
        return None, "영상을 찾을 수 없습니다."
    except Exception as e:
        return None, f"자막 추출 중 오류 발생: {str(e)}"
