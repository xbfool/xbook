import { Suspense } from 'react';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ReadingPage({ params }: PageProps) {
  const { id } = await params;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">XBook Reader</h1>
          <div className="flex gap-4">
            <button className="px-4 py-2 border rounded-lg hover:bg-accent">
              返回书库
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Suspense fallback={<div>加载中...</div>}>
          <ReaderContent textId={id} />
        </Suspense>
      </main>
    </div>
  );
}

async function ReaderContent({ textId }: { textId: string }) {
  // Fetch text from API
  // Use API_URL for SSR (container to container), NEXT_PUBLIC_API_URL for client
  const apiUrl = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const res = await fetch(`${apiUrl}/api/v1/texts/${textId}`, {
    cache: 'no-store',
  });

  if (!res.ok) {
    return <div className="text-center py-20">文本未找到</div>;
  }

  const text = await res.json();

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="mb-8 pb-6 border-b">
        <h2 className="text-3xl font-bold mb-2">{text.title}</h2>
        {text.author && (
          <p className="text-muted-foreground">作者: {text.author}</p>
        )}
        <div className="flex gap-4 mt-4 text-sm text-muted-foreground">
          <span>语言: {text.language === 'ja' ? '日语' : '英语'}</span>
          <span>字数: {text.word_count}</span>
        </div>
      </div>

      {/* Content */}
      <div className="prose prose-lg max-w-none">
        <p className="text-lg leading-relaxed whitespace-pre-wrap">
          {text.content}
        </p>
      </div>

      {/* Placeholder for future features */}
      <div className="mt-12 p-6 border rounded-lg bg-muted/50">
        <h3 className="font-semibold mb-2">即将推出:</h3>
        <ul className="space-y-1 text-sm text-muted-foreground">
          <li>✨ 点击单词查看翻译</li>
          <li>🎨 词汇熟悉度颜色高亮</li>
          <li>📝 一键添加到学习列表</li>
          <li>🎵 音频同步播放</li>
        </ul>
      </div>
    </div>
  );
}
