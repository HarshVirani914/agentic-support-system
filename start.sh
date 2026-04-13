#!/bin/bash

echo "🚀 Starting Agentic Support System API"
echo "======================================"
echo ""

# Activate virtual environment
source .venv/bin/activate

# Navigate to backend
cd backend

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found in backend/"
    echo "   Copy .env.example to .env and add your API keys"
    exit 1
fi

# Start server
echo "Starting FastAPI server..."
echo "API: http://localhost:8000"
echo "Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
