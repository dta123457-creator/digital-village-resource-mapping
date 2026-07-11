"""
Image processing utilities for satellite imagery
"""

import numpy as np
from PIL import Image
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Image processing utilities"""
    
    @staticmethod
    def load_image(image_path: str, size: Tuple[int, int] = (224, 224)) -> np.ndarray:
        """Load and preprocess image
        
        Args:
            image_path: Path to image file
            size: Target size for resizing
            
        Returns:
            Preprocessed image as numpy array
        """
        try:
            img = Image.open(image_path)
            img = img.resize(size)
            img_array = np.array(img) / 255.0
            logger.info(f"Image loaded and preprocessed: {image_path}")
            return img_array
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {str(e)}")
            raise
    
    @staticmethod
    def normalize_image(image: np.ndarray) -> np.ndarray:
        """Normalize image for model input
        
        Args:
            image: Input image array
            
        Returns:
            Normalized image
        """
        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        
        if len(image.shape) == 3 and image.shape[2] == 3:
            for i in range(3):
                image[:, :, i] = (image[:, :, i] - mean[i]) / std[i]
        
        return image
    
    @staticmethod
    def enhance_contrast(image: np.ndarray, factor: float = 1.5) -> np.ndarray:
        """Enhance image contrast
        
        Args:
            image: Input image
            factor: Contrast factor
            
        Returns:
            Enhanced image
        """
        mean = np.mean(image)
        enhanced = (image - mean) * factor + mean
        return np.clip(enhanced, 0, 1)
    
    @staticmethod
    def extract_patches(image: np.ndarray, patch_size: int = 32, stride: int = 16) -> np.ndarray:
        """Extract patches from image
        
        Args:
            image: Input image
            patch_size: Size of patches
            stride: Stride for patching
            
        Returns:
            Array of patches
        """
        patches = []
        h, w = image.shape[:2]
        
        for i in range(0, h - patch_size + 1, stride):
            for j in range(0, w - patch_size + 1, stride):
                patch = image[i:i+patch_size, j:j+patch_size]
                patches.append(patch)
        
        return np.array(patches)
