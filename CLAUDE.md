# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Multi-agent customer support system: FastAPI + LangGraph backend (query classification → routed retrieval → RAG answer generation) with a Next.js chat frontend. Live at `agentic-support-system.vercel.app` (frontend) and `agentic-support-system-yile.onrender.com` (backend).

## Commands

### Backend (from `backend/`, with `.venv` activated at repo root)

```bash
source ../.venv/bin/activate       # or use ./start.sh from repo root
pip install -r requirements.txt
cp .env.example .env               # then fill in GROQ_API_KEY, GOOGLE_API_KEY, QDRANT_URL, QDRANT_API_KEY
python scripts/update_knowledge_base.py   # (re)build the Qdrant collection from backend/data/sample_docs.txt
uvicorn app.main:app --reload      # serves on :8000, docs at /docs
```

`backend/tests/` exists but is currently empty — there is no automated test suite to run.

Knowledge base management:
```bash
python scripts/update_knowledge_base.py data/new_docs.txt            # replace KB
python scripts/update_knowledge_base.py data/additional_docs.txt --append
python scripts/update_knowledge_base.py --clear                      # empty the collection
```
KB documents are plain text chunked on blank lines (`\n\n`); `##` headers seed a section's category.

### Frontend (from `frontend/`)

```bash
npm install
npm run dev      # :3000, requires NEXT_PUBLIC_API_URL in .env.local (defaults to http://localhost:8000)
npm run build
npm run lint
```

## Architecture

### Backend agent pipeline (`backend/app/agents/`)

LangGraph `StateGraph` over a single `AgentState` TypedDict (`state.py`: question, limit, category, documents, answer, sources). Flow, defined in `graph.py`:

```
classifier_node → route_by_category (conditional edge) → {order_search | shipping_search | general_search} → generate_node → END
```

- `nodes/classifier.py` — LLM call that assigns `category` (order/shipping/general).
- `router.py` (`route_by_category`) — pure dict lookup from category to the next node name; defaults to `general_search`.
- `nodes/specialized_search.py` — three node functions, each rewriting/expanding the query with domain keywords before hitting the vector store, so retrieval differs per category even though it's the same underlying Qdrant collection.
- `nodes/response.py` (`generate_node`) — category-aware prompt to produce the final answer + source citations.
- `graph.py` also exposes `run_agent(question, limit)`, the single entry point used by the API layer; it builds `initial_state`, invokes the compiled graph, and logs start/end. Any new agent behavior should extend this graph rather than bypassing it.

### Backend core services (`backend/app/core/`)

- `embeddings.py` — `EmbeddingModel` wraps `GoogleGenerativeAIEmbeddings` (`gemini-embedding-2-preview`, forced to 768 dimensions). Despite comments elsewhere referencing Groq/HuggingFace for embeddings, **embeddings are Google Gemini**, not Groq — Groq (`llm.py`) is used only for the classification/generation LLM calls (Llama 3.3 70B).
- `vectorstore.py` — Qdrant Cloud client wrapper; collection name from `settings.COLLECTION_NAME` (default `support_docs`).
- `exceptions.py` — `AppException` + handlers registered globally in `main.py` for consistent error JSON.

### API layer

`app/main.py` wires CORS (from `CORS_ORIGINS` env, comma-separated or `*`), registers exception handlers, and mounts `app/api/routes/chat.py` under `/api`. `POST /api/chat` is the only functional endpoint (`{message, limit}` → `{answer, sources, category}`); `/` and `/health` are health checks.

Config (`app/config.py`) is a single Pydantic `Settings` object read from `backend/.env` (required: `GROQ_API_KEY`, `GOOGLE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`; optional LangSmith tracing vars).

### Frontend (`frontend/`)

Next.js 16 App Router, single-page chat app. `components/chat/chat-interface.tsx` owns conversation state and calls the backend via `lib/api.ts`; `lib/types.ts` mirrors the backend's request/response schemas. UI is shadcn/ui + TailwindCSS v4 (`components/ui/`).

The frontend's own `AGENTS.md`/`CLAUDE.md` (`frontend/CLAUDE.md` → `frontend/AGENTS.md`) flags that this Next.js version has breaking changes from training-data knowledge — check `node_modules/next/dist/docs/` before writing frontend code that touches routing/conventions.

## Repo conventions (from `.cursor/rules/`)

- **MVP-first**: this project's purpose is to demonstrate end-to-end build/deploy skill for job applications, not to be feature-complete. Prefer the smallest working change; skip auth hardening, rate limiting, and elaborate error handling unless asked. Don't add "one more agent" — the 3-agent routing setup is intentionally the ceiling for MVP scope.
- **No unsolicited docs**: don't create or update README/CHANGELOG/other `.md` files unless explicitly requested, and don't append a "Summary of Changes" after finishing a task.
- **Precision edits**: use incremental diffs, stay strictly within the requested scope, don't refactor unrelated code, and don't add comments describing what an edit changed.
- **Backend style** (`*.py`, FastAPI): favor plain functions over classes, `async def` for I/O-bound work, Pydantic models over raw dicts, type hints everywhere, guard-clause/early-return error handling, and the RORO (Receive an Object, Return an Object) pattern for endpoints.
