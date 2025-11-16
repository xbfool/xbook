'use client';

import { useState } from 'react';
import TextReader from './TextReader';
import Link from 'next/link';

interface ReaderWithChaptersProps {
  title: string;
  author?: string;
  content: string;
  language: string;
  wordCount: number;
}

export default function ReaderWithChapters({
  title,
  author,
  content,
  language,
  wordCount
}: ReaderWithChaptersProps) {
  const [currentChapterIndex, setCurrentChapterIndex] = useState(0);
  const [showTOC, setShowTOC] = useState(false);

  // Detect chapters from content
  const detectChapters = () => {
    const lines = content.split('\n');
    const chapters: { title: string; content: string }[] = [];
    let currentContent: string[] = [];
    let chapterTitle = '开始';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Chapter detection patterns
      const isChapter =
        /^(第[0-9一二三四五六七八九十百]+[章話]|Chapter\s+\d+|[0-9]+\.)/i.test(line) ||
        (line.length > 0 && line.length < 30 && lines[i - 1]?.trim() === '');

      if (isChapter && currentContent.length > 50) {
        chapters.push({ title: chapterTitle, content: currentContent.join('\n') });
        chapterTitle = line || `第${chapters.length + 1}章`;
        currentContent = [];
      } else {
        currentContent.push(line);
      }
    }

    if (currentContent.length > 0) {
      chapters.push({ title: chapterTitle, content: currentContent.join('\n') });
    }

    return chapters.length > 1 ? chapters : [{ title: '全文', content }];
  };

  const chapters = detectChapters();
  const currentChapter = chapters[currentChapterIndex];

  return (
    <div className="flex min-h-screen">
      {/* Left Sidebar - TOC */}
      {chapters.length > 1 && (
        <aside className={`fixed left-0 top-0 h-full bg-background border-r transition-transform z-30 ${showTOC ? 'translate-x-0' : '-translate-x-full'} w-80 overflow-y-auto`}>
          <div className="sticky top-0 bg-background border-b p-4 flex items-center justify-between">
            <h2 className="font-bold text-lg">📑 目录</h2>
            <button
              onClick={() => setShowTOC(false)}
              className="text-2xl hover:text-primary"
            >
              ✕
            </button>
          </div>

          <div className="p-4">
            {chapters.map((chapter, index) => (
              <button
                key={index}
                onClick={() => {
                  setCurrentChapterIndex(index);
                  setShowTOC(false);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className={`w-full text-left px-4 py-3 rounded-lg mb-2 transition-colors ${
                  currentChapterIndex === index
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent'
                }`}
              >
                <div className="font-medium">{chapter.title}</div>
                <div className="text-xs opacity-70 mt-1">
                  约 {Math.ceil(chapter.content.length / 400)} 页
                </div>
              </button>
            ))}
          </div>
        </aside>
      )}

      {/* Backdrop */}
      {showTOC && (
        <div
          className="fixed inset-0 bg-black/30 z-20"
          onClick={() => setShowTOC(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1">
        {/* Sticky Header */}
        <div className="sticky top-0 z-10 bg-background/95 backdrop-blur border-b">
          <div className="container mx-auto px-4 py-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                {chapters.length > 1 && (
                  <button
                    onClick={() => setShowTOC(true)}
                    className="px-4 py-2 border rounded-lg hover:bg-accent font-medium"
                  >
                    📑 目录
                  </button>
                )}

                <Link
                  href="/library"
                  className="px-4 py-2 border rounded-lg hover:bg-accent"
                >
                  ← 返回
                </Link>
              </div>

              <div className="text-right">
                <h1 className="font-bold text-lg">{title}</h1>
                {chapters.length > 1 && (
                  <p className="text-sm text-primary">
                    {currentChapter.title}
                  </p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Reader Content */}
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <TextReader content={currentChapter.content} language={language} />
        </div>

      {/* Chapter Navigation */}
      {chapters.length > 1 && (
        <div className="max-w-4xl mx-auto px-4 mt-8 flex justify-between items-center">
          <button
            onClick={() => {
              setCurrentChapterIndex(Math.max(0, currentChapterIndex - 1));
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
            disabled={currentChapterIndex === 0}
            className="px-6 py-3 border-2 rounded-lg hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            ← 上一章
          </button>

          <span className="text-sm text-muted-foreground">
            {currentChapterIndex + 1} / {chapters.length} 章
          </span>

          <button
            onClick={() => {
              setCurrentChapterIndex(Math.min(chapters.length - 1, currentChapterIndex + 1));
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }}
            disabled={currentChapterIndex === chapters.length - 1}
            className="px-6 py-3 border-2 rounded-lg hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed font-medium"
          >
            下一章 →
          </button>
        </div>
      )}
    </div>
  );
}
