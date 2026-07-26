# ============================================================
# Dockerfile — HuggingFace Spaces (FastAPI Backend)
# ============================================================
# This runs the FastAPI + LangGraph + Guardrails backend.
# Deploy on HuggingFace Spaces as a "Docker" space.
# ============================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker caches this layer)
COPY requirements-backend.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (only the app/ package is needed at runtime)
COPY app/ ./app/

# HuggingFace Spaces requires port 7860
ENV PORT=7860

# Expose the port
EXPOSE 7860

# Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
