import anthropic
import json
from typing import Optional, Dict, List, Any
from ..config import get_settings

settings = get_settings()

# 추가 분석 프롬프트
ADDITIONAL_ANALYSIS_PROMPT = """너는 투자 유튜브 콘텐츠 전문 기획자야.

[입력 데이터 - 1단계 영상 분석 결과]
- 영상 요약: {summary}
- 핵심 메시지: {key_message}
- 키포인트: {key_points}
- 거장의 전략: {strategy}
- 인용할 대사: {quotes}
- 등장 인물: {people}
- 출처 추적: {source_tracking}
- 소재 적합성 판단: {suitability_analysis}

[입력 데이터 - 2단계 비판적 분석 결과]
- 숨겨진 전제: {hidden_premises}
- 현실적 모순: {realistic_contradictions}
- 출처 기반 모순 분석: {source_based_contradictions}
- 후킹 포인트: {hooking_points}
- 콘텐츠 방향: {content_direction}

[채널 철학 - 고정값]
- 핵심 메시지: 거장의 전략은 틀리지 않았다. 문제는 실행이다.
- 톤: 비판적이지만 논리적, 감정적 비난 X
- 타겟: 직장인/대학생/부업러 (시간 없고, 감정 조절 어려운 사람들)
- 절대 하지 않을 것: 자동매매 과도한 홍보, 영상 전체가 유도용
- 자동매매 언급: 전개3에서 가볍게 한 줄 (감정 개입 없이 원칙대로 실행되는 방법)
- 멤버십 언급: 공감 파트에서 자연스럽게 ("더 자세한 방법은 멤버십에")
- 마무리: 비판적 사고 + 자신에게 유리한 전략 개선 = 투자 본질/원칙

위 데이터를 기반으로 추가 분석을 진행해.

---

[출력 형식 - 반드시 JSON 형식으로 응답]

{{
  "thumbnail_suggestions": [
    {{
      "type": "반전형|질문형|숫자형|권위형|공감형",
      "text": "10자 이내 문구",
      "basis": "어떤 후킹 포인트/모순점/데이터/인물/감정 활용했는지",
      "click_psychology": "왜 클릭하게 되는지 심리"
    }}
  ],
  "title_suggestions": [
    {{
      "pattern": "권위 뒤집기|공감형|논쟁형|호기심형|숫자형",
      "title": "40자 이내 제목",
      "basis": "출처 기반 모순/현실적 모순/숨겨진 전제/후킹 포인트/근거 데이터 활용",
      "target": "어떤 타겟에게 효과적인지"
    }}
  ],
  "video_length": {{
    "recommended_length": "00분 00초",
    "format": "숏폼|미드폼|롱폼",
    "judgment_basis": "모순 분석 개수 + 출처 설명 필요 여부 + 스토리 전환점 수",
    "parts": [
      {{
        "part": "인트로|전개1|전개2|전개3|공감|꿀팁|마무리",
        "time_range": "0:00~0:00",
        "content": "해당 파트 내용"
      }}
    ]
  }},
  "script_directions": [
    {{
      "part": "인트로 (후킹)|전개1 (권위 인정)|전개2 (모순 제기)|전개3 (원인 분석 + 자동매매 힌트)|공감 (멤버십 언급)|꿀팁|마무리",
      "keypoint": "예시 문장",
      "basis": "활용 근거 (후킹 포인트/거장의 전략/출처 기반 모순/숨겨진 전제/현실적 모순/관련 실용 정보/채널 철학)",
      "emotion": "호기심: '뭔데?'|신뢰: '맞아, 대단하지'|의외: '어? 진짜?'|납득: '아, 그래서...'|안심: '내 탓 아니었네' + 관심|만족: '이건 건졌다'|완결: '좋은 영상이었다'"
    }}
  ],
  "bonus_tip": {{
    "topic": "꿀팁 주제",
    "summary": "내용 요약 (바로 실행 가능한 구체적 내용)",
    "why_helpful": "왜 도움 되는지",
    "source": "출처명",
    "source_url": "출처 링크 또는 null"
  }},
  "video_sources": {{
    "interview_clips": [
      {{
        "person": "인물명",
        "video_title": "영상 제목",
        "quote": "발언 내용",
        "timestamp": "시간대 (예: 2:35~3:10)",
        "link": "실제 YouTube URL (예: https://www.youtube.com/watch?v=...) 또는 '검색: [검색어]'"
      }}
    ],
    "evidence_sources": [
      {{
        "contradiction": "모순 내용",
        "evidence": "증거 자료",
        "source_type": "기사|논문|보고서|영상",
        "link": "실제 URL (한국거래소: https://data.krx.co.kr, 금융감독원: https://www.fss.or.kr 등) 또는 '검색: [검색어]'"
      }}
    ],
    "broll_keywords": [
      {{
        "scene": "장면 설명",
        "keyword": "검색 키워드 (영문)",
        "usage_part": "활용 파트"
      }}
    ],
    "veo3_prompts": [
      {{
        "scene": "장면 설명",
        "prompt": "Veo3 프롬프트 (영문, 상세하게)",
        "usage_part": "활용 파트"
      }}
    ]
  }},
  "performance_prediction": {{
    "target_fits": [
      {{
        "target": "직장인|대학생|부업러",
        "fit_level": 1~5,
        "reason": "적합도 이유"
      }}
    ],
    "controversy": {{
      "level": 1~5,
      "expected_reactions": "예상 반응 설명"
    }},
    "expected_comments": [
      {{
        "type": "긍정|부정|질문",
        "comment": "예상 댓글"
      }}
    ],
    "series_expansions": [
      {{
        "topic": "후속 영상 주제",
        "connection": "연결 포인트"
      }}
    ]
  }},
  "membership_connection": {{
    "timings": [
      {{
        "timing": "추천 타이밍 (예: 6:30)",
        "video_position": "영상 위치 (예: 공감 파트 직후)",
        "reason": "왜 자연스러운지"
      }}
    ],
    "contexts": [
      {{
        "previous_line": "직전 대사",
        "connection": "멤버십 연결 문구 (자동화/시스템 관점)"
      }}
    ],
    "teasers": [
      {{
        "situation": "상황 (예: 자동매매 언급 후)",
        "teaser": "티저 문구 - 반드시 자동화/시스템 관점으로 작성"
      }}
    ],
    "content_suggestions": [
      {{
        "topic": "멤버십 콘텐츠 주제 (자동화 관점)",
        "connection": "이 영상과 연결점"
      }}
    ]
  }}
}}

[주의사항]
1. 반드시 유효한 JSON 형식으로만 응답하세요.
2. 다른 텍스트 없이 JSON만 출력하세요.
3. 한국어로 분석해주세요. (B-roll 키워드, Veo3 프롬프트는 영문)
4. 자동매매는 전개3에서 한 줄만, 과도한 홍보 금지
5. 멤버십은 공감 파트에서 자연스럽게만
6. 꿀팁은 영상 자체 가치를 높이는 실용 정보
7. 마무리는 광고/유도가 아닌 투자 철학으로 완결
8. 영상 소스 링크 규칙:
   - interview_clips: 실제 YouTube URL (https://www.youtube.com/watch?v=...) 필수, 못 찾으면 "검색: [검색어]"
   - evidence_sources: 실제 기사/보고서 URL 필수, 한국거래소(data.krx.co.kr), 금융감독원(fss.or.kr) 등
   - 링크 못 찾으면 반드시 "검색: [검색어]" 형식으로 표시
9. 성과 예측은 근거 기반으로
10. 모든 추천에는 근거 명시
11. thumbnail_suggestions는 5개 (유형별 1개씩)
12. title_suggestions는 5개 (패턴별 1개씩)
13. script_directions는 7개 (파트별 1개씩)
14. 멤버십 연결 포인트 필수 규칙:
    - 절대 금지: "구체적인 투자 방법", "어떤 종목 사야 하는지", "수익률 보장"
    - 반드시 사용: "자동화", "시스템", "감정 개입 없이", "원칙대로 실행"
    - 티저 문구 예시:
      * "이 전략을 자동으로 실행하는 방법, 멤버십에서 다룹니다"
      * "감정 없이 원칙대로 매매하는 시스템, 멤버십에서 공개합니다"
      * "자동화된 매매 시스템 구축법은 멤버십에서 확인하세요"
    - 멤버십 콘텐츠 제안도 자동화 관점:
      * "버핏 20개 투자권을 자동매매로 구현하는 법"
      * "손절 원칙을 자동 실행하는 EA 설정"
      * "감정 배제 시스템 구축 가이드"

15. 전개3 (자동매매 힌트) 예시 문구 - 실제 구현 가능한 것만:
    - ✅ 사용 가능:
      * "그래서 저는 재무제표를 자동으로 분석하는 시스템을 만들었습니다"
      * "뉴스가 나오면 자동으로 알림 오게 세팅해뒀어요"
      * "규칙 정해두면 프로그램이 알아서 매수/매도 해줍니다"
      * "백테스팅으로 전략 검증하고 자동 실행하게 했어요"
      * "손절 원칙을 코드로 정해두니까 감정이 개입할 틈이 없어요"
      * "RSI가 30 이하로 떨어지면 알림 오게 설정해뒀습니다"
    - ❌ 절대 쓰지 말 것:
      * "AI가 알아서 좋은 종목 찾아줍니다" (과장)
      * "기업 분석을 자동화했습니다" (질적 분석은 불가능)
      * "자동으로 수익 나는 시스템" (수익 보장 불가)
      * "AI가 시장을 예측합니다" (과장)

16. 멤버십 콘텐츠 제안 - 실제 구현 가능한 것만:
    - ✅ 제안 가능:
      * "Python으로 재무제표 크롤링하는 법"
      * "키움증권 API로 자동매매 봇 만들기"
      * "MT5 자동매매 EA 기초 설정"
      * "텔레그램 알림 봇 연동하기"
      * "백테스팅으로 전략 검증하는 법"
      * "뉴스 크롤링 + 감성 분석 기초"
      * "업비트 API로 코인 자동매매"
      * "트레일링 스탑 자동화하기"
      * "포트폴리오 리밸런싱 자동화"
    - ❌ 제안하지 말 것:
      * "AI가 종목 추천해주는 시스템" (과장)
      * "수익률 보장 전략" (불가능)
      * "기업 분석 자동화" (질적 분석 불가)
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


def format_list_for_prompt(items: List[Any]) -> str:
    """리스트를 프롬프트용 문자열로 변환"""
    if not items:
        return "없음"

    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(json.dumps(item, ensure_ascii=False))
        elif isinstance(item, str):
            result.append(item)
        else:
            result.append(str(item))

    return "\n".join(f"- {r}" for r in result)


async def analyze_additional(
    summary: str,
    key_message: str,
    key_points: List[str],
    strategy: str,
    quotes: List[Any],
    people: List[Dict],
    source_tracking: List[Dict],
    suitability_analysis: Dict,
    hidden_premises: List[Any],
    realistic_contradictions: List[Any],
    source_based_contradictions: List[Any],
    hooking_points: List[Any],
    content_direction: Any
) -> tuple[Optional[Dict], Optional[str]]:
    """
    Claude API로 추가 분석 수행 (1단계 + 2단계 결과 기반)

    Returns:
        Tuple[Optional[Dict], Optional[str]]: (분석 결과, 에러 메시지)
    """
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        # 프롬프트 생성
        prompt = ADDITIONAL_ANALYSIS_PROMPT.format(
            summary=summary,
            key_message=key_message,
            key_points=format_list_for_prompt(key_points),
            strategy=strategy or "없음",
            quotes=format_list_for_prompt(quotes),
            people=format_list_for_prompt(people),
            source_tracking=format_list_for_prompt(source_tracking),
            suitability_analysis=json.dumps(suitability_analysis, ensure_ascii=False) if suitability_analysis else "없음",
            hidden_premises=format_list_for_prompt(hidden_premises),
            realistic_contradictions=format_list_for_prompt(realistic_contradictions),
            source_based_contradictions=format_list_for_prompt(source_based_contradictions),
            hooking_points=format_list_for_prompt(hooking_points),
            content_direction=json.dumps(content_direction, ensure_ascii=False) if content_direction else "없음"
        )

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
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
            return analysis_result, None

        except json.JSONDecodeError as e:
            return None, f"추가 분석 결과 파싱 오류: {str(e)}"

    except anthropic.AuthenticationError:
        return None, "Anthropic API 인증 오류: API 키를 확인해주세요."
    except anthropic.RateLimitError:
        return None, "API 요청 한도 초과: 잠시 후 다시 시도해주세요."
    except Exception as e:
        return None, f"추가 분석 중 오류 발생: {str(e)}"
