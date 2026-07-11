"""Database connection and session management"""

from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, Session
from app.config import config
from app.logger import logger
import os

# Create engine with connection pooling
engine = create_engine(
    config.DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    echo=config.API_DEBUG,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db() -> Session:
    """Get database session dependency.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_all_tables():
    """Create all database tables."""
    from app.models.resource import Resource
    from app.models.village import Village
    from app.models.analysis import Analysis
    
    try:
        logger.info("Creating database tables...")
        Resource.metadata.create_all(bind=engine)
        Village.metadata.create_all(bind=engine)
        Analysis.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")
        raise

def health_check():
    """Check database connection health."""
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False
