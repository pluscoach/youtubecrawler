"""
비판적 분석 관점 관리 모듈
각 관점별로 Claude에게 전달할 프롬프트 템플릿을 관리합니다.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Perspective:
    """분석 관점 정의"""
    id: str
    name: str
    description: str
    focus_area: str  # 해당 관점의 핵심 초점


# 비판적 분석 관점 정의
PERSPECTIVES: Dict[str, Perspective] = {
    "auto_trading": Perspective(
        id="auto_trading",
        name="자동매매 관점",
        description="투자 전략을 자동매매 시스템 관점에서 비판적으로 분석합니다. (Claude와 코드 개발로 구현 가능한 것 기준)",
        focus_area="코드로 자동화 가능한 부분 (기술적 지표, 규칙 기반 매매, 리스크 관리)"
    ),
    "value_investing": Perspective(
        id="value_investing",
        name="가치투자 관점",
        description="워렌 버핏 스타일의 가치투자 관점에서 비판적으로 분석합니다.",
        focus_area="본질 가치 분석, 안전마진, 장기 보유 관점"
    ),
    "day_trading": Perspective(
        id="day_trading",
        name="단타 관점",
        description="데이트레이딩/단기매매 관점에서 비판적으로 분석합니다.",
        focus_area="진입/청산 타이밍, 손절 기준, 리스크 관리"
    ),
    "psychology": Perspective(
        id="psychology",
        name="심리 분석 관점",
        description="투자 심리학 관점에서 비판적으로 분석합니다.",
        focus_area="심리적 함정 극복, 행동경제학 적용"
    ),
}

# 기본 관점
DEFAULT_PERSPECTIVE = "auto_trading"


def get_perspective(perspective_id: str) -> Perspective:
    """관점 ID로 관점 정보 조회"""
    return PERSPECTIVES.get(perspective_id, PERSPECTIVES[DEFAULT_PERSPECTIVE])


def get_all_perspectives() -> List[Dict]:
    """모든 관점 목록 반환 (프론트엔드용)"""
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
        }
        for p in PERSPECTIVES.values()
    ]


# 자동매매 구현 가능 범위 정의
AUTO_TRADING_SCOPE = """
[자동매매 구현 가능 범위 - Claude와 코드 개발 기준]

✅ 구현 가능:
- 기술적 지표 기반 자동매매 (RSI, MACD, 볼린저밴드, 이동평균 등)
- 규칙 기반 매수/매도 자동화 (조건 충족 시 자동 주문)
- 재무제표 크롤링 + 정량 분석 (PER, PBR, ROE 등 수치 필터링)
- 뉴스/공시 크롤링 + 감성 분석 (키워드 기반)
- 24시간 모니터링 봇 (가격/거래량 알림)
- 포트폴리오 리밸런싱 자동화
- 손절/익절 자동화 (트레일링 스탑)
- 백테스팅 자동화
- 알림 시스템 연동 (텔레그램, 카카오톡, 이메일)
- API 기반 자동 주문 (키움증권, 업비트, 바이낸스 등)

⚠️ 부분 가능 (한계 있음):
- 저평가 성장주 발굴 → 재무 데이터 필터링은 가능, 질적 판단은 어려움
- AI 기반 예측 → 단순 패턴 인식은 가능, 복잡한 시장 예측은 한계
- 뉴스 해석 → 키워드 감성 분석은 가능, 맥락 파악은 제한적

❌ 구현 불가능:
- 기업 방문, 매장 직접 확인 등 물리적 행동
- 경영진 면담, 인맥 기반 정보 수집
- 직관, 감각, 경험 기반 판단
- 비공개 정보 접근
- 정성적 기업 분석 (경영진 역량, 기업 문화 등)
"""

# 비판적 분석 프롬프트 (1단계 결과 기반)
CRITICAL_ANALYSIS_PROMPT = """너는 투자 철학 비평가야. 감정적 비난이 아닌 논리적 근거로 분석해.

[입력 데이터 - 1단계 영상 분석 결과]
- 영상 요약: {summary}
- 핵심 메시지: {key_message}
- 키포인트: {key_points}
- 거장의 전략: {strategy}
- 인용할 대사: {quotes}
- 등장 인물: {people}
- 출처 추적: {source_tracking}
- 소재 적합성 판단: {suitability_analysis}

[분석 관점]
{perspective_name}: {perspective_focus}

위 1단계 분석 결과를 기반으로 비판적 분석을 진행해.

---

[비판적 분석 원칙]

1. 거장의 전략 자체는 틀리지 않았다고 전제해
2. 문제는 "일반인이 실행할 수 있는가"에 집중해
3. 모든 비판은 출처 기반 팩트로 뒷받침해
4. 감정적 표현("할 수 있을까?", "누가 해?") 대신 데이터/사례로 말해
5. 1단계에서 추출한 출처 추적 데이터를 적극 활용해

---

[출력 형식 - 반드시 JSON 형식으로 응답]
{{
    "hidden_premises": [
        {{
            "premise": "암묵적으로 가정하는 조건",
            "why_problem": "왜 비현실적인지 데이터로 증명 (구체적 수치 포함)",
            "source": "출처명 (책/기사/논문/인터뷰/보고서)",
            "source_url": "URL 또는 null"
        }}
    ],
    "realistic_contradictions": [
        {{
            "strategy": "영상에서 말한 전략",
            "difficulty_reason": "실행 어려운 이유 (행동경제학/심리학 용어 활용)",
            "evidence_data": "근거 데이터 (%, 년도, 수치)",
            "source": "출처명",
            "source_url": "URL 또는 null"
        }}
    ],
    "source_based_contradictions": [
        {{
            "original_claim": "거장이 말한 원본 주장",
            "original_source": "원본 출처 (년도, 매체)",
            "original_source_url": "URL 또는 null",
            "counterexample": "실제 데이터/사례로 반박",
            "counterexample_source": "반례 출처",
            "counterexample_source_url": "URL 또는 null",
            "hidden_condition": "전략 성립에 필요한 숨겨진 조건 (정보/자원 격차)",
            "hidden_condition_source": "조건 출처",
            "hidden_condition_source_url": "URL 또는 null",
            "conclusion": "왜 일반인에게 적용 어려운지"
        }}
    ],
    "hooking_points": [
        {{
            "point": "후킹 포인트 (반전 요소 포함)",
            "empathy_reason": "공감 이유",
            "target": "직장인/대학생/부업러 등",
            "level": 3
        }}
    ],
    "content_direction": [
        {{
            "stage": "후킹",
            "example_script": "모순을 활용한 첫 문장 예시",
            "intention": "권위 뒤집기"
        }},
        {{
            "stage": "모순지적",
            "example_script": "팩트 기반 비판 예시",
            "intention": "신뢰 확보"
        }},
        {{
            "stage": "공감",
            "example_script": "타겟이 느낄 감정 예시",
            "intention": "시청자 안심"
        }},
        {{
            "stage": "해결암시",
            "example_script": "시스템/원칙 방향 제시 (직접 언급 X)",
            "intention": "궁금증 유발"
        }}
    ],
    "perspective_insights": [
        "{perspective_name} 관점에서의 해결책/인사이트"
    ],
    "auto_trading_connection": [
        {{
            "strategy_content": "영상에서 말한 전략 내용",
            "implementation_method": "코드로 구현하는 방법 (구체적)",
            "tech_stack": "기술 스택 (예: Python + 키움API, MT5 EA, 업비트 API 등)",
            "feasibility": "높음/중간/낮음/불가능",
            "limitation": "구현 시 한계점 (있으면)"
        }}
    ],
    "automation_insight": {{
        "video_type": "매매 기법|가치 투자|심리/멘탈|리스크 관리",
        "video_type_reason": "왜 이 유형인지 설명",
        "problem_solution_table": [
            {{
                "problem": "현실적 모순에서 추출한 문제점",
                "human_difficulty": "사람이 힘든 이유 (숨겨진 전제에서)",
                "automation_solution": "자동화 해결책 (기술적)",
                "implementation": "간단 요약",
                "implementation_detail": {{
                    "condition": "구체적 조건 (예: PER < 15, ROE > 15%, -10% 손절)",
                    "tool": "사용 도구 (예: 키움 HTS 조건검색, Python FinanceDataReader, 엑셀)",
                    "backtest_result": "백테스트 결과 (예: 2010-2024 적용 시 연 12%, MDD 18%)",
                    "caution": "주의사항/한계 (예: 급등주엔 부적합, 거래량 적은 종목 제외 필요)"
                }}
            }}
        ],
        "core_insight": "한 문장 요약: 이 전략은 [전제]를 가정하는데, 사람이 직접 하기엔 [한계]가 있다. → [자동화 방법]을 적용하면 실행 가능해진다.",
        "life_expansion": {{
            "applicable": true,
            "areas": ["습관 관리", "지출 관리", "학습 루틴"],
            "examples": [
                {{
                    "area": "적용 영역",
                    "principle": "투자에서 추출한 원리",
                    "application": "구체적 적용 방법"
                }}
            ]
        }},
        "improvement_cases": [
            {{
                "original_limitation": "원본 영상/전략의 한계점",
                "improver": "조엘 그린블라트",
                "method": "마법공식 - ROC+EY 정량화",
                "verified_result": "연평균 24%",
                "verification_period": "1988-2009"
            }},
            {{
                "original_limitation": "감정 통제 필요",
                "improver": "레이 달리오",
                "method": "올웨더 포트폴리오 - 자산배분 리밸런싱",
                "verified_result": "연평균 9.5%",
                "verification_period": "1984-2013"
            }}
        ],
        "differentiation_points": [
            {{
                "type": "정량화 성공",
                "summary": "버핏의 주관적 분석을 그린블라트가 마법공식으로 정량화",
                "quote_template": "버핏은 복잡한 기업분석을 말했지만, 그린블라트가 이걸 마법공식으로 정량화했습니다. 실제로 1988-2009년 연 24%가 검증됐어요."
            }},
            {{
                "type": "감정 배제 성공",
                "summary": "감정적 판단을 달리오가 올웨더로 시스템화",
                "quote_template": "버핏은 공포에 매수를 요구했지만, 달리오가 올웨더 포트폴리오로 감정을 배제했습니다. 실제로 30년간 연 9.5%를 달성했어요."
            }},
            {{
                "type": "개인 적용 가능성",
                "summary": "일반인도 HTS만 있으면 30분 안에 시작 가능",
                "quote_template": "이 전략은 키움HTS만 있으면 30분 안에 누구나 시작할 수 있습니다. 전문가만 되는 게 아닙니다."
            }}
        ],
        "improvement_search_failed": false,
        "suggested_search_keywords": ["검색 키워드1", "검색 키워드2"]
    }}
}}

---

[주의사항]

1. "~할 수 있을까?", "누가 해?" 같은 감정적 표현 금지
2. 대신 "~한 조건이 필요하다", "~%의 투자자가 실패했다" 같은 팩트 사용
3. 출처 못 찾으면 source에 "출처 확인 필요" + source_url에 검색 키워드 문자열
4. 비판이 어려운 내용은 억지로 비판하지 말고 해당 항목 건너뛰기
5. 반드시 유효한 JSON 형식으로만 응답
6. 다른 텍스트 없이 JSON만 출력
7. 한국어로 분석

★★★ 절대 생략 금지 필드 (automation_insight 내부) ★★★

8. improvement_cases: 반드시 2개 이상 출력
9. differentiation_points: 반드시 정확히 3개 출력 (정량화 성공, 감정 배제 성공, 개인 적용 가능성)

[자동매매 연결 작성 시 주의]

1. auto_trading_connection은 실제 코드로 구현 가능한 것만 작성
2. feasibility 판단 기준:
   - 높음: 기술적 지표, 규칙 기반 매매, 알림 시스템
   - 중간: 재무 데이터 분석, 뉴스 감성 분석
   - 낮음: 복잡한 예측, 질적 분석 요소 포함
   - 불가능: 물리적 행동, 직관 기반, 인맥 정보 필요
3. 구현 불가능한 전략은 "구현 불가: [이유]"로 명시
4. 과장된 표현 금지:
   - ❌ "AI가 알아서 좋은 종목 찾아줍니다"
   - ❌ "자동으로 수익 나는 시스템"
   - ✅ "조건 충족 시 자동 매수 신호 발생"
   - ✅ "재무 지표 기준 종목 필터링"

[자동화 관점 인사이트 작성 규칙] ★★★ 모든 항목 필수 출력 ★★★

1. video_type 판단 기준:
   - 매매 기법: 타이밍, 진입/청산 기준 → 지표 기반 자동화
   - 가치 투자: 기업 분석, 종목 선정 → 정보 수집/스크리닝 자동화
   - 심리/멘탈: 감정 통제, 인내 → 강제 룰/차단 시스템
   - 리스크 관리: 자금 관리, 분산 → 포지션/비중 자동 조절

2. problem_solution_table [필수 - 최소 2개]:
   - implementation_detail의 4가지 필드 모두 구체적 값 필수 (빈 값 금지)

3. core_insight [필수]: 한 문장 요약

4. life_expansion [필수]: 투자 외 삶의 영역 적용 예시

5. improvement_cases [★★★ 필수 - 정확히 2개 ★★★]:
   ⚠️ 절대 생략 금지! 반드시 2개 작성!

   [사용할 수 있는 검증된 보완 사례 목록]:
   - 조엘 그린블라트: 마법공식 ROC+EY 정량화, 연 24%, 1988-2009
   - 레이 달리오: 올웨더 포트폴리오, 연 9.5%, 1984-2013
   - 벤저민 그레이엄: NCAV 공식, 시장+7%p, 1930-1956
   - 게리 안토나치: 듀얼 모멘텀, 연 17%, 1974-2013

6. differentiation_points [★★★ 필수 - 정확히 3개 ★★★]:
   ⚠️ 절대 생략 금지! 반드시 3개 모두 작성!

   반드시 아래 3가지 type으로 작성:
   [
     {{
       "type": "정량화 성공",
       "summary": "[영상 거장]의 [주관적 방법]을 [누가] [어떤 공식]으로 정량화함",
       "quote_template": "[거장]은 [주관적 방법]을 말했지만, [그린블라트]가 이걸 [마법공식]으로 정량화했습니다. 실제로 [1988-2009년] 연 [24%]가 검증됐어요."
     }},
     {{
       "type": "감정 배제 성공",
       "summary": "[감정적 요소]를 [시스템/규칙]으로 대체한 사례",
       "quote_template": "[거장]은 [감정적 판단]을 요구했지만, [달리오]가 [올웨더 포트폴리오]로 감정을 배제했습니다. 실제로 [30년간] [연 9.5%]를 달성했어요."
     }},
     {{
       "type": "개인 적용 가능성",
       "summary": "일반인도 [도구]만 있으면 [시간] 안에 시작 가능",
       "quote_template": "이 전략은 [키움HTS]만 있으면 [30분] 안에 누구나 시작할 수 있습니다. 전문가만 되는 게 아닙니다."
     }}
   ]
"""


def get_critical_analysis_prompt(
    perspective_id: str,
    summary: str,
    key_message: str,
    key_points: List[str],
    strategy: str,
    quotes: List[Dict],
    people: List[Dict],
    source_tracking: List[Dict],
    suitability_analysis: Dict,
    improvement_search_results: List[Dict] = None
) -> str:
    """1단계 결과 기반 비판적 분석 프롬프트 생성"""
    perspective = get_perspective(perspective_id)

    # 데이터 포맷팅
    key_points_str = '\n'.join([f'  - {p}' for p in key_points]) if key_points else '없음'

    quotes_str = '\n'.join([
        f'  - "{q.get("text", q) if isinstance(q, dict) else q}" ({q.get("speaker", "") if isinstance(q, dict) else ""})'
        for q in quotes
    ]) if quotes else '없음'

    people_str = '\n'.join([
        f'  - {p.get("name", "")} ({p.get("role", "")})'
        for p in people
    ]) if people else '없음'

    source_str = '\n'.join([
        f'  - "{s.get("quote", "")}" → {s.get("source_title", "")} ({s.get("source_type", "")})'
        for s in source_tracking
    ]) if source_tracking else '없음'

    suitability_str = f"""
  - 실현 가능성 이슈: {suitability_analysis.get('feasibility_issue', {}).get('content', '없음')}
  - 숨겨진 전제: {suitability_analysis.get('hidden_premise', {}).get('content', '없음')}
  - 비판 포인트: {suitability_analysis.get('criticism_point', {}).get('content', '없음')}
  - 타겟 공감: {suitability_analysis.get('target_empathy', {}).get('level', '없음')} - {suitability_analysis.get('target_empathy', {}).get('reason', '')}
  - 판단: {suitability_analysis.get('judgment', '없음')}
""" if suitability_analysis else '없음'

    # 기본 프롬프트 생성
    prompt = CRITICAL_ANALYSIS_PROMPT.format(
        summary=summary or '없음',
        key_message=key_message or '없음',
        key_points=key_points_str,
        strategy=strategy or '없음',
        quotes=quotes_str,
        people=people_str,
        source_tracking=source_str,
        suitability_analysis=suitability_str,
        perspective_name=perspective.name,
        perspective_focus=perspective.focus_area
    )

    # 자동매매 관점일 경우 구현 가능 범위 추가
    if perspective_id == "auto_trading":
        prompt = AUTO_TRADING_SCOPE + "\n\n" + prompt

    # Tavily 보완 사례 검색 결과 추가
    if improvement_search_results and len(improvement_search_results) > 0:
        improvement_context = "\n\n[참고: Tavily 웹 검색으로 찾은 보완 사례 자료]\n"
        for i, result in enumerate(improvement_search_results, 1):
            improvement_context += f"""
{i}. {result.get('title', '제목 없음')}
   - URL: {result.get('url', '')}
   - 요약: {result.get('snippet', '')[:200]}...
"""
        improvement_context += "\n위 검색 결과를 참고하여 improvement_cases와 differentiation_points를 구체적으로 작성하세요."
        prompt += improvement_context

    return prompt


def get_integrated_analysis_prompt(transcript: str) -> str:
    """출처 추적이 포함된 통합 분석 프롬프트 생성 (deprecated)"""
    return f"Deprecated - use claude.py ANALYSIS_PROMPT_WITH_SUITABILITY instead"


def get_contradiction_analysis_prompt(
    perspective_name: str,
    transcript: str,
    critical_points: List[str]
) -> str:
    """출처 기반 모순 분석 프롬프트 생성 (deprecated - 통합됨)"""
    return f"Deprecated - integrated into critical analysis"
