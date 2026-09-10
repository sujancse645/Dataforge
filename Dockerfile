# ==========================================
# Stage 1: Build the static frontend
# ==========================================
FROM node:20-slim AS frontend-builder

WORKDIR /app/apps/web

# Install dependencies
COPY apps/web/package.json apps/web/package-lock.json ./
RUN npm ci

# Copy web source files (node_modules and .next are excluded by .dockerignore)
COPY apps/web/ ./

# Build Next.js static export (outputs to /app/apps/web/out)
RUN npm run build

# ==========================================
# Stage 2: Python FastAPI backend runtime
# ==========================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=7860

# Create non-root user (Hugging Face Spaces runs as user ID 1000)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy backend engine and API source
COPY --chown=user:user src/ ./src/
COPY --chown=user:user smoke_test.py api_smoke_test.py ./

# Copy compiled static frontend from builder stage
COPY --chown=user:user --from=frontend-builder /app/apps/web/out ./apps/web/out

# Hugging Face Spaces port
EXPOSE 7860

# Start unified FastAPI server on port 7860
CMD ["python", "-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
