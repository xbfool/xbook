# 单用户配置说明

由于 XBook 是为个人使用设计的，我们简化了用户认证流程。

## 配置说明

### 方式 1: 跳过认证（推荐用于本地开发）

在本地部署时，可以完全跳过用户认证：

1. **后端配置**

编辑 `backend/.env`，添加：

```env
# 单用户模式（跳过认证）
SINGLE_USER_MODE=true
DEFAULT_USER_ID=00000000-0000-0000-0000-000000000001
```

2. **创建默认用户**

首次启动后，运行以下命令创建默认用户：

```bash
docker compose exec backend python -c "
from app.db.models import User
from app.core.database import AsyncSessionLocal
from app.core.security import get_password_hash
import asyncio

async def create_default_user():
    async with AsyncSessionLocal() as db:
        user = User(
            id='00000000-0000-0000-0000-000000000001',
            email='me@localhost',
            username='me',
            hashed_password=get_password_hash('not-needed'),
            native_language='zh',
            target_languages=['en', 'ja']
        )
        db.add(user)
        await db.commit()
        print('✅ Default user created!')

asyncio.run(create_default_user())
"
```

3. **前端配置**

在前端，所有请求将自动使用默认用户ID，无需登录。

### 方式 2: 数据库直接插入（更简单）

启动服务后，直接在数据库中插入用户：

```bash
# 进入数据库
docker compose exec postgres psql -U xbook_admin -d xbook

# 插入默认用户（复制粘贴以下 SQL）
INSERT INTO users (
    id,
    email,
    username,
    hashed_password,
    native_language,
    target_languages,
    settings
) VALUES (
    '00000000-0000-0000-0000-000000000001',
    'me@localhost',
    'me',
    '$2b$12$dummy_hash_not_used_in_single_user_mode',
    'zh',
    ARRAY['en', 'ja']::varchar[],
    '{}'::jsonb
);

# 退出
\q
```

### 方式 3: 使用迁移脚本（自动化）

创建 Alembic 迁移来自动创建默认用户：

```bash
# 创建新迁移
docker compose exec backend alembic revision -m "add_default_user"
```

在生成的迁移文件中添加：

```python
def upgrade():
    # 创建默认用户
    op.execute("""
        INSERT INTO users (
            id, email, username, hashed_password,
            native_language, target_languages, settings
        ) VALUES (
            '00000000-0000-0000-0000-000000000001',
            'me@localhost',
            'me',
            '$2b$12$dummy',
            'zh',
            ARRAY['en', 'ja']::varchar[],
            '{}'::jsonb
        ) ON CONFLICT (id) DO NOTHING;
    """)

def downgrade():
    op.execute("DELETE FROM users WHERE id = '00000000-0000-0000-0000-000000000001';")
```

然后运行：

```bash
docker compose exec backend alembic upgrade head
```

## 简化的 API 使用

### 不需要认证的端点

由于是单用户模式，所有 API 端点都不需要 JWT token：

```bash
# 直接调用 API，无需 Authorization header
curl http://localhost:8000/api/v1/vocabulary

# 创建词汇
curl -X POST http://localhost:8000/api/v1/vocabulary \
  -H "Content-Type: application/json" \
  -d '{
    "surface_form": "走る",
    "dictionary_form": "走る",
    "language": "ja",
    "translations": [{"lang": "zh", "text": "跑"}]
  }'
```

### 前端自动注入用户ID

前端会自动在所有请求中注入默认用户ID：

```typescript
// lib/api.ts
const DEFAULT_USER_ID = '00000000-0000-0000-0000-000000000001';

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    'X-User-ID': DEFAULT_USER_ID,  // 自动注入用户ID
  },
});
```

## 后端中间件（自动处理）

在后端添加一个简单的中间件来处理单用户模式：

```python
# app/api/deps.py
from typing import Optional
from fastapi import Header
from uuid import UUID

DEFAULT_USER_ID = UUID('00000000-0000-0000-0000-000000000001')

async def get_current_user_id(
    x_user_id: Optional[str] = Header(None)
) -> UUID:
    """获取当前用户ID（单用户模式直接返回默认ID）"""
    return DEFAULT_USER_ID
```

## 优势

单用户模式的优势：

1. **无需登录** - 打开就用，零摩擦
2. **简化开发** - 不需要实现复杂的认证流程
3. **性能更好** - 跳过 JWT 验证
4. **数据纯净** - 所有数据都是你自己的
5. **隐私保护** - 本地部署，数据不出本机

## 安全考虑

由于是本地个人使用：

- ✅ 不需要密码强度验证
- ✅ 不需要 JWT token 刷新
- ✅ 不需要会话管理
- ✅ 不需要权限控制
- ✅ 不需要防止 CSRF
- ✅ 不需要速率限制

## 未来扩展

如果将来需要支持多用户，可以轻松添加认证：

1. 将 `SINGLE_USER_MODE` 设为 `false`
2. 实现 JWT 认证中间件
3. 添加登录/注册页面
4. 前端添加 token 管理

但现在，享受简单的单用户体验就好！🎉

## 推荐配置

**backend/.env**:
```env
SINGLE_USER_MODE=true
DEFAULT_USER_ID=00000000-0000-0000-0000-000000000001

# 其他配置保持不变
DATABASE_URL=postgresql://xbook_admin:xbook_dev_password_change_in_production@postgres:5432/xbook
REDIS_URL=redis://:xbook_redis_password@redis:6379/0
```

**前端自动配置** - 无需手动设置

就这么简单！
