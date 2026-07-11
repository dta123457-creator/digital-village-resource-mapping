"""Unit tests for geospatial utilities"""

import pytest
from app.utils.geo import GeoAnalyzer


class TestGeoAnalyzer:
    """Test geospatial utilities"""
    
    def test_calculate_distance(self):
        """Test distance calculation"""
        # Two points in India
        lat1, lon1 = 20.593, 78.963  # Indore
        lat2, lon2 = 20.595, 78.965
        
        distance = GeoAnalyzer.calculate_distance(lat1, lon1, lat2, lon2)
        
        assert distance > 0
        assert distance < 1  # Very close points
    
    def test_find_nearest_resources(self):
        """Test finding nearest resources"""
        center_lat, center_lon = 20.593, 78.963
        
        resources = [
            {"id": 1, "name": "R1", "latitude": 20.593, "longitude": 78.963},
            {"id": 2, "name": "R2", "latitude": 20.595, "longitude": 78.965},
            {"id": 3, "name": "R3", "latitude": 20.600, "longitude": 78.970},
        ]
        
        nearest = GeoAnalyzer.find_nearest_resources(center_lat, center_lon, resources, k=2)
        
        assert len(nearest) == 2
        assert nearest[0]["id"] == 1  # Closest
    
    def test_calculate_coverage(self):
        """Test coverage calculation"""
        resources = [
            {"latitude": 20.593, "longitude": 78.963},
            {"latitude": 20.595, "longitude": 78.965},
        ]
        
        area_bounds = (20.590, 20.600, 78.960, 78.970)
        
        coverage = GeoAnalyzer.calculate_coverage(resources, area_bounds)
        
        assert 0 <= coverage <= 100
        assert coverage == 100  # All in bounds
