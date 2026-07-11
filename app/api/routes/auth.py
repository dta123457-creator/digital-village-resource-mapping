"""
Authentication endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import timedelta
from app.security import SecurityUtils
from app.logger import logger

router = APIRouter()

class LoginRequest(BaseModel):
    """Login request model"""
    username: str
    password: str

class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    expires_in: int

class UserResponse(BaseModel):
    """User response model"""
    username: str
    email: str

# Mock user database - replace with real DB in production
MOCK_USERS = {
    "admin": SecurityUtils.hash_password("admin123"),
    "user": SecurityUtils.hash_password("user123")
}

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    """User login endpoint"""
    try:
        if credentials.username not in MOCK_USERS:
            logger.warning(f"Login attempt for non-existent user: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        if not SecurityUtils.verify_password(
            credentials.password,
            MOCK_USERS[credentials.username]
        ):
            logger.warning(f"Failed login attempt for user: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        
        # Create token
        token_data = {"sub": credentials.username, "role": "admin"}
        token = SecurityUtils.create_access_token(
            token_data,
            expires_delta=timedelta(hours=24)
        )
        
        logger.info(f"User {credentials.username} logged in successfully")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 86400
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login error"
        )

@router.post("/verify-token")
async def verify_token(token: str):
    """Verify JWT token"""
    try:
        payload = SecurityUtils.verify_token(token)
        logger.info(f"Token verified for user: {payload.get('sub')}")
        return {"valid": True, "user": payload.get("sub")}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return {"valid": False}
