-- YouTube Analyzer - Supabase DB 스키마
-- Supabase SQL Editor에서 이 스크립트를 실행하세요

-- UUID 확장 활성화 (이미 활성화되어 있을 수 있음)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- analyses 테이블 생성
CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,  -- 추후 인증 기능 추가 시 사용
    video_id TEXT NOT NULL,
    video_title TEXT,
    video_url TEXT NOT NULL,
    channel_name TEXT,
    thumbnail_url TEXT,
    transcript TEXT,
    summary TEXT,
    key_message TEXT,
    key_points JSONB DEFAULT '[]'::jsonb,
    quotes JSONB DEFAULT '[]'::jsonb,  -- {text, speaker} 구조
    people JSONB DEFAULT '[]'::jsonb,
    investment_strategy TEXT,  -- 거장의 전략
    -- 출처 추적 컬럼
    source_tracking JSONB DEFAULT '[]'::jsonb,
    -- 1단계: 소재 적합성 분석
    suitability_analysis JSONB DEFAULT NULL,
    -- 2단계: 비판적 분석 (버튼 클릭 시)
    perspective TEXT DEFAULT NULL,
    critical_analysis JSONB DEFAULT NULL,
    -- 3단계: 추가 분석 (버튼 클릭 시)
    additional_analysis JSONB DEFAULT NULL,
    -- deprecated (기존 호환성)
    content_ideas JSONB DEFAULT '[]'::jsonb,
    script_direction JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_video_id ON analyses(video_id);

-- RLS (Row Level Security) 비활성화 (1단계: 개인 사용)
-- 추후 멀티유저 지원 시 RLS 활성화 필요
ALTER TABLE analyses DISABLE ROW LEVEL SECURITY;

-- 테이블에 대한 권한 설정 (anon 및 authenticated 사용자)
GRANT ALL ON analyses TO anon;
GRANT ALL ON analyses TO authenticated;

-- 확인 메시지
SELECT 'YouTube Analyzer 스키마가 성공적으로 생성되었습니다!' as message;
