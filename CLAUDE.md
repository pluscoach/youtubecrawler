# YouTube Analyzer 프로젝트 규칙

## 배포 환경
- 프론트엔드: https://youtubecrawler-ie6g.vercel.app (Vercel)
- 백엔드: https://youtube-analyzer-ap.onrender.com (Render)

## 코드 수정 후 필수 작업
1. 프론트엔드 수정 시: `cd frontend && npm run build`로 빌드 테스트
2. 타입 에러 없는지 확인 후 push
3. push하면 자동 배포됨

## 환경변수
- 백엔드 .env는 GitHub에 올리지 않음
- Render/Vercel에 직접 설정됨

## API 연동
- 프론트엔드 → 백엔드: NEXT_PUBLIC_API_URL 사용
- 백엔드 API 키들: Render 환경변수에 저장됨

## 수정 시 주의사항
- TypeScript 타입 에러 꼭 확인
- optional 필드는 ?. 또는 || 처리
- 로컬 빌드 성공 후 push
