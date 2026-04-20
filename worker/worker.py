import redis
import time
import os
import signal

# Configuration from environment variables
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

# Global flag for graceful shutdown
shutdown_flag = False


def signal_handler(signum, frame):
    """Handle SIGTERM and SIGINT for graceful shutdown"""
    global shutdown_flag
    print(f"Received signal {signum}, shutting down gracefully...")
    shutdown_flag = True


# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)


def connect_redis():
    """Connect to Redis with retry logic"""
    max_retries = 10
    for attempt in range(max_retries):
        try:
            client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                decode_responses=True,
                socket_connect_timeout=5
            )
            client.ping()
            print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
            return client
        except redis.ConnectionError as e:
            print(f"Redis connection attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(3)
            else:
                raise


# Connect to Redis
r = connect_redis()


def process_job(job_id):
    """Process a single job"""
    print(f"Processing job {job_id}")
    r.hset(f"job:{job_id}", "status", "processing")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")


print(f"Worker started, listening on queue: {QUEUE_NAME}")

while not shutdown_flag:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)
        if job:
            _, job_id = job
            process_job(job_id)
    except redis.ConnectionError as e:
        print(f"Redis connection lost: {e}")
        r = connect_redis()  # Reconnect
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(1)

print("Worker shutdown complete")