# 开源字典和词库资源清单

本文档整理了可用于XBook的开源字典和词库资源。

---

## 📚 日语资源

### 1. JMdict - 核心日英词典 ⭐⭐⭐⭐⭐

**简介**: 最权威的开源日英词典，由Electronic Dictionary Research and Development Group维护

**官网**: http://www.edrdg.org/jmdict/j_jmdict.html

**数据格式**:
- XML (官方格式)
- JSON (社区转换)

**包含内容**:
- 180,000+ 词条
- 多语言翻译（英语、德语、法语等）
- 词性标注
- 例句
- 常用度信息

**下载地址**:
- 官方XML: http://ftp.edrdg.org/pub/Nihongo/JMdict_e.gz
- JSON版本: https://github.com/scriptin/jmdict-simplified

**许可证**: Creative Commons Attribution-ShareAlike 4.0

**推荐使用**:
```python
# 使用jmdict-simplified的JSON版本
import json

# 下载: https://github.com/scriptin/jmdict-simplified/releases
with open('jmdict-eng-3.5.0.json') as f:
    jmdict = json.load(f)

# 示例数据结构
{
    "id": "1000320",
    "kanji": [{"common": true, "text": "日本語", "tags": []}],
    "kana": [{"common": true, "text": "にほんご", "tags": [], "appliesToKanji": ["*"]}],
    "sense": [{
        "partOfSpeech": ["noun"],
        "gloss": [{"text": "Japanese (language)"}]
    }]
}
```

---

### 2. JMdict-Furigana - 带假名标注 ⭐⭐⭐⭐

**简介**: JMdict的扩展版本，为每个单词添加了假名标注

**GitHub**: https://github.com/Doublevil/JmdictFurigana

**特点**:
- 基于JMdict
- 每个汉字都有对应的假名
- JSON格式
- 适合语言学习应用

**数据示例**:
```json
{
    "word": "日本語",
    "furigana": "日本語[にほん|ご]",
    "readings": ["にほんご"]
}
```

---

### 3. JLPT词汇列表 ⭐⭐⭐⭐

**GitHub资源**:

#### a) jlpt-vocab (推荐)
- 仓库: https://github.com/stephenmk/jlpt-vocab
- 格式: CSV, JSON
- 内容: N5-N1全部词汇 (约6000词)
- 包含: 汉字、假名、英文释义、JLPT等级

#### b) JLPT-Study-Resources
- 仓库: https://github.com/echamudi/jlpt-study-resources
- 格式: JSON, CSV
- 详细的JLPT词汇分级
- 包含例句

**Kaggle数据集**:
- JLPT Words by Level: https://www.kaggle.com/datasets/robinpourtaud/jlpt-words-by-level
- 17,000+ 词汇，按N5-N1分级
- CSV格式，易于导入

**数据示例**:
```csv
kanji,hiragana,english,jlpt_level
日本語,にほんご,Japanese language,N5
勉強,べんきょう,study,N5
```

---

### 4. KANJIDIC - 汉字字典 ⭐⭐⭐⭐

**官网**: http://www.edrdg.org/wiki/index.php/KANJIDIC_Project

**内容**:
- 13,000+ 汉字
- 读音（音読み/訓読み）
- 笔画数
- 部首
- JLPT等级
- 使用频率

**格式**: XML, JSON

**GitHub JSON版本**:
- https://github.com/scriptin/jmdict-simplified (包含kanjidic)

---

### 5. japanese-db (npm包) ⭐⭐⭐

**NPM**: https://www.npmjs.com/package/japanese-db

**特点**:
- 整合JMdict, JMnedict, kanjidic2
- 生成SQLite数据库
- 可以直接集成到项目

**使用**:
```bash
npm install japanese-db
```

---

## 🔤 英语资源

### 1. Free Dictionary API ⭐⭐⭐⭐⭐

**API**: https://dictionaryapi.dev/

**特点**:
- 完全免费，无需API key
- 基于Wiktionary数据
- 实时查询

**端点**:
```bash
https://api.dictionaryapi.dev/api/v2/entries/en/{word}
```

**返回数据**:
- 定义（多个义项）
- 音标
- 发音音频URL
- 词性
- 例句
- 同义词/反义词

**示例响应**:
```json
[{
    "word": "hello",
    "phonetic": "/həˈloʊ/",
    "phonetics": [{"audio": "https://..."}],
    "meanings": [{
        "partOfSpeech": "noun",
        "definitions": [{
            "definition": "A greeting...",
            "example": "She greeted me with a warm hello."
        }]
    }]
}]
```

---

### 2. WordNet - 语义词典 ⭐⭐⭐⭐

**官网**: https://wordnet.princeton.edu/

**特点**:
- 语义关系网络
- 同义词集（synsets）
- 上下位关系
- 词义消歧

**Python库**:
```python
from nltk.corpus import wordnet

# 下载
import nltk
nltk.download('wordnet')

# 使用
syns = wordnet.synsets('learn')
# Synset('learn.v.01'): acquire knowledge
```

**适用场景**:
- 同义词查找
- 词义辨析
- 语义相关词

---

### 3. COCA词频表 ⭐⭐⭐⭐

**GitHub**: https://github.com/brucewlee/COCA-WordFrequency

**内容**:
- 前5000个高频词
- 基于4.5亿词的语料库
- 词性标注
- 搭配信息

**格式**: CSV, TXT

**示例**:
```csv
rank,word,pos,frequency
1,the,det,22038615
2,be,v,12545825
3,and,conj,10741073
```

---

### 4. BNC/COCA词频列表 ⭐⭐⭐⭐

**来源**: https://www.eapfoundation.com/vocab/general/bnccoca/

**规模**:
- 1k-25k词汇
- 基于BNC (1亿词) 和 COCA (4.5亿词)
- 按频率分级

**下载格式**:
- PDF
- Excel
- 分级列表（1k, 2k, 3k...25k）

---

### 5. English Dictionary Open Source ⭐⭐⭐

**GitHub**: https://github.com/CloudBytes-Academy/English-Dictionary-Open-Source

**特点**:
- 基于OPTED词典
- 多种格式（JSON, XML, SQL）
- 可直接导入数据库

**格式示例**:
```json
{
    "word": "study",
    "definition": "The devotion of time and attention...",
    "etymology": "From Latin studium"
}
```

---

## 🌐 多语言资源

### 1. Tatoeba - 例句数据库 ⭐⭐⭐⭐⭐

**官网**: https://tatoeba.org/

**特点**:
- 多语言例句（含日语、英语、中文）
- 句子对齐（翻译对）
- CC BY 2.0许可
- 可下载完整数据库

**下载**: https://tatoeba.org/en/downloads

**数据量**:
- 日语: 200,000+ 句子
- 英语: 1,400,000+ 句子
- 中日对照句子: 100,000+

**格式**:
```tsv
1	jpn	これは日本語です。
2	eng	This is Japanese.
```

---

## 📊 推荐集成方案

### 日语字典组合（最佳）

**1. 核心词典**: JMdict JSON版本
- 离线查询
- 完整释义
- 约200MB

**2. JLPT分级**: jlpt-vocab GitHub
- 词汇难度标注
- 学习路径规划
- 约5MB

**3. 例句库**: Tatoeba日语句子
- 真实例句
- 中日对照
- 约50MB

**4. 汉字信息**: KANJIDIC
- 汉字详情
- 笔画顺序
- 约10MB

**总计**: ~265MB，可完全离线使用

---

### 英语字典组合（最佳）

**1. 在线API**: Free Dictionary API
- 实时查询
- 无需下载
- 免费无限制

**2. 词频数据**: COCA Top 5000
- 标记常用词
- 学习优先级
- 约1MB

**3. 语义网络**: WordNet (NLTK)
- 同义词
- 词义关系
- 约20MB

**4. 例句**: Tatoeba英语句子
- 真实用例
- 多语言翻译
- 约200MB

**总计**: ~221MB (大部分通过API)

---

## 🚀 实施建议

### 阶段1: 基础集成（本周）
```bash
# 下载核心资源
1. JMdict JSON简化版
2. JLPT词汇CSV
3. COCA Top 5000

# 导入到PostgreSQL
- 创建dictionary表
- 批量导入
- 建立索引
```

### 阶段2: API集成（下周）
```bash
# 集成在线API
1. Free Dictionary API (英语)
2. 实现查询缓存
3. 回退到离线词典
```

### 阶段3: 例句丰富（未来）
```bash
# Tatoeba例句
1. 下载句子对
2. 导入数据库
3. 关联到词汇
```

---

## 📥 快速下载链接

### 日语
- **JMdict JSON**: https://github.com/scriptin/jmdict-simplified/releases (下载最新版)
- **JLPT词汇**: https://github.com/stephenmk/jlpt-vocab (克隆仓库)
- **Tatoeba日语**: https://downloads.tatoeba.org/exports/sentences.tar.bz2

### 英语
- **COCA 5000**: https://github.com/brucewlee/COCA-WordFrequency (克隆仓库)
- **BNC/COCA**: https://www.eapfoundation.com/vocab/general/bnccoca/ (下载Excel)
- **Tatoeba英语**: https://downloads.tatoeba.org/exports/sentences.tar.bz2

---

## 💻 集成示例代码

### 导入JMdict到PostgreSQL

```python
import json
import asyncpg

async def import_jmdict():
    conn = await asyncpg.connect('postgresql://...')

    with open('jmdict-eng-3.5.0.json') as f:
        jmdict = json.load(f)

    for word_id, entry in jmdict.items():
        # 提取汉字形式
        kanji = entry['kanji'][0]['text'] if entry.get('kanji') else None

        # 提取假名
        kana = entry['kana'][0]['text']

        # 提取释义
        gloss = entry['sense'][0]['gloss'][0]['text']

        # 插入数据库
        await conn.execute("""
            INSERT INTO jmdict_entries (
                entry_id, kanji, kana, gloss, pos
            ) VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (entry_id) DO NOTHING
        """, word_id, kanji, kana, gloss, entry['sense'][0].get('partOfSpeech', []))
```

### 调用Free Dictionary API

```python
import httpx

async def lookup_english_word(word: str):
    async with httpx.AsyncClient() as client:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = await client.get(url)

        if response.status_code == 200:
            data = response.json()[0]
            return {
                'word': data['word'],
                'phonetic': data.get('phonetic'),
                'definitions': [
                    {
                        'pos': m['partOfSpeech'],
                        'definition': m['definitions'][0]['definition']
                    }
                    for m in data['meanings']
                ]
            }
```

---

## 📝 数据库设计建议

### 新增表结构

```sql
-- JMdict词条表
CREATE TABLE jmdict_entries (
    entry_id VARCHAR(20) PRIMARY KEY,
    kanji TEXT,
    kana TEXT NOT NULL,
    gloss TEXT NOT NULL,
    pos TEXT[],
    jlpt_level VARCHAR(5),
    frequency_rank INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_jmdict_kanji ON jmdict_entries(kanji);
CREATE INDEX idx_jmdict_kana ON jmdict_entries(kana);
CREATE INDEX idx_jmdict_jlpt ON jmdict_entries(jlpt_level);

-- 英语词频表
CREATE TABLE english_frequency (
    word TEXT PRIMARY KEY,
    lemma TEXT,
    pos VARCHAR(20),
    frequency_rank INTEGER NOT NULL,
    frequency_count BIGINT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_eng_freq_rank ON english_frequency(frequency_rank);
CREATE INDEX idx_eng_freq_lemma ON english_frequency(lemma);

-- Tatoeba例句表
CREATE TABLE example_sentences (
    id SERIAL PRIMARY KEY,
    sentence_id INTEGER UNIQUE,
    language VARCHAR(10) NOT NULL,
    text TEXT NOT NULL,
    translation_id INTEGER,
    translation_lang VARCHAR(10),
    translation_text TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sentences_lang ON example_sentences(language);
```

---

## 🎯 优先级排序

### 必须（立即集成）
1. ✅ **JMdict** - 日语核心词典
2. ✅ **JLPT词汇** - 难度分级
3. ✅ **Free Dictionary API** - 英语查询
4. ✅ **COCA Top 5000** - 英语词频

### 推荐（近期集成）
5. ⏳ **JMdict-Furigana** - 假名标注
6. ⏳ **WordNet** - 英语语义
7. ⏳ **Tatoeba** - 例句库

### 可选（未来集成）
8. ⏸️ **日语语料库** - 词频统计
9. ⏸️ **Collins词典** - 英语详细释义
10. ⏸️ **成语俗语库** - 惯用表达

---

## 💾 存储空间估算

### 最小配置（约300MB）
- JMdict: 200MB
- JLPT: 5MB
- COCA: 1MB
- 其他: 100MB

### 完整配置（约1.5GB）
- 上述全部
- Tatoeba: 500MB
- WordNet: 20MB
- 汉字数据: 50MB
- 音频文件: 500MB

---

## ⚡ 下一步行动

### 今天可做
1. 下载JMdict JSON版本
2. 下载JLPT词汇CSV
3. 创建导入脚本
4. 测试词典查询

### 本周完成
1. 完整词典集成
2. API查询接口
3. 缓存优化
4. 前端词汇展示

---

## 📚 参考链接

**日语**:
- EDRDG主页: http://www.edrdg.org/
- JMdict文档: http://www.edrdg.org/jmdict/jmdictart.html
- JLPT官网: https://www.jlpt.jp/ (无官方词汇表)

**英语**:
- COCA: https://www.english-corpora.org/coca/
- BNC: https://www.english-corpora.org/bnc/
- Wiktionary: https://en.wiktionary.org/

**多语言**:
- Tatoeba: https://tatoeba.org/
- CC-CEDICT (中英): https://cc-cedict.org/

---

**更新时间**: 2025-11-16
**下次审查**: 集成完成后
