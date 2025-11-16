import { Suspense } from 'react';
import Link from 'next/link';
import ReaderWithChapters from '@/components/reader/ReaderWithChapters';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ReadingPage({ params }: PageProps) {
  const { id } = await params;

  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto px-4 py-8">
        <Suspense fallback={<div className="text-center py-20">加载中...</div>}>
          <ReaderContent textId={id} />
        </Suspense>
      </main>
    </div>
  );
}

async function ReaderContent({ textId }: { textId: string }) {
  // Fetch text from API
  const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${apiUrl}/api/v1/texts/${textId}`, {
    cache: 'no-store',
  });

  if (!res.ok) {
    return <div className="text-center py-20">文本未找到</div>;
  }

  const text = await res.json();

  return (
    <ReaderWithChapters
      title={text.title}
      author={text.author}
      content={text.content}
      language={text.language}
      wordCount={text.word_count}
    />
  );
}
