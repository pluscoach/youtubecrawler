import anthropic
import json
from typing import Optional, Dict, List
from ..config import get_settings
from .perspectives import (
    get_critical_analysis_prompt,
    get_perspective,
    get_integrated_analysis_prompt,
    get_contradiction_analysis_prompt
)

settings = get_settings()

# 모델 설정 - 1단계는 빠른 Haiku, 2~3단계는 고품질 Sonnet
MODEL_FAST = "claude-3-haiku-20240307"  # 1단계: 빠른 필터링
MODEL_QUALITY = "claude-sonnet-4-20250514"  # 2~3단계: 상세 분석

# 1단계: 영상 분석 + 소재 적합성 판단 프롬프트
ANALYSIS_PROMPT_WITH_SUITABILITY = """너는 투자 유튜브 콘텐츠 기획자야.

아래 영상 자막을 분석해서 두 가지를 출력해줘.

[영상 자막]
{transcript}

---

[출력 형식 - 반드시 JSON 형식으로 응답]
{{
    "video_analysis": {{
        "summary": "영상 요약 (3~5문장으로 핵심 내용 정리)",
        "key_message": "이 영상이 전달하려는 한 줄 메시지",
        "key_points": ["주요 내용 1", "주요 내용 2", "주요 내용 3", "주요 내용 4", "주요 내용 5"],
        "quotes": [
            {{"text": "콘텐츠에 활용 가능한 명언/발언 원문", "speaker": "발언자"}}
        ],
        "people": [
            {{"name": "인물명", "role": "한 줄 설명 (예: 버크셔 해서웨이 회장)"}}
        ],
        "investment_strategy": "이 영상에서 말하는 투자법/철학 정리",
        "source_tracking": [
            {{
                "quote": "인용된 문장",
                "source_title": "원본 출처 (책 제목, 인터뷰명 등)",
                "source_type": "책|인터뷰 영상|기사|주주서한|논문|보고서|출처 확인 필요",
                "source_url": "URL 또는 null",
                "search_keywords": ["검색 키워드1", "검색 키워드2"]
            }}
        ]
    }},
    "suitability_analysis": {{
        "feasibility_issue": {{
            "exists": true,
            "content": "이 전략을 일반인이 실행하기 어려운 감정적/현실적 이유"
        }},
        "hidden_premise": {{
            "exists": true,
            "content": "이 전략이 암묵적으로 가정하는 조건 (예: 감정 통제 가능, 전문 팀 보유)"
        }},
        "criticism_point": {{
            "exists": true,
            "content": "논리적으로 반박하거나 모순을 지적할 수 있는 부분"
        }},
        "target_empathy": {{
            "level": "높음|중간|낮음",
            "reason": "직장인/대학생/부업러가 '나도 그래'라고 느낄 수 있는지 이유"
        }},
        "source_availability": {{
            "level": "높음|중간|낮음",
            "reason": "원본 인터뷰, 책, 기사 등 신뢰도 있는 출처 활용 가능 여부"
        }},
        "suitability_score": 3,
        "judgment": "적합|보류|부적합",
        "usage_recommendation": "메인 콘텐츠|숏폼|참고만|패스",
        "unsuitable_reason": "부적합/보류일 경우 사유, 적합이면 null"
    }}
}}

주의사항:
1. 반드시 유효한 JSON 형식으로만 응답하세요.
2. 다른 텍스트 없이 JSON만 출력하세요.
3. 한국어로 분석해주세요.
4. quotes는 자막에서 실제로 나온 문장을 그대로 사용하세요.
5. 등장 인물이 없으면 빈 배열로 응답하세요.
6. suitability_score는 1(매우 부적합)~5(매우 적합) 사이 정수
7. source_tracking: 출처 못 찾으면 source_type을 "출처 확인 필요"로, search_keywords에 검색 키워드 제안
"""


def parse_json_response(response_text: str) -> Dict:
    """Claude 응답에서 JSON 파싱"""
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    return json.loads(response_text)


async def analyze_transcript(transcript: str) -> tuple[Optional[Dict], Optional[str]]:
    """
    Claude API로 자막 분석 (영상 분석 + 소재 적합성 판단)

    Returns:
        Tuple[Optional[Dict], Optional[str]]: (분석 결과, 에러 메시지)
    """
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # 자막이 너무 길면 잘라내기 (Haiku 최적화)
        max_length = 50000
        if len(transcript) > max_length:
            transcript = transcript[:max_length] + "... (자막 일부 생략)"

        message = client.messages.create(
            model=MODEL_FAST,  # Haiku - 빠른 1단계 분석
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": ANALYSIS_PROMPT_WITH_SUITABILITY.format(transcript=transcript)
                }
            ]
        )

        # 응답 텍스트 추출
        response_text = message.content[0].text

        try:
            analysis_result = parse_json_response(response_text)
            return analysis_result, None
        except json.JSONDecodeError as e:
            return None, f"분석 결과 파싱 오류: {str(e)}"

    except anthropic.AuthenticationError:
        return None, "Anthropic API 인증 오류: API 키를 확인해주세요."
    except anthropic.RateLimitError:
        return None, "API 요청 한도 초과: 잠시 후 다시 시도해주세요."
    except Exception as e:
        return None, f"분석 중 오류 발생: {str(e)}"


async def analyze_critical_v2(
    perspective_id: str,
    summary: str,
    key_message: str,
    key_points: List[str],
    strategy: str,
    quotes: List[Dict],
    people: List[Dict],
    source_tracking: List[Dict],
    suitability_analysis: Dict
) -> tuple[Optional[Dict], Optional[str]]:
    """
    Claude API로 비판적 분석 수행 (1단계 결과 기반)

    Args:
        perspective_id: 분석 관점 ID
        summary: 영상 요약
        key_message: 핵심 메시지
        key_points: 키포인트
        strategy: 거장의 전략
        quotes: 인용 대사
        people: 등장 인물
        source_tracking: 출처 추적
        suitability_analysis: 소재 적합성 분석

    Returns:
        Tuple[Optional[Dict], Optional[str]]: (분석 결과, 에러 메시지)
    """
    try:
        # 소재 적합성 체크 - 부적합이면 분석 진행 안함
        if suitability_analysis:
            judgment = suitability_analysis.get('judgment', '')
            if judgment == '부적합':
                return {
                    "error": "unsuitable",
                    "message": "이 영상은 비판적 분석에 적합하지 않습니다.",
                    "reason": suitability_analysis.get('unsuitable_reason', '소재 부적합')
                }, None

        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # 1단계 결과 기반 프롬프트 생성
        prompt = get_critical_analysis_prompt(
            perspective_id=perspective_id,
            summary=summary,
            key_message=key_message,
            key_points=key_points,
            strategy=strategy,
            quotes=quotes,
            people=people,
            source_tracking=source_tracking,
            suitability_analysis=suitability_analysis
        )

        message = client.messages.create(
            model=MODEL_QUALITY,  # Sonnet - 고품질 2단계 분석
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = message.content[0].text

        try:
            analysis_result = parse_json_response(response_text)
            perspective = get_perspective(perspective_id)

            # 새 구조로 정규화
            normalized_result = {
                "perspective": perspective_id,
                "perspective_name": perspective.name,
                "hidden_premises": analysis_result.get("hidden_premises", []),
                "realistic_contradictions": analysis_result.get("realistic_contradictions", []),
                "source_based_contradictions": analysis_result.get("source_based_contradictions", []),
                "hooking_points": analysis_result.get("hooking_points", []),
                "content_direction": analysis_result.get("content_direction", []),
                "perspective_insights": analysis_result.get("perspective_insights", []),
                "contradiction_analyses": [],  # deprecated
            }

            return normalized_result, None

        except json.JSONDecodeError as e:
            return None, f"비판적 분석 결과 파싱 오류: {str(e)}"

    except anthropic.AuthenticationError:
        return None, "Anthropic API 인증 오류: API 키를 확인해주세요."
    except anthropic.RateLimitError:
        return None, "API 요청 한도 초과: 잠시 후 다시 시도해주세요."
    except Exception as e:
        return None, f"비판적 분석 중 오류 발생: {str(e)}"


# deprecated - 기존 호환용
async def analyze_critical(transcript: str, perspective_id: str) -> tuple[Optional[Dict], Optional[str]]:
    """[Deprecated] 기존 비판적 분석 - analyze_critical_v2 사용 권장"""
    return None, "이 함수는 deprecated되었습니다. analyze_critical_v2를 사용하세요."


async def analyze_contradictions(
    transcript: str,
    perspective_id: str,
    critical_points: List[str]
) -> tuple[Optional[List[Dict]], Optional[str]]:
    """
    출처 기반 모순 분석 수행

    Args:
        transcript: 자막 텍스트
        perspective_id: 분석 관점 ID
        critical_points: 비판적 분석 포인트들

    Returns:
        Tuple[Optional[List[Dict]], Optional[str]]: (모순 분석 결과, 에러 메시지)
    """
    if not critical_points:
        return [], None

    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        perspective = get_perspective(perspective_id)

        prompt = get_contradiction_analysis_prompt(
            perspective.name,
            transcript[:5000],  # 모순 분석은 요약된 버전 사용
            critical_points
        )

        message = client.messages.create(
            model=MODEL_QUALITY,  # Sonnet - 고품질 3단계 분석
            max_tokens=8192,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = message.content[0].text

        try:
            result = parse_json_response(response_text)
            return result.get("contradiction_analyses", []), None

        except json.JSONDecodeError as e:
            return None, f"모순 분석 파싱 오류: {str(e)}"

    except anthropic.AuthenticationError:
        return None, "Anthropic API 인증 오류: API 키를 확인해주세요."
    except anthropic.RateLimitError:
        return None, "API 요청 한도 초과: 잠시 후 다시 시도해주세요."
    except Exception as e:
        return None, f"모순 분석 중 오류 발생: {str(e)}"
