'use client';

import { useState } from 'react';
import type {
  AnalysisResult,
  SourceTracking,
  SuitabilityAnalysis,
  Quote,
  CriticalAnalysis,
  HiddenPremise,
  RealisticContradiction,
  SourceBasedContradiction,
  HookingPoint,
  ContentDirectionStep,
  PerspectiveInfo,
  OldContentDirection,
  AdditionalAnalysisResult,
  ThumbnailSuggestion,
  TitleSuggestion,
  VideoLength,
  ScriptDirectionItem,
  BonusTip,
  VideoSourceRecommendation,
  PerformancePrediction,
  MembershipConnection,
} from '@/lib/api';
import { analyzeCritical, analyzeAdditional, getPerspectives } from '@/lib/api';

interface ResultCardProps {
  result: AnalysisResult;
  onUpdate?: (result: AnalysisResult) => void;
}

interface SectionProps {
  icon: string;
  title: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}

function Section({ icon, title, children, defaultOpen = true }: SectionProps) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <div className="bg-card border border-border rounded-xl overflow-hidden">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full px-6 py-4 flex items-center justify-between hover:bg-border/20 transition-colors"
      >
        <div className="flex items-center gap-3">
          <span className="text-2xl">{icon}</span>
          <h3 className="text-lg font-semibold text-text-primary">{title}</h3>
        </div>
        <span className="text-text-secondary text-xl">{isOpen ? '−' : '+'}</span>
      </button>
      {isOpen && <div className="px-6 pb-6 pt-2">{children}</div>}
    </div>
  );
}

function StarRating({ score, max = 5 }: { score: number; max?: number }) {
  return (
    <span className="text-yellow-400">
      {'★'.repeat(Math.min(score, max))}
      {'☆'.repeat(Math.max(max - score, 0))}
    </span>
  );
}

function SourceLink({ url, text }: { url?: string | null; text: string }) {
  if (url && url.startsWith('http')) {
    return (
      <a href={url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
        {text}
      </a>
    );
  }
  return <span className="text-text-secondary">{text}</span>;
}

function SourceTrackingTable({ sources }: { sources: SourceTracking[] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-3 px-2 text-text-secondary font-medium">인용 문장</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">원본 출처</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">유형</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">링크</th>
          </tr>
        </thead>
        <tbody>
          {sources.map((source, index) => (
            <tr key={index} className="border-b border-border/50">
              <td className="py-3 px-2 text-text-secondary max-w-xs">
                <div className="truncate" title={source.quote}>
                  &ldquo;{source.quote.substring(0, 50)}...&rdquo;
                </div>
              </td>
              <td className="py-3 px-2 text-text-primary">{source.source_title}</td>
              <td className="py-3 px-2">
                <span className={`px-2 py-1 rounded text-xs ${
                  source.source_type === '출처 확인 필요'
                    ? 'bg-yellow-500/20 text-yellow-400'
                    : 'bg-accent/20 text-accent'
                }`}>
                  {source.source_type}
                </span>
              </td>
              <td className="py-3 px-2">
                {source.source_url ? (
                  <a href={source.source_url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                    바로가기
                  </a>
                ) : (
                  <span className="text-text-secondary text-xs">
                    검색: {source.search_keywords?.join(', ') || '-'}
                  </span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SuitabilitySection({ suitability }: { suitability: SuitabilityAnalysis }) {
  const getJudgmentColor = (judgment: string) => {
    switch (judgment) {
      case '적합': return 'text-green-400 bg-green-500/20';
      case '보류': return 'text-yellow-400 bg-yellow-500/20';
      case '부적합': return 'text-red-400 bg-red-500/20';
      default: return 'text-text-secondary bg-border/20';
    }
  };

  const getRecommendationColor = (rec: string) => {
    switch (rec) {
      case '메인 콘텐츠': return 'text-green-400';
      case '숏폼': return 'text-blue-400';
      case '참고만': return 'text-yellow-400';
      case '패스': return 'text-red-400';
      default: return 'text-text-secondary';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <span className="text-text-secondary">소재 적합도:</span>
          <StarRating score={suitability.suitability_score} />
        </div>
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getJudgmentColor(suitability.judgment)}`}>
          {suitability.judgment}
        </span>
        <span className={`text-sm font-medium ${getRecommendationColor(suitability.usage_recommendation)}`}>
          추천: {suitability.usage_recommendation}
        </span>
      </div>

      {suitability.unsuitable_reason && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3">
          <span className="text-red-400 text-sm">{suitability.unsuitable_reason}</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-border/10 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className={suitability.feasibility_issue.exists ? 'text-red-400' : 'text-green-400'}>
              {suitability.feasibility_issue.exists ? '⚠️' : '✓'}
            </span>
            <span className="text-text-primary font-medium">실현 가능성 이슈</span>
          </div>
          <p className="text-text-secondary text-sm">{suitability.feasibility_issue.content}</p>
        </div>

        <div className="bg-border/10 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className={suitability.hidden_premise.exists ? 'text-yellow-400' : 'text-green-400'}>
              {suitability.hidden_premise.exists ? '🎭' : '✓'}
            </span>
            <span className="text-text-primary font-medium">숨겨진 전제</span>
          </div>
          <p className="text-text-secondary text-sm">{suitability.hidden_premise.content}</p>
        </div>

        <div className="bg-border/10 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className={suitability.criticism_point.exists ? 'text-blue-400' : 'text-text-secondary'}>
              {suitability.criticism_point.exists ? '💥' : '−'}
            </span>
            <span className="text-text-primary font-medium">비판 포인트</span>
          </div>
          <p className="text-text-secondary text-sm">{suitability.criticism_point.content}</p>
        </div>

        <div className="bg-border/10 rounded-lg p-4">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-pink-400">💗</span>
            <span className="text-text-primary font-medium">타겟 공감</span>
            <span className={`text-xs px-2 py-0.5 rounded ${
              suitability.target_empathy.level === '높음' ? 'bg-green-500/20 text-green-400' :
              suitability.target_empathy.level === '중간' ? 'bg-yellow-500/20 text-yellow-400' :
              'bg-red-500/20 text-red-400'
            }`}>
              {suitability.target_empathy.level}
            </span>
          </div>
          <p className="text-text-secondary text-sm">{suitability.target_empathy.reason}</p>
        </div>

        <div className="bg-border/10 rounded-lg p-4 md:col-span-2">
          <div className="flex items-center gap-2 mb-2">
            <span className="text-purple-400">📚</span>
            <span className="text-text-primary font-medium">출처 활용 가능성</span>
            <span className={`text-xs px-2 py-0.5 rounded ${
              suitability.source_availability.level === '높음' ? 'bg-green-500/20 text-green-400' :
              suitability.source_availability.level === '중간' ? 'bg-yellow-500/20 text-yellow-400' :
              'bg-red-500/20 text-red-400'
            }`}>
              {suitability.source_availability.level}
            </span>
          </div>
          <p className="text-text-secondary text-sm">{suitability.source_availability.reason}</p>
        </div>
      </div>
    </div>
  );
}

// 비판적 분석 UI 컴포넌트들
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function HiddenPremisesTable({ premises }: { premises: (HiddenPremise | string | any)[] }) {
  if (!premises || premises.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-3 px-2 text-text-secondary font-medium">전제</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">왜 문제인가</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">출처</th>
          </tr>
        </thead>
        <tbody>
          {premises.map((item, index) => {
            // 문자열인 경우 (기존 데이터)
            if (typeof item === 'string') {
              return (
                <tr key={index} className="border-b border-border/50">
                  <td className="py-3 px-2 text-text-primary" colSpan={3}>{item}</td>
                </tr>
              );
            }
            // 객체인 경우 (새 데이터)
            return (
              <tr key={index} className="border-b border-border/50">
                <td className="py-3 px-2 text-text-primary">{item.premise || '-'}</td>
                <td className="py-3 px-2 text-text-secondary">{item.why_problem || '-'}</td>
                <td className="py-3 px-2">
                  <SourceLink url={item.source_url} text={item.source || '-'} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function RealisticContradictionsTable({ contradictions }: { contradictions: (RealisticContradiction | string | any)[] }) {
  if (!contradictions || contradictions.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-3 px-2 text-text-secondary font-medium">전략</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">실행 어려운 이유</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">근거 데이터</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">출처</th>
          </tr>
        </thead>
        <tbody>
          {contradictions.map((item, index) => {
            // 문자열인 경우 (기존 데이터)
            if (typeof item === 'string') {
              return (
                <tr key={index} className="border-b border-border/50">
                  <td className="py-3 px-2 text-text-primary" colSpan={4}>{item}</td>
                </tr>
              );
            }
            // 객체인 경우 (새 데이터)
            return (
              <tr key={index} className="border-b border-border/50">
                <td className="py-3 px-2 text-text-primary">{item.strategy || '-'}</td>
                <td className="py-3 px-2 text-text-secondary">{item.difficulty_reason || '-'}</td>
                <td className="py-3 px-2 text-yellow-400">{item.evidence_data || '-'}</td>
                <td className="py-3 px-2">
                  <SourceLink url={item.source_url} text={item.source || '-'} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function SourceBasedContradictionsSection({ contradictions }: { contradictions: SourceBasedContradiction[] }) {
  if (!contradictions || contradictions.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="space-y-6">
      {contradictions.map((item, index) => (
        <div key={index} className="bg-border/10 rounded-xl p-4 space-y-4">
          <h4 className="text-accent font-semibold border-b border-border pb-2">
            모순 분석 #{index + 1}
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2 px-2 text-text-secondary font-medium w-24">항목</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">내용</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium w-40">출처</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border/50">
                  <td className="py-3 px-2 text-blue-400 font-medium">원본 주장</td>
                  <td className="py-3 px-2 text-text-secondary">{item.original_claim}</td>
                  <td className="py-3 px-2">
                    <SourceLink url={item.original_source_url} text={item.original_source} />
                  </td>
                </tr>
                <tr className="border-b border-border/50">
                  <td className="py-3 px-2 text-red-400 font-medium">반례/팩트</td>
                  <td className="py-3 px-2 text-text-secondary">{item.counterexample}</td>
                  <td className="py-3 px-2">
                    <SourceLink url={item.counterexample_source_url} text={item.counterexample_source} />
                  </td>
                </tr>
                <tr className="border-b border-border/50">
                  <td className="py-3 px-2 text-yellow-400 font-medium">숨겨진 조건</td>
                  <td className="py-3 px-2 text-text-secondary">{item.hidden_condition}</td>
                  <td className="py-3 px-2">
                    <SourceLink url={item.hidden_condition_source_url} text={item.hidden_condition_source} />
                  </td>
                </tr>
                <tr>
                  <td className="py-3 px-2 text-green-400 font-medium">결론</td>
                  <td className="py-3 px-2 text-text-primary font-medium" colSpan={2}>{item.conclusion}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function HookingPointsTable({ points }: { points: (HookingPoint | string | any)[] }) {
  if (!points || points.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border">
            <th className="text-left py-3 px-2 text-text-secondary font-medium">후킹 포인트</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">공감 이유</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">타겟</th>
            <th className="text-left py-3 px-2 text-text-secondary font-medium">레벨</th>
          </tr>
        </thead>
        <tbody>
          {points.map((item, index) => {
            // 문자열인 경우 (기존 데이터)
            if (typeof item === 'string') {
              return (
                <tr key={index} className="border-b border-border/50">
                  <td className="py-3 px-2 text-text-primary" colSpan={4}>{item}</td>
                </tr>
              );
            }
            // 객체인 경우 (새 데이터)
            return (
              <tr key={index} className="border-b border-border/50">
                <td className="py-3 px-2 text-text-primary">{item.point || '-'}</td>
                <td className="py-3 px-2 text-text-secondary">{item.empathy_reason || '-'}</td>
                <td className="py-3 px-2">
                  <span className="px-2 py-1 rounded text-xs bg-accent/20 text-accent">
                    {item.target || '-'}
                  </span>
                </td>
                <td className="py-3 px-2">
                  <StarRating score={item.level || 0} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

function ContentDirectionCards({ steps }: { steps: ContentDirectionStep[] | OldContentDirection }) {
  const getStageColor = (stage: string) => {
    switch (stage) {
      case '후킹': return 'text-red-400 border-red-400';
      case '모순지적': return 'text-yellow-400 border-yellow-400';
      case '공감': return 'text-blue-400 border-blue-400';
      case '해결암시': return 'text-green-400 border-green-400';
      default: return 'text-text-secondary border-border';
    }
  };

  // 배열인 경우 (새 형식)
  if (Array.isArray(steps)) {
    if (steps.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {steps.map((step, index) => (
          <div key={index} className={`bg-border/10 rounded-lg p-4 border-l-4 ${getStageColor(step.stage)}`}>
            <div className="flex items-center gap-2 mb-2">
              <span className={`font-semibold ${getStageColor(step.stage).split(' ')[0]}`}>
                {step.stage}
              </span>
              <span className="text-text-secondary text-xs">({step.intention})</span>
            </div>
            <p className="text-text-secondary italic">&ldquo;{step.example_script}&rdquo;</p>
          </div>
        ))}
      </div>
    );
  }

  // 객체인 경우 (기존 형식)
  const oldData = steps as OldContentDirection;
  if (!oldData || (!oldData.hook && !oldData.contradiction && !oldData.empathy && !oldData.solution_hint)) {
    return <p className="text-text-secondary">데이터 없음</p>;
  }

  const oldStages = [
    { stage: '후킹', content: oldData.hook },
    { stage: '모순지적', content: oldData.contradiction },
    { stage: '공감', content: oldData.empathy },
    { stage: '해결암시', content: oldData.solution_hint },
  ].filter(s => s.content);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {oldStages.map((step, index) => (
        <div key={index} className={`bg-border/10 rounded-lg p-4 border-l-4 ${getStageColor(step.stage)}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className={`font-semibold ${getStageColor(step.stage).split(' ')[0]}`}>
              {step.stage}
            </span>
          </div>
          <p className="text-text-secondary italic">&ldquo;{step.content}&rdquo;</p>
        </div>
      ))}
    </div>
  );
}

function CriticalAnalysisSection({ analysis }: { analysis: CriticalAnalysis }) {
  return (
    <div className="space-y-4">
      {/* 숨겨진 전제 */}
      <Section icon="🎭" title="숨겨진 전제">
        <HiddenPremisesTable premises={analysis.hidden_premises} />
      </Section>

      {/* 현실적 모순 */}
      <Section icon="💥" title="현실적 모순">
        <RealisticContradictionsTable contradictions={analysis.realistic_contradictions} />
      </Section>

      {/* 출처 기반 모순 분석 */}
      {analysis.source_based_contradictions && analysis.source_based_contradictions.length > 0 && (
        <Section icon="⚔️" title="출처 기반 모순 분석">
          <SourceBasedContradictionsSection contradictions={analysis.source_based_contradictions} />
        </Section>
      )}

      {/* 후킹 포인트 */}
      <Section icon="🎣" title="후킹 포인트">
        <HookingPointsTable points={analysis.hooking_points} />
      </Section>

      {/* 콘텐츠 방향 */}
      <Section icon="📝" title="콘텐츠 방향">
        <ContentDirectionCards steps={analysis.content_direction} />
      </Section>

      {/* 관점별 인사이트 */}
      {analysis.perspective_insights && analysis.perspective_insights.length > 0 && (
        <Section icon="🔗" title={`${analysis.perspective_name} 인사이트`}>
          <ul className="space-y-2">
            {analysis.perspective_insights.map((insight, index) => (
              <li key={index} className="flex gap-3 text-text-secondary">
                <span className="text-green-400">✓</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </Section>
      )}
    </div>
  );
}

// ===== 추가 분석 UI 컴포넌트 =====

// 썸네일 문구 카드
function ThumbnailSuggestionsGrid({ suggestions }: { suggestions: ThumbnailSuggestion[] }) {
  if (!suggestions || suggestions.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  const getTypeColor = (type: string) => {
    switch (type) {
      case '반전형': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case '질문형': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case '숫자형': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case '권위형': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      case '공감형': return 'bg-pink-500/20 text-pink-400 border-pink-500/30';
      default: return 'bg-border/20 text-text-secondary border-border';
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {suggestions.map((item, index) => (
        <div key={index} className={`rounded-xl p-4 border ${getTypeColor(item.type)}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-medium px-2 py-1 rounded bg-black/20">{item.type}</span>
          </div>
          <p className="text-lg font-bold mb-2">{item.text}</p>
          <p className="text-sm text-white mb-1">근거: {item.basis}</p>
          <p className="text-xs text-white">심리: {item.click_psychology}</p>
        </div>
      ))}
    </div>
  );
}

// 제목 후보 리스트
function TitleSuggestionsList({ suggestions }: { suggestions: TitleSuggestion[] }) {
  if (!suggestions || suggestions.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="space-y-3">
      {suggestions.map((item, index) => (
        <div key={index} className="bg-border/10 rounded-lg p-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <span className="text-xs font-medium px-2 py-1 rounded bg-accent/20 text-accent mr-2">
                {item.pattern}
              </span>
              <span className="text-xs px-2 py-1 rounded bg-border/30 text-text-secondary">
                {item.target}
              </span>
              <p className="text-text-primary font-medium mt-2">{item.title}</p>
              <p className="text-text-secondary text-sm mt-1">근거: {item.basis}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// 영상 길이 타임라인
function VideoLengthTimeline({ videoLength }: { videoLength: VideoLength }) {
  if (!videoLength) return <p className="text-text-secondary">데이터 없음</p>;

  const getFormatColor = (format: string) => {
    switch (format) {
      case '숏폼': return 'text-green-400';
      case '미드폼': return 'text-yellow-400';
      case '롱폼': return 'text-red-400';
      default: return 'text-text-secondary';
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4 flex-wrap">
        <span className="text-2xl font-bold text-text-primary">{videoLength.recommended_length}</span>
        <span className={`text-lg font-medium ${getFormatColor(videoLength.format)}`}>
          {videoLength.format}
        </span>
      </div>
      <p className="text-text-secondary text-sm">{videoLength.judgment_basis}</p>

      {videoLength.parts && videoLength.parts.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-2 px-2 text-text-secondary font-medium">파트</th>
                <th className="text-left py-2 px-2 text-text-secondary font-medium">시간</th>
                <th className="text-left py-2 px-2 text-text-secondary font-medium">내용</th>
              </tr>
            </thead>
            <tbody>
              {videoLength.parts.map((part, index) => (
                <tr key={index} className="border-b border-border/50">
                  <td className="py-2 px-2 text-accent font-medium">{part.part}</td>
                  <td className="py-2 px-2 text-text-primary">{part.time_range}</td>
                  <td className="py-2 px-2 text-text-secondary">{part.content}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

// 대본 방향 카드
function ScriptDirectionsList({ directions }: { directions: ScriptDirectionItem[] }) {
  if (!directions || directions.length === 0) return <p className="text-text-secondary">데이터 없음</p>;

  const getPartColor = (part: string) => {
    if (part.includes('후킹') || part.includes('인트로')) return 'border-red-400 bg-red-500/10';
    if (part.includes('권위')) return 'border-blue-400 bg-blue-500/10';
    if (part.includes('모순')) return 'border-yellow-400 bg-yellow-500/10';
    if (part.includes('원인') || part.includes('전개3')) return 'border-purple-400 bg-purple-500/10';
    if (part.includes('공감')) return 'border-pink-400 bg-pink-500/10';
    if (part.includes('꿀팁')) return 'border-green-400 bg-green-500/10';
    if (part.includes('마무리')) return 'border-accent bg-accent/10';
    return 'border-border bg-border/10';
  };

  return (
    <div className="space-y-4">
      {directions.map((item, index) => (
        <div key={index} className={`rounded-xl p-4 border-l-4 ${getPartColor(item.part)}`}>
          <div className="flex items-center gap-2 mb-2">
            <span className="font-bold text-text-primary">{item.part}</span>
            <span className="text-xs px-2 py-1 rounded bg-black/20 text-text-secondary">
              {item.emotion}
            </span>
          </div>
          <p className="text-text-secondary italic mb-2">&ldquo;{item.keypoint}&rdquo;</p>
          <p className="text-text-secondary text-sm">근거: {item.basis}</p>
        </div>
      ))}
    </div>
  );
}

// 꿀팁 박스
function BonusTipBox({ tip }: { tip: BonusTip }) {
  if (!tip) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="bg-gradient-to-r from-yellow-500/20 to-orange-500/20 border border-yellow-500/30 rounded-xl p-6">
      <h4 className="text-lg font-bold text-yellow-400 mb-2">{tip.topic}</h4>
      <p className="text-text-primary mb-3">{tip.summary}</p>
      <p className="text-text-secondary text-sm mb-2">왜 도움이 되나: {tip.why_helpful}</p>
      <div className="flex items-center gap-2">
        <span className="text-text-secondary text-sm">출처: {tip.source}</span>
        {tip.source_url && (
          <a href={tip.source_url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline text-sm">
            바로가기
          </a>
        )}
      </div>
    </div>
  );
}

// 영상 소스 추천
function VideoSourcesSection({ sources }: { sources: VideoSourceRecommendation }) {
  if (!sources) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="space-y-6">
      {/* 인터뷰 클립 */}
      {sources.interview_clips && sources.interview_clips.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">원본 인터뷰 클립</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">인물</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">영상</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">발언</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">시간</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">링크</th>
                </tr>
              </thead>
              <tbody>
                {sources.interview_clips.map((clip, index) => (
                  <tr key={index} className="border-b border-border/50">
                    <td className="py-2 px-2 text-accent font-medium">{clip.person}</td>
                    <td className="py-2 px-2 text-text-primary">{clip.video_title}</td>
                    <td className="py-2 px-2 text-text-secondary max-w-xs truncate">{clip.quote}</td>
                    <td className="py-2 px-2 text-text-secondary">{clip.timestamp}</td>
                    <td className="py-2 px-2">
                      {clip.link ? (
                        clip.link.startsWith('검색:') ? (
                          <span className="text-yellow-400 text-xs">{clip.link}</span>
                        ) : (
                          <a href={clip.link} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                            바로가기
                          </a>
                        )
                      ) : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 반례 증거 */}
      {sources.evidence_sources && sources.evidence_sources.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">반례 증거 영상/기사</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">모순 내용</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">증거</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">유형</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">링크</th>
                </tr>
              </thead>
              <tbody>
                {sources.evidence_sources.map((src, index) => (
                  <tr key={index} className="border-b border-border/50">
                    <td className="py-2 px-2 text-text-primary">{src.contradiction}</td>
                    <td className="py-2 px-2 text-text-secondary">{src.evidence}</td>
                    <td className="py-2 px-2">
                      <span className="px-2 py-1 rounded text-xs bg-accent/20 text-accent">{src.source_type}</span>
                    </td>
                    <td className="py-2 px-2">
                      {src.link ? (
                        src.link.startsWith('검색:') ? (
                          <span className="text-yellow-400 text-xs">{src.link}</span>
                        ) : (
                          <a href={src.link} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                            바로가기
                          </a>
                        )
                      ) : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* B-roll 키워드 */}
      {sources.broll_keywords && sources.broll_keywords.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">B-roll 검색 키워드</h4>
          <div className="flex flex-wrap gap-2">
            {sources.broll_keywords.map((kw, index) => (
              <div key={index} className="bg-border/20 rounded-lg px-3 py-2">
                <p className="text-text-primary font-mono text-sm">{kw.keyword}</p>
                <p className="text-text-secondary text-xs">{kw.scene} - {kw.usage_part}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Veo3 프롬프트 */}
      {sources.veo3_prompts && sources.veo3_prompts.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">Veo3 프롬프트</h4>
          <div className="space-y-3">
            {sources.veo3_prompts.map((veo, index) => (
              <div key={index} className="bg-border/10 rounded-lg p-3">
                <p className="text-text-secondary text-sm mb-1">{veo.scene} ({veo.usage_part})</p>
                <code className="block bg-black/30 rounded p-2 text-green-400 text-sm overflow-x-auto">
                  {veo.prompt}
                </code>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// 성과 예측
function PerformancePredictionSection({ prediction }: { prediction: PerformancePrediction }) {
  if (!prediction) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="space-y-6">
      {/* 타겟 적합도 */}
      {prediction.target_fits && prediction.target_fits.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">타겟 적합도</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {prediction.target_fits.map((fit, index) => (
              <div key={index} className="bg-border/10 rounded-lg p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-text-primary font-medium">{fit.target}</span>
                  <span className="text-yellow-400">{'★'.repeat(fit.fit_level)}{'☆'.repeat(5 - fit.fit_level)}</span>
                </div>
                <p className="text-text-secondary text-sm">{fit.reason}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 논쟁 유발도 */}
      {prediction.controversy && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">논쟁 유발도</h4>
          <div className="bg-border/10 rounded-lg p-4">
            <div className="flex items-center gap-4 mb-2">
              <div className="flex-1 bg-border/30 rounded-full h-3">
                <div
                  className="bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 h-3 rounded-full transition-all"
                  style={{ width: `${prediction.controversy.level * 20}%` }}
                />
              </div>
              <span className="text-text-primary font-bold">{prediction.controversy.level}/5</span>
            </div>
            <p className="text-text-secondary text-sm">{prediction.controversy.expected_reactions}</p>
          </div>
        </div>
      )}

      {/* 예상 댓글 */}
      {prediction.expected_comments && prediction.expected_comments.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">예상 댓글</h4>
          <div className="space-y-2">
            {prediction.expected_comments.map((comment, index) => {
              const typeColor = comment.type === '긍정' ? 'bg-green-500/20 border-green-500/30' :
                               comment.type === '부정' ? 'bg-red-500/20 border-red-500/30' :
                               'bg-blue-500/20 border-blue-500/30';
              return (
                <div key={index} className={`rounded-lg p-3 border ${typeColor}`}>
                  <span className="text-xs font-medium mr-2">[{comment.type}]</span>
                  <span className="text-text-secondary">&ldquo;{comment.comment}&rdquo;</span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 시리즈 확장 */}
      {prediction.series_expansions && prediction.series_expansions.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">시리즈 확장성</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {prediction.series_expansions.map((series, index) => (
              <div key={index} className="bg-border/10 rounded-lg p-4 border-l-4 border-accent">
                <p className="text-text-primary font-medium">{series.topic}</p>
                <p className="text-text-secondary text-sm mt-1">{series.connection}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// 멤버십 연결 포인트
function MembershipConnectionSection({ membership }: { membership: MembershipConnection }) {
  if (!membership) return <p className="text-text-secondary">데이터 없음</p>;

  return (
    <div className="space-y-6">
      {/* 연결 타이밍 */}
      {membership.timings && membership.timings.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">연결 타이밍</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">타이밍</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">위치</th>
                  <th className="text-left py-2 px-2 text-text-secondary font-medium">이유</th>
                </tr>
              </thead>
              <tbody>
                {membership.timings.map((timing, index) => (
                  <tr key={index} className="border-b border-border/50">
                    <td className="py-2 px-2 text-accent font-bold">{timing.timing}</td>
                    <td className="py-2 px-2 text-text-primary">{timing.video_position}</td>
                    <td className="py-2 px-2 text-text-secondary">{timing.reason}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 연결 문맥 */}
      {membership.contexts && membership.contexts.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">연결 문맥</h4>
          <div className="space-y-3">
            {membership.contexts.map((ctx, index) => (
              <div key={index} className="bg-border/10 rounded-lg p-4">
                <p className="text-text-secondary text-sm mb-2">직전: &ldquo;{ctx.previous_line}&rdquo;</p>
                <p className="text-accent font-medium">→ &ldquo;{ctx.connection}&rdquo;</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 티저 문구 */}
      {membership.teasers && membership.teasers.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">티저 문구</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {membership.teasers.map((teaser, index) => (
              <div key={index} className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 border border-purple-500/30 rounded-lg p-4">
                <p className="text-text-secondary text-sm mb-1">{teaser.situation}</p>
                <p className="text-text-primary font-medium">&ldquo;{teaser.teaser}&rdquo;</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 멤버십 콘텐츠 제안 */}
      {membership.content_suggestions && membership.content_suggestions.length > 0 && (
        <div>
          <h4 className="text-text-primary font-semibold mb-3">멤버십 콘텐츠 제안</h4>
          <div className="space-y-3">
            {membership.content_suggestions.map((content, index) => (
              <div key={index} className="bg-border/10 rounded-lg p-4 border-l-4 border-purple-400">
                <p className="text-text-primary font-medium">{content.topic}</p>
                <p className="text-text-secondary text-sm mt-1">{content.connection}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// 추가 분석 전체 섹션
function AdditionalAnalysisSection({ analysis }: { analysis: AdditionalAnalysisResult }) {
  return (
    <div className="space-y-6">
      {/* 1. 영상 제작 보조 */}
      <Section icon="🎨" title="영상 제작 보조" defaultOpen={true}>
        <div className="space-y-6">
          {/* 썸네일 문구 */}
          <div>
            <h4 className="text-text-primary font-semibold mb-3">썸네일 문구 추천</h4>
            <ThumbnailSuggestionsGrid suggestions={analysis.thumbnail_suggestions} />
          </div>

          {/* 제목 후보 */}
          <div>
            <h4 className="text-text-primary font-semibold mb-3">제목 후보 추천</h4>
            <TitleSuggestionsList suggestions={analysis.title_suggestions} />
          </div>

          {/* 영상 길이 */}
          {analysis.video_length && (
            <div>
              <h4 className="text-text-primary font-semibold mb-3">예상 영상 길이</h4>
              <VideoLengthTimeline videoLength={analysis.video_length} />
            </div>
          )}
        </div>
      </Section>

      {/* 2. 대본 방향 */}
      <Section icon="📝" title="대본 방향">
        <ScriptDirectionsList directions={analysis.script_directions} />
      </Section>

      {/* 3. 꿀팁 */}
      {analysis.bonus_tip && (
        <Section icon="🍯" title="꿀팁 추천">
          <BonusTipBox tip={analysis.bonus_tip} />
        </Section>
      )}

      {/* 4. 영상 소스 추천 */}
      {analysis.video_sources && (
        <Section icon="🎬" title="영상 소스 추천">
          <VideoSourcesSection sources={analysis.video_sources} />
        </Section>
      )}

      {/* 5. 콘텐츠 성과 예측 */}
      {analysis.performance_prediction && (
        <Section icon="📊" title="콘텐츠 성과 예측">
          <PerformancePredictionSection prediction={analysis.performance_prediction} />
        </Section>
      )}

      {/* 6. 멤버십 연결 포인트 */}
      {analysis.membership_connection && (
        <Section icon="💎" title="멤버십 연결 포인트">
          <MembershipConnectionSection membership={analysis.membership_connection} />
        </Section>
      )}
    </div>
  );
}

export default function ResultCard({ result, onUpdate }: ResultCardProps) {
  const [isLoadingCritical, setIsLoadingCritical] = useState(false);
  const [isLoadingAdditional, setIsLoadingAdditional] = useState(false);
  const [criticalError, setCriticalError] = useState<string | null>(null);
  const [additionalError, setAdditionalError] = useState<string | null>(null);
  const [perspectives, setPerspectives] = useState<PerspectiveInfo[]>([]);
  const [selectedPerspective, setSelectedPerspective] = useState('auto_trading');
  const [showPerspectiveSelector, setShowPerspectiveSelector] = useState(false);

  const loadPerspectives = async () => {
    const response = await getPerspectives();
    if (response.success) {
      setPerspectives(response.data);
    }
  };

  const handleCriticalAnalysis = async () => {
    // 소재 부적합 체크
    if (result.suitability_analysis?.judgment === '부적합') {
      setCriticalError(`이 영상은 비판적 분석에 적합하지 않습니다. 사유: ${result.suitability_analysis.unsuitable_reason || '소재 부적합'}`);
      return;
    }

    if (!showPerspectiveSelector) {
      await loadPerspectives();
      setShowPerspectiveSelector(true);
      return;
    }

    setIsLoadingCritical(true);
    setCriticalError(null);

    const response = await analyzeCritical(result.id, selectedPerspective);

    if (response.success && response.data) {
      if (onUpdate) {
        onUpdate(response.data);
      }
      setShowPerspectiveSelector(false);
    } else {
      setCriticalError(response.error || '비판적 분석에 실패했습니다.');
    }

    setIsLoadingCritical(false);
  };

  const handleAdditionalAnalysis = async () => {
    // 비판적 분석 완료 여부 체크
    if (!result.critical_analysis) {
      setAdditionalError('비판적 분석을 먼저 진행해주세요.');
      setTimeout(() => setAdditionalError(null), 3000);
      return;
    }

    setIsLoadingAdditional(true);
    setAdditionalError(null);

    const response = await analyzeAdditional(result.id);

    if (response.success && response.data) {
      if (onUpdate) {
        onUpdate(response.data);
      }
    } else {
      setAdditionalError(response.error || '추가 분석에 실패했습니다.');
    }

    setIsLoadingAdditional(false);
  };

  return (
    <div className="space-y-8">
      {/* 영상 정보 카드 */}
      <div className="bg-card border border-border rounded-xl p-6 flex flex-col md:flex-row gap-6">
        <img
          src={result.thumbnail_url}
          alt={result.video_title}
          className="w-full md:w-64 h-36 object-cover rounded-lg"
        />
        <div className="flex-1">
          <h2 className="text-xl font-bold text-text-primary mb-2">{result.video_title}</h2>
          <p className="text-text-secondary mb-4">{result.channel_name}</p>
          <a href={result.video_url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
            원본 보기
          </a>
        </div>
      </div>

      {/* 섹션 1: 영상 분석 */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
          <span>📺</span> 영상 분석
        </h2>

        <Section icon="📌" title="영상 요약">
          <p className="text-text-secondary whitespace-pre-line">{result.summary}</p>
        </Section>

        <Section icon="💡" title="핵심 메시지">
          <p className="text-lg text-text-primary font-medium">{result.key_message}</p>
        </Section>

        <Section icon="🎯" title="키포인트">
          <ul className="space-y-2">
            {result.key_points.map((point, index) => (
              <li key={index} className="flex gap-3 text-text-secondary">
                <span className="text-accent font-bold">{index + 1}.</span>
                <span>{point}</span>
              </li>
            ))}
          </ul>
        </Section>

        {result.quotes && result.quotes.length > 0 && (
          <Section icon="🗣️" title="인용할 대사">
            <div className="space-y-3">
              {result.quotes.map((quote: Quote | string, index: number) => {
                if (typeof quote === 'string') {
                  if (!quote) return null;
                  return (
                    <blockquote key={index} className="border-l-4 border-accent pl-4 py-2">
                      <p className="text-text-secondary italic">&ldquo;{quote}&rdquo;</p>
                    </blockquote>
                  );
                }
                const text = quote?.text || '';
                const speaker = quote?.speaker || '';
                if (!text) return null;
                return (
                  <blockquote key={index} className="border-l-4 border-accent pl-4 py-2">
                    <p className="text-text-secondary italic">&ldquo;{text}&rdquo;</p>
                    {speaker && <p className="text-text-primary text-sm mt-1">— {speaker}</p>}
                  </blockquote>
                );
              })}
            </div>
          </Section>
        )}

        {result.people.length > 0 && (
          <Section icon="👤" title="등장 인물">
            <ul className="space-y-2">
              {result.people.map((person, index) => (
                <li key={index} className="text-text-secondary">
                  <span className="text-text-primary font-medium">{person.name}</span>
                  {person.role && <span className="ml-2">- {person.role}</span>}
                </li>
              ))}
            </ul>
          </Section>
        )}

        {result.investment_strategy && (
          <Section icon="🎯" title="거장의 전략">
            <p className="text-text-secondary whitespace-pre-line">{result.investment_strategy}</p>
          </Section>
        )}

        {result.source_tracking && result.source_tracking.length > 0 && (
          <Section icon="📚" title="출처 추적">
            <SourceTrackingTable sources={result.source_tracking} />
          </Section>
        )}
      </div>

      {/* 섹션 2: 소재 적합성 판단 */}
      {result.suitability_analysis && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
            <span>⚖️</span> 소재 적합성 판단
          </h2>
          <div className="bg-card border border-border rounded-xl p-6">
            <SuitabilitySection suitability={result.suitability_analysis} />
          </div>
        </div>
      )}

      {/* 비판적 분석 버튼 (아직 안했을 때만) */}
      {!result.critical_analysis && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
            <span>🔥</span> 비판적 분석
          </h2>

          {/* 관점 선택 UI */}
          {showPerspectiveSelector && (
            <div className="bg-card border border-border rounded-xl p-4 space-y-4">
              <p className="text-text-secondary text-sm">비판적 분석 관점을 선택하세요:</p>
              <div className="flex flex-wrap gap-2">
                {perspectives.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => setSelectedPerspective(p.id)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      selectedPerspective === p.id
                        ? 'bg-accent text-white'
                        : 'bg-border/20 border border-border text-text-secondary hover:border-accent hover:text-accent'
                    }`}
                    title={p.description}
                  >
                    {p.name}
                  </button>
                ))}
              </div>
              <button
                onClick={handleCriticalAnalysis}
                disabled={isLoadingCritical}
                className="px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition-colors disabled:opacity-50"
              >
                {isLoadingCritical ? '상세 분석 중... (30초~1분)' : '분석 시작'}
              </button>
            </div>
          )}

          {!showPerspectiveSelector && (
            <button
              onClick={handleCriticalAnalysis}
              disabled={isLoadingCritical}
              className="px-6 py-3 bg-red-500/20 text-red-400 border border-red-500/30 rounded-xl hover:bg-red-500/30 transition-colors flex items-center gap-2 disabled:opacity-50"
            >
              <span>🔥</span>
              <span>{isLoadingCritical ? '상세 분석 중... (30초~1분)' : '비판적 분석 시작'}</span>
            </button>
          )}

          {criticalError && (
            <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-4 text-center">
              <p className="text-red-400">{criticalError}</p>
            </div>
          )}
        </div>
      )}

      {/* 비판적 분석 결과 */}
      {result.critical_analysis && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
            <span>🔥</span> 비판적 분석
            <span className="text-sm font-normal text-accent bg-accent/10 px-2 py-1 rounded-lg">
              {result.critical_analysis.perspective_name}
            </span>
          </h2>
          <CriticalAnalysisSection analysis={result.critical_analysis} />
        </div>
      )}

      {/* 추가 분석 버튼 (비판적 분석 완료 후, 추가 분석 아직 안했을 때) */}
      {result.critical_analysis && !result.additional_analysis && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
            <span>🎬</span> 추가 분석
          </h2>

          <button
            onClick={handleAdditionalAnalysis}
            disabled={isLoadingAdditional}
            className="px-6 py-3 bg-blue-500/20 text-blue-400 border border-blue-500/30 rounded-xl hover:bg-blue-500/30 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <span>🎬</span>
            <span>{isLoadingAdditional ? '상세 분석 중... (30초~1분)' : '추가 분석 시작'}</span>
          </button>

          {additionalError && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 text-center">
              <p className="text-yellow-400">{additionalError}</p>
            </div>
          )}
        </div>
      )}

      {/* 추가 분석 결과 */}
      {result.additional_analysis && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-text-primary flex items-center gap-2">
            <span>🎬</span> 추가 분석
            <span className="text-sm font-normal text-green-400 bg-green-500/10 px-2 py-1 rounded-lg">
              영상 제작 가이드
            </span>
          </h2>
          <AdditionalAnalysisSection analysis={result.additional_analysis} />
        </div>
      )}
    </div>
  );
}
