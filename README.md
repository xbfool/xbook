# XBook - 智能外语学习平台

一个现代化的外语学习工具，专注于通过阅读和音频同步来提升英语和日语学习效率。

## 核心功能

### 📖 交互式阅读
- 支持 EPUB、PDF 电子书导入
- 点击单词/词组即时查询翻译
- 智能分词（日语 SudachiPy、英语 spaCy）
- 5级颜色编码（未知→精通）
- 自动识别惯用法和搭配

### 🎵 音频-文本同步
- 卡拉OK 样式高亮播放
- 自动音频-文本对齐（aeneas）
- 可调播放速度
- 精确到词级别的时间戳

### 📝 智能词汇管理
- 自动收集查询过的词汇
- 熟悉度分级系统
- 上下文保存（原句）
- JLPT/词频等级标注
- 词形变化识别

### 🧠 间隔重复记忆 (SRS)
- SuperMemo SM-2 算法
- 每日智能复习队列
- 闪卡式学习界面
- 学习曲线可视化
- 连续学习天数追踪

## 技术栈

### 后端
- **FastAPI** - 高性能异步 Python 框架
- **PostgreSQL 17** - 主数据库
- **Redis** - 缓存和会话管理
- **SudachiPy** - 日语形态分析
- **spaCy** - 英语 NLP
- **PyMuPDF** - 文档解析
- **aeneas** - 音频对齐

### 前端
- **Next.js 15** - React App Router
- **TailwindCSS** - 样式框架
- **shadcn/ui** - UI 组件库
- **Zustand** - 状态管理
- **React Query** - 服务端状态

### 部署
- **Docker Compose** - 容器化部署
- 支持本地开发和生产环境

## 快速开始

### 前置要求
- Docker 和 Docker Compose
- Node.js 18+ (可选，容器内已包含)
- Python 3.11+ (可选，容器内已包含)

### 启动服务

```bash
# 克隆仓库
git clone <repository-url>
cd xbook

# 启动所有服务（PostgreSQL + Redis + Backend + Frontend）
docker compose up -d

# 查看服务状态
docker compose ps

# 访问应用
# - 前端: http://localhost:3000
# - 后端 API: http://localhost:8000
# - API 文档: http://localhost:8000/docs
```

### 开发模式

```bash
# 后端开发
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 前端开发
cd frontend
npm install
npm run dev
```

## 项目结构

```
xbook/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/v1/            # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── db/models/         # SQLAlchemy 模型
│   │   ├── services/          # 业务逻辑
│   │   │   ├── tokenizer/    # 分词服务
│   │   │   ├── translator/   # 翻译服务
│   │   │   ├── srs/          # SRS 算法
│   │   │   └── audio/        # 音频处理
│   │   └── schemas/           # Pydantic 模型
│   ├── alembic/               # 数据库迁移
│   └── tests/                 # 测试
│
├── frontend/                   # Next.js 前端
│   ├── app/                   # App Router
│   │   ├── reading/          # 阅读界面
│   │   ├── review/           # 复习界面
│   │   ├── library/          # 书库管理
│   │   └── stats/            # 统计面板
│   ├── components/
│   │   ├── reader/           # 阅读器组件
│   │   ├── audio-player/     # 音频播放器
│   │   ├── vocab-card/       # 词汇卡片
│   │   └── ui/               # shadcn 组件
│   └── lib/                   # 工具函数
│
├── data/                      # 数据文件
│   ├── dictionaries/         # 词典数据
│   ├── books/                # 电子书存储
│   └── audio/                # 音频文件
│
├── deploy/                    # 部署配置
├── docs/                      # 文档
└── docker-compose.yml         # Docker 编排
```

## 词汇分级系统

| 级别 | 名称 | 颜色 | 标准 | 复习间隔 |
|------|------|------|------|----------|
| 0 | 未知 | 🔴 红色 | 从未见过 | 立即学习 |
| 1 | 认识 | 🟠 橙色 | 1-2次，<50% | 1天 |
| 2 | 学习中 | 🟡 黄色 | 3-5次，50-70% | 3-6天 |
| 3 | 熟悉 | 🔵 蓝色 | 6-10次，70-90% | 1-2周 |
| 4 | 掌握 | 🟢 绿色 | 10+次，>90% | 1-2月 |
| 5 | 精通 | ⚪ 灰色 | 20+次，100% | 6月+ |

## 数据库表设计

核心表：
- `users` - 用户信息
- `vocabulary` - 词汇库（字/词/词组/惯用法）
- `vocab_cards` - SRS 卡片状态
- `review_logs` - 复习历史记录
- `texts` - 文本/电子书库
- `audio_files` - 音频文件
- `audio_alignments` - 音频-文本对齐数据
- `reading_progress` - 阅读进度
- `user_stats` - 用户学习统计
- `collocations` - 惯用搭配库

## 开发路线图

### Phase 1: 基础设施 ✅
- [x] 项目结构搭建
- [ ] Docker 环境配置
- [ ] 数据库 Schema 设计
- [ ] 用户认证系统

### Phase 2: 文本处理
- [ ] 电子书解析（EPUB/PDF）
- [ ] 日语分词集成
- [ ] 英语分词集成
- [ ] 词典数据导入

### Phase 3: 阅读界面
- [ ] 文本展示组件
- [ ] 点词查询功能
- [ ] 词汇标记和分级
- [ ] 翻译弹窗
- [ ] 惯用法识别

### Phase 4: 词汇管理
- [ ] 词汇 CRUD API
- [ ] 自动收集功能
- [ ] 熟悉度评分
- [ ] 上下文保存

### Phase 5: 音频同步
- [ ] 音频上传管理
- [ ] 强制对齐处理
- [ ] 卡拉OK 播放器
- [ ] 进度控制

### Phase 6: SRS 复习
- [ ] SM-2 算法实现
- [ ] 复习队列生成
- [ ] 闪卡界面
- [ ] 学习统计

### Phase 7: 高级功能
- [ ] 进度仪表盘
- [ ] 连续天数追踪
- [ ] 数据导出
- [ ] 全文搜索

### Phase 8: 优化完善
- [ ] 性能优化
- [ ] UI/UX 打磨
- [ ] 移动端适配
- [ ] PWA 支持
- [ ] 数据备份

## API 文档

启动后端服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 贡献指南

这是一个个人学习工具项目，暂不接受外部贡献。

## 许可证

MIT License

## 作者

个人学习项目

---

**开发周期**: 3-6个月（业余时间）
**最后更新**: 2025-01-16
