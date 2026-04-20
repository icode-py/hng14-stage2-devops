# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# Runtime stage
FROM python:3.11-slim
# Create non-root user
RUN addgroup --gid 1001 --system appgroup && \
    adduser --uid 1001 --system appuser --gid 1001
WORKDIR /app
# Copy dependencies from builder
COPY --from=builder --chown=appuser:appgroup /install /usr/local/lib/python3.11/site-packages
# Copy application code
COPY --chown=appuser:appuser . .
# Switch to non-root user
USER appuser
# Expose API port
EXPOSE 8000
# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]