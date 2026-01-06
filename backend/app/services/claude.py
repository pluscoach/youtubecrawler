import anthropic
import json
from typing import Optional, Dict
from ..config import get_settings

settings = get_settings()

ANALYSIS_PROMPT = """당신은 유튜브 콘텐츠 분석 전문가입니다.
아래 유튜브 영상 자막을 분석해서 다음 형식으로 정리해주세요.

[자막 내용]
{transcript}

[출력 형식 - 반드시 JSON 형식으로 응답]
{{
    "summary": "영상 요약 (3~5줄)",
    "key_message": "핵심 메시지 (한 문장)",
    "key_points": ["키포인트1", "키포인트2", "키포인트3"],
    "quotes": ["인용할 만한 대사1", "인용할 만한 대사2"],
    "people": [
        {{"name": "이름", "role": "역할", "related_links": []}}
    ],
    "content_ideas": [
        {{
            "target": "뇌동매매 타겟",
            "title_example": "제목 예시",
            "direction": "활용 방향"
        }},
        {{
            "target": "원칙 투자 타겟",
            "title_example": "제목 예시",
            "direction": "활용 방향"
        }},
        {{
            "target": "경제적 자유 타겟",
            "title_example": "제목 예시",
            "direction": "활용 방향"
        }}
    ],
    "script_direction": {{
        "intro": "도입 내용",
        "development": "전개 내용",
        "transition": "전환 내용",
        "conclusion": "마무리 내용"
    }}
}}

주의사항:
1. 반드시 유효한 JSON 형식으로만 응답하세요.
2. 다른 텍스트 없이 JSON만 출력하세요.
3. 한국어로 분석해주세요.
4. 인용 대사는 자막에서 실제로 나온 문장을 그대로 사용하세요.
5. 등장 인물이 없으면 빈 배열로 응답하세요.
"""


async def analyze_transcript(transcript: str) -> tuple[Optional[Dict], Optional[str]]:
    """
    Claude API로 자막 분석

    Returns:
        Tuple[Optional[Dict], Optional[str]]: (분석 결과, 에러 메시지)
    """
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # 자막이 너무 길면 잘라내기 (Claude 컨텍스트 제한)
        max_length = 100000
        if len(transcript) > max_length:
            transcript = transcript[:max_length] + "... (자막이 너무 길어 일부가 생략되었습니다)"

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT.format(transcript=transcript)
                }
            ]
        )

        # 응답 텍스트 추출
        response_text = message.content[0].text

        # JSON 파싱
        try:
            # JSON 블록 추출 (```json ... ``` 형식 처리)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()

            analysis_result = json.loads(response_text)
            return analysis_result, None

        except json.JSONDecodeError as e:
            return None, f"분석 결과 파싱 오류: {str(e)}"

    except anthropic.AuthenticationError:
        return None, "Anthropic API 인증 오류: API 키를 확인해주세요."
    except anthropic.RateLimitError:
        return None, "API 요청 한도 초과: 잠시 후 다시 시도해주세요."
    except Exception as e:
        return None, f"분석 중 오류 발생: {str(e)}"
