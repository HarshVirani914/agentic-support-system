# Agentic AI Customer Support System

Multi-agent customer support system using LangGraph for intelligent query handling with Next.js frontend.

## ✅ Iteration 1 Complete - Basic RAG System Working

### Current Features

- ✅ Document ingestion & chunking
- ✅ Vector embeddings (Sentence Transformers)
- ✅ Qdrant vector database integration
- ✅ Groq LLM (Llama 3.3 70B)
- ✅ FastAPI REST API
- ✅ RAG pipeline working end-to-end
- 🚧 LangGraph multi-agent system (Next)

### Progress

- [x] Project setup
- [x] Document ingestion pipeline
- [x] FastAPI backend (basic)
- [ ] Multi-agent system with LangGraph
- [ ] Next.js frontend
- [ ] Deployment

## Tech Stack

**Backend**: Python 3.14, LangChain, LangGraph, FastAPI, Qdrant, Groq, Sentence Transformers  
**Frontend**: Next.js 15, TypeScript, TailwindCSS, shadcn/ui (coming soon)  
**Deployment**: Docker, Render/Fly.io, Vercel

## Quick Start

### Prerequisites

- Python 3.14+
- Qdrant Cloud account (free tier)
- Groq API key (free tier)

### Setup

```bash
# 1. Create virtual environment
python3.14 -m venv venv
source venv/bin/activate

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Ingest documents
python scripts/ingest_docs.py

# 5. Start server
cd backend && ./start_dev.sh # For development server
# or
./start.sh # For production server
```

Response:

```json
{
  "answer": "Our refund policy allows customers to request a full refund...",
  "sources": [{ "text": "...", "score": 0.89 }]
}
```

### Documentation

FastAPI auto-docs: http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── api/routes/     # API endpoints
│   ├── core/           # LLM, embeddings, vector store
│   ├── services/       # RAG pipeline
│   ├── models/         # Pydantic schemas
│   └── config.py       # Settings
├── scripts/            # Utility scripts
└── data/               # Sample documents
```

## Development Roadmap

**Week 1** (Current):

- ✅ Document ingestion
- ✅ Basic RAG system
- ✅ FastAPI endpoints

**Week 2** (Next):

- [ ] LangGraph agent setup
- [ ] Multi-agent orchestration
- [ ] Supervisor agent

**Week 3**:

- [ ] Next.js frontend
- [ ] Agent status UI
- [ ] Deployment

## License

MIT
