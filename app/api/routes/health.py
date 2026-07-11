"""
Health check endpoints
"""

from fastapi import APIRouter, status
from app.logger import logger

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {
        "status": "healthy",
        "service": "village-resource-mapping-api",
        "version": "0.1.0"
    }

@router.get("/readiness", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "status": "ready",
        "message": "Service is ready to accept requests"
    }
