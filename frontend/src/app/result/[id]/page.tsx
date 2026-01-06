'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Loading from '@/components/Loading';
import ResultCard from '@/components/ResultCard';
import { getResult, type AnalysisResult } from '@/lib/api';

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

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <ResultCard result={result} />

      {/* Actions */}
      <div className="flex gap-4 justify-center mt-8">
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
      </div>
    </div>
  );
}
