# XBook Development Roadmap

完整的开发路线图，覆盖 3-6 个月的开发周期。

## Phase 1: 基础设施 (Week 1-2) ✅ COMPLETED

### 已完成
- [x] 项目目录结构搭建
- [x] Docker Compose 环境配置
- [x] FastAPI 后端项目初始化
- [x] Next.js 15 前端项目初始化
- [x] PostgreSQL 数据库设计（11个核心表）
- [x] Alembic 迁移配置
- [x] Redis 缓存配置
- [x] 基础文档（README, Getting Started）

### 核心表结构
1. `users` - 用户信息
2. `vocabulary` - 词汇库
3. `vocab_cards` - SRS 卡片
4. `review_logs` - 复习历史
5. `texts` - 文本库
6. `audio_files` - 音频文件
7. `audio_alignments` - 音频对齐
8. `reading_progress` - 阅读进度
9. `user_stats` - 用户统计
10. `collocations` - 搭配库
11. `user_collocations` - 用户搭配

## Phase 2: 文本处理 (Week 3-4)

### 任务清单
- [ ] EPUB 文件解析（PyMuPDF + ebooklib）
- [ ] PDF 文件解析
- [ ] 纯文本上传支持
- [ ] 日语分词服务（SudachiPy）
  - [ ] 安装和配置
  - [ ] API 端点实现
  - [ ] 词形还原
  - [ ] 读音提取（Furigana）
- [ ] 英语分词服务（spaCy）
  - [ ] 模型下载（en_core_web_sm）
  - [ ] 词性标注
  - [ ] 词形还原
  - [ ] 命名实体识别
- [ ] 文本预处理流程
  - [ ] 清理和格式化
  - [ ] 段落分割
  - [ ] 句子分割
- [ ] JLPT 词汇数据导入
- [ ] 词频数据导入

### API 端点
- `POST /api/v1/texts/upload` - 上传电子书
- `POST /api/v1/tokenizer/japanese` - 日语分词
- `POST /api/v1/tokenizer/english` - 英语分词
- `GET /api/v1/texts/{id}` - 获取文本内容
- `GET /api/v1/texts` - 列出所有文本

## Phase 3: 阅读界面 (Week 5-7)

### 前端组件
- [ ] TextReader 主组件
  - [ ] 文本渲染
  - [ ] 词汇高亮（5级颜色）
  - [ ] 点击选词
  - [ ] 触摸支持（移动端）
- [ ] TranslationPopup 组件
  - [ ] 词典查询显示
  - [ ] 翻译显示
  - [ ] 上下文句子
  - [ ] 添加到词汇库按钮
- [ ] VocabularyMarker 组件
  - [ ] 熟悉度评分
  - [ ] 快速标记（已知/不认识）
  - [ ] 颜色编码更新
- [ ] ReadingProgress 组件
  - [ ] 进度条
  - [ ] 阅读时间追踪
  - [ ] 位置保存

### 后端服务
- [ ] 翻译服务集成
  - [ ] DeepL API（优先）
  - [ ] Google Translate（后备）
  - [ ] 翻译缓存（Redis）
- [ ] 词典查询服务
  - [ ] 离线词典支持
  - [ ] API 词典集成
- [ ] 惯用法识别
  - [ ] n-gram 分析
  - [ ] 搭配数据库查询

### API 端点
- `POST /api/v1/translate` - 翻译文本
- `GET /api/v1/dictionary/{word}` - 词典查询
- `POST /api/v1/vocabulary` - 添加词汇
- `PUT /api/v1/vocabulary/{id}/grade` - 更新熟悉度
- `GET /api/v1/reading/progress/{text_id}` - 获取阅读进度
- `POST /api/v1/reading/progress` - 保存阅读进度

## Phase 4: 词汇管理 (Week 8-9)

### 功能实现
- [ ] 词汇 CRUD 操作
  - [ ] 创建词汇条目
  - [ ] 读取词汇详情
  - [ ] 更新熟悉度
  - [ ] 删除词汇
- [ ] 自动收集功能
  - [ ] 查询即收集
  - [ ] 上下文保存
  - [ ] 首次见到时间
- [ ] 词汇分组
  - [ ] 按语言分组
  - [ ] 按熟悉度分组
  - [ ] 按来源文本分组
  - [ ] 按词性分组
- [ ] 词汇搜索
  - [ ] 全文搜索
  - [ ] 过滤和排序
  - [ ] 批量操作
- [ ] 词汇导出
  - [ ] CSV 格式
  - [ ] JSON 格式
  - [ ] Anki 格式

### 前端页面
- [ ] /vocabulary - 词汇库主页
- [ ] /vocabulary/[id] - 词汇详情页
- [ ] VocabularyList 组件
- [ ] VocabularyFilter 组件
- [ ] VocabularyStats 组件

### API 端点
- `GET /api/v1/vocabulary` - 列出词汇（分页、过滤）
- `GET /api/v1/vocabulary/{id}` - 词汇详情
- `POST /api/v1/vocabulary` - 创建词汇
- `PUT /api/v1/vocabulary/{id}` - 更新词汇
- `DELETE /api/v1/vocabulary/{id}` - 删除词汇
- `GET /api/v1/vocabulary/export` - 导出词汇

## Phase 5: 音频同步 (Week 10-12)

### 音频处理
- [ ] 音频文件上传
  - [ ] MP3 支持
  - [ ] WAV 支持
  - [ ] M4A 支持
- [ ] 音频-文本对齐
  - [ ] aeneas 集成
  - [ ] Whisper 集成（可选）
  - [ ] 对齐数据存储
- [ ] 对齐数据优化
  - [ ] 词级别时间戳
  - [ ] 置信度评分
  - [ ] 手动调整接口

### 前端播放器
- [ ] AudioPlayer 组件
  - [ ] Web Audio API 集成
  - [ ] 播放/暂停
  - [ ] 进度条
  - [ ] 速度调节（0.5x - 2x）
- [ ] KaraokeHighlight 组件
  - [ ] 实时词汇高亮
  - [ ] 平滑过渡动画
  - [ ] 同步准确度优化
- [ ] 播放控制
  - [ ] 单句重复
  - [ ] AB 循环
  - [ ] 跳转到句子

### API 端点
- `POST /api/v1/audio/upload` - 上传音频
- `POST /api/v1/audio/align` - 强制对齐
- `GET /api/v1/audio/{id}/alignment` - 获取对齐数据
- `PUT /api/v1/audio/{id}/alignment` - 更新对齐

## Phase 6: SRS 复习系统 (Week 13-14)

### SM-2 算法实现
- [ ] 核心算法
  - [ ] 计算 Easiness Factor
  - [ ] 计算下次复习间隔
  - [ ] 处理失败（Lapse）
  - [ ] 识别困难卡片（Leech）
- [ ] 复习队列生成
  - [ ] 每日队列
  - [ ] 优先级排序
  - [ ] 新卡片限制
- [ ] 复习统计
  - [ ] 准确率追踪
  - [ ] 学习曲线
  - [ ] 保留率预测

### 前端界面
- [ ] /review - 复习主页
- [ ] FlashCard 组件
  - [ ] 正面（词汇）
  - [ ] 背面（翻译+例句）
  - [ ] 翻转动画
- [ ] ReviewControls 组件
  - [ ] Again (0)
  - [ ] Hard (3)
  - [ ] Good (4)
  - [ ] Easy (5)
- [ ] ReviewStats 组件
  - [ ] 今日进度
  - [ ] 复习数量
  - [ ] 准确率

### API 端点
- `GET /api/v1/reviews/queue` - 获取复习队列
- `POST /api/v1/reviews/{card_id}` - 提交复习结果
- `GET /api/v1/reviews/stats` - 获取复习统计

## Phase 7: 高级功能 (Week 15-18)

### 进度仪表盘
- [ ] /stats - 统计主页
- [ ] 学习统计可视化
  - [ ] 词汇量增长曲线
  - [ ] 每日复习热图
  - [ ] 阅读时间统计
  - [ ] 熟悉度分布
- [ ] 成就系统
  - [ ] 连续学习天数
  - [ ] 里程碑徽章
  - [ ] 学习目标

### 搜索功能
- [ ] 全文搜索（PostgreSQL FTS）
  - [ ] 多语言支持
  - [ ] 相关性排序
  - [ ] 搜索建议
- [ ] 高级过滤
  - [ ] 按难度
  - [ ] 按词性
  - [ ] 按来源

### 数据管理
- [ ] 数据导出
  - [ ] 完整数据导出
  - [ ] 选择性导出
- [ ] 数据导入
  - [ ] CSV 导入
  - [ ] Anki 导入
- [ ] 数据备份
  - [ ] 自动备份
  - [ ] 手动备份

### API 端点
- `GET /api/v1/stats/overview` - 总览统计
- `GET /api/v1/stats/vocabulary` - 词汇统计
- `GET /api/v1/stats/reading` - 阅读统计
- `GET /api/v1/stats/reviews` - 复习统计
- `GET /api/v1/search` - 全局搜索
- `POST /api/v1/export` - 导出数据
- `POST /api/v1/import` - 导入数据

## Phase 8: 优化和完善 (Week 19-24)

### 性能优化
- [ ] 后端优化
  - [ ] 数据库查询优化
  - [ ] 索引优化
  - [ ] 缓存策略优化
  - [ ] API 响应时间优化
- [ ] 前端优化
  - [ ] 代码分割
  - [ ] 懒加载
  - [ ] 图片优化
  - [ ] 包大小优化

### UI/UX 完善
- [ ] 响应式设计完善
- [ ] 暗黑模式支持
- [ ] 键盘快捷键
- [ ] 可访问性（a11y）
  - [ ] ARIA 标签
  - [ ] 键盘导航
  - [ ] 屏幕阅读器支持

### 移动端优化
- [ ] 触摸手势
- [ ] 移动端布局
- [ ] PWA 支持
  - [ ] Service Worker
  - [ ] 离线模式
  - [ ] 安装提示

### 测试
- [ ] 后端测试
  - [ ] 单元测试
  - [ ] 集成测试
  - [ ] API 测试
- [ ] 前端测试
  - [ ] 组件测试
  - [ ] E2E 测试
- [ ] 测试覆盖率 > 80%

### 文档完善
- [ ] API 文档完善
- [ ] 用户手册
- [ ] 开发者指南
- [ ] 部署指南
- [ ] 贡献指南

## 关键指标

### 开发目标
- **总开发周期**: 20-24 周（5-6 个月）
- **代码覆盖率**: > 80%
- **API 响应时间**: < 200ms (p95)
- **前端加载时间**: < 3s (首次)
- **移动端支持**: 完全响应式

### 技术债务
- 定期重构
- 代码审查
- 文档同步更新
- 依赖更新

## 下一步行动

当前 Phase 1 已完成，下一步：

1. **Week 3**: 开始 Phase 2 - 文本处理
   - 实现日语分词服务
   - 实现英语分词服务
   - 创建文本上传 API

2. **准备工作**:
   - 下载 JLPT 词汇数据
   - 准备测试用电子书
   - 准备测试用音频文件

3. **验证环境**:
   ```bash
   # 启动所有服务
   docker compose up -d

   # 检查服务状态
   docker compose ps

   # 运行数据库迁移
   docker compose exec backend alembic upgrade head

   # 访问前端
   open http://localhost:3000

   # 访问 API 文档
   open http://localhost:8000/docs
   ```

## 资源链接

- [Getting Started Guide](./GETTING_STARTED.md)
- [API Documentation](http://localhost:8000/docs)
- [Database Schema](./DATABASE_SCHEMA.md)
- [Architecture Overview](./ARCHITECTURE.md)
