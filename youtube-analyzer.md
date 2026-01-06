# YouTube Analyzer 프로젝트 설정 (v2)

## 프로젝트 개요
- **서비스명**: YouTube Analyzer (유튜브 소재 분석기)
- **목적**: 유튜브 영상 URL을 입력하면 자막 기반으로 AI가 분석해서 콘텐츠 제작에 필요한 소재를 정리해주는 도구
- **사용자**: 나 혼자 사용 (추후 SaaS 확장 고려)

## 서비스 확장 단계
| 단계 | 기능 | 필요한 것 |
|------|------|----------|
| 1단계 (지금) | 너 혼자 사용 | 로그인 필요 없음, 간단한 배포 |
| 2단계 (나중) | 로그인 + 개인 데이터 저장 | 백엔드 + DB 필요 |
| 3단계 (판매) | 멀티 유저 SaaS | 결제 시스템 + 사용자 관리 |

## 핵심 기능
1. 유튜브 URL 입력 → 자막 추출
2. AI가 자막 분석 → 구조화된 결과 출력
3. 분석 히스토리 저장
4. (추후) 로그인/회원관리

## 기술 스택
| 구분 | 기술 | 이유 |
|------|------|------|
| **프론트엔드** | Next.js | React 기반, SSR 지원, Vercel 배포 쉬움, SaaS 확장 대비 |
| **백엔드** | FastAPI | Python, AI 연동 쉬움, 빠름 |
| **DB** | Supabase | 무료, 인증 내장, PostgreSQL |
| **AI** | Anthropic Claude API | Claude로 분석 |
| **자막 추출** | youtube-transcript-api | Python 라이브러리 |
| **배포** | Vercel (프론트) + Railway (백엔드) | 무료 티어 있음 |

## API 키
- **YouTube Data API**: AIzaSyDwZsJwAuh5-qrC7bcSAv6ne_NNMmPWygo
- **Anthropic API**: (나중에 입력)

## 타겟 고객층 (콘텐츠 추천용)
1. **뇌동매매 하는 사람**: 감정 조절 못하고 충동 매매하는 투자자
2. **원칙 투자 원하는 사람**: 규칙 기반 투자를 하고 싶은 사람
3. **경제적 자유 원하는 사람**: 부업/투자로 자유를 꿈꾸는 직장인/대학생

---

## 1단계: 폴더 구조 생성

아래 폴더 구조를 전체 생성해줘:

```
youtube-analyzer/
├── frontend/                    # Next.js 프론트엔드
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx         # 메인 페이지
│   │   │   ├── layout.tsx       # 레이아웃
│   │   │   ├── result/
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx # 결과 페이지
│   │   │   └── history/
│   │   │       └── page.tsx     # 히스토리 페이지
│   │   ├── components/
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── UrlInput.tsx
│   │   │   ├── ResultCard.tsx
│   │   │   ├── HistoryList.tsx
│   │   │   └── Loading.tsx
│   │   ├── lib/
│   │   │   └── api.ts           # API 호출 함수
│   │   └── styles/
│   │       └── globals.css
│   ├── public/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── next.config.js
├── backend/                     # FastAPI 백엔드
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI 앱 초기화
│   │   ├── config.py            # 환경변수 로드
│   │   ├── database.py          # Supabase 연결
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # 인증 API (추후 사용)
│   │   │   ├── youtube.py       # 유튜브 관련 API
│   │   │   ├── analyzer.py      # AI 분석 API
│   │   │   └── history.py       # 히스토리 CRUD
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── transcript.py    # 자막 추출 로직
│   │   │   ├── claude.py        # Claude API 연동
│   │   │   └── youtube_api.py   # YouTube Data API 연동
│   │   └── models/
│   │       ├── __init__.py
│   │       └── schemas.py       # Pydantic 모델
│   ├── requirements.txt
│   └── Dockerfile
├── plans/
│   ├── wireframes/
│   │   ├── main.xml
│   │   ├── result.xml
│   │   └── history.xml
│   ├── CLAUDE.md
│   ├── ARCHITECTURE.md
│   ├── DESIGN.md
│   ├── PROGRESS.md
│   └── NOTE.md
├── .env.example
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## 2단계: plans/CLAUDE.md 작성

```markdown
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
```

---

## 3단계: plans/ARCHITECTURE.md 작성

```markdown
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
```

---

## 4단계: plans/DESIGN.md 작성

```markdown
# YouTube Analyzer 디자인 가이드

## 디자인 컨셉
- **스타일**: 다크 모드, Trend Finder 참고
- **컬러**: 
  - 배경: #0f0f0f (거의 검정)
  - 카드: #1a1a1a
  - 강조: #ff0050 (핑크/레드)
  - 텍스트: #ffffff, #a0a0a0
- **폰트**: Pretendard 또는 시스템 폰트

## 페이지 구성

### 1. 메인 페이지 (/)
- 헤더: 로고 + 히스토리 링크
- 히어로: 타이틀 + 설명
- URL 입력 폼 (중앙 배치, 크게)
- 최근 분석 목록 (썸네일 카드)

### 2. 분석 결과 페이지 (/result/[id])
- 영상 정보 카드 (썸네일, 제목, 채널)
- 분석 결과 섹션들 (아코디언 또는 탭)
  - 영상 요약
  - 핵심 메시지
  - 키포인트
  - 인용 대사
  - 등장 인물
  - 콘텐츠 추천 (타겟별)
  - 대본 방향

### 3. 히스토리 페이지 (/history)
- 분석 목록 (테이블 또는 카드)
- 검색/필터
- 삭제 기능

## 컴포넌트 스타일

### 버튼
- Primary: 배경 #ff0050, 텍스트 흰색
- Secondary: 배경 투명, 테두리 #ff0050

### 카드
- 배경: #1a1a1a
- 테두리: 1px solid #333
- border-radius: 12px
- 호버 시 테두리 #ff0050

### 입력 필드
- 배경: #0f0f0f
- 테두리: 1px solid #333
- 포커스 시 테두리 #ff0050
```

---

## 5단계: plans/wireframes/main.xml 작성

```xml
<page path="/">
    <header>
        <left>
            <logo href="/">YouTube Analyzer</logo>
        </left>
        <right>
            <link href="/history">히스토리</link>
        </right>
    </header>
    
    <main>
        <hero>
            <title>유튜브 영상 소재 분석기</title>
            <description>URL만 입력하면 AI가 콘텐츠 소재를 정리해드립니다</description>
        </hero>
        
        <form action="/api/analyze" method="POST">
            <input 
                type="text" 
                name="url" 
                placeholder="https://youtube.com/watch?v=..."
                required
            />
            <button type="submit">분석하기</button>
        </form>
        
        <loading id="loading" style="display:none">
            <spinner/>
            <text>영상을 분석하고 있습니다...</text>
        </loading>
        
        <recent>
            <title>최근 분석</title>
            <grid>
                <card href="/result/{id}">
                    <thumbnail src="{썸네일}"/>
                    <title>{영상 제목}</title>
                    <channel>{채널명}</channel>
                    <date>{분석 일시}</date>
                </card>
            </grid>
        </recent>
    </main>
    
    <footer>
        <text>© 2025 YouTube Analyzer</text>
    </footer>
</page>
```

---

## 6단계: plans/wireframes/result.xml 작성

```xml
<page path="/result/{id}">
    <header>
        <left>
            <logo href="/">YouTube Analyzer</logo>
        </left>
        <right>
            <link href="/history">히스토리</link>
        </right>
    </header>
    
    <main>
        <video-card>
            <thumbnail src="{썸네일}"/>
            <info>
                <title>{영상 제목}</title>
                <channel>{채널명}</channel>
                <link href="{원본 URL}" target="_blank">원본 보기 →</link>
            </info>
        </video-card>
        
        <analysis>
            <section id="summary">
                <header>
                    <icon>📌</icon>
                    <title>영상 요약</title>
                </header>
                <content>{요약 내용}</content>
            </section>
            
            <section id="key-message">
                <header>
                    <icon>💡</icon>
                    <title>핵심 메시지</title>
                </header>
                <content>{핵심 메시지}</content>
            </section>
            
            <section id="key-points">
                <header>
                    <icon>🎯</icon>
                    <title>키포인트</title>
                </header>
                <list>
                    <item>1. {키포인트1}</item>
                    <item>2. {키포인트2}</item>
                    <item>3. {키포인트3}</item>
                </list>
            </section>
            
            <section id="quotes">
                <header>
                    <icon>🗣️</icon>
                    <title>인용할 대사</title>
                </header>
                <quote>"{인용 대사}"</quote>
            </section>
            
            <section id="people">
                <header>
                    <icon>👤</icon>
                    <title>등장 인물</title>
                </header>
                <list>
                    <item>
                        <name>{이름}</name>
                        <links>
                            <link href="{관련 링크}">인터뷰 보기</link>
                        </links>
                    </item>
                </list>
            </section>
            
            <section id="content-ideas">
                <header>
                    <icon>🔥</icon>
                    <title>콘텐츠 추천</title>
                </header>
                
                <target-group name="뇌동매매 타겟">
                    <title-example>{제목 예시}</title-example>
                    <direction>{활용 방향}</direction>
                </target-group>
                
                <target-group name="원칙 투자 타겟">
                    <title-example>{제목 예시}</title-example>
                    <direction>{활용 방향}</direction>
                </target-group>
                
                <target-group name="경제적 자유 타겟">
                    <title-example>{제목 예시}</title-example>
                    <direction>{활용 방향}</direction>
                </target-group>
            </section>
            
            <section id="script">
                <header>
                    <icon>🎬</icon>
                    <title>대본 방향</title>
                </header>
                <steps>
                    <step name="도입">{도입 내용}</step>
                    <step name="전개">{전개 내용}</step>
                    <step name="전환">{전환 내용}</step>
                    <step name="마무리">{마무리 내용}</step>
                </steps>
            </section>
        </analysis>
        
        <actions>
            <button href="/">새 분석하기</button>
            <button href="/history">히스토리</button>
        </actions>
    </main>
    
    <footer>
        <text>© 2025 YouTube Analyzer</text>
    </footer>
</page>
```

---

## 7단계: plans/wireframes/history.xml 작성

```xml
<page path="/history">
    <header>
        <left>
            <logo href="/">YouTube Analyzer</logo>
        </left>
        <right>
            <link href="/history" active>히스토리</link>
        </right>
    </header>
    
    <main>
        <title>분석 히스토리</title>
        
        <search>
            <input type="text" placeholder="검색..." />
        </search>
        
        <table>
            <thead>
                <th>썸네일</th>
                <th>영상 제목</th>
                <th>채널</th>
                <th>분석 일시</th>
                <th>액션</th>
            </thead>
            <tbody>
                <tr>
                    <td><thumbnail src="{썸네일}"/></td>
                    <td><link href="/result/{id}">{제목}</link></td>
                    <td>{채널명}</td>
                    <td>{날짜}</td>
                    <td>
                        <button onclick="delete({id})">삭제</button>
                    </td>
                </tr>
            </tbody>
        </table>
        
        <pagination>
            <prev>이전</prev>
            <numbers>1 2 3 4 5</numbers>
            <next>다음</next>
        </pagination>
    </main>
    
    <footer>
        <text>© 2025 YouTube Analyzer</text>
    </footer>
</page>
```

---

## 8단계: backend/requirements.txt 작성

```
fastapi==0.109.0
uvicorn==0.27.0
httpx==0.26.0
youtube-transcript-api==0.6.2
google-api-python-client==2.116.0
anthropic==0.18.1
python-dotenv==1.0.1
supabase==2.3.0
pydantic==2.5.3
python-multipart==0.0.6
```

---

## 9단계: .env.example 작성

```
# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# YouTube
YOUTUBE_API_KEY=AIzaSyDwZsJwAuh5-qrC7bcSAv6ne_NNMmPWygo

# Supabase
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here

# Backend
BACKEND_URL=http://localhost:8000
```

---

## 10단계: .gitignore 작성

```
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
*.so
.eggs/
*.egg-info/
*.egg

# Node
node_modules/
.next/
out/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local
.venv/
venv/
ENV/

# Database
*.db
*.sqlite3

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Vercel
.vercel

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
```

---

## 11단계: docker-compose.yml 작성 (로컬 개발용)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - YOUTUBE_API_KEY=${YOUTUBE_API_KEY}
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    command: npm run dev
```

---

## 12단계: backend/Dockerfile 작성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 13단계: frontend/Dockerfile 작성

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]
```

---

## 실행 순서

### 로컬 개발
1. 위 폴더 구조 전체 생성
2. 각 파일에 위 내용 작성
3. `.env` 파일 생성 (`.env.example` 복사 후 API 키 입력)
4. `docker-compose up` 또는 각각 실행:
   - 백엔드: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload`
   - 프론트: `cd frontend && npm install && npm run dev`

### 배포
1. **프론트엔드**: Vercel에 frontend 폴더 연결
2. **백엔드**: Railway에 backend 폴더 연결
3. 환경변수 설정

---

## 작업 완료 후

- PROGRESS.md에 완료 사항 기록
- 다음 단계: backend/app/main.py 및 기본 라우터 구현
