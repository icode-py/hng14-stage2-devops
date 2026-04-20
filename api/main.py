from fastapi import FastAPI
import redis
import uuid
import os
os.environ.setdefault("REDIS_HOST", "localhost")
from fastapi.middleware.cors import CORSMiddleware


# Wrap Redis connection in try/except for local testing
try:
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    redis_client.ping()  # Test connection
except:
    print("Warning: Redis not available, running in limited mode")
    redis_client = None

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)
