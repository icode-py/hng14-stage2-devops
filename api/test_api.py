import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
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
    mock_redis.incr.return_value = 1
    job_data = {"type": "test", "data": "sample"}
    response = client.post("/jobs", json=job_data)
    assert response.status_code == 201
    assert "id" in response.json()
    mock_redis.hset.assert_called_once()

@patch('main.redis_client')
def test_get_job_status(mock_redis):
    """Test job status retrieval"""
    mock_redis.hgetall.return_value = {"status": "completed", "result": "success"}
    response = client.get("/jobs/1")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"