# YouTube Analyzer 개발 가이드

## 프로젝트 구조

```
youtubecrawler/
├── backend/
│   ├── app/
│   │   ├── config.py          # 환경변수 로드
│   │   ├── database.py        # Supabase 연결
│   │   ├── main.py            # FastAPI 앱
│   │   ├── models/
│   │   │   └── schemas.py     # Pydantic 모델
│   │   ├── routers/
│   │   │   ├── youtube.py     # /api/analyze, /api/result
│   │   │   ├── history.py     # /api/history
│   │   │   └── analyzer.py    # /api/analyze-only (테스트용)
│   │   └── services/
│   │       ├── transcript.py  # YouTube 자막 추출
│   │       ├── youtube_api.py # YouTube Data API
│   │       └── claude.py      # Claude API 분석
│   ├── .env                   # 환경변수 (gitignore)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx       # 메인 페이지
│   │   │   ├── result/[id]/page.tsx  # 결과 페이지
│   │   │   └── history/page.tsx      # 히스토리 페이지
│   │   ├── components/
│   │   └── lib/
│   │       └── api.ts         # API 클라이언트
│   └── package.json
├── .env                       # 루트 환경변수 (백업용)
└── plans/
```

---

## 환경변수 설정

### backend/.env 파일
```env
# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-api03-...

# YouTube Data API
YOUTUBE_API_KEY=AIzaSy...

# Supabase
SUPABASE_URL=https://[project-ref].supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIs...  # service_role key (JWT 형식)

# URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

### 주의사항
- `.env` 파일이 **두 곳**에 있을 수 있음: 루트(`/`) 와 백엔드(`/backend/`)
- pydantic-settings는 현재 작업 디렉토리의 `.env`를 읽음
- **두 파일 모두 동일하게 유지**할 것

---

## 자주 발생하는 에러와 해결법

### 1. "Invalid API key" 에러

**증상:** 분석 요청 시 "Invalid API key" 에러 발생

**원인 파악:**
1. 어떤 API 키가 문제인지 확인 (Anthropic / YouTube / Supabase)
2. 서버 로그에서 어느 단계에서 실패하는지 확인

**디버깅 방법:**
```python
# youtube.py에 단계별 로그 추가
print("[STEP 1] Extracting video_id...")
print("[STEP 2] Getting video info...")
print("[STEP 3] Getting transcript...")
print("[STEP 4] Analyzing with Claude...")
print("[STEP 5] Saving to DB...")
```

**해결법:**
- **Anthropic:** `sk-ant-api03-...` 형식, 직접 테스트:
  ```python
  python -c "
  import anthropic
  client = anthropic.Anthropic(api_key='YOUR_KEY')
  response = client.messages.create(
      model='claude-sonnet-4-20250514',
      max_tokens=50,
      messages=[{'role': 'user', 'content': 'Hi'}]
  )
  print(response.content[0].text)
  "
  ```

- **Supabase:** JWT 형식 (`eyJhbGciOiJIUzI1NiIs...`), URL과 ref 일치 확인
  - JWT의 `ref` 필드와 URL의 프로젝트 ID가 일치해야 함

---

### 2. "getaddrinfo failed" (DNS 에러)

**증상:** Supabase 연결 시 DNS 조회 실패

**원인:** Supabase URL이 잘못됨

**해결법:**
- Supabase Dashboard → Settings → API → Project URL 확인
- JWT의 `ref` 값과 URL이 일치하는지 확인

---

### 3. youtube-transcript-api 에러

**증상:**
- `'YouTubeTranscriptApi' has no attribute 'list_transcripts'`
- `'YouTubeTranscriptApi' has no attribute 'get_transcript'`

**원인:** youtube-transcript-api 1.x 버전에서 API 변경됨

**해결법 (v1.2.3+ 기준):**
```python
from youtube_transcript_api import YouTubeTranscriptApi

api = YouTubeTranscriptApi()
transcript_list = api.list(video_id)
transcripts = list(transcript_list)

target_transcript = transcripts[0]
transcript_data = target_transcript.fetch()
full_text = ' '.join([item.text for item in transcript_data])
```

---

### 4. @lru_cache() 캐싱 문제

**증상:** `.env` 파일 수정 후에도 이전 값이 사용됨

**원인:** `config.py`의 `@lru_cache()` 데코레이터

**해결법:**
1. 서버 완전 종료 후 재시작
2. `__pycache__` 폴더 삭제:
   ```bash
   find backend -type d -name "__pycache__" -exec rm -rf {} +
   ```

---

### 5. httpx 버전 충돌

**증상:** Anthropic/Supabase 라이브러리 간 httpx 버전 충돌

**해결법:**
```bash
pip install httpx==0.27.0 --force-reinstall
```

---

## 서버 실행 명령어

### 백엔드 (FastAPI)
```bash
cd backend
uvicorn app.main:app --reload
# 또는
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 (Next.js)
```bash
cd frontend
npm run dev
```

---

## API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/api/analyze` | YouTube URL 분석 |
| GET | `/api/result/{id}` | 분석 결과 조회 |
| GET | `/api/history` | 분석 히스토리 |
| DELETE | `/api/history/{id}` | 히스토리 삭제 |
| GET | `/api/transcript/{video_id}` | 자막만 추출 (테스트용) |
| POST | `/api/analyze-only` | DB 저장 없이 분석 (테스트용) |

---

## 디버깅 팁

### 1. curl로 API 직접 테스트
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### 2. 서버 로그 확인
- uvicorn 실행 터미널에서 실시간 로그 확인
- `[DEBUG]`, `[STEP]` 등의 태그로 진행 상황 추적

### 3. Python 직접 테스트
```python
# 환경변수 로드 테스트
import sys
sys.path.insert(0, 'backend')
from app.config import get_settings
settings = get_settings()
print(f"API Key: {settings.anthropic_api_key[:20]}...")
print(f"Supabase URL: {settings.supabase_url}")
```

### 4. 포트 사용 확인
```bash
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

---

## Supabase 테이블 스키마

```sql
CREATE TABLE analyses (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  video_id TEXT NOT NULL,
  video_title TEXT NOT NULL,
  video_url TEXT NOT NULL,
  channel_name TEXT,
  thumbnail_url TEXT,
  transcript TEXT,
  summary TEXT,
  key_message TEXT,
  key_points JSONB DEFAULT '[]',
  quotes JSONB DEFAULT '[]',
  people JSONB DEFAULT '[]',
  content_ideas JSONB DEFAULT '[]',
  script_direction JSONB DEFAULT '{}',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 체크리스트

서버 시작 전:
- [ ] `.env` 파일 존재 확인 (backend/.env)
- [ ] 모든 API 키 설정 확인
- [ ] Supabase URL과 JWT ref 일치 확인

에러 발생 시:
- [ ] 서버 로그 확인
- [ ] 어느 단계에서 실패하는지 파악
- [ ] 해당 API 키 직접 테스트
- [ ] `__pycache__` 삭제 후 재시작
