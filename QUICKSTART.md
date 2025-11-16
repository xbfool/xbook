# XBook 快速启动指南

5分钟快速上手指南

## 前置要求

- Docker 和 Docker Compose
- Git

## 三步启动

### 1️⃣ 克隆并设置

```bash
# 进入项目目录（如果还没有克隆）
cd /mnt/d/GitHub/xbook

# 运行自动设置脚本
./scripts/setup.sh

# 验证设置（可选）
./scripts/verify-setup.sh
```

### 2️⃣ 启动所有服务

```bash
# 启动 PostgreSQL + Redis + Backend + Frontend
docker compose up -d

# 查看启动日志
docker compose logs -f
```

等待所有服务启动完成（约30秒）

### 3️⃣ 初始化数据库

```bash
# 运行数据库迁移，创建所有表
docker compose exec backend alembic upgrade head
```

## 访问应用

现在你可以访问：

- 🎨 **前端界面**: http://localhost:3000
- 🚀 **API后端**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs
- 📖 **备用文档**: http://localhost:8000/redoc

## 验证安装

```bash
# 检查所有服务是否运行
docker compose ps

# 应该看到 4 个服务都是 "Up" 状态:
# - xbook-postgres
# - xbook-redis
# - xbook-backend
# - xbook-frontend

# 测试 API
curl http://localhost:8000/health

# 应该返回:
# {"status":"healthy","service":"XBook","version":"0.1.0","environment":"development"}
```

## 常用命令

```bash
# 查看所有日志
docker compose logs -f

# 查看特定服务日志
docker compose logs -f backend
docker compose logs -f frontend

# 重启服务
docker compose restart backend

# 停止所有服务
docker compose down

# 停止并删除所有数据（⚠️ 谨慎使用）
docker compose down -v

# 进入后端容器
docker compose exec backend bash

# 进入数据库
docker compose exec postgres psql -U xbook_admin -d xbook
```

## 下一步

现在基础设施已经就绪，你可以：

1. **阅读开发文档**: `docs/DEVELOPMENT_ROADMAP.md`
2. **查看项目状态**: `PROJECT_STATUS.md`
3. **开始开发**: Phase 2 - 文本处理和分词
4. **探索 API**: http://localhost:8000/docs

## 遇到问题？

### 端口被占用

如果提示端口被占用，编辑 `docker-compose.yml` 修改端口映射：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 改用 8001 端口
```

### 数据库连接失败

```bash
# 检查 PostgreSQL 日志
docker compose logs postgres

# 重启数据库
docker compose restart postgres

# 等待几秒后重试
```

### 前端构建失败

```bash
# 重新构建前端
docker compose build frontend

# 重启前端
docker compose restart frontend
```

## 技术支持

- 📖 完整文档: `docs/GETTING_STARTED.md`
- 🐛 问题报告: GitHub Issues
- 💬 讨论: GitHub Discussions

---

祝你使用愉快！🎉
