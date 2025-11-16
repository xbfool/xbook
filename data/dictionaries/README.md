# 字典数据说明

## 📊 已下载资源

### 日语资源 (约140MB)

#### 1. JMdict - 日英词典
- **文件**:
  - `jmdict/jmdict-eng-common-3.6.1.json` (16MB, 22,567词)
  - `jmdict/jmdict-eng-3.6.1.json` (110MB, 180,000+词)

- **数据结构**:
```json
{
  "id": "1000110",
  "kanji": [{"text": "日本語", "common": true}],
  "kana": [{"text": "にほんご", "common": true}],
  "sense": [{
    "partOfSpeech": ["noun"],
    "gloss": [{"text": "Japanese (language)"}]
  }]
}
```

- **用途**:
  - 词汇查询
  - 获取释义
  - 词性标注

#### 2. JLPT词汇 - 难度分级
- **文件**: `jlpt/term_meta_bank_*.json` (5个文件, 800KB)
- **词条数**: 3,214个

- **数据结构** (Yomichan格式):
```json
["相", "freq", {
  "reading": "あい",
  "frequency": {"value": -1, "displayValue": "N1"}
}]
```

- **用途**:
  - 标记JLPT等级
  - 学习路径规划
  - 难度评估

#### 3. KANJIDIC - 汉字字典
- **文件**: `kanjidic/kanjidic2-en-3.6.1.json` (15MB)
- **汉字数**: 13,000+

- **用途**:
  - 汉字详情
  - 读音信息
  - 笔画数据

### 英语资源 (约682KB)

#### 1. COCA - 词频表
- **文件**: `english/COCA_WordFrequency.csv` (682KB)
- **词条数**: 5,000个高频词

- **数据结构**:
```csv
rank,lemma,PoS,freq,perMil
1,the,a,50033612,50385.16
2,be,v,32394756,32622.71
3,and,c,24778098,24952.20
```

- **字段说明**:
  - rank: 频率排名
  - lemma: 词根
  - PoS: 词性
  - freq: 出现次数
  - perMil: 每百万词出现次数

- **用途**:
  - 标记常用词
  - 优先学习排序
  - 词频统计

## 🚀 使用方式

### 方式1: 直接加载到内存（快速查询）

适用于：实时查询，小数据量

```python
# Python示例
import json

# 加载JMdict常用词
with open('data/dictionaries/jmdict/jmdict-eng-common-3.6.1.json') as f:
    jmdict = json.load(f)

# 查询
def lookup_word(kanji_or_kana):
    for word in jmdict['words']:
        # 匹配汉字
        if any(k['text'] == kanji_or_kana for k in word.get('kanji', [])):
            return word
        # 匹配假名
        if any(k['text'] == kanji_or_kana for k in word.get('kana', [])):
            return word
    return None
```

### 方式2: 导入到PostgreSQL（推荐）

适用于：大规模数据，复杂查询

```sql
-- 创建词典表
CREATE TABLE jmdict_entries (
    id VARCHAR(20) PRIMARY KEY,
    kanji TEXT,
    kana TEXT NOT NULL,
    meaning TEXT,
    pos TEXT,
    is_common BOOLEAN DEFAULT false
);

CREATE INDEX idx_jmdict_kanji ON jmdict_entries(kanji);
CREATE INDEX idx_jmdict_kana ON jmdict_entries(kana);
```

### 方式3: 使用API查询（推荐英语）

```python
# Free Dictionary API (英语)
import httpx

async def lookup_english(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = await httpx.get(url)
    return response.json()
```

## 📝 数据质量

### JMdict
- ✅ 权威来源（EDRDG维护）
- ✅ 定期更新（当前: 2024.11.10）
- ✅ CC-BY-SA许可
- ✅ 多语言支持

### JLPT
- ⚠️ 非官方（无官方JLPT词表）
- ✅ 社区整理
- ✅ 广泛使用
- ✅ 定期更新（2025.08.01）

### COCA
- ✅ 学术语料库
- ✅ 4.5亿词规模
- ✅ 权威词频数据

## 🔧 下一步集成

1. **创建导入脚本** (`scripts/import-dictionaries.py`)
2. **创建词典查询API** (`/api/v1/dictionary/lookup`)
3. **集成到翻译服务** (替换mock翻译)
4. **添加JLPT等级标注** (词汇难度)
5. **词频排序** (学习优先级)

## 💾 存储占用

```
jmdict/    125M  (日语核心词典)
kanjidic/   15M  (汉字字典)
jlpt/      804K  (难度分级)
english/   682K  (词频表)
------------------------
总计:      ~141M
```

## 📚 数据统计

- 日语词条: 22,567 (常用) / 180,000+ (完整)
- JLPT词汇: 3,214
- 汉字: 13,000+
- 英语词频: 5,000

---

**所有数据已准备就绪，可以开始集成！**

下次会话：创建导入脚本，将数据加载到PostgreSQL
