# YouTube Analyzer - 유튜브 소재 분석기

## 프로젝트 개요
- **서비스명**: YouTube Analyzer
- **목적**: 유튜브 영상 분석 → 콘텐츠 제작 소재 추출
- **타겟 사용자**: 유튜브 크리에이터, 콘텐츠 기획자

## 서비스 확장 단계
1. **1단계**: 개인 사용 (로그인 없음)
2. **2단계**: 로그인 + 개인 데이터 저장
3. **3단계**: 멀티 유저 SaaS + 결제

## 기술 스택
- **프론트엔드**: Next.js + TypeScript + Tailwind CSS
- **백엔드**: FastAPI (Python)
- **DB**: Supabase (PostgreSQL)
- **AI**: Anthropic Claude API
- **자막**: youtube-transcript-api
- **배포**: Vercel (프론트) + Railway (백엔드)

## 핵심 기능
1. URL 입력 → 자막 추출 → AI 분석 → 결과 출력
2. 분석 히스토리 저장/조회
3. (추후) 로그인, 멀티유저

## 분석 결과 출력 형식

📌 **영상 요약**
(전체 내용 3~5줄)

💡 **핵심 메시지**
(영상의 핵심 한 문장)

🎯 **키포인트**
1. ...
2. ...
3. ...

🗣️ **인용할 대사**
(쓸만한 명언/멘트 원문)

👤 **등장 인물**
- 이름 (관련 인터뷰 링크)

---

🔥 **콘텐츠 추천**

[뇌동매매 타겟]
→ 제목 예시
→ 활용 방향

[원칙 투자 타겟]
→ 제목 예시
→ 활용 방향

[경제적 자유 타겟]
→ 제목 예시
→ 활용 방향

🎬 **대본 방향**
- 도입:
- 전개:
- 전환:
- 마무리:

## 환경변수 (.env)
```
ANTHROPIC_API_KEY=your_key
YOUTUBE_API_KEY=AIzaSyDwZsJwAuh5-qrC7bcSAv6ne_NNMmPWygo
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 핵심 문서
- **@CLAUDE.md**: 프로젝트 개요 (이 파일)
- **@ARCHITECTURE.md**: 시스템 구조, DB 스키마, API 명세
- **@DESIGN.md**: UI/UX 디자인 가이드
- **@PROGRESS.md**: 개발 진행 상황
- **@NOTE.md**: 실수/해결방법 기록

## 작업 가이드
1. 모든 작업은 순차적으로 진행 (sub agents 분리 X)
2. 현재 상태 분석 → 계획 수립 → 구현 → 테스트
3. 작업 완료 후 PROGRESS.md 업데이트
4. 실수/해결방법은 NOTE.md에 기록
5. 필요시 ARCHITECTURE.md 등 문서 업데이트
