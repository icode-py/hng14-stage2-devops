# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# Runtime stage
FROM python:3.11-slim
# Install procps for pgrep command with pinned versions and no-install-recommends
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    procps=2:4.0.2-3 \
    && rm -rf /var/lib/apt/lists/*
# Create non-root user
RUN addgroup --gid 1002 --system appgroup && \
    adduser --uid 1002 --system appuser --gid 1002
WORKDIR /app
# Copy dependencies from builder
COPY --from=builder --chown=appuser:appgroup /install /usr/local/lib/python3.11/site-packages
# Copy application code
COPY --chown=appuser:appuser . .
# Switch to non-root user
USER appuser
# Health check - verify process is running
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD pgrep -f "python.*worker.py" || exit 1
# Run the worker
CMD ["python", "-u", "worker.py"]