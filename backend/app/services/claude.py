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

# 1단계: 영상 분석 + 소재 적합성 판단 + 영상 구조 분석 프롬프트
ANALYSIS_PROMPT_WITH_SUITABILITY = """너는 투자 유튜브 콘텐츠 기획자야.

아래 영상 자막을 분석해서 세 가지를 출력해줘.

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
                "source_url": "실제 접근 가능한 URL 또는 null",
                "search_keywords": ["검색 키워드1", "검색 키워드2"]
            }}
        ]
    }},
    "video_structure": {{
        "structure_items": [
            {{
                "order": 1,
                "element": "후킹",
                "type": "질문형|충격형|공감형|권위형",
                "description": "실제 사용된 문장이나 방식"
            }},
            {{
                "order": 2,
                "element": "권위 인정",
                "type": null,
                "description": "인물 소개, 실적 언급 등"
            }}
        ],
        "structure_summary": "후킹(질문) → 권위 → 주장 → 근거 → 반박 → CTA"
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
        "auto_trading_potential": {{
            "level": "높음|중간|낮음|없음",
            "implementable": ["구현 가능한 요소1", "구현 가능한 요소2"],
            "not_implementable": ["구현 불가능한 요소1"],
            "reason": "Claude와 코드 개발로 구현 가능한 부분과 불가능한 부분"
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
7. source_tracking 출처 링크 작성 규칙:
   - 출처 링크는 반드시 실제 접근 가능한 URL로 제공
   - 기사: 실제 기사 URL (예: https://www.hankyung.com/...)
   - 논문: Google Scholar 또는 원문 링크
   - 인터뷰 영상: YouTube 영상 URL (예: https://www.youtube.com/watch?v=...)
   - 책: 교보문고, Yes24, 알라딘, Google Books 링크
   - 보고서: 원본 PDF 또는 발행 기관 페이지
   - URL을 찾을 수 없으면: source_url은 null, source_type은 "출처 확인 필요", search_keywords에 검색 키워드 제안
8. auto_trading_potential (자동매매 연결 가능성) 평가 기준 - Claude와 코드 개발로 구현 가능한가?:
   - 높음: 기술적 지표(RSI, MACD 등), 규칙 기반 매매, 손절/익절 자동화, 알림 시스템
   - 중간: 재무 데이터 분석(PER, PBR 필터링), 뉴스 감성 분석, 백테스팅
   - 낮음: 복잡한 예측, 질적 분석 요소 포함
   - 없음: 물리적 행동, 경영진 면담, 직관/경험 기반 판단
   - implementable에는 실제 코드로 구현 가능한 요소만 작성
   - not_implementable에는 코드로 구현 불가능한 요소 작성
9. video_structure (영상 구조 분석) 작성 규칙:
   - 영상에서 사용된 구조 요소들을 순서대로 분석
   - element 종류: 후킹, 권위 인정, 핵심 주장, 근거 제시, 반박/모순 제기, 해결 암시, 꿀팁, CTA
   - 후킹 type 종류: 질문형, 충격형, 공감형, 권위형
   - description은 실제 영상에서 사용된 문장이나 방식 구체적으로 작성
   - structure_summary는 "후킹(질문) → 권위 → 주장 → 근거 → CTA" 형식으로 요약
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
            max_tokens=4096,
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

        # Tavily로 보완 사례 검색 (자동매매 관점일 때만)
        improvement_search_results = []
        if perspective_id == "auto_trading":
            from .tavily_search import search_improvement_cases

            # 등장 인물에서 거장 이름 추출
            master_names = [p.get("name", "") for p in people if p.get("name")]

            # 소재 적합성에서 문제점 추출
            problems = []
            if suitability_analysis:
                feasibility = suitability_analysis.get('feasibility_issue', {})
                if feasibility.get('exists') and feasibility.get('content'):
                    problems.append(feasibility.get('content')[:50])
                hidden = suitability_analysis.get('hidden_premise', {})
                if hidden.get('exists') and hidden.get('content'):
                    problems.append(hidden.get('content')[:50])

            # 각 거장에 대해 보완 사례 검색
            for master_name in master_names[:2]:  # 최대 2명만
                print(f"[Improvement Search] Searching for: {master_name}")
                results = search_improvement_cases(master_name, problems)
                improvement_search_results.extend(results)

            print(f"[Improvement Search] Total results: {len(improvement_search_results)}")

        # 1단계 결과 기반 프롬프트 생성 (보완 사례 검색 결과 포함)
        prompt = get_critical_analysis_prompt(
            perspective_id=perspective_id,
            summary=summary,
            key_message=key_message,
            key_points=key_points,
            strategy=strategy,
            quotes=quotes,
            people=people,
            source_tracking=source_tracking,
            suitability_analysis=suitability_analysis,
            improvement_search_results=improvement_search_results
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

            # DEBUG: Claude 원본 응답 키 확인
            print(f"[DEBUG] Claude 원본 응답 keys: {analysis_result.keys()}")

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
                "auto_trading_connection": analysis_result.get("auto_trading_connection", []),
                "automation_insight": analysis_result.get("automation_insight"),
                "contradiction_analyses": [],  # deprecated
            }

            # DEBUG: automation_insight 상세 확인
            print(f"[DEBUG] Claude 응답에서 automation_insight 존재: {'automation_insight' in analysis_result}")
            if analysis_result.get("automation_insight"):
                ai = analysis_result.get('automation_insight')
                print(f"[DEBUG] automation_insight keys: {ai.keys()}")
                print(f"[DEBUG] ├─ improvement_cases 개수: {len(ai.get('improvement_cases', []))}")
                print(f"[DEBUG] ├─ differentiation_points 개수: {len(ai.get('differentiation_points', []))}")
                # differentiation_points type 확인
                for i, dp in enumerate(ai.get('differentiation_points', [])):
                    print(f"[DEBUG] │  differentiation_points[{i}] type: {dp.get('type', 'MISSING')}")

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


async def verify_sources(analysis_result: Dict) -> Dict:
    """
    Claude가 언급한 출처들을 Tavily로 검증하고 실제 URL 추가

    Args:
        analysis_result: Claude 분석 결과

    Returns:
        출처 링크가 추가된 분석 결과
    """
    from .tavily_search import search_source_by_type

    print("[Tavily] verify_sources 호출됨")

    # 1. 출처 추적 (source_tracking) 검증
    if "video_analysis" in analysis_result and "source_tracking" in analysis_result["video_analysis"]:
        sources = analysis_result["video_analysis"]["source_tracking"]
        print(f"[Tavily] source_tracking 개수: {len(sources)}")

        for i, source in enumerate(sources):
            source_title = source.get("source_title", "")
            source_type = source.get("source_type", "기타")
            quote = source.get("quote", "")
            existing_url = source.get("source_url")

            print(f"[Tavily] [{i+1}] 출처: {source_title}, 유형: {source_type}, 기존URL: {existing_url}")

            # URL이 없거나 null인 경우 검색
            if source_title and (not existing_url or existing_url == "null" or existing_url is None):
                print(f"[Tavily] [{i+1}] Tavily 검색 시작: {source_title}")
                result = search_source_by_type(source_title, source_type, quote)
                print(f"[Tavily] [{i+1}] 검색 결과: found={result.get('found')}, url={result.get('url')}")

                source["source_url"] = result.get("url")
                source["verified"] = result.get("found", False)
                source["search_query"] = result.get("search_query", source_title)
            else:
                print(f"[Tavily] [{i+1}] 이미 URL 있음, 스킵")

    # 2. 소재 적합성의 출처들은 별도 처리 불필요 (텍스트만 있음)

    return analysis_result


async def verify_critical_sources(critical_result: Dict) -> Dict:
    """
    비판적 분석 결과의 출처들을 Tavily로 검증하고 실제 URL 추가

    Args:
        critical_result: 비판적 분석 결과

    Returns:
        출처 링크가 추가된 분석 결과
    """
    from .tavily_search import search_source_by_type

    print("[Tavily] verify_critical_sources 호출됨")

    def needs_url_search(url_value):
        """URL 검색이 필요한지 확인 (null, 빈값, 'null' 문자열 등)"""
        if not url_value:
            return True
        if isinstance(url_value, str):
            url_lower = url_value.lower().strip()
            if url_lower in ['null', 'none', '', '-']:
                return True
            # Google 검색 URL도 재검색 대상
            if 'google.com/search' in url_lower:
                return True
        return False

    # 1. 숨겨진 전제 (hidden_premises) 출처 검증
    if "hidden_premises" in critical_result:
        print(f"[Tavily] hidden_premises 개수: {len(critical_result['hidden_premises'])}")
        for i, premise in enumerate(critical_result["hidden_premises"]):
            if isinstance(premise, dict) and premise.get("source"):
                current_url = premise.get("source_url")
                print(f"[Tavily] hidden_premise[{i}] 현재 source_url: {current_url}")
                if needs_url_search(current_url):
                    print(f"[Tavily] hidden_premise[{i}] 검색: {premise.get('source')}")
                    result = search_source_by_type(premise["source"], "기타", premise.get("premise", ""))
                    premise["source_url"] = result.get("url")
                    premise["verified"] = result.get("found", False)
                    print(f"[Tavily] hidden_premise[{i}] 결과: found={result.get('found')}, url={result.get('url')}")

    # 2. 현실적 모순 (realistic_contradictions) 출처 검증
    if "realistic_contradictions" in critical_result:
        print(f"[Tavily] realistic_contradictions 개수: {len(critical_result['realistic_contradictions'])}")
        for i, contradiction in enumerate(critical_result["realistic_contradictions"]):
            if isinstance(contradiction, dict) and contradiction.get("source"):
                current_url = contradiction.get("source_url")
                print(f"[Tavily] contradiction[{i}] 현재 source_url: {current_url}")
                if needs_url_search(current_url):
                    print(f"[Tavily] contradiction[{i}] 검색: {contradiction.get('source')}")
                    result = search_source_by_type(contradiction["source"], "기타", contradiction.get("strategy", ""))
                    contradiction["source_url"] = result.get("url")
                    contradiction["verified"] = result.get("found", False)
                    print(f"[Tavily] contradiction[{i}] 결과: found={result.get('found')}, url={result.get('url')}")

    # 3. 출처 기반 모순 분석 (source_based_contradictions) 출처 검증
    if "source_based_contradictions" in critical_result:
        print(f"[Tavily] source_based_contradictions 개수: {len(critical_result['source_based_contradictions'])}")
        for i, item in enumerate(critical_result["source_based_contradictions"]):
            if isinstance(item, dict):
                # 원본 출처
                if item.get("original_source") and needs_url_search(item.get("original_source_url")):
                    print(f"[Tavily] sbc[{i}] original 검색: {item.get('original_source')}")
                    result = search_source_by_type(item["original_source"], "기타", item.get("original_claim", ""))
                    item["original_source_url"] = result.get("url")
                    print(f"[Tavily] sbc[{i}] original 결과: {result.get('url')}")

                # 반례 출처
                if item.get("counterexample_source") and needs_url_search(item.get("counterexample_source_url")):
                    print(f"[Tavily] sbc[{i}] counter 검색: {item.get('counterexample_source')}")
                    result = search_source_by_type(item["counterexample_source"], "기타", item.get("counterexample", ""))
                    item["counterexample_source_url"] = result.get("url")
                    print(f"[Tavily] sbc[{i}] counter 결과: {result.get('url')}")

                # 숨겨진 조건 출처
                if item.get("hidden_condition_source") and needs_url_search(item.get("hidden_condition_source_url")):
                    print(f"[Tavily] sbc[{i}] hidden 검색: {item.get('hidden_condition_source')}")
                    result = search_source_by_type(item["hidden_condition_source"], "기타", item.get("hidden_condition", ""))
                    item["hidden_condition_source_url"] = result.get("url")
                    print(f"[Tavily] sbc[{i}] hidden 결과: {result.get('url')}")

    print(f"[Tavily] verify_critical_sources 완료")
    return critical_result


async def verify_additional_sources(additional_result: Dict) -> Dict:
    """
    추가 분석 결과의 출처들을 Tavily로 검증하고 실제 URL 추가

    Args:
        additional_result: 추가 분석 결과

    Returns:
        출처 링크가 추가된 분석 결과
    """
    from .tavily_search import search_interview_clip, search_evidence_source, search_book_source

    def needs_url_search(url_value):
        """URL 검색이 필요한지 확인"""
        if not url_value:
            return True
        if isinstance(url_value, str):
            url_lower = url_value.lower().strip()
            if url_lower in ['null', 'none', '', '-']:
                return True
            if url_lower.startswith('검색:'):
                return True
            if 'google.com/search' in url_lower:
                return True
        return False

    print("[Tavily] verify_additional_sources 호출됨", flush=True)

    # 1. video_sources.interview_clips 검증 (YouTube 우선)
    video_sources = additional_result.get("video_sources", {})
    if video_sources:
        interview_clips = video_sources.get("interview_clips", [])
        if interview_clips:
            print(f"[Tavily] interview_clips 개수: {len(interview_clips)}", flush=True)
            for i, clip in enumerate(interview_clips):
                if isinstance(clip, dict) and needs_url_search(clip.get("link")):
                    person = clip.get("person", "")
                    video_title = clip.get("video_title", "")
                    quote = clip.get("quote", "")
                    print(f"[Tavily] interview_clip[{i}] 검색: {person} - {video_title}", flush=True)
                    result = search_interview_clip(person, video_title, quote)
                    clip["link"] = result.get("url")
                    clip["verified"] = result.get("found", False)
                    print(f"[Tavily] interview_clip[{i}] 결과: {result.get('url')}", flush=True)

        # 2. video_sources.evidence_sources 검증
        evidence_sources = video_sources.get("evidence_sources", [])
        if evidence_sources:
            print(f"[Tavily] evidence_sources 개수: {len(evidence_sources)}", flush=True)
            for i, ev in enumerate(evidence_sources):
                if isinstance(ev, dict) and needs_url_search(ev.get("link")):
                    evidence = ev.get("evidence", "")
                    source_type = ev.get("source_type", "")
                    print(f"[Tavily] evidence[{i}] 검색: {evidence} ({source_type})", flush=True)
                    result = search_evidence_source(evidence, source_type)
                    ev["link"] = result.get("url")
                    ev["verified"] = result.get("found", False)
                    print(f"[Tavily] evidence[{i}] 결과: {result.get('url')}", flush=True)

    # 3. bonus_tip.source_url 검증
    bonus_tip = additional_result.get("bonus_tip", {})
    if bonus_tip and isinstance(bonus_tip, dict):
        if needs_url_search(bonus_tip.get("source_url")):
            source = bonus_tip.get("source", "")
            if source:
                print(f"[Tavily] bonus_tip 검색: {source}", flush=True)
                result = search_book_source(source)  # 교보문고 우선
                bonus_tip["source_url"] = result.get("url")
                bonus_tip["verified"] = result.get("found", False)
                print(f"[Tavily] bonus_tip 결과: {result.get('url')}", flush=True)

    print("[Tavily] verify_additional_sources 완료", flush=True)
    return additional_result
