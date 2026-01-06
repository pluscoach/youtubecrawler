'use client';

import Link from 'next/link';
import type { HistoryItem } from '@/lib/api';

interface HistoryListProps {
  items: HistoryItem[];
  onDelete?: (id: string) => void;
}

export default function HistoryList({ items, onDelete }: HistoryListProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-16 text-text-secondary">
        아직 분석 히스토리가 없습니다.
      </div>
    );
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="space-y-4">
      {items.map((item) => (
        <div
          key={item.id}
          className="bg-card border border-border rounded-xl p-4 flex flex-col sm:flex-row gap-4 hover:border-accent/50 transition-colors"
        >
          <img
            src={item.thumbnail_url}
            alt={item.video_title}
            className="w-full sm:w-40 h-24 object-cover rounded-lg"
          />
          <div className="flex-1 min-w-0">
            <Link
              href={`/result/${item.id}`}
              className="text-text-primary font-semibold hover:text-accent transition-colors line-clamp-2"
            >
              {item.video_title}
            </Link>
            <p className="text-text-secondary text-sm mt-1">{item.channel_name}</p>
            <p className="text-text-secondary text-xs mt-2">{formatDate(item.created_at)}</p>
          </div>
          <div className="flex sm:flex-col gap-2">
            <Link
              href={`/result/${item.id}`}
              className="px-4 py-2 text-sm bg-accent text-white rounded-lg hover:bg-accent/90 transition-colors text-center"
            >
              보기
            </Link>
            {onDelete && (
              <button
                onClick={() => onDelete(item.id)}
                className="px-4 py-2 text-sm border border-border text-text-secondary rounded-lg hover:border-red-500 hover:text-red-500 transition-colors"
              >
                삭제
              </button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
