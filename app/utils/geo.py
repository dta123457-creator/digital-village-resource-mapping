"""
Geospatial analysis utilities
"""

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class GeoAnalyzer:
    """Geospatial analysis utilities"""
    
    @staticmethod
    def buffer_point(lat: float, lon: float, radius_km: float) -> box:
        """Create buffer around point
        
        Args:
            lat: Latitude
            lon: Longitude
            radius_km: Radius in kilometers
            
        Returns:
            Buffered geometry
        """
        point = Point(lon, lat)
        # Approximate conversion: 1 degree ≈ 111 km
        radius_deg = radius_km / 111.0
        return point.buffer(radius_deg)
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        from math import radians, cos, sin, asin, sqrt
        
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    @staticmethod
    def find_nearest_resources(center_lat: float, center_lon: float, 
                              resources: List[Dict], k: int = 5) -> List[Dict]:
        """Find k nearest resources
        
        Args:
            center_lat, center_lon: Center point
            resources: List of resource dicts with latitude/longitude
            k: Number of nearest resources to return
            
        Returns:
            List of k nearest resources sorted by distance
        """
        distances = []
        for r in resources:
            dist = GeoAnalyzer.calculate_distance(
                center_lat, center_lon,
                r['latitude'], r['longitude']
            )
            distances.append((r, dist))
        
        # Sort by distance and return k nearest
        distances.sort(key=lambda x: x[1])
        return [r for r, _ in distances[:k]]
    
    @staticmethod
    def calculate_coverage(resources: List[Dict], area_bounds: Tuple[float, float, float, float]) -> float:
        """Calculate resource coverage percentage
        
        Args:
            resources: List of resources
            area_bounds: (min_lat, max_lat, min_lon, max_lon)
            
        Returns:
            Coverage percentage
        """
        if not resources:
            return 0.0
        
        min_lat, max_lat, min_lon, max_lon = area_bounds
        covered = 0
        
        for r in resources:
            if (min_lat <= r['latitude'] <= max_lat and 
                min_lon <= r['longitude'] <= max_lon):
                covered += 1
        
        return (covered / len(resources)) * 100
