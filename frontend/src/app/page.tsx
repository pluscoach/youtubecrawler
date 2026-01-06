'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import UrlInput from '@/components/UrlInput';
import Loading from '@/components/Loading';
import HistoryList from '@/components/HistoryList';
import { analyzeVideo, getHistory, type HistoryItem } from '@/lib/api';

export default function Home() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [recentHistory, setRecentHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    loadRecentHistory();
  }, []);

  const loadRecentHistory = async () => {
    const response = await getHistory(5, 0);
    if (response.success) {
      setRecentHistory(response.data);
    }
  };

  const handleSubmit = async (url: string) => {
    setIsLoading(true);
    setError(null);

    const response = await analyzeVideo(url);

    if (response.success && response.data) {
      router.push(`/result/${response.data.id}`);
    } else {
      setError(response.error || '분석에 실패했습니다.');
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-16">
      {/* Hero Section */}
      <section className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-text-primary mb-4">
          유튜브 영상 소재 분석기
        </h1>
        <p className="text-text-secondary text-lg">
          URL만 입력하면 AI가 콘텐츠 소재를 정리해드립니다
        </p>
      </section>

      {/* URL Input */}
      <section className="mb-8">
        <UrlInput onSubmit={handleSubmit} isLoading={isLoading} />
      </section>

      {/* Loading */}
      {isLoading && (
        <section className="my-12">
          <Loading message="영상을 분석하고 있습니다... (30초~1분 소요)" />
        </section>
      )}

      {/* Error */}
      {error && (
        <section className="my-8">
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl p-4 text-center">
            {error}
          </div>
        </section>
      )}

      {/* Recent History */}
      {!isLoading && recentHistory.length > 0 && (
        <section className="mt-16">
          <h2 className="text-2xl font-bold text-text-primary mb-6">최근 분석</h2>
          <HistoryList items={recentHistory} />
        </section>
      )}
    </div>
  );
}
