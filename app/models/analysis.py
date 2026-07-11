"""
Analysis database model
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Analysis(Base):
    """Analysis results ORM model"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_type = Column(String(100), nullable=False)
    region = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    
    # Results
    results = Column(JSON)
    summary = Column(String(500))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    accuracy = Column(Float, default=0.0)
    
    def __repr__(self):
        return f"<Analysis(id={self.id}, type='{self.analysis_type}', region='{self.region}')>"
