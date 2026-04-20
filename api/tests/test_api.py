from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

# Add parent directory to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


@patch('main.redis_client')
def test_create_job(mock_redis):
    """Test job creation endpoint"""
    mock_redis.lpush.return_value = None
    mock_redis.hset.return_value = None
    job_data = {}
    response = client.post("/jobs", json=job_data)
    assert response.status_code == 200
    assert "job_id" in response.json()


@patch('main.redis_client')
def test_get_job_status(mock_redis):
    """Test job status retrieval"""
    mock_redis.hget.return_value = "completed"
    response = client.get("/jobs/test-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
