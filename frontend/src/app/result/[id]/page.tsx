'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Loading from '@/components/Loading';
import ResultCard from '@/components/ResultCard';
import { getResult, type AnalysisResult } from '@/lib/api';

// MD 파일 생성 함수
function generateMarkdown(result: AnalysisResult): string {
  const date = new Date().toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });

  let md = `# ${result.video_title} 분석 결과\n\n`;
  md += `> 분석일: ${date}\n\n`;

  // 영상 정보
  md += `## 📺 영상 정보\n\n`;
  md += `- **URL**: ${result.video_url}\n`;
  md += `- **채널**: ${result.channel_name}\n`;
  if (result.view_count) md += `- **조회수**: ${result.view_count.toLocaleString()}회\n`;
  if (result.like_count) md += `- **좋아요**: ${result.like_count.toLocaleString()}개\n`;
  if (result.comment_count) md += `- **댓글**: ${result.comment_count.toLocaleString()}개\n`;
  if (result.subscriber_count) md += `- **구독자**: ${result.subscriber_count.toLocaleString()}명\n`;
  if (result.view_sub_ratio) md += `- **조회/구독 비율**: ${(result.view_sub_ratio * 100).toFixed(1)}%\n`;
  if (result.published_at) md += `- **업로드일**: ${result.published_at}\n`;
  md += `\n`;

  // 영상 구조 분석
  if (result.video_structure && result.video_structure.length > 0) {
    md += `## 🎬 영상 구조 분석\n\n`;
    if (result.structure_summary) md += `**구조 요약**: ${result.structure_summary}\n\n`;
    md += `| 순서 | 요소 | 유형 | 설명 |\n`;
    md += `|------|------|------|------|\n`;
    result.video_structure.forEach((item: any) => {
      md += `| ${item.order} | ${item.element} | ${item.type || '-'} | ${item.description} |\n`;
    });
    md += `\n`;
  }

  // 1단계: 영상 분석
  md += `---\n\n`;
  md += `## 📊 1단계: 영상 분석\n\n`;

  md += `### 영상 요약\n${result.summary}\n\n`;
  md += `### 핵심 메시지\n${result.key_message}\n\n`;

  if (result.key_points && result.key_points.length > 0) {
    md += `### 키포인트\n`;
    result.key_points.forEach((point, i) => {
      md += `${i + 1}. ${point}\n`;
    });
    md += `\n`;
  }

  if (result.investment_strategy) {
    md += `### 투자 전략\n${result.investment_strategy}\n\n`;
  }

  if (result.quotes && result.quotes.length > 0) {
    md += `### 인용구\n`;
    result.quotes.forEach((quote: any) => {
      const text = typeof quote === 'string' ? quote : quote.text;
      const speaker = typeof quote === 'string' ? '' : quote.speaker;
      md += `> "${text}"${speaker ? ` - ${speaker}` : ''}\n\n`;
    });
  }

  if (result.people && result.people.length > 0) {
    md += `### 등장 인물\n`;
    result.people.forEach((person: any) => {
      md += `- **${person.name}**${person.role ? ` (${person.role})` : ''}\n`;
    });
    md += `\n`;
  }

  // 출처 추적
  if (result.source_tracking && result.source_tracking.length > 0) {
    md += `### 출처 추적\n`;
    md += `| 인용 | 출처 | 유형 | URL |\n`;
    md += `|------|------|------|-----|\n`;
    result.source_tracking.forEach((src: any) => {
      const url = src.source_url ? `[링크](${src.source_url})` : '-';
      md += `| ${src.quote || '-'} | ${src.source_title || '-'} | ${src.source_type || '-'} | ${url} |\n`;
    });
    md += `\n`;
  }

  // 소재 적합성 분석
  if (result.suitability_analysis) {
    const sa = result.suitability_analysis;
    md += `### 소재 적합성 분석\n`;
    md += `- **적합도 점수**: ${sa.suitability_score}/5\n`;
    md += `- **판단**: ${sa.judgment}\n`;
    md += `- **활용 추천**: ${sa.usage_recommendation}\n`;
    if (sa.feasibility_issue?.exists) md += `- **실현 가능성 이슈**: ${sa.feasibility_issue.content}\n`;
    if (sa.hidden_premise?.exists) md += `- **숨겨진 전제**: ${sa.hidden_premise.content}\n`;
    if (sa.criticism_point?.exists) md += `- **비판 포인트**: ${sa.criticism_point.content}\n`;
    md += `\n`;
  }

  // 2단계: 비판적 분석
  if (result.critical_analysis) {
    const ca = result.critical_analysis;
    md += `---\n\n`;
    md += `## 🔍 2단계: 비판적 분석 (${ca.perspective_name || result.perspective})\n\n`;

    // 숨겨진 전제
    if (ca.hidden_premises && ca.hidden_premises.length > 0) {
      md += `### 숨겨진 전제\n`;
      md += `| 전제 | 문제점 | 출처 |\n`;
      md += `|------|--------|------|\n`;
      ca.hidden_premises.forEach((hp: any) => {
        const url = hp.source_url ? `[${hp.source}](${hp.source_url})` : (hp.source || '-');
        md += `| ${hp.premise || '-'} | ${hp.why_problem || '-'} | ${url} |\n`;
      });
      md += `\n`;
    }

    // 현실적 모순
    if (ca.realistic_contradictions && ca.realistic_contradictions.length > 0) {
      md += `### 현실적 모순\n`;
      md += `| 전략 | 어려운 이유 | 근거 | 출처 |\n`;
      md += `|------|-------------|------|------|\n`;
      ca.realistic_contradictions.forEach((rc: any) => {
        const url = rc.source_url ? `[${rc.source}](${rc.source_url})` : (rc.source || '-');
        md += `| ${rc.strategy || '-'} | ${rc.difficulty_reason || '-'} | ${rc.evidence_data || '-'} | ${url} |\n`;
      });
      md += `\n`;
    }

    // 출처 기반 모순
    if (ca.source_based_contradictions && ca.source_based_contradictions.length > 0) {
      md += `### 출처 기반 모순 분석\n`;
      ca.source_based_contradictions.forEach((sbc: any, i: number) => {
        md += `#### 모순 ${i + 1}\n`;
        md += `- **원본 주장**: ${sbc.original_claim || '-'}\n`;
        md += `- **원본 출처**: ${sbc.original_source || '-'}${sbc.original_source_url ? ` ([링크](${sbc.original_source_url}))` : ''}\n`;
        md += `- **반례**: ${sbc.counterexample || '-'}\n`;
        md += `- **반례 출처**: ${sbc.counterexample_source || '-'}${sbc.counterexample_source_url ? ` ([링크](${sbc.counterexample_source_url}))` : ''}\n`;
        md += `- **숨겨진 조건**: ${sbc.hidden_condition || '-'}\n`;
        md += `- **결론**: ${sbc.conclusion || '-'}\n\n`;
      });
    }

    // 후킹 포인트
    if (ca.hooking_points && ca.hooking_points.length > 0) {
      md += `### 후킹 포인트\n`;
      ca.hooking_points.forEach((hp: any, i: number) => {
        md += `${i + 1}. **${hp.point || '-'}**\n`;
        if (hp.empathy_reason) md += `   - 공감 이유: ${hp.empathy_reason}\n`;
        if (hp.target) md += `   - 타겟: ${hp.target}\n`;
        if (hp.level) md += `   - 레벨: ${hp.level}/5\n`;
      });
      md += `\n`;
    }

    // 콘텐츠 방향
    if (ca.content_direction) {
      md += `### 콘텐츠 방향\n`;
      if (Array.isArray(ca.content_direction)) {
        ca.content_direction.forEach((step: any) => {
          md += `#### ${step.stage}\n`;
          md += `- **예시**: ${step.example_script}\n`;
          md += `- **의도**: ${step.intention}\n\n`;
        });
      }
    }

    // 자동화 인사이트
    if (ca.automation_insight) {
      const ai = ca.automation_insight;
      md += `### 자동화 관점 인사이트\n`;
      md += `- **영상 유형**: ${ai.video_type || '-'}\n`;
      if (ai.video_type_reason) md += `- **유형 이유**: ${ai.video_type_reason}\n`;
      if (ai.core_insight) md += `- **핵심 인사이트**: ${ai.core_insight}\n`;
      md += `\n`;

      if (ai.problem_solution_table && ai.problem_solution_table.length > 0) {
        md += `#### 문제-해결책 테이블\n`;
        md += `| 문제점 | 사람이 힘든 이유 | 자동화 해결책 | 구현 방법 |\n`;
        md += `|--------|------------------|---------------|----------|\n`;
        ai.problem_solution_table.forEach((item: any) => {
          md += `| ${item.problem || '-'} | ${item.human_difficulty || '-'} | ${item.automation_solution || '-'} | ${item.implementation || '-'} |\n`;
        });
        md += `\n`;
      }

      if (ai.life_expansion?.applicable) {
        md += `#### 삶의 영역 확장\n`;
        md += `- **적용 영역**: ${ai.life_expansion.areas?.join(', ') || '-'}\n`;
        if (ai.life_expansion.examples && ai.life_expansion.examples.length > 0) {
          ai.life_expansion.examples.forEach((ex: any) => {
            md += `- **${ex.area}**: ${ex.application}\n`;
          });
        }
        md += `\n`;
      }
    }

    // 관점별 인사이트
    if (ca.perspective_insights && ca.perspective_insights.length > 0) {
      md += `### ${ca.perspective_name} 인사이트\n`;
      ca.perspective_insights.forEach((insight: string) => {
        md += `- ${insight}\n`;
      });
      md += `\n`;
    }
  }

  // 3단계: 추가 분석
  if (result.additional_analysis) {
    const aa = result.additional_analysis;
    md += `---\n\n`;
    md += `## 🎯 3단계: 추가 분석 (영상 제작 가이드)\n\n`;

    // 썸네일 문구
    if (aa.thumbnail_suggestions && aa.thumbnail_suggestions.length > 0) {
      md += `### 썸네일 문구 추천\n`;
      md += `| 유형 | 문구 | 클릭 심리 |\n`;
      md += `|------|------|----------|\n`;
      aa.thumbnail_suggestions.forEach((ts: any) => {
        md += `| ${ts.type} | ${ts.text} | ${ts.click_psychology} |\n`;
      });
      md += `\n`;
    }

    // 제목 추천
    if (aa.title_suggestions && aa.title_suggestions.length > 0) {
      md += `### 제목 추천\n`;
      aa.title_suggestions.forEach((ts: any, i: number) => {
        md += `${i + 1}. **${ts.title}**\n`;
        md += `   - 패턴: ${ts.pattern} | 타겟: ${ts.target}\n`;
        md += `   - 근거: ${ts.basis}\n\n`;
      });
    }

    // 영상 길이
    if (aa.video_length) {
      md += `### 영상 길이 추천\n`;
      md += `- **추천 길이**: ${aa.video_length.recommended_length}\n`;
      md += `- **형식**: ${aa.video_length.format}\n`;
      md += `- **판단 근거**: ${aa.video_length.judgment_basis}\n`;
      if (aa.video_length.parts && aa.video_length.parts.length > 0) {
        md += `\n| 파트 | 시간 | 내용 |\n`;
        md += `|------|------|------|\n`;
        aa.video_length.parts.forEach((part: any) => {
          md += `| ${part.part} | ${part.time_range} | ${part.content} |\n`;
        });
      }
      md += `\n`;
    }

    // 대본 방향
    if (aa.script_directions && aa.script_directions.length > 0) {
      md += `### 대본 방향\n`;
      aa.script_directions.forEach((sd: any) => {
        md += `#### ${sd.part}\n`;
        md += `- **예시**: ${sd.keypoint}\n`;
        md += `- **감정**: ${sd.emotion}\n`;
        md += `- **근거**: ${sd.basis}\n\n`;
      });
    }

    // 꿀팁
    if (aa.bonus_tip) {
      md += `### 보너스 꿀팁\n`;
      md += `- **주제**: ${aa.bonus_tip.topic}\n`;
      md += `- **내용**: ${aa.bonus_tip.summary}\n`;
      md += `- **도움 이유**: ${aa.bonus_tip.why_helpful}\n`;
      md += `- **출처**: ${aa.bonus_tip.source}${aa.bonus_tip.source_url ? ` ([링크](${aa.bonus_tip.source_url}))` : ''}\n\n`;
    }

    // 영상 소스
    if (aa.video_sources) {
      const vs = aa.video_sources;

      if (vs.interview_clips && vs.interview_clips.length > 0) {
        md += `### 인터뷰 클립 추천\n`;
        vs.interview_clips.forEach((clip: any) => {
          md += `- **${clip.person}**: ${clip.video_title}\n`;
          md += `  - 발언: "${clip.quote}"\n`;
          if (clip.link) md += `  - [영상 링크](${clip.link})\n`;
        });
        md += `\n`;
      }

      if (vs.evidence_sources && vs.evidence_sources.length > 0) {
        md += `### 반례 증거 소스\n`;
        vs.evidence_sources.forEach((es: any) => {
          md += `- **${es.contradiction}**\n`;
          md += `  - 증거: ${es.evidence}\n`;
          if (es.link) md += `  - [링크](${es.link})\n`;
        });
        md += `\n`;
      }

      if (vs.broll_keywords && vs.broll_keywords.length > 0) {
        md += `### B-roll 키워드\n`;
        md += `| 장면 | 키워드 | 활용 파트 |\n`;
        md += `|------|--------|----------|\n`;
        vs.broll_keywords.forEach((br: any) => {
          md += `| ${br.scene} | ${br.keyword} | ${br.usage_part} |\n`;
        });
        md += `\n`;
      }

      if (vs.veo3_prompts && vs.veo3_prompts.length > 0) {
        md += `### Veo3 프롬프트\n`;
        vs.veo3_prompts.forEach((vp: any) => {
          md += `#### ${vp.scene}\n`;
          md += `\`\`\`\n${vp.prompt}\n\`\`\`\n`;
          md += `활용: ${vp.usage_part}\n\n`;
        });
      }
    }

    // 성과 예측
    if (aa.performance_prediction) {
      const pp = aa.performance_prediction;
      md += `### 성과 예측\n`;

      if (pp.target_fits && pp.target_fits.length > 0) {
        md += `#### 타겟 적합도\n`;
        pp.target_fits.forEach((tf: any) => {
          md += `- **${tf.target}**: ${tf.fit_level}/5 - ${tf.reason}\n`;
        });
        md += `\n`;
      }

      if (pp.controversy) {
        md += `#### 논쟁 유발도\n`;
        md += `- 레벨: ${pp.controversy.level}/5\n`;
        md += `- 예상 반응: ${pp.controversy.expected_reactions}\n\n`;
      }

      if (pp.expected_comments && pp.expected_comments.length > 0) {
        md += `#### 예상 댓글\n`;
        pp.expected_comments.forEach((ec: any) => {
          md += `- [${ec.type}] "${ec.comment}"\n`;
        });
        md += `\n`;
      }

      if (pp.series_expansions && pp.series_expansions.length > 0) {
        md += `#### 시리즈 확장\n`;
        pp.series_expansions.forEach((se: any) => {
          md += `- **${se.topic}**: ${se.connection}\n`;
        });
        md += `\n`;
      }
    }

    // 멤버십 연결
    if (aa.membership_connection) {
      const mc = aa.membership_connection;
      md += `### 멤버십 연결 포인트\n`;

      if (mc.timings && mc.timings.length > 0) {
        md += `#### 추천 타이밍\n`;
        mc.timings.forEach((t: any) => {
          md += `- **${t.timing}** (${t.video_position}): ${t.reason}\n`;
        });
        md += `\n`;
      }

      if (mc.teasers && mc.teasers.length > 0) {
        md += `#### 티저 문구\n`;
        mc.teasers.forEach((t: any) => {
          md += `- [${t.situation}] "${t.teaser}"\n`;
        });
        md += `\n`;
      }

      if (mc.content_suggestions && mc.content_suggestions.length > 0) {
        md += `#### 멤버십 콘텐츠 제안\n`;
        mc.content_suggestions.forEach((cs: any) => {
          md += `- **${cs.topic}**: ${cs.connection}\n`;
        });
        md += `\n`;
      }
    }
  }

  md += `---\n\n`;
  md += `*이 분석 결과는 YouTube Analyzer에서 자동 생성되었습니다.*\n`;

  return md;
}

// 다운로드 함수
function downloadMarkdown(result: AnalysisResult) {
  const markdown = generateMarkdown(result);
  const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);

  const date = new Date().toISOString().split('T')[0];
  const sanitizedTitle = result.video_title.replace(/[<>:"/\\|?*]/g, '_').substring(0, 50);
  const filename = `${sanitizedTitle}_${date}_분석결과.md`;

  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export default function ResultPage() {
  const params = useParams();
  const id = params.id as string;

  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (id) {
      loadResult();
    }
  }, [id]);

  const loadResult = async () => {
    setIsLoading(true);
    const response = await getResult(id);

    if (response.success && response.data) {
      setResult(response.data);
    } else {
      setError(response.error || '결과를 불러오는데 실패했습니다.');
    }
    setIsLoading(false);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16">
        <Loading message="결과를 불러오는 중..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16">
        <div className="text-center">
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-6 mb-8">
            {error}
          </div>
          <Link
            href="/"
            className="inline-block px-6 py-3 bg-accent text-white rounded-xl hover:bg-accent/90 transition-colors"
          >
            홈으로 돌아가기
          </Link>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  const handleResultUpdate = (updatedResult: AnalysisResult) => {
    setResult(updatedResult);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <ResultCard result={result} onUpdate={handleResultUpdate} />

      {/* Actions */}
      <div className="flex flex-wrap gap-4 justify-center mt-8">
        <Link
          href="/"
          className="px-6 py-3 bg-accent text-white font-semibold rounded-xl hover:bg-accent/90 transition-colors"
        >
          새 분석하기
        </Link>
        <Link
          href="/history"
          className="px-6 py-3 border border-border text-text-secondary rounded-xl hover:border-accent hover:text-accent transition-colors"
        >
          히스토리
        </Link>
        <button
          onClick={() => downloadMarkdown(result)}
          className="px-6 py-3 bg-green-600 text-white font-semibold rounded-xl hover:bg-green-700 transition-colors flex items-center gap-2"
        >
          <span>📥</span>
          분석 결과 다운로드 (MD)
        </button>
      </div>
    </div>
  );
}
