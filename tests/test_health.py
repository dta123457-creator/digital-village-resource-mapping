"""Unit tests for API health endpoints"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_check(self):
        """Test /api/health endpoint"""
        client = TestClient(app)
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "village-resource-mapping-api"
        assert "version" in data
    
    def test_readiness_check(self):
        """Test /api/readiness endpoint"""
        client = TestClient(app)
        response = client.get("/api/readiness")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert "message" in data
