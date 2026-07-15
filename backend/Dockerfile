FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Pre-download the sparse (BM25) and cross-encoder reranker models into the
# image at build time, so cold starts never depend on a live Hugging Face
# download -- which is unreliable on shared-IP hosts like Cloud Run/Render
# (anonymous requests from those IP ranges get rate-limited by HF's API).
# Both models are public/ungated, so no credentials are needed to fetch them.
RUN python -c "\
from fastembed import SparseTextEmbedding; \
SparseTextEmbedding(model_name='Qdrant/bm25'); \
from sentence_transformers import CrossEncoder; \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')"

# Expose port (both Render and Cloud Run inject PORT at runtime)
EXPOSE 8080

# Start command
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
