@echo off
chcp 65001 >nul
echo ========================================
echo   YouTube Analyzer 서버 시작
echo ========================================
echo.

:: 백엔드 서버 시작 (새 창)
echo [1/3] 백엔드 서버 시작 중...
start "Backend Server" cmd /k "cd /d %~dp0backend && python -m uvicorn app.main:app --reload --port 8000"

:: 잠시 대기 (백엔드 먼저 시작되도록)
timeout /t 3 /nobreak >nul

:: 프론트엔드 서버 시작 (새 창)
echo [2/3] 프론트엔드 서버 시작 중...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

:: 브라우저 열기 대기
echo [3/3] 브라우저 열기 대기 중...
timeout /t 5 /nobreak >nul

:: 브라우저 열기
echo 브라우저를 엽니다...
start http://localhost:3000

echo.
echo ========================================
echo   서버가 실행되었습니다!
echo   - 백엔드: http://localhost:8000
echo   - 프론트엔드: http://localhost:3000
echo ========================================
echo.
echo 이 창은 닫아도 됩니다.
pause
