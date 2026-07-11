"""Unit tests for resource endpoints"""

import pytest
from fastapi.testclient import TestClient
from app.api.main import app
from app.models.resource import Resource
from sqlalchemy.orm import Session


class TestResourceEndpoints:
    """Test resource CRUD endpoints"""
    
    @pytest.fixture
    def sample_resource_data(self):
        """Sample resource for testing"""
        return {
            "name": "Test School",
            "resource_type": "School",
            "latitude": 20.593,
            "longitude": 78.963,
            "status": "Active",
            "description": "Test description"
        }
    
    def test_list_resources(self):
        """Test GET /resources/"""
        client = TestClient(app)
        response = client.get("/api/resources/")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_create_resource(self, sample_resource_data):
        """Test POST /resources/"""
        client = TestClient(app)
        response = client.post("/api/resources/", json=sample_resource_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_resource_data["name"]
        assert data["resource_type"] == sample_resource_data["resource_type"]
        assert "id" in data
    
    def test_get_resource(self, sample_resource_data):
        """Test GET /resources/{id}"""
        client = TestClient(app)
        
        # Create resource first
        create_response = client.post("/api/resources/", json=sample_resource_data)
        resource_id = create_response.json()["id"]
        
        # Get resource
        response = client.get(f"/api/resources/{resource_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == resource_id
        assert data["name"] == sample_resource_data["name"]
    
    def test_update_resource(self, sample_resource_data):
        """Test PUT /resources/{id}"""
        client = TestClient(app)
        
        # Create resource
        create_response = client.post("/api/resources/", json=sample_resource_data)
        resource_id = create_response.json()["id"]
        
        # Update resource
        update_data = sample_resource_data.copy()
        update_data["name"] = "Updated School"
        
        response = client.put(f"/api/resources/{resource_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated School"
    
    def test_delete_resource(self, sample_resource_data):
        """Test DELETE /resources/{id}"""
        client = TestClient(app)
        
        # Create resource
        create_response = client.post("/api/resources/", json=sample_resource_data)
        resource_id = create_response.json()["id"]
        
        # Delete resource
        response = client.delete(f"/api/resources/{resource_id}")
        
        assert response.status_code == 204
    
    def test_invalid_coordinates(self):
        """Test validation of invalid coordinates"""
        client = TestClient(app)
        
        invalid_data = {
            "name": "Test",
            "resource_type": "School",
            "latitude": 91,  # Invalid
            "longitude": 78.963,
            "status": "Active"
        }
        
        response = client.post("/api/resources/", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
