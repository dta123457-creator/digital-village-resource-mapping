"""
FastAPI main application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import config
from app.logger import logger
from app.api.routes import health, resources, analysis, geospatial
import time

# Create FastAPI app
app = FastAPI(
    title="Village Resource Mapping API",
    description="AI-powered GIS platform for village resource mapping",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware for logging
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )
    return response

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(geospatial.router, prefix="/api/geo", tags=["Geospatial"])

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    logger.info(f"Environment: {config.ENVIRONMENT if hasattr(config, 'ENVIRONMENT') else 'development'}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        debug=config.API_DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
