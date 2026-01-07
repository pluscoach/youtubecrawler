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
        description="투자 전략을 자동매매 시스템 관점에서 비판적으로 분석합니다.",
        focus_area="감정 없이 프로그램으로 실행하면 해결되는 부분"
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
    ]
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
    suitability_analysis: Dict
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

    return CRITICAL_ANALYSIS_PROMPT.format(
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
