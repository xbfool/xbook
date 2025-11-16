# ttsu.app Ebook Reader 技术分析

基于 `/mnt/d/GitHub/ebook-reader` 源代码分析

---

## 📁 项目结构

```
ebook-reader/
├── apps/web/          # 主应用（SvelteKit）
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── book-reader/    # 阅读器核心组件
│   │   │   │   │   ├── book-reader-continuous/  # 连续滚动模式
│   │   │   │   │   ├── book-reader-paginated/   # 分页模式
│   │   │   │   ├── book-card/      # 书籍卡片
│   │   │   │   └── book-export/    # 导出功能
│   │   │   └── functions/
│   │   │       ├── file-loaders/
│   │   │       │   └── epub/       # EPUB处理核心
│   │   │       │       ├── extract-epub.ts
│   │   │       │       ├── generate-epub-html.ts
│   │   │       │       └── load-epub.ts
│   │   └── routes/    # SvelteKit路由
│   └── package.json
└── pnpm-workspace.yaml
```

---

## 🔧 核心技术栈

### EPUB处理（✅ 可直接复用）
```json
{
  "@zip.js/zip.js": "2.4.26",      // ZIP解压（EPUB格式）
  "fast-xml-parser": "5.3.2",      // XML元数据解析
  "path-browserify": "1.0.1"       // 路径处理
}
```

### 数据存储
```json
{
  "idb": "8.0.3",                   // IndexedDB封装
  "fake-indexeddb": "6.2.5"         // 测试mock
}
```

### UI与交互
```json
{
  "@popperjs/core": "2.11.8",       // 弹窗定位
  "svelte-gestures": "5.0.7",       // 手势识别
  "svelte-fa": "4.0.4",             // 图标
  "rxjs": "7.8.2"                   // 响应式流
}
```

---

## 💡 EPUB处理核心流程

### 1. 解压EPUB（extract-epub.ts）
```typescript
import { ZipReader, BlobReader } from '@zip.js/zip.js';
import { XMLParser } from 'fast-xml-parser';

// 1. 打开ZIP
const reader = new ZipReader(new BlobReader(epubBlob));
const entries = await reader.getEntries();

// 2. 读取META-INF/container.xml（找到content.opf位置）
const containerXml = await entries['META-INF/container.xml'].getData();
const container = parser.parse(containerXml);
const opfPath = container.rootfile['@_full-path'];

// 3. 读取content.opf（目录和清单）
const opfXml = await entries[opfPath].getData();
const manifest = parser.parse(opfXml);

// 4. 提取所有内容文件
manifest.item.forEach(async (item) => {
  if (item['@_media-type'].startsWith('image/')) {
    // 图片作为Blob
    result[item.href] = await entry.getData(new BlobWriter());
  } else {
    // 文本作为String
    result[item.href] = await entry.getData(new TextWriter());
  }
});
```

**关键点**:
- EPUB = ZIP格式
- 元数据在XML中
- HTML内容需要提取和组合

### 2. 生成HTML（generate-epub-html.ts）
```typescript
// 提取所有章节HTML
// 组合成连续文档
// 处理内部链接和资源引用
// 返回可渲染的DOM元素
```

### 3. 样式处理（generate-epub-style-sheet.ts）
```typescript
// 提取EPUB中的CSS
// 合并和清理样式
// 生成统一样式表
```

---

## 🎯 关键功能实现

### 1. 文本选择与词典集成

**实现位置**: `book-reader-continuous.svelte` / `book-reader-paginated.svelte`

**核心思路**:
```typescript
// 监听文本选择
document.addEventListener('selectionchange', () => {
  const selection = window.getSelection();
  const text = selection.toString();

  if (text) {
    // 触发词典查询（通过Yomitan扩展API）
    // 或显示自定义弹窗
  }
});
```

### 2. 假名显示

**实现方式**: 使用HTML `<ruby>` 标签
```html
<ruby>
  日本語
  <rt>にほんご</rt>
</ruby>
```

**CSS控制**:
```css
ruby rt {
  font-size: 0.5em;
  display: none; /* 可通过设置切换显示 */
}
```

### 3. 阅读进度追踪

**统计字符数**:
```typescript
// character-stats-calculator.ts
function countCharacters(element: HTMLElement) {
  return element.innerText.length;
}

// 持续追踪
setInterval(() => {
  const visible = getVisibleElements();
  const chars = countCharacters(visible);
  updateReadingStats(chars, timeElapsed);
}, 1000);
```

### 4. 书签功能

**保存位置**:
```typescript
// bookmark-manager-continuous.ts
interface Bookmark {
  cfiRange: string;      // EPUB CFI（标准位置格式）
  text: string;          // 摘录文本
  timestamp: number;
}

// 保存到IndexedDB
await db.bookmarks.add(bookmark);
```

---

## 📊 可复用的核心代码

### 1. EPUB解析逻辑 ✅ 100%可复用
```
/lib/functions/file-loaders/epub/
├── extract-epub.ts          # ZIP解压 + XML解析
├── generate-epub-html.ts    # HTML生成
└── load-epub.ts             # 主入口
```

**这些文件是纯TypeScript，无Svelte依赖！**

### 2. 实用工具函数 ✅ 可参考
```
/lib/functions/
├── css-parser/              # CSS处理
├── file-loaders/utils/      # 通用工具
└── statistics-calculator/   # 阅读统计
```

### 3. 数据模型 ✅ 可参考
```typescript
interface Book {
  id: string;
  title: string;
  language: string;
  characters: number;
  sections: Section[];
  lastBookModified: number;
  lastBookOpen: number;
}

interface Section {
  reference: string;
  charactersWeight: number;
  characters: number;
}
```

---

## 🚀 我们的实施方案

### 方案：提取核心逻辑 + React封装

#### Step 1: 复制EPUB处理代码
```bash
# 创建目录
mkdir -p frontend/lib/epub

# 复制核心文件（纯TS，无框架依赖）
cp /mnt/d/GitHub/ebook-reader/apps/web/src/lib/functions/file-loaders/epub/* \
   frontend/lib/epub/

# 安装依赖
cd frontend
pnpm add @zip.js/zip.js fast-xml-parser path-browserify
```

#### Step 2: 创建React组件
```typescript
// frontend/components/reader/EpubReader.tsx
'use client';

import { useState, useEffect } from 'react';
import { loadEpub } from '@/lib/epub/load-epub';

export default function EpubReader({ bookUrl }: { bookUrl: string }) {
  const [content, setContent] = useState<string>('');

  useEffect(() => {
    async function load() {
      const res = await fetch(bookUrl);
      const blob = await res.blob();
      const epubData = await loadEpub(blob);
      setContent(epubData.elementHtml);
    }
    load();
  }, [bookUrl]);

  return (
    <div
      className="epub-content"
      dangerouslySetInnerHTML={{ __html: content }}
      onClick={handleTextSelection}
    />
  );
}
```

#### Step 3: 添加词汇查询
```typescript
function handleTextSelection(e: MouseEvent) {
  const selection = window.getSelection();
  const text = selection?.toString().trim();

  if (text) {
    // 调用我们的分词API
    tokenizeAndShowPopup(text);
  }
}
```

---

## 📝 关键学习点

### 1. EPUB = ZIP + XML + HTML
- 用ZIP库解压
- 用XML库解析元数据
- 用DOM解析HTML内容

### 2. 文本选择最佳实践
```typescript
// 监听selectionchange而非mouseup
document.addEventListener('selectionchange', handler);

// 获取选中文本的上下文
const selection = window.getSelection();
const range = selection.getRangeAt(0);
const container = range.commonAncestorContainer;
```

### 3. 阅读位置保存
- 使用EPUB CFI（Canonical Fragment Identifier）
- 或使用字符偏移量
- 存储到本地/数据库

---

## 🎯 建议实施步骤

### 今天可做（2小时）
1. ✅ 安装EPUB处理依赖
   ```bash
   pnpm add @zip.js/zip.js fast-xml-parser path-browserify
   ```

2. ✅ 复制EPUB解析代码
   - extract-epub.ts
   - generate-epub-html.ts
   - load-epub.ts

3. ✅ 创建简单React阅读器
   - 加载EPUB
   - 显示HTML内容
   - 基础样式

### 明天继续（3小时）
4. ⏳ 添加文本选择
5. ⏳ 集成分词API
6. ⏳ 显示翻译弹窗
7. ⏳ 保存词汇功能

---

## 💡 优势分析

### ttsu.app的优点
- ✅ 成熟的EPUB渲染
- ✅ 丰富的阅读模式
- ✅ 详细的统计追踪
- ✅ Yomitan集成

### 我们的优势
- ✅ 后端API集成（词汇同步）
- ✅ 数据库持久化
- ✅ SRS复习系统
- ✅ 跨设备同步（未来）
- ✅ 自定义词典（JMdict）

### 结合方案
- **借用**: EPUB解析逻辑
- **保留**: 我们的后端API
- **增强**: 词汇自动收集
- **创新**: 与SRS系统集成

---

## 📦 需要安装的包

```json
{
  "dependencies": {
    "@zip.js/zip.js": "^2.7.52",
    "fast-xml-parser": "^4.5.0",
    "path-browserify": "^1.0.1"
  }
}
```

---

**结论**: ttsu.app的EPUB处理核心是纯TypeScript，完全可以提取并用于React项目！

**下一步**: 要不要现在开始集成？
