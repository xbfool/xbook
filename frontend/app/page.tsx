import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8">
      <main className="max-w-4xl mx-auto text-center">
        <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-blue-600 to-purple-600 text-transparent bg-clip-text">
          XBook
        </h1>
        <p className="text-2xl text-muted-foreground mb-12">
          Smart Language Learning Platform
        </p>

        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-3">📖 Interactive Reading</h2>
            <p className="text-muted-foreground">
              Click on any word to instantly translate. Smart tokenization for English and Japanese.
            </p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-3">🎵 Audio Sync</h2>
            <p className="text-muted-foreground">
              Karaoke-style text highlighting synchronized with audio playback.
            </p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-3">📝 Vocabulary Tracking</h2>
            <p className="text-muted-foreground">
              Automatic vocabulary collection with 5-level proficiency grading system.
            </p>
          </div>

          <div className="border rounded-lg p-6 hover:shadow-lg transition-shadow">
            <h2 className="text-xl font-semibold mb-3">🧠 Spaced Repetition</h2>
            <p className="text-muted-foreground">
              SM-2 algorithm for optimal learning intervals and long-term retention.
            </p>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <Link
            href="/library"
            className="px-6 py-3 bg-primary text-primary-foreground rounded-lg font-semibold hover:opacity-90 transition-opacity"
          >
            Get Started
          </Link>
          <Link
            href="/docs"
            className="px-6 py-3 border rounded-lg font-semibold hover:bg-accent transition-colors"
          >
            Learn More
          </Link>
        </div>

        <div className="mt-16 pt-8 border-t">
          <p className="text-sm text-muted-foreground">
            Built with Next.js 15, FastAPI, PostgreSQL, and modern NLP tools
          </p>
        </div>
      </main>
    </div>
  );
}
