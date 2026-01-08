@echo off
chcp 65001 >nul
echo ========================================
echo   YouTube Analyzer 서버 종료
echo ========================================
echo.

:: Node.js 프로세스 종료 (프론트엔드)
echo 프론트엔드 서버 종료 중...
taskkill /f /im node.exe 2>nul
if %errorlevel%==0 (
    echo   - Node.js 프로세스 종료됨
) else (
    echo   - Node.js 프로세스 없음
)

:: Python 프로세스 종료 (백엔드)
echo 백엔드 서버 종료 중...
taskkill /f /im python.exe 2>nul
if %errorlevel%==0 (
    echo   - Python 프로세스 종료됨
) else (
    echo   - Python 프로세스 없음
)

echo.
echo ========================================
echo   모든 서버가 종료되었습니다.
echo ========================================
pause
