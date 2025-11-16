# 阅读器实现方案

基于ttsu.app ebook-reader的技术研究和我们的需求分析。

---

## 🔍 ttsu.app 技术分析

### 技术栈
- **框架**: SvelteKit (非React)
- **EPUB处理**: @zip.js/zip.js + fast-xml-parser
- **UI**: TailwindCSS
- **存储**: IndexedDB (本地)
- **包管理**: pnpm

### 核心功能
- ✅ EPUB/文本解析
- ✅ 连续/分页模式
- ✅ Yomitan词典集成
- ✅ 阅读统计追踪
- ✅ 假名显示
- ✅ 书签功能

### 优点
- 专为日语学习设计
- 成熟的EPUB渲染
- 离线支持
- PWA功能

### 限制
- Svelte框架（我们用React）
- 前端全栈方案（我们有独立后端）
- 无服务端词汇追踪

---

## 💡 我们的实现方案

### 方案A: 借鉴设计，React重写 ⭐⭐⭐⭐⭐

**优势**:
- 完全控制代码
- 与现有Next.js栈整合
- 可以连接后端API
- 词汇自动同步到数据库

**实现要点**:
1. 使用相同的EPUB库 (`@zip.js/zip.js`)
2. React组件化阅读器
3. 集成我们的分词API
4. 连接词汇管理API

**工作量**: 2-3天

### 方案B: iframe嵌入ttsu.app ⭐⭐

**优势**:
- 快速集成
- 功能完整

**劣势**:
- 无法自定义
- 跨域限制
- 无法与后端集成

**不推荐**

### 方案C: 使用现有React EPUB库 ⭐⭐⭐⭐

**推荐库**:

1. **epubjs (最流行)** ⭐⭐⭐⭐⭐
   ```bash
   npm install epubjs react-reader
   ```
   - 50k+ 周下载
   - 完整EPUB支持
   - React组件封装
   - 高度可定制

2. **@react-reader/react-reader**
   - epubjs的React封装
   - 开箱即用
   - 简单集成

---

## 🎯 推荐实现方案

### 使用 epubjs + 自定义扩展

#### 第一步：集成epubjs基础阅读器
```typescript
// components/reader/EpubReader.tsx
'use client';

import { ReactReader } from '@react-reader/react-reader';
import { useState } from 'react';

export default function EpubReader({ bookUrl }: { bookUrl: string }) {
  const [location, setLocation] = useState(0);

  return (
    <ReactReader
      url={bookUrl}
      location={location}
      locationChanged={(epubcfi: string) => setLocation(epubcfi)}
      tocChanged={(toc: any) => console.log('TOC:', toc)}
      epubOptions={{
        flow: 'paginated',
        manager: 'default'
      }}
    />
  );
}
```

#### 第二步：添加文本选择处理
```typescript
// 监听文本选择
useEffect(() => {
  const handleSelection = async () => {
    const selection = window.getSelection();
    const selectedText = selection?.toString().trim();

    if (selectedText) {
      // 1. 调用分词API
      const tokens = await tokenize(selectedText);

      // 2. 显示翻译弹窗
      showTranslationPopup(tokens);

      // 3. 提供"添加到词汇库"按钮
    }
  };

  document.addEventListener('mouseup', handleSelection);
  return () => document.removeEventListener('mouseup', handleSelection);
}, []);
```

#### 第三步：集成我们的API
```typescript
async function tokenize(text: string) {
  const res = await fetch('/api/v1/tokenizer/japanese', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return res.json();
}

async function addToVocabulary(token: Token) {
  await fetch('/api/v1/vocabulary', {
    method: 'POST',
    body: JSON.stringify({
      surface_form: token.surface,
      dictionary_form: token.dictionary_form,
      language: 'ja',
      reading: token.reading,
      part_of_speech: token.part_of_speech
    })
  });
}
```

---

## 📦 需要安装的包

```json
{
  "dependencies": {
    "epubjs": "^0.3.93",
    "react-reader": "^2.0.6",
    "@zip.js/zip.js": "^2.7.52",
    "fast-xml-parser": "^4.5.0"
  }
}
```

---

## 🎨 UI设计借鉴

从ttsu.app学到的UX设计：

1. **阅读模式**
   - 分页 vs 滚动
   - 横向 vs 纵向
   - 自动滚动

2. **阅读体验**
   - 字体大小调节
   - 行间距控制
   - 背景色主题
   - 假名显示开关

3. **交互设计**
   - 点击单词查询
   - 双击/长按选择
   - 快捷键导航

4. **统计追踪**
   - 阅读时间
   - 阅读速度
   - 进度百分比
   - 热力图可视化

---

## 🚀 实施计划

### Phase 1: 基础阅读器 (2-3小时)
```bash
# 1. 安装依赖
pnpm add epubjs react-reader @zip.js/zip.js

# 2. 创建组件
frontend/components/reader/EpubReader.tsx
frontend/components/reader/ReaderControls.tsx

# 3. 集成到阅读页面
frontend/app/reading/[id]/page.tsx
```

### Phase 2: 词汇查询 (1-2小时)
```bash
# 1. 文本选择监听
frontend/components/reader/SelectionHandler.tsx

# 2. 翻译弹窗
frontend/components/reader/TranslationPopup.tsx

# 3. API集成
- 调用分词API
- 调用翻译API
- 保存词汇
```

### Phase 3: 增强功能 (2-3小时)
```bash
# 1. 阅读进度
- 保存当前位置
- 自动恢复
- 进度条

# 2. 假名显示
- Ruby标签处理
- 开关控制

# 3. 样式定制
- 主题切换
- 字体调整
```

---

## 💻 示例代码（epubjs方案）

### 完整阅读器组件

```typescript
'use client';

import { ReactReader } from 'react-reader';
import { useState, useCallback } from 'react';

interface EpubReaderProps {
  bookUrl: string;
  bookId: string;
}

export default function EpubReader({ bookUrl, bookId }: EpubReaderProps) {
  const [location, setLocation] = useState<string | number>(0);
  const [selections, setSelections] = useState<string>('');

  const locationChanged = useCallback((epubcfi: string) => {
    setLocation(epubcfi);
    // 保存阅读进度到后端
    saveProgress(bookId, epubcfi);
  }, [bookId]);

  const getRendition = useCallback((rendition: any) => {
    // 监听文本选择
    rendition.on('selected', async (cfiRange: string, contents: any) => {
      const text = rendition.getRange(cfiRange).toString();
      setSelections(text);

      // 调用分词API
      const tokens = await tokenizeText(text);

      // 显示翻译弹窗
      showPopup(tokens);
    });

    // 添加假名支持
    rendition.themes.default({
      ruby: { 'font-size': '0.5em' }
    });
  }, []);

  return (
    <div style={{ height: '100vh' }}>
      <ReactReader
        url={bookUrl}
        location={location}
        locationChanged={locationChanged}
        getRendition={getRendition}
        epubOptions={{
          flow: 'paginated',
          manager: 'default',
        }}
      />

      {selections && (
        <TranslationPopup text={selections} />
      )}
    </div>
  );
}
```

---

## 📝 ttsu.app的核心优势我们可以借鉴

### 1. 文本分段策略
```
"文本通过标点符号（。？！）和闭合括号分割成段落"
```
→ 我们也应该智能分段，方便词汇查询

### 2. 阅读统计
```
- 每日阅读时间/字符数
- 阅读速度追踪
- 空闲自动暂停
```
→ 集成到我们的user_stats表

### 3. 词典集成模式
```
- 支持Yomitan扩展
- 点击查词
- 假名标注
```
→ 我们可以直接调用后端API，更强大

---

## 🎯 最终建议

**推荐方案**: 使用 `react-reader` (epubjs封装)

**理由**:
1. ✅ React生态，与Next.js无缝集成
2. ✅ 成熟稳定（50k+周下载）
3. ✅ 开箱即用的阅读器UI
4. ✅ 易于扩展（添加词汇查询）
5. ✅ 与我们的后端API完美配合

**实施步骤**:
1. 安装 `react-reader`
2. 创建客户端阅读器组件
3. 添加文本选择监听
4. 集成分词+翻译API
5. 实现词汇保存功能

**预计时间**: 4-6小时完成基础版本

---

**下一步**: 是否开始实现epubjs阅读器？
