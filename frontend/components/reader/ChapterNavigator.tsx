'use client';

import { useState, useMemo } from 'react';

interface Chapter {
  title: string;
  startIndex: number;
  content: string;
}

interface ChapterNavigatorProps {
  content: string;
  onChapterChange: (chapterIndex: number) => void;
}

export default function ChapterNavigator({ content, onChapterChange }: ChapterNavigatorProps) {
  const [isOpen, setIsOpen] = useState(false);

  // Auto-detect chapters from content
  const chapters = useMemo(() => {
    const lines = content.split('\n');
    const detectedChapters: Chapter[] = [];
    let currentChapter: string[] = [];
    let chapterTitle = '开始';
    let startIndex = 0;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();

      // Detect chapter titles (various patterns)
      const isChapterTitle =
        // Pattern 1: 第X章, Chapter X, 第X話
        /^(第[0-9一二三四五六七八九十百千]+[章話节]|Chapter\s+\d+|[0-9]+\.)/i.test(line) ||
        // Pattern 2: Short lines that might be titles (< 30 chars, not empty)
        (line.length > 0 && line.length < 30 && i > 0 && lines[i - 1].trim() === '');

      if (isChapterTitle && currentChapter.length > 50) {
        // Save previous chapter
        detectedChapters.push({
          title: chapterTitle,
          startIndex,
          content: currentChapter.join('\n')
        });

        // Start new chapter
        chapterTitle = line || `第${detectedChapters.length + 1}章`;
        currentChapter = [];
        startIndex = content.split('\n').slice(0, i).join('\n').length;
      } else {
        currentChapter.push(line);
      }
    }

    // Add last chapter
    if (currentChapter.length > 0) {
      detectedChapters.push({
        title: chapterTitle,
        startIndex,
        content: currentChapter.join('\n')
      });
    }

    // If no chapters detected, split by length
    if (detectedChapters.length <= 1) {
      const chunkSize = 10000;
      const chunks: Chapter[] = [];
      let start = 0;

      while (start < content.length) {
        const chunk = content.slice(start, start + chunkSize);
        chunks.push({
          title: `第${chunks.length + 1}部分`,
          startIndex: start,
          content: chunk
        });
        start += chunkSize;
      }

      return chunks;
    }

    return detectedChapters;
  }, [content]);

  return (
    <div className="relative">
      {/* TOC Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="px-4 py-2 border rounded-lg hover:bg-accent flex items-center gap-2"
        title="章节目录"
      >
        📑 目录 ({chapters.length}章)
      </button>

      {/* TOC Panel */}
      {isOpen && (
        <>
          <div
            className="fixed inset-0 bg-black/20 z-40"
            onClick={() => setIsOpen(false)}
          />

          <div className="fixed right-0 top-0 bottom-0 w-80 bg-background border-l shadow-2xl z-50 overflow-y-auto">
            <div className="sticky top-0 bg-background border-b p-4 flex items-center justify-between">
              <h2 className="font-bold text-lg">章节目录</h2>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-500 hover:text-gray-700 text-xl"
              >
                ✕
              </button>
            </div>

            <div className="p-2">
              {chapters.map((chapter, index) => (
                <button
                  key={index}
                  onClick={() => {
                    onChapterChange(index);
                    setIsOpen(false);
                  }}
                  className="w-full text-left px-4 py-3 hover:bg-accent rounded-lg transition-colors mb-1"
                >
                  <div className="font-medium">{chapter.title}</div>
                  <div className="text-xs text-muted-foreground mt-1">
                    约 {Math.ceil(chapter.content.length / 400)} 页
                  </div>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export { type Chapter };
