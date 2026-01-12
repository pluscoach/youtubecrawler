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
  quote?: string;
  source_type?: string;
  search_keywords?: string[];
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
  evidence?: string;
  why_problem?: string;
  source?: string;
  source_url?: string;
  verified?: boolean;
}

export interface RealisticContradiction {
  point?: string;
  strategy?: string;
  evidence?: string;
  difficulty_reason?: string;
  evidence_data?: string;
  source?: string;
  source_url?: string;
  verified?: boolean;
}

export interface SourceBasedContradiction {
  claim?: string;
  counter_evidence?: string;
  original_claim?: string;
  original_source?: string;
  original_source_url?: string;
  counterexample?: string;
  counterexample_source?: string;
  counterexample_source_url?: string;
  hidden_condition?: string;
  hidden_condition_source?: string;
  hidden_condition_source_url?: string;
  conclusion?: string;
  source_url?: string;
  verified?: boolean;
}

export interface HookingPoint {
  hook: string;
  usage: string;
  point?: string;
  empathy_reason?: string;
  target?: string;
  level?: number;
}

// 자동화 관점 인사이트
export interface ProblemSolutionItem {
  problem: string;
  human_difficulty: string;
  automation_solution: string;
  implementation: string;
}

export interface LifeExpansionExample {
  area: string;
  principle: string;
  application: string;
}

export interface LifeExpansion {
  applicable: boolean;
  areas: string[];
  examples: LifeExpansionExample[];
}

// 보완 사례 타입
export interface ImprovementCase {
  original_limitation?: string;
  improver?: string;
  method?: string;
  verified_result?: string;
  source_link?: string;
}

// 차별화 포인트 타입
export interface DifferentiationPoint {
  summary?: string;
  quote_template?: string;
}

export interface AutomationInsight {
  video_type: string;
  video_type_reason?: string;
  problem_solution_table: ProblemSolutionItem[];
  core_insight: string;
  life_expansion?: LifeExpansion;
  // 보완 사례 관련 필드
  improvement_cases?: ImprovementCase[];
  differentiation_points?: DifferentiationPoint[];
  improvement_search_failed?: boolean;
  suggested_search_keywords?: string[];
}

export interface ContentDirectionStep {
  stage: string;
  intention: string;
  example_script: string;
}

export interface OldContentDirection {
  hook?: string;
  contradiction?: string;
  empathy?: string;
  solution_hint?: string;
}

export interface CriticalAnalysis {
  hidden_premises: HiddenPremise[];
  realistic_contradictions: RealisticContradiction[];
  source_based_contradictions: SourceBasedContradiction[];
  hooking_points: HookingPoint[];
  content_direction: ContentDirectionStep[] | OldContentDirection;
  perspective_name?: string;
  perspective_insights?: string[];
  auto_trading_connection?: Array<{
    strategy_content: string;
    implementation_method: string;
    tech_stack: string;
    feasibility: string;
    limitation?: string;
  }>;
  automation_insight?: AutomationInsight;
}

export interface InterviewClip {
  person: string;
  topic: string;
  link: string;
  video_title?: string;
  quote?: string;
  timestamp?: string;
}

export interface EvidenceSource {
  topic: string;
  link: string;
  contradiction?: string;
  evidence?: string;
  source_type?: string;
}

export interface BrollKeyword {
  keyword: string;
  scene: string;
  usage_part: string;
}

export interface Veo3Prompt {
  scene: string;
  usage_part: string;
  prompt: string;
}

export interface VideoSourceRecommendation {
  interview_clips: InterviewClip[];
  evidence_sources: EvidenceSource[];
  broll_keywords?: BrollKeyword[];
  veo3_prompts?: Veo3Prompt[];
}

export interface BonusTip {
  tip?: string;
  topic?: string;
  summary?: string;
  why_helpful?: string;
  source: string;
  source_url?: string;
}

export interface ThumbnailSuggestion {
  type: string;
  text: string;
  basis: string;
  click_psychology: string;
}

export interface TitleSuggestion {
  pattern: string;
  target: string;
  title: string;
  basis: string;
}

export interface VideoLengthPart {
  part: string;
  time_range: string;
  content: string;
}

export interface VideoLength {
  recommended_length: string;
  format: string;
  judgment_basis: string;
  parts?: VideoLengthPart[];
}

export interface ScriptDirectionItem {
  part: string;
  emotion: string;
  keypoint: string;
  basis: string;
}

export interface TargetFit {
  target: string;
  fit_level: number;
  reason: string;
}

export interface Controversy {
  level: number;
  expected_reactions: string;
}

export interface ExpectedComment {
  type: string;
  comment: string;
}

export interface SeriesExpansion {
  topic: string;
  connection: string;
}

export interface PerformancePrediction {
  target_fits?: TargetFit[];
  controversy?: Controversy;
  expected_comments?: ExpectedComment[];
  series_expansions?: SeriesExpansion[];
}

export interface MembershipTiming {
  timing: string;
  video_position: string;
  reason: string;
}

export interface MembershipContext {
  previous_line: string;
  connection: string;
}

export interface MembershipTeaser {
  situation: string;
  teaser: string;
}

export interface MembershipContentSuggestion {
  topic: string;
  connection: string;
}

export interface MembershipConnection {
  timings?: MembershipTiming[];
  contexts?: MembershipContext[];
  teasers?: MembershipTeaser[];
  content_suggestions?: MembershipContentSuggestion[];
}

export interface AdditionalAnalysisResult {
  thumbnail_suggestions: ThumbnailSuggestion[];
  title_suggestions: TitleSuggestion[];
  video_length?: VideoLength;
  script_directions: ScriptDirectionItem[];
  bonus_tip?: BonusTip;
  video_sources?: VideoSourceRecommendation;
  performance_prediction?: PerformancePrediction;
  membership_connection?: MembershipConnection;
}

export interface AdditionalAnalysis {
  video_sources: VideoSourceRecommendation;
  bonus_tip: BonusTip;
}

export interface Person {
  name: string;
  role?: string;
}

export interface VideoStructureItem {
  order: number;
  element: string;
  type?: string | null;
  description: string;
}

export interface AnalysisResult {
  id: string;
  video_id: string;
  video_title: string;
  video_url: string;
  channel_name: string;
  thumbnail_url: string;
  // 영상 성과 데이터
  view_count?: number;
  like_count?: number;
  comment_count?: number;
  subscriber_count?: number;
  view_sub_ratio?: number;
  published_at?: string;
  // 영상 구조 분석
  video_structure?: VideoStructureItem[];
  structure_summary?: string;
  summary: string;
  key_message: string;
  key_points: string[];
  quotes: Quote[];
  people: Person[];
  investment_strategy: string;
  source_tracking: SourceTracking[];
  suitability_analysis?: SuitabilityAnalysis;
  perspective?: string;
  critical_analysis?: CriticalAnalysis;
  additional_analysis?: AdditionalAnalysisResult;
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
