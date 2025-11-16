'use client';

import { useState } from 'react';
import TextReader from './TextReader';
import ChapterNavigator from './ChapterNavigator';
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
    <div>
      {/* Sticky Header */}
      <div className="sticky top-0 z-20 bg-background/95 backdrop-blur border-b mb-6">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between mb-4">
            <Link
              href="/library"
              className="px-4 py-2 border rounded-lg hover:bg-accent text-sm"
            >
              ← 返回书库
            </Link>

            <div className="flex gap-2">
              <ChapterNavigator
                content={content}
                onChapterChange={(index) => {
                  setCurrentChapterIndex(index);
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
              />
            </div>
          </div>

          {/* Book Info */}
          <div>
            <h1 className="text-2xl font-bold mb-1">{title}</h1>
            {author && <p className="text-sm text-muted-foreground mb-2">{author}</p>}
            <div className="flex gap-4 text-xs text-muted-foreground">
              <span>语言: {language === 'ja' ? '日语' : language === 'en' ? '英语' : language}</span>
              <span>字数: {wordCount.toLocaleString()}</span>
              {chapters.length > 1 && (
                <span className="text-primary font-medium">
                  {currentChapter.title}
                </span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Reader Content */}
      <div className="max-w-4xl mx-auto px-4">
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
