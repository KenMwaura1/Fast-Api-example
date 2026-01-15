"""
Tests for the health check endpoint
"""
import pytest
from starlette.testclient import TestClient
from app.main import app
from app.db import database


def test_ping_success(test_app):
    """Test successful health check response"""
    response = test_app.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert data["status"] in ["healthy", "degraded"]


def test_ping_response_schema(test_app):
    """Test that ping response matches expected schema"""
    response = test_app.get("/ping")
    assert response.status_code == 200
    data = response.json()
    
    # Verify response has required fields
    assert isinstance(data["status"], str)
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
