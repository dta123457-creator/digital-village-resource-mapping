"""
Resource database model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from datetime import datetime

Base = declarative_base()

class Resource(Base):
    """Resource ORM model"""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    resource_type = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    status = Column(String(50), default="active", nullable=False)
    
    # Geospatial columns
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geometry('POINT', srid=4326))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    verified = Column(Boolean, default=False)
    quality_score = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<Resource(id={self.id}, name='{self.name}', type='{self.resource_type}')>"
