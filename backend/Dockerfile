# Dockerfile for Render deployment
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Render will set PORT env var)
EXPOSE 10000

# Start command
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
