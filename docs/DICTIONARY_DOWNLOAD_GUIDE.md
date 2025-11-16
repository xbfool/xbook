# 字典数据下载指南

由于网络限制，请手动下载以下资源。

## 📥 下载清单

### 日语资源

#### 1. JMdict (必需) - 约50MB
**最简单的方法**：
```bash
# 直接访问release页面下载
https://github.com/scriptin/jmdict-simplified/releases/latest

# 下载这两个文件：
- jmdict-eng-common.json (常用词，约25MB)
- jmdict-eng.json (完整版，约50MB)

# 保存到：
/mnt/d/GitHub/xbook/data/dictionaries/jmdict/
```

**或者浏览器下载**：
1. 访问 https://github.com/scriptin/jmdict-simplified/releases
2. 下载最新版的 `jmdict-eng-common.json`
3. 保存到 `data/dictionaries/jmdict/` 目录

#### 2. JLPT词汇 (推荐) - 约5MB
```bash
# 访问并下载zip
https://github.com/stephenmk/jlpt-vocab

# 点击 Code -> Download ZIP
# 解压到：
/mnt/d/GitHub/xbook/data/dictionaries/jlpt/jlpt-vocab/
```

#### 3. KANJIDIC (可选) - 约3MB
```bash
# 下载地址
https://github.com/scriptin/jmdict-simplified/releases/latest

# 下载：
- kanjidic.json

# 保存到：
/mnt/d/GitHub/xbook/data/dictionaries/kanjidic/
```

---

### 英语资源

#### 1. Free Dictionary API (推荐)
**无需下载！直接使用API**
```bash
# 测试
curl https://api.dictionaryapi.dev/api/v2/entries/en/hello
```

#### 2. COCA Top 5000 (推荐) - 约1MB
```bash
# 访问
https://github.com/brucewlee/COCA-WordFrequency

# 下载：
- COCA_5000.txt

# 保存到：
/mnt/d/GitHub/xbook/data/dictionaries/english/
```

---

## 📁 目录结构

下载完成后应该是这样：

```
data/dictionaries/
├── jmdict/
│   ├── jmdict-eng-common.json  (必需)
│   └── jmdict-eng.json          (可选，完整版)
│
├── jlpt/
│   └── jlpt-vocab/
│       ├── data/
│       │   ├── source/
│       │   │   ├── N5.csv
│       │   │   ├── N4.csv
│       │   │   ├── N3.csv
│       │   │   ├── N2.csv
│       │   │   └── N1.csv
│       │   └── ...
│       └── README.md
│
├── kanjidic/
│   └── kanjidic.json            (可选)
│
└── english/
    ├── COCA_5000.txt            (推荐)
    └── api-config.json          (自动生成)
```

---

## ✅ 验证下载

```bash
# 检查文件是否存在
ls -lh data/dictionaries/jmdict/
ls -lh data/dictionaries/jlpt/jlpt-vocab/data/source/
ls -lh data/dictionaries/english/

# 查看文件大小
du -sh data/dictionaries/*
```

---

## 🔧 下次会话

下载完成后，下次可以：

1. **导入JMdict到数据库**
   - 创建dictionary表
   - 批量导入JSON数据
   - 建立索引

2. **导入JLPT词汇**
   - 读取CSV文件
   - 标注难度等级
   - 关联到vocabulary表

3. **集成词典查询**
   - 实现查询API
   - 替换mock翻译
   - 添加缓存

---

## 📝 备注

- JMdict数据每周更新，建议下载最新版
- JLPT词汇无官方列表，这些是社区整理
- 所有资源都是开源免费
- 不需要API key

---

**下次会话准备好这些文件，我们就可以继续集成了！**
