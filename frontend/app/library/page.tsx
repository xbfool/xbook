import Link from 'next/link';

export default async function LibraryPage() {
  // Fetch texts from API
  const res = await fetch('http://localhost:8000/api/v1/texts', {
    cache: 'no-store',
  });

  const data = await res.json();
  const texts = data.items || [];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">我的书库</h1>
          <p className="text-muted-foreground mt-2">
            开始阅读你的学习材料
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {texts.length === 0 ? (
          <div className="text-center py-20">
            <h2 className="text-2xl font-semibold mb-4">书库为空</h2>
            <p className="text-muted-foreground mb-8">
              上传你的第一本电子书开始学习吧！
            </p>
            <div className="flex gap-4 justify-center">
              <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold">
                上传EPUB/PDF
              </button>
              <Link
                href="/"
                className="px-6 py-3 border rounded-lg font-semibold hover:bg-accent"
              >
                返回首页
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {texts.map((text: any) => (
              <Link
                key={text.id}
                href={`/reading/${text.id}`}
                className="border rounded-lg p-6 hover:shadow-lg transition-all hover:scale-105"
              >
                <h3 className="text-xl font-semibold mb-2 line-clamp-2">
                  {text.title}
                </h3>
                {text.author && (
                  <p className="text-sm text-muted-foreground mb-4">
                    {text.author}
                  </p>
                )}
                <div className="flex gap-3 text-xs text-muted-foreground">
                  <span className="px-2 py-1 bg-primary/10 rounded">
                    {text.language === 'ja' ? '日语' : '英语'}
                  </span>
                  <span>{text.word_count} 词</span>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Stats */}
        <div className="mt-12 grid md:grid-cols-3 gap-6">
          <div className="border rounded-lg p-6">
            <h3 className="text-sm font-medium text-muted-foreground mb-2">
              总文本数
            </h3>
            <p className="text-3xl font-bold">{data.total}</p>
          </div>
          <div className="border rounded-lg p-6">
            <h3 className="text-sm font-medium text-muted-foreground mb-2">
              日语文本
            </h3>
            <p className="text-3xl font-bold">
              {texts.filter((t: any) => t.language === 'ja').length}
            </p>
          </div>
          <div className="border rounded-lg p-6">
            <h3 className="text-sm font-medium text-muted-foreground mb-2">
              英语文本
            </h3>
            <p className="text-3xl font-bold">
              {texts.filter((t: any) => t.language === 'en').length}
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
