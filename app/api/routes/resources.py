"""
Resource management endpoints with database integration
"""

from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas import ResourceCreate, ResourceUpdate, ResourceResponse
from app.models.resource import Resource
from app.database import get_db
from app.logger import logger

router = APIRouter()

@router.get("/", response_model=List[ResourceResponse])
async def get_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    resource_type: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get all resources with optional filtering"""
    try:
        query = db.query(Resource)
        
        if resource_type:
            query = query.filter(Resource.resource_type == resource_type)
        
        resources = query.offset(skip).limit(limit).all()
        logger.info(f"Fetched {len(resources)} resources")
        return resources
    except Exception as e:
        logger.error(f"Error fetching resources: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching resources")

@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get specific resource by ID"""
    try:
        resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not resource:
            logger.warning(f"Resource {resource_id} not found")
            raise HTTPException(status_code=404, detail="Resource not found")
        return resource
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching resource {resource_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching resource")

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    """Create new resource"""
    try:
        db_resource = Resource(
            name=resource.name,
            resource_type=resource.resource_type,
            latitude=resource.latitude,
            longitude=resource.longitude,
            status=resource.status,
            description=resource.description,
            verified=False,
            quality_score=0.0
        )
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)
        logger.info(f"Created resource {db_resource.id}: {resource.name}")
        return db_resource
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating resource: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating resource")

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: int,
    resource: ResourceUpdate,
    db: Session = Depends(get_db)
):
    """Update existing resource"""
    try:
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        # Update fields that are provided
        update_data = resource.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_resource, field, value)
        
        db.commit()
        db.refresh(db_resource)
        logger.info(f"Updated resource {resource_id}")
        return db_resource
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating resource {resource_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating resource")

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    """Delete resource"""
    try:
        db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
        if not db_resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        db.delete(db_resource)
        db.commit()
        logger.info(f"Deleted resource {resource_id}")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting resource {resource_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting resource")

@router.post("/search/by-bbox")
async def search_by_bbox(
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
    db: Session = Depends(get_db)
):
    """Search resources within bounding box"""
    try:
        resources = db.query(Resource).filter(
            Resource.latitude >= min_lat,
            Resource.latitude <= max_lat,
            Resource.longitude >= min_lon,
            Resource.longitude <= max_lon
        ).all()
        
        logger.info(f"Found {len(resources)} resources in bbox")
        return {
            "count": len(resources),
            "resources": resources
        }
    except Exception as e:
        logger.error(f"Error searching bbox: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching resources")

@router.get("/stats/by-type")
async def get_stats_by_type(db: Session = Depends(get_db)):
    """Get resource statistics by type"""
    try:
        from sqlalchemy import func
        
        stats = db.query(
            Resource.resource_type,
            func.count(Resource.id).label("count"),
            func.avg(Resource.quality_score).label("avg_quality")
        ).group_by(Resource.resource_type).all()
        
        result = [
            {
                "type": s[0],
                "count": s[1],
                "avg_quality": float(s[2]) if s[2] else 0.0
            }
            for s in stats
        ]
        
        logger.info(f"Retrieved stats for {len(result)} resource types")
        return result
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics")
