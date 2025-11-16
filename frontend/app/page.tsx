import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
            XBook
          </h1>
          <nav className="flex gap-4">
            <Link href="/library" className="px-4 py-2 hover:text-primary transition-colors">
              书库
            </Link>
            <Link href="/review" className="px-4 py-2 hover:text-primary transition-colors">
              复习
            </Link>
            <Link href="/stats" className="px-4 py-2 hover:text-primary transition-colors">
              统计
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center p-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-5xl md:text-6xl font-bold mb-6">
            智能外语学习平台
          </h2>
          <p className="text-xl md:text-2xl text-muted-foreground mb-12">
            通过阅读学习英语和日语，AI助力词汇记忆
          </p>

          {/* CTA Buttons */}
          <div className="flex gap-4 justify-center mb-16">
            <Link
              href="/library"
              className="px-8 py-4 bg-primary text-primary-foreground rounded-lg text-lg font-semibold hover:opacity-90 transition-opacity shadow-lg"
            >
              开始学习 →
            </Link>
            <Link
              href="/library"
              className="px-8 py-4 border-2 rounded-lg text-lg font-semibold hover:bg-accent transition-colors"
            >
              浏览书库
            </Link>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 gap-6 mb-12">
            <div className="border rounded-lg p-6 text-left hover:shadow-lg transition-shadow bg-card">
              <div className="text-4xl mb-3">📖</div>
              <h3 className="text-xl font-semibold mb-2">交互式阅读</h3>
              <p className="text-muted-foreground">
                点击任意单词即时查询翻译，智能分词支持日语和英语
              </p>
            </div>

            <div className="border rounded-lg p-6 text-left hover:shadow-lg transition-shadow bg-card">
              <div className="text-4xl mb-3">🎵</div>
              <h3 className="text-xl font-semibold mb-2">音频同步</h3>
              <p className="text-muted-foreground">
                卡拉OK样式文本高亮，跟随音频播放
              </p>
            </div>

            <div className="border rounded-lg p-6 text-left hover:shadow-lg transition-shadow bg-card">
              <div className="text-4xl mb-3">📝</div>
              <h3 className="text-xl font-semibold mb-2">词汇追踪</h3>
              <p className="text-muted-foreground">
                自动收集词汇，5级熟悉度分级系统
              </p>
            </div>

            <div className="border rounded-lg p-6 text-left hover:shadow-lg transition-shadow bg-card">
              <div className="text-4xl mb-3">🧠</div>
              <h3 className="text-xl font-semibold mb-2">间隔重复</h3>
              <p className="text-muted-foreground">
                SM-2算法优化记忆间隔，长期记忆更牢固
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">14</div>
              <div className="text-sm text-muted-foreground">API端点</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">2</div>
              <div className="text-sm text-muted-foreground">支持语言</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-primary mb-1">11</div>
              <div className="text-sm text-muted-foreground">数据库表</div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t py-6">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>基于 Next.js 15, FastAPI, PostgreSQL 和现代 NLP 工具构建</p>
          <p className="mt-2">支持 EPUB/PDF 电子书 · 日语假名标注 · 英语词形还原</p>
        </div>
      </footer>
    </div>
  );
}
