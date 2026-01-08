'use client';

import { useEffect, useState } from 'react';
import HistoryList from '@/components/HistoryList';
import Loading from '@/components/Loading';
import { getHistory, deleteHistory, type HistoryItem } from '@/lib/api';

export default function HistoryPage() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const limit = 10;

  useEffect(() => {
    loadHistory();
  }, [page]);

  const loadHistory = async () => {
    setIsLoading(true);
    const response = await getHistory(limit, page * limit);

    if (response.success) {
      setItems(response.data || []);
      setTotal(response.total || 0);
    }
    setIsLoading(false);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('정말 삭제하시겠습니까?')) return;

    const response = await deleteHistory(id);
    if (response.success) {
      setItems(items.filter((item) => item.id !== id));
      setTotal(total - 1);
    } else {
      alert(response.error || '삭제에 실패했습니다.');
    }
  };

  const filteredItems = searchTerm
    ? items.filter(
        (item) =>
          item.video_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
          item.channel_name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : items;

  const totalPages = Math.ceil(total / limit);

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-text-primary mb-8">분석 히스토리</h1>

      {/* Search */}
      <div className="mb-6">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="검색..."
          className="w-full px-4 py-3 bg-background border border-border rounded-xl text-text-primary placeholder-text-secondary focus:border-accent transition-colors"
        />
      </div>

      {/* Content */}
      {isLoading ? (
        <Loading message="히스토리를 불러오는 중..." />
      ) : (
        <>
          <HistoryList items={filteredItems} onDelete={handleDelete} />

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex justify-center items-center gap-4 mt-8">
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className="px-4 py-2 border border-border rounded-lg text-text-secondary hover:border-accent hover:text-accent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                이전
              </button>
              <span className="text-text-secondary">
                {page + 1} / {totalPages}
              </span>
              <button
                onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                disabled={page >= totalPages - 1}
                className="px-4 py-2 border border-border rounded-lg text-text-secondary hover:border-accent hover:text-accent disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                다음
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
