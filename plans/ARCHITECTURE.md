# YouTube Analyzer 아키텍처

## 시스템 구조

```
[사용자 브라우저]
       ↓ HTTP
[Next.js 프론트엔드] (Vercel)
       ↓ API 호출
[FastAPI 백엔드] (Railway)
       ├── YouTube Data API (영상 메타 정보)
       ├── youtube-transcript-api (자막 추출)
       ├── Anthropic Claude API (AI 분석)
       └── Supabase (DB 저장)
```

## 프론트엔드 라우팅 (Next.js App Router)

```
/                    - 메인 페이지 (URL 입력 폼)
/result/[id]         - 분석 결과 상세
/history             - 분석 히스토리 목록
/login               - 로그인 (추후)
/signup              - 회원가입 (추후)
```

## 백엔드 API 엔드포인트 (FastAPI)

### 분석 API
- POST `/api/analyze` : 영상 분석 요청
- GET `/api/result/{id}` : 분석 결과 조회

### 히스토리 API
- GET `/api/history` : 히스토리 목록
- DELETE `/api/history/{id}` : 히스토리 삭제

### 인증 API (추후)
- POST `/api/auth/login` : 로그인
- POST `/api/auth/signup` : 회원가입
- POST `/api/auth/logout` : 로그아웃

## DB 스키마 (Supabase)

### users 테이블 (추후)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### analyses 테이블
```sql
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),  -- 추후 연결
    video_id TEXT NOT NULL,
    video_title TEXT,
    video_url TEXT NOT NULL,
    channel_name TEXT,
    thumbnail_url TEXT,
    transcript TEXT,
    summary TEXT,
    key_message TEXT,
    key_points JSONB,
    quotes JSONB,
    people JSONB,
    content_ideas JSONB,
    script_direction JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 분석 플로우

1. 사용자가 YouTube URL 입력
2. 프론트엔드 → 백엔드 API 호출 (POST /api/analyze)
3. video_id 추출 (정규식)
4. YouTube Data API로 영상 메타 정보 가져오기 (제목, 채널, 썸네일)
5. youtube-transcript-api로 자막 추출
6. Claude API로 자막 분석 (프롬프트 전송)
7. 분석 결과 Supabase 저장
8. 결과 ID 반환 → 프론트엔드에서 결과 페이지로 이동

## Claude 분석 프롬프트

```
당신은 유튜브 콘텐츠 분석 전문가입니다.
아래 유튜브 영상 자막을 분석해서 다음 형식으로 정리해주세요.

[자막 내용]
{transcript}

[출력 형식]
1. 영상 요약 (3~5줄)
2. 핵심 메시지 (한 문장)
3. 키포인트 (3~5개)
4. 인용할 만한 대사 (원문 그대로)
5. 등장 인물 (이름, 역할)
6. 콘텐츠 추천
   - 뇌동매매 타겟: 제목 예시 + 활용 방향
   - 원칙 투자 타겟: 제목 예시 + 활용 방향
   - 경제적 자유 타겟: 제목 예시 + 활용 방향
7. 대본 방향 (도입/전개/전환/마무리)

JSON 형식으로 응답해주세요.
```

## 백엔드 프로젝트 구조

```
backend/
├── app/
│   ├── main.py           # FastAPI 앱 초기화, 라우터 등록
│   ├── config.py         # 환경변수 로드
│   ├── database.py       # Supabase 연결
│   ├── routers/
│   │   ├── auth.py       # 인증 API (추후)
│   │   ├── youtube.py    # 메인 페이지, 분석 요청 처리
│   │   ├── analyzer.py   # AI 분석 API
│   │   └── history.py    # 히스토리 CRUD
│   ├── services/
│   │   ├── transcript.py # 자막 추출 로직
│   │   ├── claude.py     # Claude API 연동
│   │   └── youtube_api.py # YouTube Data API 연동
│   └── models/
│       └── schemas.py    # Pydantic 모델
```

## 프론트엔드 프로젝트 구조

```
frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx           # 메인 페이지
│   │   ├── layout.tsx         # 공통 레이아웃
│   │   ├── result/[id]/page.tsx
│   │   └── history/page.tsx
│   ├── components/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   ├── UrlInput.tsx
│   │   ├── ResultCard.tsx
│   │   ├── HistoryList.tsx
│   │   └── Loading.tsx
│   └── lib/
│       └── api.ts             # API 호출 함수
```
