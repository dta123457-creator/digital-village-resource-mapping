"""Test configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.main import app
from app.database import get_db
from app.models.resource import Resource
from app.models.village import Village
from app.models.analysis import Analysis

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db():
    """Create test database"""
    # Create all tables
    Resource.metadata.create_all(bind=engine)
    Village.metadata.create_all(bind=engine)
    Analysis.metadata.create_all(bind=engine)
    
    yield TestingSessionLocal()
    
    # Drop all tables after test
    Resource.metadata.drop_all(bind=engine)
    Village.metadata.drop_all(bind=engine)
    Analysis.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create test client"""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
