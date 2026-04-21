# Backend - Agentic AI Customer Support System

FastAPI backend with LangGraph multi-agent system for intelligent customer support.

## Architecture

Multi-agent system with conditional routing:

```
Query → Classifier → Router → Specialized Search → Response Generator → JSON
```

### Agent Workflow

1. **Classifier Node** - Categorizes query (order/shipping/general)
2. **Router** - Conditional edges route to specialized agent
3. **Specialized Search** - Category-optimized document retrieval
4. **Response Generator** - Category-aware answer with sources

## Quick Start

```bash
# Activate virtual environment
source ../.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env file
cp .env.example .env
# Add your API keys

# Initialize knowledge base
python scripts/update_knowledge_base.py

# Start server
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

## API Endpoints

### POST /api/chat
Process a customer support query.

**Request:**
```json
{
  "message": "What is your refund policy?",
  "limit": 3
}
```

**Response:**
```json
{
  "answer": "Our refund policy allows...",
  "sources": [
    {
      "text": "To request a refund...",
      "score": 0.605
    }
  ],
  "category": "order"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

## Core Components

### Agent System (`app/agents/`)

**graph.py** - LangGraph workflow definition
- Creates state graph with nodes
- Defines conditional routing
- Compiles executable workflow

**state.py** - Shared state schema
- TypedDict defining data flow
- Question, category, documents, answer, sources

**router.py** - Conditional routing logic
- Maps categories to specialized nodes
- Returns next node name for LangGraph

**nodes/** - Individual agent nodes
- `classifier.py` - Query categorization
- `specialized_search.py` - Category-specific retrieval
- `response.py` - Answer generation

### Core Services (`app/core/`)

**embeddings.py** - Text embeddings
- Sentence Transformers (all-MiniLM-L6-v2)
- 384-dimensional vectors

**vectorstore.py** - Qdrant operations
- Collection management
- Document upsert
- Similarity search

**llm.py** - LLM initialization
- ChatGroq (Llama 3.3 70B)
- Temperature and API key config

**exceptions.py** - Custom exceptions
- VectorSearchError
- LLMError
- DocumentNotFoundError
- InvalidInputError

### API Layer (`app/api/`)

**routes/chat.py** - Chat endpoint
- Input validation
- Agent execution
- Response serialization

### Configuration (`app/config.py`)

Pydantic Settings for environment management:
- LLM API credentials
- Vector database connection
- LangSmith tracing config
- API server settings

## Scripts

### update_knowledge_base.py
Manage knowledge base documents:
```bash
python scripts/update_knowledge_base.py                    # Replace KB
python scripts/update_knowledge_base.py --append           # Append to KB
python scripts/update_knowledge_base.py --clear            # Clear KB
python scripts/update_knowledge_base.py data/custom.txt    # Use custom file
```

### visualize_graph.py
Print LangGraph workflow structure:
```bash
python scripts/visualize_graph.py
```

## Environment Variables

Required:
- `GROQ_API_KEY` - Groq API key
- `QDRANT_URL` - Qdrant Cloud URL
- `QDRANT_API_KEY` - Qdrant API key

Optional:
- `LANGCHAIN_TRACING_V2=true` - Enable LangSmith
- `LANGCHAIN_API_KEY` - LangSmith API key
- `LANGCHAIN_PROJECT` - LangSmith project name
- `HF_TOKEN` - HuggingFace token (suppresses warning)
- `API_HOST=0.0.0.0` - Server host
- `API_PORT=8000` - Server port
- `ENVIRONMENT=development` - Environment mode

## Development

### Adding New Agent Nodes

1. Create node function in `app/agents/nodes/`:
```python
def new_node(state: AgentState) -> dict:
    # Process state
    return {"field": "value"}
```

2. Register in `graph.py`:
```python
workflow.add_node("new_node", new_node)
workflow.add_edge("previous_node", "new_node")
```

### Adding New Categories

1. Update classifier prompt in `classifier.py`
2. Add new search node in `specialized_search.py`
3. Update router in `router.py`
4. Update state schema if needed

## Testing

### API Testing
```bash
# Use test script
bash scripts/test_api.sh

# Or curl directly
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test question"}'
```

### Error Testing
```bash
# Empty message (should return 400)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'

# Invalid limit (should return 400)
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "limit": 20}'
```

## Deployment Considerations

### Environment Variables in Production
- Use secrets management (Railway secrets, Render env vars)
- Never commit `.env` file
- Update CORS origins to specific domains

### Database
- Qdrant Cloud free tier supports up to 1GB
- Consider upgrading for production scale
- Implement backup strategy

### Monitoring
- Enable LangSmith for production traces
- Set up error alerting
- Monitor API response times
- Track category distribution

## Troubleshooting

### Common Issues

**Import errors:**
```bash
source ../.venv/bin/activate
cd backend
python -c "import app.main"
```

**Qdrant connection failed:**
- Verify credentials in `.env`
- Check Qdrant Cloud dashboard
- Test connection: `python -c "from app.core.vectorstore import vector_store; print(vector_store.client.get_collections())"`

**LLM errors:**
- Verify Groq API key
- Check rate limits (free tier: 30 requests/min)
- Monitor Groq dashboard

## Performance Optimization

Current optimizations:
- Qdrant vector search (< 100ms)
- Groq LLM (fastest inference available)
- Efficient document chunking
- Query enhancement for better retrieval

Potential improvements:
- Caching frequent queries
- Batch document ingestion
- Async document processing
- Response streaming

## Security

- API key validation
- Input sanitization
- CORS configuration
- Rate limiting (implement for production)
- No sensitive data in logs

## Code Quality

- Type hints throughout
- Pydantic validation
- Centralized error handling
- Structured logging
- Clean, readable code
- No unnecessary comments

## License

MIT
