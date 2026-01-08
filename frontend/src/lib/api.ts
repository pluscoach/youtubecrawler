const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types
export interface HistoryItem {
  id: string;
  video_id: string;
  video_title: string;
  video_url: string;
  channel_name: string;
  thumbnail_url: string;
  created_at: string;
}

export interface Quote {
  text: string;
  speaker: string;
}

export interface SourceTracking {
  source_title: string;
  source_url: string | null;
  verified?: boolean;
}

export interface SuitabilityItem {
  exists: boolean;
  content: string;
}

export interface SuitabilityLevel {
  level: string;
  reason: string;
}

export interface SuitabilityAnalysis {
  feasibility_issue: SuitabilityItem;
  hidden_premise: SuitabilityItem;
  criticism_point: SuitabilityItem;
  target_empathy: SuitabilityLevel;
  source_availability: SuitabilityLevel;
  suitability_score: number;
  judgment: string;
  usage_recommendation: string;
  unsuitable_reason?: string;
}

export interface HiddenPremise {
  premise: string;
  evidence: string;
  source_url?: string;
  verified?: boolean;
}

export interface RealisticContradiction {
  point: string;
  evidence: string;
  source_url?: string;
  verified?: boolean;
}

export interface SourceBasedContradiction {
  claim: string;
  counter_evidence: string;
  source_url?: string;
  verified?: boolean;
}

export interface HookingPoint {
  hook: string;
  usage: string;
}

export interface CriticalAnalysis {
  hidden_premises: HiddenPremise[];
  realistic_contradictions: RealisticContradiction[];
  source_based_contradictions: SourceBasedContradiction[];
  hooking_points: HookingPoint[];
  content_direction: string[];
}

export interface InterviewClip {
  person: string;
  topic: string;
  link: string;
}

export interface EvidenceSource {
  topic: string;
  link: string;
}

export interface VideoSources {
  interview_clips: InterviewClip[];
  evidence_sources: EvidenceSource[];
}

export interface BonusTip {
  tip: string;
  source: string;
  source_url?: string;
}

export interface AdditionalAnalysis {
  video_sources: VideoSources;
  bonus_tip: BonusTip;
}

export interface AnalysisResult {
  id: string;
  video_id: string;
  video_title: string;
  video_url: string;
  channel_name: string;
  thumbnail_url: string;
  summary: string;
  key_message: string;
  key_points: string[];
  quotes: Quote[];
  people: string[];
  investment_strategy: string;
  source_tracking: SourceTracking[];
  suitability_analysis?: SuitabilityAnalysis;
  perspective?: string;
  critical_analysis?: CriticalAnalysis;
  additional_analysis?: AdditionalAnalysis;
  created_at: string;
}

export interface PerspectiveInfo {
  id: string;
  name: string;
  description: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  cached?: boolean;
  total?: number;
}

// API Functions
export async function analyzeVideo(url: string): Promise<ApiResponse<AnalysisResult>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

export async function getAnalysisResult(id: string): Promise<ApiResponse<AnalysisResult>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/result/${id}`);
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

// Alias for getAnalysisResult
export const getResult = getAnalysisResult;

export async function getHistory(limit: number = 20, offset: number = 0): Promise<ApiResponse<HistoryItem[]>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history?limit=${limit}&offset=${offset}`);
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

export async function deleteHistory(id: string): Promise<ApiResponse<null>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/history/${id}`, {
      method: 'DELETE',
    });
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

export async function getPerspectives(): Promise<ApiResponse<PerspectiveInfo[]>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/perspectives`);
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

export async function analyzeCritical(
  analysisId: string,
  perspective: string
): Promise<ApiResponse<AnalysisResult>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze/critical`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        analysis_id: analysisId,
        perspective,
      }),
    });
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}

export async function analyzeAdditional(analysisId: string): Promise<ApiResponse<AnalysisResult>> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analyze/additional`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        analysis_id: analysisId,
      }),
    });
    return await response.json();
  } catch (error) {
    return {
      success: false,
      error: '서버 연결에 실패했습니다.',
    };
  }
}
