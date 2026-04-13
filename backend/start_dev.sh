#!/bin/bash

# Quick dev server startup from backend directory

echo "🚀 Starting Development Server"
echo ""

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Copy .env.example to .env and add your API keys"
    exit 1
fi

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
    source ../.venv/bin/activate
fi

echo "✅ Virtual environment: $VIRTUAL_ENV"
echo "✅ Python: $(python --version)"
echo ""
echo "Starting uvicorn..."
echo "📡 API: http://localhost:8000"
echo "📚 Docs: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
