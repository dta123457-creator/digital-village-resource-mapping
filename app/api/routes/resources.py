"""
Resource management endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.logger import logger

router = APIRouter()

class Resource(BaseModel):
    """Resource model"""
    id: int
    name: str
    resource_type: str
    latitude: float
    longitude: float
    status: str
    description: Optional[str] = None

class ResourceCreate(BaseModel):
    """Create resource model"""
    name: str
    resource_type: str
    latitude: float
    longitude: float
    status: str
    description: Optional[str] = None

# In-memory storage (replace with database in production)
resources_db: List[Resource] = [
    Resource(id=1, name="School A", resource_type="School", latitude=20.593, longitude=78.963, status="Active", description="Primary School"),
    Resource(id=2, name="Hospital B", resource_type="Hospital", latitude=20.595, longitude=78.961, status="Active", description="General Hospital"),
]

@router.get("/", response_model=List[Resource])
async def get_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    resource_type: Optional[str] = None
):
    """Get all resources"""
    logger.info(f"Fetching resources: skip={skip}, limit={limit}, type={resource_type}")
    
    filtered = resources_db
    if resource_type:
        filtered = [r for r in filtered if r.resource_type == resource_type]
    
    return filtered[skip:skip + limit]

@router.get("/{resource_id}", response_model=Resource)
async def get_resource(resource_id: int):
    """Get specific resource"""
    for resource in resources_db:
        if resource.id == resource_id:
            logger.info(f"Resource {resource_id} retrieved")
            return resource
    raise HTTPException(status_code=404, detail="Resource not found")

@router.post("/", response_model=Resource, status_code=201)
async def create_resource(resource: ResourceCreate):
    """Create new resource"""
    new_resource = Resource(
        id=len(resources_db) + 1,
        **resource.dict()
    )
    resources_db.append(new_resource)
    logger.info(f"Resource {new_resource.id} created: {new_resource.name}")
    return new_resource

@router.put("/{resource_id}", response_model=Resource)
async def update_resource(resource_id: int, resource: ResourceCreate):
    """Update resource"""
    for i, existing in enumerate(resources_db):
        if existing.id == resource_id:
            updated = Resource(id=resource_id, **resource.dict())
            resources_db[i] = updated
            logger.info(f"Resource {resource_id} updated")
            return updated
    raise HTTPException(status_code=404, detail="Resource not found")

@router.delete("/{resource_id}", status_code=204)
async def delete_resource(resource_id: int):
    """Delete resource"""
    for i, resource in enumerate(resources_db):
        if resource.id == resource_id:
            resources_db.pop(i)
            logger.info(f"Resource {resource_id} deleted")
            return
    raise HTTPException(status_code=404, detail="Resource not found")
