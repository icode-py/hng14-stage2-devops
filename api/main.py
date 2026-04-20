from fastapi import FastAPI
import redis
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware

# Wrap Redis connection in try/except for local testing
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    redis_client.ping()  # Test connection
    print(f"Connected to Redis at {redis_host}:{redis_port}")
except Exception as e:
    print(f"Warning: Redis not available - {e}")
    redis_client = None

app = FastAPI()

# Add CORS middleware (must be before routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/jobs")
def create_job():
    if redis_client is None:
        return {"error": "Redis unavailable"}

    job_id = str(uuid.uuid4())
    redis_client.lpush("job", job_id)
    redis_client.hset(f"job:{job_id}", "status", "pending")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    if redis_client is None:
        return {"error": "Redis unavailable"}

    status = redis_client.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status}
