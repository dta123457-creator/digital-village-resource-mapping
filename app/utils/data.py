"""
Data processing utilities
"""

import pandas as pd
import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def normalize_coordinates(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize latitude and longitude
        
        Args:
            df: DataFrame with latitude and longitude columns
            
        Returns:
            DataFrame with normalized coordinates
        """
        df_normalized = df.copy()
        df_normalized['latitude'] = (df['latitude'] - df['latitude'].min()) / (df['latitude'].max() - df['latitude'].min())
        df_normalized['longitude'] = (df['longitude'] - df['longitude'].min()) / (df['longitude'].max() - df['longitude'].min())
        return df_normalized
    
    @staticmethod
    def aggregate_by_type(resources: List[Dict]) -> Dict[str, int]:
        """Aggregate resources by type
        
        Args:
            resources: List of resource dicts
            
        Returns:
            Dictionary with resource type counts
        """
        aggregation = {}
        for r in resources:
            rtype = r.get('resource_type', 'Unknown')
            aggregation[rtype] = aggregation.get(rtype, 0) + 1
        return aggregation
    
    @staticmethod
    def calculate_statistics(resources: List[Dict]) -> Dict:
        """Calculate statistics for resources
        
        Args:
            resources: List of resource dicts
            
        Returns:
            Dictionary with statistics
        """
        if not resources:
            return {}
        
        df = pd.DataFrame(resources)
        
        stats = {
            'total_count': len(resources),
            'resource_types': df['resource_type'].nunique() if 'resource_type' in df else 0,
            'average_quality': df.get('quality_score', pd.Series([0])).mean(),
            'verified_count': len([r for r in resources if r.get('verified', False)])
        }
        
        return stats
    
    @staticmethod
    def filter_by_quality(resources: List[Dict], min_quality: float = 0.7) -> List[Dict]:
        """Filter resources by quality score
        
        Args:
            resources: List of resource dicts
            min_quality: Minimum quality threshold
            
        Returns:
            Filtered list of resources
        """
        return [r for r in resources if r.get('quality_score', 0) >= min_quality]
