'use client';

import { useState } from 'react';

interface TextReaderProps {
  content: string;
  language: string;
}

export default function TextReader({ content, language }: TextReaderProps) {
  const [selectedText, setSelectedText] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [popupData, setPopupData] = useState<any>(null);
  const [popupPosition, setPopupPosition] = useState({ x: 0, y: 0 });

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
      <div
        className="prose prose-lg max-w-none leading-relaxed"
        onMouseUp={handleMouseUp}
        style={{ userSelect: 'text', cursor: 'text' }}
      >
        <p className="whitespace-pre-wrap text-lg">{content}</p>
      </div>

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
