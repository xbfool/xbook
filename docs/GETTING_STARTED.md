# Getting Started with XBook

This guide will help you set up and run XBook on your local machine.

## Prerequisites

- Docker and Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+, PostgreSQL 17, Redis 7

## Quick Start with Docker (Recommended)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd xbook

# Run setup script
./scripts/setup.sh
```

### 2. Start Services

```bash
# Start all services in background
docker compose up -d

# View logs
docker compose logs -f

# Check service status
docker compose ps
```

### 3. Run Database Migrations

```bash
# Access backend container and run migrations
docker compose exec backend alembic upgrade head
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy English model
python -m spacy download en_core_web_sm

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### Database Setup

```bash
# Install PostgreSQL 17
# Create database
createdb xbook

# Install Redis
# Start Redis server
redis-server
```

## Configuration

### Backend Configuration

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://xbook_admin:password@localhost:5432/xbook
REDIS_URL=redis://:password@localhost:6379/0
SECRET_KEY=your-secret-key-here
```

### Frontend Configuration

Edit `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## First Steps

### 1. Create a User Account

For now, you'll need to create a user directly in the database:

```bash
docker compose exec postgres psql -U xbook_admin -d xbook

INSERT INTO users (email, username, hashed_password, native_language, target_languages)
VALUES (
    'user@example.com',
    'testuser',
    'hashed_password_here',  -- Use bcrypt to hash your password
    'zh',
    ARRAY['en', 'ja']
);
```

### 2. Upload Your First Book

- Navigate to http://localhost:3000/library
- Click "Upload Book"
- Select an EPUB or PDF file
- The system will process and tokenize the text

### 3. Start Reading

- Click on any text to start reading
- Click words to look up translations
- Mark words as known/unknown
- Build your vocabulary automatically

### 4. Review Vocabulary

- Navigate to http://localhost:3000/review
- Practice your vocabulary with spaced repetition
- Track your progress

## Development Workflow

### Backend Development

```bash
# Run tests
cd backend
pytest

# Format code
black app/
ruff check app/

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```

### Frontend Development

```bash
# Run type checking
npm run type-check

# Lint code
npm run lint

# Build for production
npm run build
```

### Docker Development

```bash
# Rebuild containers after code changes
docker compose build

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend

# Restart specific service
docker compose restart backend

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```

## Troubleshooting

### Port Already in Use

If ports 3000, 5432, 6379, or 8000 are already in use:

```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker compose ps postgres

# View PostgreSQL logs
docker compose logs postgres

# Access PostgreSQL directly
docker compose exec postgres psql -U xbook_admin -d xbook
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker compose ps redis

# Test Redis connection
docker compose exec redis redis-cli ping
```

### Python Dependencies Issues

```bash
# Rebuild backend container
docker compose build backend

# Or manually install in container
docker compose exec backend pip install -r requirements.txt
```

## Next Steps

- Read the [Architecture Documentation](./ARCHITECTURE.md)
- Explore the [API Documentation](http://localhost:8000/docs)
- Check the [Database Schema](./DATABASE_SCHEMA.md)
- Learn about [Vocabulary Grading System](./VOCABULARY_GRADING.md)

## Getting Help

- Check the [FAQ](./FAQ.md)
- Review [Common Issues](./COMMON_ISSUES.md)
- Check GitHub Issues

## License

MIT License - See LICENSE file for details
