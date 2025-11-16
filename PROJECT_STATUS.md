# XBook - 项目状态

**最后更新**: 2025-01-16
**当前阶段**: Phase 1 完成 ✅
**下一阶段**: Phase 2 - 文本处理和分词

---

## 📋 项目概述

XBook 是一个智能外语学习平台，专注于通过阅读和音频同步来提升英语和日语学习效率。

**核心特性**:
- 📖 交互式阅读（点词查询、智能标记）
- 🎵 音频-文本卡拉OK同步
- 📝 智能词汇管理（5级分级系统）
- 🧠 间隔重复记忆（SM-2算法）
- 📊 学习进度可视化

---

## ✅ 已完成工作 (Phase 1)

### 基础设施
- [x] 完整的项目目录结构（前后端分离）
- [x] Docker Compose 多容器编排
  - PostgreSQL 17 数据库
  - Redis 7 缓存
  - FastAPI 后端
  - Next.js 15 前端
- [x] 开发环境一键启动脚本

### 后端 (FastAPI)
- [x] 项目初始化和配置
- [x] 核心模块结构
  - `app/core/` - 配置、数据库、认证
  - `app/api/v1/` - API 路由
  - `app/db/models/` - 数据模型
  - `app/services/` - 业务逻辑
  - `app/schemas/` - Pydantic 模型
- [x] 数据库连接（asyncpg + SQLAlchemy）
- [x] Redis 连接池管理
- [x] JWT 认证基础设施
- [x] 依赖注入系统
- [x] 健康检查端点

### 数据库设计
- [x] 完整的 Schema 设计（11个核心表）
- [x] Alembic 迁移配置
- [x] 索引优化策略
- [x] 全文搜索支持（TSVector）

**核心表**:
1. `users` - 用户账户和偏好
2. `vocabulary` - 词汇数据（字/词/短语）
3. `vocab_cards` - SRS 学习卡片
4. `review_logs` - 复习历史记录
5. `texts` - 电子书/文本库
6. `audio_files` - 音频文件
7. `audio_alignments` - 音频-文本对齐数据
8. `reading_progress` - 阅读进度追踪
9. `user_stats` - 用户学习统计
10. `collocations` - 惯用搭配库
11. `user_collocations` - 用户搭配掌握度

### 前端 (Next.js 15)
- [x] Next.js 15 + App Router 初始化
- [x] TailwindCSS + shadcn/ui 配置
- [x] 完整的主题系统（亮/暗模式）
- [x] 词汇分级配色方案
- [x] TypeScript 配置
- [x] 响应式布局基础
- [x] 首页原型

### 文档
- [x] README（项目介绍）
- [x] GETTING_STARTED（快速开始指南）
- [x] DEVELOPMENT_ROADMAP（开发路线图）
- [x] PROJECT_STATUS（当前文档）

---

## 📁 项目结构

```
xbook/
├── backend/                    # FastAPI 后端 ✅
│   ├── app/
│   │   ├── api/v1/            # API 路由 ✅
│   │   ├── core/              # 核心配置 ✅
│   │   ├── db/models/         # 数据模型 ✅
│   │   ├── services/          # 业务逻辑（待实现）
│   │   └── schemas/           # Pydantic 模型（待实现）
│   ├── alembic/               # 数据库迁移 ✅
│   ├── Dockerfile             ✅
│   ├── requirements.txt       ✅
│   └── .env.example           ✅
│
├── frontend/                   # Next.js 前端 ✅
│   ├── app/                   # App Router ✅
│   ├── components/            # React 组件（待实现）
│   ├── lib/                   # 工具函数 ✅
│   ├── Dockerfile             ✅
│   ├── package.json           ✅
│   └── tailwind.config.ts     ✅
│
├── data/                      # 数据文件 ✅
│   ├── dictionaries/          # 词典数据（待导入）
│   ├── books/                 # 电子书存储
│   └── audio/                 # 音频文件
│
├── deploy/                    # 部署配置 ✅
├── docs/                      # 文档 ✅
├── scripts/                   # 工具脚本 ✅
├── docker-compose.yml         ✅
└── README.md                  ✅
```

---

## 🎯 下一步计划 (Phase 2 - Week 3-4)

### 优先级 1: 文本处理
1. **电子书解析**
   - [ ] EPUB 解析器（PyMuPDF + ebooklib）
   - [ ] PDF 解析器
   - [ ] 文本清理和格式化

2. **日语分词服务**
   - [ ] SudachiPy 集成
   - [ ] API 端点: `POST /api/v1/tokenizer/japanese`
   - [ ] 词形还原
   - [ ] 读音提取（Furigana）

3. **英语分词服务**
   - [ ] spaCy 集成（en_core_web_sm）
   - [ ] API 端点: `POST /api/v1/tokenizer/english`
   - [ ] 词性标注
   - [ ] 词形还原

### 优先级 2: 数据准备
1. **词典数据导入**
   - [ ] JLPT N5-N1 词汇表
   - [ ] 英语词频数据
   - [ ] 常用搭配数据

2. **测试数据**
   - [ ] 准备日语测试文本（EPUB）
   - [ ] 准备英语测试文本（EPUB）
   - [ ] 准备测试音频文件

### 优先级 3: API 开发
- [ ] `POST /api/v1/texts/upload` - 上传电子书
- [ ] `GET /api/v1/texts` - 列出文本
- [ ] `GET /api/v1/texts/{id}` - 获取文本详情
- [ ] `POST /api/v1/tokenizer/japanese` - 日语分词
- [ ] `POST /api/v1/tokenizer/english` - 英语分词

---

## 🚀 快速启动

### 首次设置
```bash
# 1. 运行设置脚本
./scripts/setup.sh

# 2. 启动所有服务
docker compose up -d

# 3. 运行数据库迁移
docker compose exec backend alembic upgrade head

# 4. 查看服务状态
docker compose ps

# 5. 访问应用
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 开发命令
```bash
# 查看日志
docker compose logs -f

# 重启服务
docker compose restart backend

# 停止所有服务
docker compose down

# 进入后端容器
docker compose exec backend bash

# 进入前端容器
docker compose exec frontend sh

# 访问数据库
docker compose exec postgres psql -U xbook_admin -d xbook
```

---

## 📊 技术栈

### 后端
- **框架**: FastAPI 0.115.0
- **数据库**: PostgreSQL 17
- **缓存**: Redis 7
- **ORM**: SQLAlchemy 2.0.36 (async)
- **迁移**: Alembic 1.14.0
- **日语NLP**: SudachiPy 0.6.9
- **英语NLP**: spaCy 3.8.2
- **文档解析**: PyMuPDF 1.24.14, ebooklib 0.18

### 前端
- **框架**: Next.js 15.1.0 (React 19)
- **样式**: TailwindCSS 3.4.1
- **UI组件**: shadcn/ui (Radix UI)
- **状态管理**: Zustand 5.0.2
- **数据获取**: TanStack Query 5.62.7
- **图标**: Lucide React 0.469.0

### 基础设施
- **容器化**: Docker + Docker Compose
- **反向代理**: (待部署时配置 Nginx)
- **CI/CD**: (待配置 GitHub Actions)

---

## 📈 开发进度

### 总体进度: 15%

- **Phase 1**: 基础设施 ████████████████████ 100% ✅
- **Phase 2**: 文本处理 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 3**: 阅读界面 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 4**: 词汇管理 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 5**: 音频同步 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 6**: SRS复习 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 7**: 高级功能 ░░░░░░░░░░░░░░░░░░░░ 0%
- **Phase 8**: 优化完善 ░░░░░░░░░░░░░░░░░░░░ 0%

### 预计完成时间
- **MVP (Phase 1-3)**: 2025年3月中旬（~8周）
- **核心功能完整 (Phase 1-6)**: 2025年5月底（~14周）
- **全部完成 (Phase 1-8)**: 2025年7月中旬（~24周）

---

## 🔧 待解决问题

### 技术决策
1. **翻译服务选择**
   - 选项A: DeepL API（高质量，成本适中）
   - 选项B: Google Translate（广泛支持，价格实惠）
   - 选项C: 离线翻译模型（免费，需本地部署）
   - **推荐**: DeepL 主 + Google 备用

2. **音频对齐工具**
   - 选项A: aeneas（成熟稳定）
   - 选项B: Whisper（AI驱动，高准确度）
   - **推荐**: Whisper（更适合本地部署）

3. **前端状态管理**
   - 已选择: Zustand (轻量级)
   - 服务端状态: TanStack Query

### 数据需求
1. **词典数据源**
   - JLPT: Kaggle 数据集 ✅
   - 英语词频: 待确认具体来源
   - 惯用法: 需要找开源数据集或 API

2. **测试数据**
   - 需要版权友好的测试电子书
   - 需要音频+文本配对的示例

---

## 💡 改进建议

### 短期
1. 完成 Phase 2 的分词服务
2. 实现基本的文本上传和展示
3. 添加单元测试框架

### 中期
1. 实现完整的阅读界面
2. 集成翻译API
3. 实现词汇管理核心功能

### 长期
1. 性能优化（查询缓存、CDN）
2. 移动端App开发
3. 社区功能（分享、讨论）

---

## 📝 备注

### 开发环境
- OS: Linux (WSL2)
- Docker版本: 最新
- Git分支策略: main（生产）+ dev（开发）

### 代码规范
- Python: Black + Ruff
- TypeScript: ESLint + Prettier
- 提交消息: Conventional Commits

### 联系方式
- 项目仓库: (待添加)
- 问题追踪: GitHub Issues
- 文档: `/docs` 目录

---

**上次更新**: 2025-01-16
**下次审查**: Phase 2 完成后
