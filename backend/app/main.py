from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers import youtube, history, auth, analyzer

settings = get_settings()

app = FastAPI(
    title="YouTube Analyzer API",
    description="유튜브 영상 자막을 분석하여 콘텐츠 소재를 추출하는 API",
    version="1.0.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://youtubecrawler-ie6g.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(youtube.router)
app.include_router(history.router)
app.include_router(auth.router)
app.include_router(analyzer.router)


@app.get("/")
async def root():
    return {
        "message": "YouTube Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
