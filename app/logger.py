"""
Logging configuration for the application
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from app.config import config


def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    # Create logger
    logger = logging.getLogger("village_mapping")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL))
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


logger = setup_logging()
