import { Suspense } from 'react';
import Link from 'next/link';

interface PageProps {
  params: Promise<{ id: string }>;
}

export default async function ReadingPage({ params }: PageProps) {
  const { id } = await params;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b sticky top-0 bg-background/95 backdrop-blur z-10">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">XBook 阅读器</h1>
          <div className="flex gap-4">
            <Link
              href="/library"
              className="px-4 py-2 border rounded-lg hover:bg-accent"
            >
              ← 返回书库
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Suspense fallback={<div className="text-center py-20">加载中...</div>}>
          <ReaderContent textId={id} />
        </Suspense>
      </main>
    </div>
  );
}

import TextReader from '@/components/reader/TextReader';

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
          <span>语言: {text.language === 'ja' ? '日语' : text.language === 'en' ? '英语' : text.language}</span>
          <span>字数: {text.word_count}</span>
        </div>
      </div>

      {/* Interactive Reader */}
      <TextReader content={text.content} language={text.language} />

      {/* Features Info */}
      <div className="mt-12 p-6 border rounded-lg bg-primary/5">
        <h3 className="font-semibold mb-3 text-primary">💡 使用提示</h3>
        <ul className="space-y-2 text-sm">
          <li>✅ <strong>选中文本</strong> - 鼠标拖选任意单词或句子</li>
          <li>✅ <strong>查看释义</strong> - 自动显示分词和翻译</li>
          <li>✅ <strong>添加词汇</strong> - 点击"添加到词汇库"按钮</li>
          <li>⏳ 词汇颜色高亮 - 即将推出</li>
          <li>⏳ 音频同步播放 - 开发中</li>
        </ul>
      </div>
    </div>
  );
}
