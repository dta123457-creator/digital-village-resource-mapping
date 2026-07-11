"""
Geospatial operations endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Tuple
from app.logger import logger

router = APIRouter()

class Point(BaseModel):
    """Point model"""
    latitude: float
    longitude: float

class BoundingBox(BaseModel):
    """Bounding box model"""
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float

class GeoQuery(BaseModel):
    """Geospatial query model"""
    point: Point
    radius_km: float = 5.0
    resource_type: str = None

@router.post("/nearby-resources")
async def find_nearby_resources(query: GeoQuery):
    """Find resources near a point"""
    logger.info(f"Finding resources near ({query.point.latitude}, {query.point.longitude}) within {query.radius_km}km")
    
    return {
        "center": {"latitude": query.point.latitude, "longitude": query.point.longitude},
        "radius_km": query.radius_km,
        "resources_found": [
            {"id": 1, "name": "School A", "distance_km": 2.3},
            {"id": 2, "name": "Hospital B", "distance_km": 3.1}
        ]
    }

@router.post("/bbox-query")
async def query_bbox(bbox: BoundingBox):
    """Query resources within bounding box"""
    logger.info(f"Querying bbox: ({bbox.min_lat}, {bbox.min_lon}) to ({bbox.max_lat}, {bbox.max_lon})")
    
    return {
        "bounding_box": bbox.dict(),
        "resources_count": 15,
        "resources": [
            {"id": 1, "name": "School A", "latitude": 20.593, "longitude": 78.963},
            {"id": 2, "name": "Hospital B", "latitude": 20.595, "longitude": 78.961}
        ]
    }

@router.get("/distance/{from_lat}/{from_lon}/{to_lat}/{to_lon}")
async def calculate_distance(from_lat: float, from_lon: float, to_lat: float, to_lon: float):
    """Calculate distance between two points"""
    # Simple Haversine approximation
    from math import radians, cos, sin, asin, sqrt
    
    lon1, lat1, lon2, lat2 = map(radians, [from_lon, from_lat, to_lon, to_lat])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    
    logger.info(f"Distance calculated: {km:.2f}km")
    
    return {
        "from": {"latitude": from_lat, "longitude": from_lon},
        "to": {"latitude": to_lat, "longitude": to_lon},
        "distance_km": round(km, 2)
    }
