'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link href="/" className="text-xl font-bold text-text-primary hover:text-accent transition-colors">
          YouTube Analyzer
        </Link>
        <nav>
          <Link
            href="/history"
            className={`px-4 py-2 rounded-lg transition-colors ${
              pathname === '/history'
                ? 'bg-accent text-white'
                : 'text-text-secondary hover:text-text-primary hover:bg-card'
            }`}
          >
            히스토리
          </Link>
        </nav>
      </div>
    </header>
  );
}
