"""Schemas for request/response validation"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ResourceBase(BaseModel):
    """Base resource schema"""
    name: str = Field(..., min_length=1, max_length=255)
    resource_type: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    status: str = Field(default="active", max_length=50)
    description: Optional[str] = None

    @validator('latitude', 'longitude')
    def validate_coordinates(cls, v):
        if v is None:
            raise ValueError('Coordinates cannot be None')
        return v


class ResourceCreate(ResourceBase):
    """Schema for creating resource"""
    pass


class ResourceUpdate(BaseModel):
    """Schema for updating resource"""
    name: Optional[str] = None
    resource_type: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    status: Optional[str] = None
    description: Optional[str] = None
    verified: Optional[bool] = None
    quality_score: Optional[float] = None


class ResourceResponse(ResourceBase):
    """Schema for resource response"""
    id: int
    verified: bool
    quality_score: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class VillageBase(BaseModel):
    """Base village schema"""
    name: str = Field(..., min_length=1, max_length=255)
    state: str = Field(..., min_length=1, max_length=100)
    district: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    population: Optional[int] = None
    area_sqkm: Optional[float] = None
    description: Optional[str] = None


class VillageCreate(VillageBase):
    """Schema for creating village"""
    pass


class VillageResponse(VillageBase):
    """Schema for village response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisCreate(BaseModel):
    """Schema for creating analysis"""
    analysis_type: str
    region: str
    resource_type: Optional[str] = None
    results: dict
    summary: Optional[str] = None
    accuracy: Optional[float] = None


class AnalysisResponse(BaseModel):
    """Schema for analysis response"""
    id: int
    analysis_type: str
    region: str
    resource_type: Optional[str]
    results: dict
    summary: Optional[str]
    accuracy: float
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
