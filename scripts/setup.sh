#!/bin/bash

# XBook Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up XBook Development Environment"
echo "============================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create environment files from examples
echo ""
echo "📝 Creating environment files..."

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
else
    echo "⏭️  backend/.env already exists"
fi

if [ ! -f frontend/.env.local ]; then
    cp frontend/.env.example frontend/.env.local
    echo "✅ Created frontend/.env.local"
else
    echo "⏭️  frontend/.env.local already exists"
fi

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/books data/audio
mkdir -p data/dictionaries/jlpt data/dictionaries/frequency data/dictionaries/collocations
touch data/books/.gitkeep data/audio/.gitkeep
touch data/dictionaries/jlpt/.gitkeep
touch data/dictionaries/frequency/.gitkeep
touch data/dictionaries/collocations/.gitkeep
echo "✅ Data directories created"

# Pull Docker images
echo ""
echo "🐳 Pulling Docker images..."
docker compose pull

# Build containers
echo ""
echo "🔨 Building containers..."
docker compose build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Review and update backend/.env with your configuration"
echo "2. Review and update frontend/.env.local with your configuration"
echo "3. Run 'docker compose up -d' to start all services"
echo "4. Run 'cd backend && docker compose exec backend alembic upgrade head' to run database migrations"
echo ""
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
