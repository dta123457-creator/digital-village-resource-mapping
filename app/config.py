"""
Configuration management for the application
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/village_mapping"
    )
    
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    API_DEBUG: bool = os.getenv("API_DEBUG", "True").lower() == "true"
    
    # Streamlit
    STREAMLIT_PORT: int = int(os.getenv("STREAMLIT_SERVER_PORT", 8501))
    
    # Geospatial
    DEFAULT_LATITUDE: float = float(os.getenv("DEFAULT_LATITUDE", "20.5937"))
    DEFAULT_LONGITUDE: float = float(os.getenv("DEFAULT_LONGITUDE", "78.9629"))
    DEFAULT_ZOOM_LEVEL: int = int(os.getenv("DEFAULT_ZOOM_LEVEL", "13"))
    MAP_PROVIDER: str = os.getenv("MAP_PROVIDER", "OpenStreetMap")
    
    # AI/ML
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
    MAX_IMAGE_SIZE: int = int(os.getenv("MAX_IMAGE_SIZE", "2048"))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-jwt-secret-key-change-in-production")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/app.log")
    
    # Feature Flags
    ENABLE_ADVANCED_ANALYTICS: bool = os.getenv("ENABLE_ADVANCED_ANALYTICS", "True").lower() == "true"
    ENABLE_REAL_TIME_PROCESSING: bool = os.getenv("ENABLE_REAL_TIME_PROCESSING", "False").lower() == "true"
    ENABLE_3D_VISUALIZATION: bool = os.getenv("ENABLE_3D_VISUALIZATION", "False").lower() == "true"
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"


def get_config() -> Config:
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)()


config = get_config()
