# YouTube Analyzer

유튜브 영상 URL을 입력하면 자막 기반으로 AI가 분석해서 콘텐츠 제작에 필요한 소재를 정리해주는 도구입니다.

## 기술 스택

| 구분 | 기술 |
|------|------|
| **프론트엔드** | Next.js + TypeScript + Tailwind CSS |
| **백엔드** | FastAPI (Python) |
| **DB** | Supabase (PostgreSQL) |
| **AI** | Anthropic Claude API |
| **자막 추출** | youtube-transcript-api |
| **배포** | Vercel (프론트) + Railway (백엔드) |

## 핵심 기능

1. 유튜브 URL 입력 → 자막 추출
2. AI가 자막 분석 → 구조화된 결과 출력
3. 분석 히스토리 저장

## 프로젝트 구조

```
youtube-analyzer/
├── frontend/          # Next.js 프론트엔드
├── backend/           # FastAPI 백엔드
├── plans/             # 프로젝트 문서
│   ├── CLAUDE.md      # 프로젝트 개요
│   ├── ARCHITECTURE.md # 시스템 구조
│   ├── DESIGN.md      # 디자인 가이드
│   ├── PROGRESS.md    # 진행 상황
│   └── NOTE.md        # 개발 노트
├── .env.example       # 환경변수 예시
├── docker-compose.yml # Docker 설정
└── README.md          # 이 파일
```

## 시작하기

### 1. 환경변수 설정

```bash
cp .env.example .env
# .env 파일에 API 키 입력
```

### 2. Docker로 실행

```bash
docker-compose up
```

### 3. 개별 실행

**백엔드:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**프론트엔드:**
```bash
cd frontend
npm install
npm run dev
```

## 접속

- 프론트엔드: http://localhost:3000
- 백엔드 API: http://localhost:8000
- API 문서: http://localhost:8000/docs

## 라이센스

MIT License
