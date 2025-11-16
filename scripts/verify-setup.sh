#!/bin/bash

# XBook Setup Verification Script
# Verifies that all components are properly configured

echo "🔍 XBook Setup Verification"
echo "============================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success_count=0
fail_count=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((success_count++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((fail_count++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Docker
echo "Checking prerequisites..."
if command -v docker &> /dev/null; then
    check_pass "Docker is installed"
else
    check_fail "Docker is not installed"
fi

if command -v docker compose &> /dev/null; then
    check_pass "Docker Compose is installed"
else
    check_fail "Docker Compose is not installed"
fi

# Check directory structure
echo ""
echo "Checking directory structure..."

dirs=(
    "backend/app"
    "backend/alembic"
    "frontend/app"
    "frontend/components"
    "data/books"
    "data/audio"
    "data/dictionaries"
    "deploy"
    "docs"
    "scripts"
)

for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        check_pass "Directory exists: $dir"
    else
        check_fail "Directory missing: $dir"
    fi
done

# Check essential files
echo ""
echo "Checking essential files..."

files=(
    "docker-compose.yml"
    "backend/requirements.txt"
    "backend/Dockerfile"
    "backend/app/main.py"
    "backend/alembic.ini"
    "frontend/package.json"
    "frontend/Dockerfile"
    "frontend/tsconfig.json"
    "README.md"
    ".gitignore"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        check_pass "File exists: $file"
    else
        check_fail "File missing: $file"
    fi
done

# Check environment files
echo ""
echo "Checking environment configuration..."

if [ -f "backend/.env" ]; then
    check_pass "backend/.env exists"
else
    check_warn "backend/.env not found (run ./scripts/setup.sh to create from example)"
fi

if [ -f "frontend/.env.local" ]; then
    check_pass "frontend/.env.local exists"
else
    check_warn "frontend/.env.local not found (run ./scripts/setup.sh to create from example)"
fi

# Check if Docker containers are running
echo ""
echo "Checking Docker containers..."

if docker compose ps | grep -q "postgres"; then
    if docker compose ps | grep postgres | grep -q "Up"; then
        check_pass "PostgreSQL container is running"
    else
        check_warn "PostgreSQL container exists but is not running"
    fi
else
    check_warn "PostgreSQL container not found (run 'docker compose up -d' to start)"
fi

if docker compose ps | grep -q "redis"; then
    if docker compose ps | grep redis | grep -q "Up"; then
        check_pass "Redis container is running"
    else
        check_warn "Redis container exists but is not running"
    fi
else
    check_warn "Redis container not found (run 'docker compose up -d' to start)"
fi

if docker compose ps | grep -q "backend"; then
    if docker compose ps | grep backend | grep -q "Up"; then
        check_pass "Backend container is running"
    else
        check_warn "Backend container exists but is not running"
    fi
else
    check_warn "Backend container not found (run 'docker compose up -d' to start)"
fi

if docker compose ps | grep -q "frontend"; then
    if docker compose ps | grep frontend | grep -q "Up"; then
        check_pass "Frontend container is running"
    else
        check_warn "Frontend container exists but is not running"
    fi
else
    check_warn "Frontend container not found (run 'docker compose up -d' to start)"
fi

# Summary
echo ""
echo "============================"
echo "Verification Summary"
echo "============================"
echo -e "${GREEN}Passed: $success_count${NC}"
echo -e "${RED}Failed: $fail_count${NC}"
echo ""

if [ $fail_count -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Start services: docker compose up -d"
    echo "2. Run migrations: docker compose exec backend alembic upgrade head"
    echo "3. Access frontend: http://localhost:3000"
    echo "4. Access API docs: http://localhost:8000/docs"
else
    echo -e "${RED}❌ Some checks failed. Please review the errors above.${NC}"
    exit 1
fi
