'use client';

import { useState, useMemo } from 'react';

interface TextReaderProps {
  content: string;
  language: string;
}

const CHARS_PER_PAGE = 2000; // Characters per page

export default function TextReader({ content, language }: TextReaderProps) {
  const [selectedText, setSelectedText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [popupData, setPopupData] = useState<any>(null);
  const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });
  const [currentPage, setCurrentPage] = useState(0);

  // Split content into pages
  const pages = useMemo(() => {
    const paragraphs = content.split('\n');
    const pagesArray: string[] = [];
    let currentPageText = '';
    let currentLength = 0;

    for (const para of paragraphs) {
      if (currentLength + para.length > CHARS_PER_PAGE && currentPageText) {
        pagesArray.push(currentPageText);
        currentPageText = para + '\n';
        currentLength = para.length;
      } else {
        currentPageText += para + '\n';
        currentLength += para.length;
      }
    }

    if (currentPageText) {
      pagesArray.push(currentPageText);
    }

    return pagesArray.length > 0 ? pagesArray : [content];
  }, [content]);

  const totalPages = pages.length;

  const handleMouseUp = async (e: React.MouseEvent) => {
    const selection = window.getSelection();
    const text = selection?.toString().trim();

    if (text && text.length > 0) {
      setSelectedText(text);

      // 调用分词API
      try {
        const endpoint = language === 'ja' ? 'japanese' : 'english';
        const res = await fetch(`http://localhost:8000/api/v1/tokenizer/${endpoint}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });

        const tokenData = await res.json();

        // 调用翻译API
        const transRes = await fetch('http://localhost:8000/api/v1/translate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            text,
            source_lang: language,
            target_lang: 'zh'
          })
        });

        const transData = await transRes.json();

        setPopupData({
          tokens: tokenData.tokens,
          translation: transData.translation
        });
        setPopupPosition({ x: e.clientX, y: e.clientY });
        setShowPopup(true);
      } catch (error) {
        console.error('Query failed:', error);
      }
    }
  };

  const handleAddVocab = async () => {
    if (!popupData || !popupData.tokens[0]) return;

    const token = popupData.tokens[0];

    try {
      await fetch('http://localhost:8000/api/v1/vocabulary', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          surface_form: token.surface,
          dictionary_form: token.dictionary_form,
          language,
          reading: token.reading,
          part_of_speech: token.part_of_speech,
          translations: [{ lang: 'zh', text: popupData.translation }],
          context_sentence: selectedText
        })
      });

      alert('词汇已添加！');
      setShowPopup(false);
    } catch (error) {
      alert('添加失败');
    }
  };

  return (
    <div className="relative">
      {/* Page Navigation */}
      {totalPages > 1 && (
        <div className="sticky top-20 z-10 mb-4 flex items-center justify-between bg-background/95 backdrop-blur border rounded-lg p-3">
          <button
            onClick={() => setCurrentPage(Math.max(0, currentPage - 1))}
            disabled={currentPage === 0}
            className="px-4 py-2 border rounded-lg hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed"
          >
            ← 上一页
          </button>

          <span className="text-sm font-medium">
            第 {currentPage + 1} 页 / 共 {totalPages} 页
          </span>

          <button
            onClick={() => setCurrentPage(Math.min(totalPages - 1, currentPage + 1))}
            disabled={currentPage === totalPages - 1}
            className="px-4 py-2 border rounded-lg hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed"
          >
            下一页 →
          </button>
        </div>
      )}

      {/* Content */}
      <div
        className="prose prose-lg max-w-none leading-relaxed min-h-[600px]"
        onMouseUp={handleMouseUp}
        style={{ userSelect: 'text', cursor: 'text' }}
      >
        <p className="whitespace-pre-wrap text-lg">{pages[currentPage]}</p>
      </div>

      {/* Bottom Navigation */}
      {totalPages > 1 && (
        <div className="mt-8 flex items-center justify-center gap-2">
          {Array.from({ length: Math.min(totalPages, 10) }, (_, i) => {
            const pageNum = Math.floor(currentPage / 10) * 10 + i;
            if (pageNum >= totalPages) return null;

            return (
              <button
                key={pageNum}
                onClick={() => setCurrentPage(pageNum)}
                className={`w-10 h-10 rounded-lg border ${
                  currentPage === pageNum
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent'
                }`}
              >
                {pageNum + 1}
              </button>
            );
          })}
        </div>
      )}

      {/* Translation Popup */}
      {showPopup && popupData && (
        <div
          className="fixed z-50 bg-white dark:bg-gray-800 border rounded-lg shadow-xl p-4 max-w-md"
          style={{
            left: Math.min(popupPosition.x, window.innerWidth - 400),
            top: Math.min(popupPosition.y + 10, window.innerHeight - 300)
          }}
        >
          <div className="flex justify-between items-start mb-3">
            <h3 className="font-bold text-lg">{selectedText}</h3>
            <button
              onClick={() => setShowPopup(false)}
              className="text-gray-500 hover:text-gray-700"
            >
              ✕
            </button>
          </div>

          <div className="space-y-3">
            {/* Translation */}
            <div>
              <p className="text-sm text-gray-500">翻译：</p>
              <p className="text-base font-medium">{popupData.translation}</p>
            </div>

            {/* Tokens */}
            <div>
              <p className="text-sm text-gray-500">分词：</p>
              <div className="space-y-1">
                {popupData.tokens.slice(0, 3).map((token: any, idx: number) => (
                  <div key={idx} className="text-sm">
                    <span className="font-medium">{token.surface}</span>
                    {token.reading && (
                      <span className="text-gray-500 ml-2">({token.reading})</span>
                    )}
                    <span className="text-gray-400 ml-2 text-xs">
                      {token.part_of_speech || token.dictionary_form}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Actions */}
            <div className="flex gap-2 pt-2 border-t">
              <button
                onClick={handleAddVocab}
                className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90"
              >
                添加到词汇库
              </button>
              <button
                onClick={() => setShowPopup(false)}
                className="px-4 py-2 border rounded-lg hover:bg-accent"
              >
                关闭
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Backdrop */}
      {showPopup && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowPopup(false)}
        />
      )}
    </div>
  );
}
