'use client';

import { useState } from 'react';
import type { AnalysisResult } from '@/lib/api';

interface ResultCardProps {
  result: AnalysisResult;
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

export default function ResultCard({ result }: ResultCardProps) {
  return (
    <div className="space-y-4">
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
          <a
            href={result.video_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-accent hover:underline"
          >
            원본 보기 →
          </a>
        </div>
      </div>

      {/* 영상 요약 */}
      <Section icon="📌" title="영상 요약">
        <p className="text-text-secondary whitespace-pre-line">{result.summary}</p>
      </Section>

      {/* 핵심 메시지 */}
      <Section icon="💡" title="핵심 메시지">
        <p className="text-lg text-text-primary font-medium">{result.key_message}</p>
      </Section>

      {/* 키포인트 */}
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

      {/* 인용할 대사 */}
      <Section icon="🗣️" title="인용할 대사">
        <div className="space-y-3">
          {result.quotes.map((quote, index) => (
            <blockquote
              key={index}
              className="border-l-4 border-accent pl-4 py-2 text-text-secondary italic"
            >
              &ldquo;{quote}&rdquo;
            </blockquote>
          ))}
        </div>
      </Section>

      {/* 등장 인물 */}
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

      {/* 콘텐츠 추천 */}
      <Section icon="🔥" title="콘텐츠 추천">
        <div className="space-y-6">
          {result.content_ideas.map((idea, index) => (
            <div key={index} className="border-l-2 border-accent pl-4">
              <h4 className="text-accent font-semibold mb-2">[{idea.target}]</h4>
              <p className="text-text-primary mb-1">→ {idea.title_example}</p>
              <p className="text-text-secondary text-sm">→ {idea.direction}</p>
            </div>
          ))}
        </div>
      </Section>

      {/* 대본 방향 */}
      <Section icon="🎬" title="대본 방향">
        <div className="space-y-4">
          {[
            { label: '도입', value: result.script_direction.intro },
            { label: '전개', value: result.script_direction.development },
            { label: '전환', value: result.script_direction.transition },
            { label: '마무리', value: result.script_direction.conclusion },
          ].map((item, index) => (
            <div key={index} className="flex gap-4">
              <span className="text-accent font-semibold w-16 shrink-0">{item.label}</span>
              <p className="text-text-secondary">{item.value}</p>
            </div>
          ))}
        </div>
      </Section>
    </div>
  );
}
