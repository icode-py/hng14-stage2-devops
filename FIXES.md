# FIXES.md - HNG Stage 2 Bug Documentation

## API Service Fixes

### 1. Missing Health Check Endpoint
**File:** `api/main.py`  
**Line:** After line 25 (app initialization)  
**Problem:** No `/health` endpoint exists for Docker HEALTHCHECK or monitoring.  
**Fix:** Added health check endpoint that returns `{"status": "healthy"}`.

### 2. Hardcoded Redis Connection
**File:** `api/main.py`  
**Line:** Line 12 (Redis client initialization)  
**Problem:** Redis host hardcoded to 'localhost', which fails in containerized environments.  
**Fix:** Changed to use environment variables `REDIS_HOST` and `REDIS_PORT` with fallback values.

### 3. Missing CORS Configuration
**File:** `api/main.py`  
**Line:** After FastAPI app initialization  
**Problem:** Frontend running on different port cannot make API calls due to CORS policy.  
**Fix:** Added CORSMiddleware to allow cross-origin requests.

## Worker Service Fixes

### 4. Hardcoded Redis Connection
**File:** `worker/worker.py`
**Line:** 5
**Problem:** `r = redis.Redis(host="localhost", port=6379)` hardcoded to localhost.
**Fix:** Changed to use `REDIS_HOST` and `REDIS_PORT` environment variables with fallback values.

### 5. No Graceful Shutdown
**File:** `worker/worker.py`
**Line:** 14-18 (while loop)
**Problem:** Infinite loop with no way to stop gracefully on SIGTERM.
**Fix:** Added `shutdown_flag` and signal handlers for SIGTERM/SIGINT.

### 6. No Error Handling or Reconnection
**File:** `worker/worker.py`
**Line:** 14-18 (while loop)
**Problem:** Worker crashes if Redis disconnects during operation.
**Fix:** Added `connect_redis()` function with retry logic and reconnection in main loop.

### 7. Unused Imports
**File:** `worker/worker.py`
**Line:** 3-4
**Problem:** `import os` and `import signal` were present but unused.
**Fix:** Now properly used for environment variables and signal handling.

### 8. Missing Production Dockerfile
**File:** `worker/Dockerfile` (new file)
**Problem:** No Dockerfile exists for containerization.
**Fix:** Created multi-stage Dockerfile with non-root user and HEALTHCHECK.

## Frontend Service Fixes

### 9. Hardcoded API URL
**File:** `frontend/app.js`
**Line:** 6
**Problem:** `const API_URL = "http://localhost:8000";` hardcoded, fails in containers.
**Fix:** Changed to `const API_URL = process.env.API_URL || 'http://localhost:8000';`

### 10. Missing Health Check Endpoint
**File:** `frontend/app.js`
**Line:** After line 11
**Problem:** No `/health` endpoint for Docker HEALTHCHECK.
**Fix:** Added `app.get('/health')` returning `{"status":"healthy"}`.

### 11. No Error Handling in Frontend JavaScript
**File:** `frontend/views/index.html`
**Line:** fetch calls (line 28-46)
**Problem:** No try/catch or error handling, poor user experience on API failure.
**Fix:** Added try/catch blocks and error status display.

### 12. Missing Production Dockerfile
**File:** `frontend/Dockerfile` (new file)
**Problem:** No Dockerfile exists for containerization.
**Fix:** Created multi-stage Dockerfile with non-root user and HEALTHCHECK.

### 13. Port Not Configurable
**File:** `frontend/app.js`
**Line:** 24
**Problem:** Port hardcoded to 3000.
**Fix:** Changed to `const PORT = process.env.PORT || 3000;`

### 14. API Redis Client Variable Name Mismatch
**File:** `api/main.py`
**Line:** 23-36
**Problem:** Redis client defined as `redis_client` but referenced as `r` in `create_job()` and `get_job()` functions, causing `NameError`. Also, Redis client was redefined after error handling, losing the try/except protection.
**Fix:** 
- Removed duplicate Redis client initialization
- Changed all `r.lpush()` and `r.hset()` to `redis_client.lpush()` and `redis_client.hset()`
- Added null check for `redis_client` in routes
- Changed initial job status from "queued" to "pending" to match worker expectations
- Moved CORS middleware before route definitions