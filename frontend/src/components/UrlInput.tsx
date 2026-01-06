'use client';

import { useState } from 'react';

interface UrlInputProps {
  onSubmit: (url: string) => void;
  isLoading?: boolean;
}

export default function UrlInput({ onSubmit, isLoading = false }: UrlInputProps) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim() && !isLoading) {
      onSubmit(url.trim());
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://youtube.com/watch?v=..."
          className="flex-1 px-4 py-4 bg-background border border-border rounded-xl text-text-primary placeholder-text-secondary focus:border-accent transition-colors"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !url.trim()}
          className="px-8 py-4 bg-accent text-white font-semibold rounded-xl hover:bg-accent/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isLoading ? '분석 중...' : '분석하기'}
        </button>
      </div>
    </form>
  );
}
