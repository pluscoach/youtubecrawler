-- YouTube Analyzer - 비판적 분석 관점 기능 마이그레이션
-- 기존 테이블이 있는 경우 이 스크립트를 실행하세요

-- source_tracking 컬럼 추가 (출처 및 원본 추적)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS source_tracking JSONB DEFAULT '[]'::jsonb;

-- perspective 컬럼 추가 (분석 관점 ID)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS perspective TEXT DEFAULT 'auto_trading';

-- critical_analysis 컬럼 추가 (비판적 분석 결과 JSON - 모순 분석 포함)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS critical_analysis JSONB DEFAULT NULL;

-- 확인 메시지
SELECT '비판적 분석 관점 및 출처 추적 마이그레이션이 완료되었습니다!' as message;
