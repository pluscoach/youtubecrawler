"""
출처 검색 서비스
인용문 기반 원본 출처 검색 및 신뢰도 평가
"""

import asyncio
import aiohttp
import re
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from enum import Enum


class SourceType(Enum):
    """출처 유형"""
    BOOK = "책"
    INTERVIEW = "인터뷰 영상"
    ARTICLE = "기사"
    SHAREHOLDER_LETTER = "주주서한"
    PAPER = "논문"
    SNS = "SNS"
    REPORT = "보고서"
    UNKNOWN = "출처 확인 필요"


@dataclass
class SourceResult:
    """출처 검색 결과"""
    quote: str
    source_title: str
    source_type: SourceType
    source_url: Optional[str]
    reliability: int  # 1-5 신뢰도
    search_keywords: List[str]  # 검색 키워드 제안


@dataclass
class ContradictionSource:
    """모순 분석 출처"""
    category: str  # 원본 주장, 반례/팩트, 숨겨진 조건, 결론
    content: str
    source_title: str
    source_url: Optional[str]


def classify_source_type(url: str, title: str) -> SourceType:
    """URL과 제목으로 출처 유형 분류"""
    url_lower = url.lower() if url else ""
    title_lower = title.lower() if title else ""

    # 책 관련
    if any(x in url_lower for x in ['amazon.com/dp', 'goodreads.com', 'yes24.com', 'kyobobook', 'aladin.co.kr']):
        return SourceType.BOOK
    if any(x in title_lower for x in ['책', 'book', '저서', '출판']):
        return SourceType.BOOK

    # 영상/인터뷰
    if any(x in url_lower for x in ['youtube.com', 'youtu.be', 'vimeo.com', 'ted.com']):
        return SourceType.INTERVIEW
    if any(x in title_lower for x in ['인터뷰', 'interview', '대담', '강연']):
        return SourceType.INTERVIEW

    # 주주서한
    if any(x in title_lower for x in ['주주서한', 'shareholder letter', 'annual letter', 'berkshire']):
        return SourceType.SHAREHOLDER_LETTER

    # 논문
    if any(x in url_lower for x in ['arxiv.org', 'scholar.google', 'ssrn.com', 'doi.org', 'pubmed']):
        return SourceType.PAPER
    if any(x in title_lower for x in ['논문', 'paper', 'study', 'research']):
        return SourceType.PAPER

    # SNS
    if any(x in url_lower for x in ['twitter.com', 'x.com', 'facebook.com', 'linkedin.com', 'instagram.com']):
        return SourceType.SNS

    # 보고서
    if any(x in title_lower for x in ['보고서', 'report', '리포트', '분석']):
        return SourceType.REPORT

    # 기사 (뉴스 사이트)
    if any(x in url_lower for x in ['news', 'article', 'blog', 'post', '.com/', '.co.kr/']):
        return SourceType.ARTICLE

    return SourceType.UNKNOWN


def generate_search_keywords(quote: str, speaker: str = "") -> List[str]:
    """인용문에서 검색 키워드 생성"""
    keywords = []

    # 화자 이름 추가
    if speaker:
        keywords.append(f'"{speaker}"')

    # 핵심 명사/동사 추출 (간단한 휴리스틱)
    # 따옴표로 묶인 정확한 구문
    if len(quote) < 50:
        keywords.append(f'"{quote}"')
    else:
        # 긴 문장은 핵심 부분만
        words = quote.split()
        if len(words) > 5:
            # 처음 5단어
            keywords.append(' '.join(words[:5]))

    # 유명 투자자 이름 패턴
    famous_investors = ['워렌 버핏', 'Warren Buffett', '찰리 멍거', 'Charlie Munger',
                       '피터 린치', 'Peter Lynch', '레이 달리오', 'Ray Dalio',
                       '조지 소로스', 'George Soros', '벤저민 그레이엄', 'Benjamin Graham']

    for investor in famous_investors:
        if investor.lower() in quote.lower():
            keywords.append(investor)

    return keywords


async def search_source_with_claude(quotes: List[str], transcript: str, client) -> List[Dict]:
    """
    Claude를 사용하여 출처 검색
    Claude가 학습 데이터에서 출처를 추론하거나 검색 키워드를 제안
    """
    prompt = f"""당신은 투자 콘텐츠 출처 검증 전문가입니다.

아래 유튜브 영상 자막에서 인용된 문장들의 원본 출처를 찾아주세요.

[영상 자막 요약]
{transcript[:5000]}

[인용 문장들]
{chr(10).join([f'{i+1}. "{q}"' for i, q in enumerate(quotes)])}

각 인용문에 대해 다음 형식으로 출처를 찾아주세요:

[출력 형식 - 반드시 JSON 형식으로 응답]
{{
    "sources": [
        {{
            "quote": "인용문",
            "source_title": "출처 제목 (책 제목, 인터뷰명, 기사 제목 등)",
            "source_type": "책|인터뷰 영상|기사|주주서한|논문|SNS|보고서|출처 확인 필요",
            "source_url": "가능하면 URL, 없으면 null",
            "reliability": 1~5 (5가 가장 신뢰),
            "search_keywords": ["검색 키워드1", "검색 키워드2"]
        }}
    ]
}}

주의사항:
1. 확실하지 않은 출처는 "출처 확인 필요"로 표시
2. 검색 키워드는 사용자가 직접 검색할 수 있도록 구체적으로 제안
3. 유명 투자자의 발언이면 어떤 책/인터뷰/서한에서 나온 것인지 최대한 특정
4. 신뢰도는 출처의 명확성에 따라 1(불확실)~5(확실)로 평가
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # JSON 파싱
        import json
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        result = json.loads(response_text)
        return result.get("sources", [])

    except Exception as e:
        print(f"출처 검색 오류: {e}")
        # 실패 시 기본 응답
        return [
            {
                "quote": q,
                "source_title": "출처 확인 필요",
                "source_type": "출처 확인 필요",
                "source_url": None,
                "reliability": 1,
                "search_keywords": generate_search_keywords(q)
            }
            for q in quotes
        ]


async def analyze_contradictions_with_sources(
    critical_points: List[str],
    transcript: str,
    perspective_name: str,
    client
) -> List[Dict]:
    """
    비판적 분석 포인트에 대한 출처 기반 모순 분석
    """
    prompt = f"""당신은 투자 전략 비판적 분석 전문가입니다.

아래 비판적 분석 포인트들에 대해 출처 기반 모순 분석을 수행해주세요.

[분석 관점]
{perspective_name}

[영상 자막 요약]
{transcript[:5000]}

[비판적 분석 포인트]
{chr(10).join([f'{i+1}. {p}' for i, p in enumerate(critical_points)])}

각 비판 포인트에 대해 다음 형식으로 출처 기반 모순 분석을 작성해주세요:

[출력 형식 - 반드시 JSON 형식으로 응답]
{{
    "contradiction_analyses": [
        {{
            "point": "비판 포인트",
            "original_claim": {{
                "content": "영상에서 주장한 내용",
                "source_title": "원본 출처 (책/인터뷰/서한 등)",
                "source_url": "가능하면 URL, 없으면 null"
            }},
            "counter_evidence": {{
                "content": "실제 데이터나 사례로 반박하는 내용",
                "source_title": "기사/인터뷰/논문/보고서 출처",
                "source_url": "가능하면 URL, 없으면 null"
            }},
            "hidden_condition": {{
                "content": "이 전략이 성립하려면 필요한 전제 조건",
                "source_title": "근거 출처",
                "source_url": "가능하면 URL, 없으면 null"
            }},
            "conclusion": {{
                "content": "왜 일반인에게 적용하기 어려운지 종합 결론",
                "sources_summary": "위 출처들 종합"
            }}
        }}
    ]
}}

주의사항:
1. 각 항목에 반드시 출처를 명시 (없으면 "출처 확인 필요" + 검색 키워드 제안)
2. 반례/팩트는 실제 데이터나 역사적 사례로 뒷받침
3. 숨겨진 조건은 전략이 성공하기 위한 현실적 전제를 분석
4. 결론은 일반 개인투자자 관점에서 적용 어려운 이유를 명확히
"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # JSON 파싱
        import json
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()
        elif "```" in response_text:
            json_start = response_text.find("```") + 3
            json_end = response_text.find("```", json_start)
            response_text = response_text[json_start:json_end].strip()

        result = json.loads(response_text)
        return result.get("contradiction_analyses", [])

    except Exception as e:
        print(f"모순 분석 오류: {e}")
        return []
