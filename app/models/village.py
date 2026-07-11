"""
Village database model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
from datetime import datetime

Base = declarative_base()

class Village(Base):
    """Village ORM model"""
    __tablename__ = "villages"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    state = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    
    # Geospatial
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    geometry = Column(Geometry('POLYGON', srid=4326))
    
    # Information
    population = Column(Integer)
    area_sqkm = Column(Float)
    description = Column(Text)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Village(id={self.id}, name='{self.name}', state='{self.state}')>"
