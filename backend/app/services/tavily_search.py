import os
from typing import Optional, Dict, List
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# tavily-python 버전에 따라 호환성 처리
try:
    from tavily import TavilyClient
except ImportError:
    from tavily import Client as TavilyClient

tavily_client: Optional[TavilyClient] = None


def init_tavily() -> Optional[TavilyClient]:
    """Tavily 클라이언트 초기화"""
    global tavily_client
    api_key = os.getenv("TAVILY_API_KEY")
    print(f"[Tavily] init_tavily called, API key exists: {bool(api_key)}")
    if api_key:
        tavily_client = TavilyClient(api_key=api_key)
        print(f"[Tavily] Client initialized successfully")
    else:
        print("[Tavily] WARNING: No API key found!")
    return tavily_client


def search_source(query: str) -> Dict:
    """
    출처 검색해서 실제 URL 반환

    Args:
        query: 검색할 출처명 또는 키워드

    Returns:
        {
            "found": True/False,
            "title": "문서 제목",
            "url": "https://...",
            "snippet": "내용 요약"
        }
    """
    global tavily_client

    if not tavily_client:
        init_tavily()

    if not tavily_client:
        return {"found": False, "url": None, "search_query": query}

    try:
        print(f"[Tavily] Searching: {query}")
        response = tavily_client.search(
            query=query,
            search_depth="basic",
            max_results=1
        )

        if response.get("results") and len(response["results"]) > 0:
            result = response["results"][0]
            url = result.get("url", "")
            print(f"[Tavily] Found URL: {url}")
            return {
                "found": True,
                "title": result.get("title", ""),
                "url": url,
                "snippet": result.get("content", "")[:200] if result.get("content") else ""
            }
        else:
            print(f"[Tavily] No results for: {query}")
            return {"found": False, "url": None, "search_query": query}

    except Exception as e:
        print(f"Tavily search error: {e}")
        return {"found": False, "url": None, "search_query": query}


def search_multiple_sources(queries: List[str]) -> List[Dict]:
    """
    여러 출처 한 번에 검색

    Args:
        queries: 검색할 출처명 리스트

    Returns:
        검색 결과 리스트
    """
    results = []
    for query in queries:
        result = search_source(query)
        results.append(result)
    return results


def search_book_source(book_title: str, quote: str = "") -> Dict:
    """
    책 출처일 때 교보문고에서 검색

    Args:
        book_title: 책 제목
        quote: 인용 문장 (선택)

    Returns:
        검색 결과 (교보문고 우선)
    """
    from urllib.parse import quote as url_quote

    # 책 제목에서 불필요한 부분 제거 (예: "더 클래식 시리즈: 오래된 버핏" -> "오래된 버핏")
    clean_title = book_title
    if ":" in book_title:
        clean_title = book_title.split(":")[-1].strip()

    # 1. 교보문고 직접 검색 시도
    kyobo_queries = [
        f"{clean_title} site:kyobobook.co.kr",
        f"{clean_title} 교보문고",
    ]

    for query in kyobo_queries:
        result = search_source(query)
        if result.get("found") and "kyobobook" in result.get("url", ""):
            return result

    # 2. 일반 검색 (Yes24, 알라딘 등)
    book_queries = [
        f"{clean_title} site:yes24.com",
        f"{clean_title} site:aladin.co.kr",
        f"{clean_title} 책",
    ]

    for query in book_queries:
        result = search_source(query)
        if result.get("found"):
            return result

    # 3. 못 찾으면 교보문고 검색 링크 반환
    return {
        "found": False,
        "url": f"https://search.kyobobook.co.kr/search?keyword={url_quote(clean_title)}",
        "search_query": clean_title
    }


def search_interview_clip(person: str, video_title: str = "", quote: str = "") -> Dict:
    """
    인터뷰 영상 클립 검색 (YouTube 우선)

    Args:
        person: 인물명
        video_title: 영상 제목
        quote: 발언 내용

    Returns:
        검색 결과 (YouTube 우선)
    """
    from urllib.parse import quote as url_quote

    # 유명 해외 인물 한글-영어 매핑 (워렌 버핏 같은 경우 영어로 검색해야 실제 인터뷰 나옴)
    english_names = {
        "워렌 버핏": "Warren Buffett",
        "워런 버핏": "Warren Buffett",
        "찰리 멍거": "Charlie Munger",
        "일론 머스크": "Elon Musk",
        "제프 베조스": "Jeff Bezos",
        "빌 게이츠": "Bill Gates",
        "스티브 잡스": "Steve Jobs",
        "레이 달리오": "Ray Dalio",
        "피터 린치": "Peter Lynch",
        "조지 소로스": "George Soros",
        "짐 로저스": "Jim Rogers",
        "하워드 막스": "Howard Marks",
        "벤저민 그레이엄": "Benjamin Graham",
        "필립 피셔": "Philip Fisher",
        "존 템플턴": "John Templeton",
        "켄 피셔": "Ken Fisher",
        "세스 클라만": "Seth Klarman",
        "조엘 그린블라트": "Joel Greenblatt",
    }

    # 영어 이름이 있으면 사용
    search_person = english_names.get(person, person)
    is_international = person in english_names

    # 영상 제목도 영어로 변환 시도
    english_titles = {
        "버크셔 해서웨이 주주총회": "Berkshire Hathaway shareholders meeting",
        "주주총회": "shareholders meeting",
        "인터뷰": "interview",
    }

    search_title = video_title
    for kor, eng in english_titles.items():
        if kor in video_title:
            search_title = video_title.replace(kor, eng)
            break

    # YouTube 검색 쿼리들
    queries = []

    if is_international:
        # 해외 인물은 영어로 검색 (한글 quote 사용 안함)
        if video_title:
            # 연도 추출 시도
            import re
            year_match = re.search(r'(19|20)\d{2}', video_title)
            year = year_match.group() if year_match else ""

            queries.extend([
                f"{search_person} {search_title} site:youtube.com",
                f"{search_person} interview {year} site:youtube.com" if year else f"{search_person} interview site:youtube.com",
                f"{search_person} {year} site:youtube.com" if year else None,
            ])
        queries.extend([
            f"{search_person} interview site:youtube.com",
            f"{search_person} speech site:youtube.com",
            f"{search_person} CNBC site:youtube.com",
        ])
        queries = [q for q in queries if q]  # None 제거
    else:
        # 한국 인물은 기존 로직
        if video_title:
            queries.append(f"{person} {video_title} site:youtube.com")
            queries.append(f"{video_title} site:youtube.com")

        queries.extend([
            f"{person} 인터뷰 site:youtube.com",
            f"{person} interview site:youtube.com",
            f"{person} 영상",
        ])

        # 한국 인물만 quote 사용
        if quote and len(quote) > 10:
            queries.insert(0, f"{person} {quote[:30]} site:youtube.com")

    print(f"[Tavily] interview_clip queries: {queries[:3]}", flush=True)

    for query in queries:
        result = search_source(query)
        if result.get("found"):
            url = result.get("url", "")
            # YouTube URL 우선
            if "youtube.com" in url or "youtu.be" in url:
                return result

    # YouTube에서 못 찾으면 뉴스/기사 검색
    news_queries = [
        f"{search_person} {search_title} 기사" if video_title else f"{search_person} 인터뷰 기사",
        f"{search_person} 발언",
    ]

    for query in news_queries:
        result = search_source(query)
        if result.get("found"):
            return result

    # 못 찾으면 YouTube 검색 링크 반환
    search_term = f"{search_person} {search_title}" if video_title else f"{search_person} interview"
    return {
        "found": False,
        "url": f"https://www.youtube.com/results?search_query={url_quote(search_term)}",
        "search_query": search_term
    }


def search_evidence_source(evidence: str, source_type: str = "") -> Dict:
    """
    증거 자료 검색 (기사/논문/보고서)

    Args:
        evidence: 증거 내용
        source_type: 출처 유형

    Returns:
        검색 결과
    """
    from urllib.parse import quote as url_quote

    queries = []

    # 출처 유형별 검색 전략
    if source_type == "기사":
        queries = [
            f"{evidence} 기사",
            f"{evidence} 뉴스",
            f"{evidence} site:hankyung.com OR site:chosun.com OR site:joongang.co.kr",
        ]
    elif source_type == "논문":
        queries = [
            f"{evidence} 논문",
            f"{evidence} 연구",
            f"{evidence} site:riss.kr OR site:scholar.google.com",
        ]
    elif source_type == "보고서":
        queries = [
            f"{evidence} 보고서",
            f"{evidence} site:fss.or.kr OR site:krx.co.kr OR site:bok.or.kr",
            f"{evidence} 리포트",
        ]
    elif source_type == "영상":
        queries = [
            f"{evidence} site:youtube.com",
            f"{evidence} 영상",
        ]
    else:
        queries = [
            evidence,
            f"{evidence} 출처",
        ]

    for query in queries:
        result = search_source(query)
        if result.get("found"):
            return result

    return {
        "found": False,
        "url": f"https://www.google.com/search?q={url_quote(evidence)}",
        "search_query": evidence
    }


def search_source_by_type(source_name: str, source_type: str, context: str = "") -> Dict:
    """
    출처 유형에 따라 다른 검색 전략

    Args:
        source_name: 출처명
        source_type: 출처 유형 (책, 논문, 보고서, 기사 등)
        context: 추가 컨텍스트 (인용문 등)

    Returns:
        검색 결과
    """
    from urllib.parse import quote as url_quote

    if not source_name or source_name == '-':
        return {"found": False, "url": None, "search_query": ""}

    # 유형별 검색 전략
    if source_type in ["책", "도서"]:
        # 책은 교보문고 우선 검색
        return search_book_source(source_name, context)

    elif source_type == "논문":
        queries = [
            f"{source_name} 논문",
            f"{source_name} site:riss.kr",
            f"{source_name} site:scholar.google.com",
            f"{source_name} 연구"
        ]
    elif source_type == "보고서":
        queries = [
            f"{source_name} 보고서 원문",
            f"{source_name} site:fss.or.kr OR site:krx.co.kr",
            f"{source_name} 보고서",
            f"{source_name} 리포트"
        ]
    elif source_type == "기사":
        queries = [
            f"{source_name} 기사",
            f"{source_name} 뉴스",
            f"{source_name} site:hankyung.com OR site:chosun.com"
        ]
    elif source_type in ["영상", "인터뷰 영상"]:
        queries = [
            f"{source_name} site:youtube.com",
            f"{source_name} 영상",
            f"{source_name} 인터뷰"
        ]
    else:
        # 기타 유형
        queries = [
            source_name,
            f"{source_name} 출처",
            f"{source_name} 원문"
        ]

    # 컨텍스트가 있으면 첫 번째 쿼리에 포함
    if context:
        queries.insert(0, f"{source_name} {context[:30]}")

    for query in queries:
        result = search_source(query)
        if result.get("found"):
            return result

    # 유형별 폴백 URL
    if source_type in ["책", "도서"]:
        fallback_url = f"https://search.kyobobook.co.kr/search?keyword={url_quote(source_name)}"
    elif source_type in ["영상", "인터뷰 영상"]:
        fallback_url = f"https://www.youtube.com/results?search_query={url_quote(source_name)}"
    else:
        fallback_url = f"https://www.google.com/search?q={url_quote(source_name)}"

    return {
        "found": False,
        "url": fallback_url,
        "search_query": source_name
    }


async def verify_and_add_links(data: Dict, field_mappings: List[Dict]) -> Dict:
    """
    데이터의 출처 필드들을 검증하고 링크 추가

    Args:
        data: 검증할 데이터
        field_mappings: 필드 매핑 리스트
            [{"source_field": "source", "url_field": "source_url"}, ...]

    Returns:
        링크가 추가된 데이터
    """
    for mapping in field_mappings:
        source_field = mapping.get("source_field")
        url_field = mapping.get("url_field")

        if source_field and url_field:
            source_value = data.get(source_field)
            url_value = data.get(url_field)

            # 출처는 있는데 URL이 없는 경우
            if source_value and (not url_value or url_value == "null"):
                result = search_source(source_value)
                if result["found"]:
                    data[url_field] = result["url"]
                    data["verified"] = True
                else:
                    # Google 검색 링크로 대체
                    search_query = source_value.replace(" ", "+")
                    data[url_field] = f"https://www.google.com/search?q={search_query}"
                    data["verified"] = False

    return data
