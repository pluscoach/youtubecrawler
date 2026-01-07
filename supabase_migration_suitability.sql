-- YouTube Analyzer - 소재 적합성 판단 기능 마이그레이션
-- 기존 테이블이 있는 경우 이 스크립트를 실행하세요

-- suitability_analysis 컬럼 추가 (소재 적합성 분석)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS suitability_analysis JSONB DEFAULT NULL;

-- investment_strategy 컬럼 추가 (거장의 전략)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS investment_strategy TEXT DEFAULT NULL;

-- additional_analysis 컬럼 추가 (추가 분석 - 추후 사용)
ALTER TABLE analyses ADD COLUMN IF NOT EXISTS additional_analysis JSONB DEFAULT NULL;

-- quotes 컬럼이 기존 문자열 배열이면 JSONB로 변환 (새 구조: {text, speaker})
-- 주의: 기존 데이터가 있으면 수동으로 변환 필요
-- ALTER TABLE analyses ALTER COLUMN quotes TYPE JSONB USING quotes::jsonb;

-- 확인 메시지
SELECT '소재 적합성 판단 마이그레이션이 완료되었습니다!' as message;
