import os
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from typing import Optional, Tuple


def get_transcript_api():
    """환경변수에 따라 프록시 사용 여부 결정"""
    use_proxy = os.getenv("USE_PROXY", "false").lower() == "true"

    if use_proxy:
        proxy_username = os.getenv("WEBSHARE_USERNAME")
        proxy_password = os.getenv("WEBSHARE_PASSWORD")

        if proxy_username and proxy_password:
            return YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    proxy_username=proxy_username,
                    proxy_password=proxy_password,
                )
            )

    return YouTubeTranscriptApi()


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
    한국어 → 영어 → 자동생성 자막 순서로 찾음
    """
    try:
        api = get_transcript_api()

        # 사용 가능한 자막 목록 가져오기
        try:
            transcript_list = api.list(video_id)
        except Exception as e:
            return None, f"자막 목록 조회 실패: {str(e)}"

        try:
            transcripts = list(transcript_list)
        except Exception as e:
            return None, f"자막 목록 변환 실패: {str(e)}"

        if not transcripts:
            return None, "자막을 찾을 수 없습니다."

        target_transcript = None

        # 1. 한국어 자막 찾기 (수동 자막 우선)
        for transcript in transcripts:
            if transcript.language_code == 'ko' and not transcript.is_generated:
                target_transcript = transcript
                break

        # 2. 한국어 자동생성 자막 찾기
        if target_transcript is None:
            for transcript in transcripts:
                if transcript.language_code == 'ko' and transcript.is_generated:
                    target_transcript = transcript
                    break

        # 3. 영어 자막 찾기 (수동 자막 우선)
        if target_transcript is None:
            for transcript in transcripts:
                if transcript.language_code == 'en' and not transcript.is_generated:
                    target_transcript = transcript
                    break

        # 4. 영어 자동생성 자막 찾기
        if target_transcript is None:
            for transcript in transcripts:
                if transcript.language_code == 'en' and transcript.is_generated:
                    target_transcript = transcript
                    break

        # 5. 아무 자막이나 가져오기 (자동생성 포함)
        if target_transcript is None:
            target_transcript = transcripts[0]

        # 자막 가져오기
        try:
            transcript_data = target_transcript.fetch()
        except Exception as e:
            return None, f"자막 fetch 실패: {str(e)}"

        # 자막 텍스트 추출
        try:
            full_text = ' '.join([item.text for item in transcript_data])
        except Exception as e:
            return None, f"텍스트 추출 실패: {str(e)}"

        return full_text, None

    except Exception as e:
        return None, f"자막 추출 중 오류 발생: {str(e)}"
