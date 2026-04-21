# Agentic AI Customer Support System

Production-ready multi-agent customer support system powered by LangGraph, featuring intelligent query routing, RAG-based answers, and a modern Next.js interface.

## Overview

An intelligent customer support system that uses multiple AI agents to handle different types of queries. The system automatically classifies incoming questions (orders, shipping, general) and routes them to specialized agents for more accurate and contextually relevant responses.

## Key Features

### Backend (Python + FastAPI + LangGraph)

- **Multi-Agent Routing** - Conditional LangGraph workflow with 3 specialized agents
- **Intelligent Classification** - LLM-powered query categorization
- **RAG Pipeline** - Retrieval-Augmented Generation with Qdrant vector database
- **Source Transparency** - Returns citations with relevance scores
- **Error Handling** - Centralized exception management with proper HTTP status codes
- **Structured Logging** - Clean, timestamped logs for debugging
- **LangSmith Tracing** - Full observability of agent execution

### Frontend (Next.js + TypeScript + shadcn/ui)

- **Clean Chat Interface** - Professional messaging UI with role-based styling
- **Category Badges** - Visual indicators for agent routing (Order/Shipping/General)
- **Collapsible Sources** - RAG citations with relevance scores
- **Real-time Updates** - Auto-scroll with manual override
- **Error Handling** - User-friendly error messages
- **Clear Chat** - Reset conversation functionality
- **Sample Questions** - Quick-start prompts for users
- **Responsive Design** - Mobile, tablet, and desktop support

## Architecture

```
User Query
    ↓
[Classifier Agent] - Determines category (order/shipping/general)
    ↓
[Conditional Router] - Routes based on category
    ↓
[Specialized Search Agents]
    ├── Order Search - Enhanced with order-specific keywords
    ├── Shipping Search - Enhanced with shipping-specific keywords
    └── General Search - Broad search for all other queries
    ↓
[Response Generator] - Category-aware answer generation
    ↓
JSON Response (answer + sources + category)
```

## Tech Stack

### Backend

- **Python 3.14** - Core language
- **FastAPI** - REST API framework
- **LangGraph** - Agent orchestration and state management
- **LangChain** - LLM abstractions
- **Groq** - LLM API (Llama 3.3 70B)
- **Qdrant Cloud** - Vector database
- **Sentence Transformers** - Embeddings (all-MiniLM-L6-v2)
- **LangSmith** - Observability and tracing
- **Pydantic** - Data validation

### Frontend

- **Next.js 15** - React framework (App Router)
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **shadcn/ui** - Component library
- **Lucide React** - Icons
- **Inter Font** - Typography

## Project Structure

```
agentic-support-system/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── graph.py              # LangGraph workflow definition
│   │   │   ├── state.py              # Agent state schema
│   │   │   ├── router.py             # Conditional routing logic
│   │   │   └── nodes/
│   │   │       ├── classifier.py     # Query classification
│   │   │       ├── specialized_search.py  # Category-specific search
│   │   │       └── response.py       # Answer generation
│   │   ├── api/routes/               # FastAPI endpoints
│   │   ├── core/
│   │   │   ├── embeddings.py         # Sentence Transformers
│   │   │   ├── vectorstore.py        # Qdrant operations
│   │   │   ├── llm.py                # Groq LLM setup
│   │   │   └── exceptions.py         # Custom exceptions
│   │   ├── models/schemas.py         # Pydantic models
│   │   ├── utils/logger.py           # Logging setup
│   │   ├── config.py                 # Environment config
│   │   └── main.py                   # FastAPI app
│   ├── scripts/
│   │   ├── update_knowledge_base.py  # KB management
│   │   └── visualize_graph.py        # Graph visualization
│   ├── data/
│   │   └── sample_docs.txt           # Knowledge base (97 chunks)
│   └── requirements.txt              # Python dependencies
│
└── frontend/
    ├── app/
    │   ├── layout.tsx                # Root layout
    │   ├── page.tsx                  # Main chat page
    │   └── globals.css               # Global styles
    ├── components/
    │   ├── chat/
    │   │   ├── chat-interface.tsx    # Main chat container
    │   │   └── chat-message.tsx      # Message component
    │   └── ui/                        # shadcn components
    ├── lib/
    │   ├── api.ts                    # Backend API client
    │   ├── types.ts                  # TypeScript interfaces
    │   └── utils.ts                  # Helper functions
    └── package.json
```

## Getting Started

### Prerequisites

- Python 3.14+
- Node.js 18+
- Qdrant Cloud account (free tier)
- Groq API key (free tier)
- LangSmith account (optional, for tracing)
- HuggingFace token (optional, for embeddings)

### Backend Setup

1. **Create virtual environment:**

```bash
python3.14 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

2. **Install dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables:**

```bash
cp .env.example .env
# Edit .env with your API keys:
# - GROQ_API_KEY
# - QDRANT_URL
# - QDRANT_API_KEY
# - LANGCHAIN_API_KEY (optional)
# - HF_TOKEN (optional)
```

4. **Initialize knowledge base:**

```bash
python scripts/update_knowledge_base.py
```

5. **Start backend server:**

```bash
uvicorn app.main:app --reload
```

Backend runs on: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Configure environment:**

```bash
# Create .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Start development server:**

```bash
npm run dev
```

Frontend runs on: `http://localhost:3000`

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

### Chat Endpoint

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is your refund policy?",
    "limit": 3
  }'
```

Response:

```json
{
  "answer": "Our refund policy allows customers to request a full refund within 30 days...",
  "sources": [
    {
      "text": "To request a refund, log into your account...",
      "score": 0.605
    }
  ],
  "category": "order"
}
```

## Knowledge Base Management

### Update Knowledge Base

```bash
cd backend

# Replace entire KB with new content
python scripts/update_knowledge_base.py data/new_docs.txt

# Append to existing KB
python scripts/update_knowledge_base.py data/additional_docs.txt --append

# Clear KB
python scripts/update_knowledge_base.py --clear
```

### Document Format

Knowledge base uses plain text with markdown-style sections:

```
## Section Title

Section content here with detailed information...

## Another Section

More content...
```

Sections are automatically chunked on double newlines (`\n\n`).

## Monitoring and Debugging

### LangSmith Tracing

View detailed execution traces in LangSmith dashboard:

- Query classification decisions
- Agent routing paths
- Search results
- LLM prompts and responses
- Execution time per node

### Backend Logs

Structured logs show the complete workflow:

```
2026-04-17 15:30:45 | INFO | Agent execution started | Question: What is your refund policy?... | Limit: 3
2026-04-17 15:30:46 | INFO | Classifier | Question: 'What is your refund policy?...' | Category: order
2026-04-17 15:30:46 | INFO | Router | Category: order → Node: order_search
2026-04-17 15:30:47 | INFO | Order Search | Found 3 docs | Limit: 3
2026-04-17 15:30:48 | INFO | Response generated | Category: order | Length: 245 chars
2026-04-17 15:30:48 | INFO | Agent execution complete | Category: order | Answer length: 245 chars
```

## Development Iterations

### ✅ Iteration 1: Basic RAG System

- Document ingestion pipeline
- Vector embeddings and storage
- Simple query → retrieve → generate flow
- FastAPI REST API

### ✅ Iteration 2: LangGraph Integration

- Migrated to LangGraph state machine
- Node-based architecture
- Centralized error handling
- Structured logging

### ✅ Iteration 3: Multi-Agent System

- Query classification with LLM
- Conditional routing based on category
- 3 specialized search agents (order, shipping, general)
- Category-aware response generation
- Enhanced query with domain keywords

### ✅ Frontend MVP

- Next.js chat interface
- Real-time messaging
- Category badges
- Collapsible source citations
- Professional UI/UX

### Manual API Tests

```bash
# Test order query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your refund policy?"}'

# Test shipping query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How long does shipping take?"}'

# Test general query
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my password?"}'

# Test with custom limit
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your warranty?", "limit": 5}'
```

## Configuration

### Backend Environment Variables

| Variable               | Description              | Required |
| ---------------------- | ------------------------ | -------- |
| `GROQ_API_KEY`         | Groq API key for LLM     | Yes      |
| `QDRANT_URL`           | Qdrant Cloud URL         | Yes      |
| `QDRANT_API_KEY`       | Qdrant API key           | Yes      |
| `LANGCHAIN_TRACING_V2` | Enable LangSmith tracing | No       |
| `LANGCHAIN_API_KEY`    | LangSmith API key        | No       |
| `LANGCHAIN_PROJECT`    | LangSmith project name   | No       |
| `HF_TOKEN`             | HuggingFace token        | No       |

### Frontend Environment Variables

| Variable              | Description     | Default                 |
| --------------------- | --------------- | ----------------------- |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## Troubleshooting

### Backend Issues

**Problem:** Import errors

```bash
# Ensure venv is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem:** Qdrant connection failed

- Verify `QDRANT_URL` and `QDRANT_API_KEY` in `.env`
- Check Qdrant Cloud dashboard for API status

**Problem:** LangSmith traces not appearing

- Verify `LANGCHAIN_TRACING_V2=true`
- Check `LANGCHAIN_API_KEY` is correct
- Restart backend after updating `.env`

### Frontend Issues

**Problem:** Cannot connect to backend

- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify CORS settings in backend

**Problem:** Build errors

```bash
rm -rf .next
npm run build
```

## Use Cases

- **E-commerce Support** - Orders, refunds, shipping inquiries
- **SaaS Customer Success** - Onboarding, troubleshooting, billing
- **Automotive Support** - Warranty claims, service appointments, parts
- **Enterprise Help Desk** - IT support, HR inquiries, policy questions

## Future Enhancements

- Conversation history with database persistence
- Multi-turn context awareness
- Streaming responses with SSE/WebSocket
- File upload for document ingestion
- Admin dashboard for KB management
- User authentication
- Analytics dashboard
- A/B testing for agent performance

## License

MIT

## Acknowledgments

- [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) for agent orchestration
- [Groq](https://groq.com) for fast LLM inference
- [Qdrant](https://qdrant.tech) for vector search
- [shadcn/ui](https://ui.shadcn.com) for UI components
- [FastAPI](https://fastapi.tiangolo.com) for backend framework

## Links

- Live Demo: https://agentic-support-system.vercel.app/
- API Documentation: `http://localhost:8000/docs` (when running)
