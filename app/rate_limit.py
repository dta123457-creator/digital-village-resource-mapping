"""
Rate limiting and throttling utilities
"""

from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Dict
from app.logger import logger
import time

class RateLimiter:
    """Rate limiting implementation"""
    
    def __init__(self, requests_per_minute: int = 60):
        """Initialize rate limiter
        
        Args:
            requests_per_minute: Max requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if client is allowed to make request
        
        Args:
            client_id: Unique identifier for client (e.g., IP address)
            
        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        cutoff = now - 60  # Last minute
        
        # Initialize or clean up
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # Remove old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > cutoff
        ]
        
        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return False
        
        # Add current request
        self.requests[client_id].append(now)
        return True
    
    def get_reset_time(self, client_id: str) -> int:
        """Get when rate limit will reset (in seconds)
        
        Args:
            client_id: Unique identifier for client
            
        Returns:
            Seconds until reset
        """
        if client_id not in self.requests or not self.requests[client_id]:
            return 0
        
        oldest_request = min(self.requests[client_id])
        reset_time = oldest_request + 60
        return max(0, int(reset_time - time.time()))

# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=100)
