"""
Base class for shock scenarios
"""

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseShock(ABC):
    """
    Abstract base class for macroeconomic shock scenarios
    
    All shock implementations must inherit from this class and implement:
    - apply_shock(): Core shock logic
    - get_shock_summary(): Description of shock parameters
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize shock scenario
        
        Args:
            name: Short name for the shock
            description: Detailed description
        """
        self.name = name
        self.description = description
        self.applied = False
        
    @abstractmethod
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply shock to household dataframe
        
        Args:
            df: DataFrame with baseline household data
            
        Returns:
            DataFrame with shocked values and exposure flags
        """
        pass
    
    @abstractmethod
    def get_shock_summary(self) -> Dict:
        """
        Return dictionary of shock parameters
        
        Returns:
            Dictionary with shock configuration
        """
        pass
    
    def _create_exposure_mask(
        self,
        df: pd.DataFrame,
        exposure_rate: float,
        condition: Optional[pd.Series] = None
    ) -> pd.Series:
        """
        Create boolean exposure mask for affected households
        
        Args:
            df: DataFrame
            exposure_rate: Proportion exposed (0.0 to 1.0)
            condition: Optional boolean condition to filter eligible households
            
        Returns:
            Boolean Series indicating exposed households
        """
        n = len(df)
        
        if condition is None:
            # All households eligible
            eligible = pd.Series(True, index=df.index)
        else:
            eligible = condition
        
        n_eligible = eligible.sum()
        
        # Random selection within eligible pool
        random_draw = np.random.random(n) < exposure_rate
        exposed = eligible & random_draw
        
        return exposed
    
    def calculate_delta_metrics(
        self,
        df: pd.DataFrame,
        baseline_suffix: str = "_baseline",
        shocked_suffix: str = "_shocked"
    ) -> pd.DataFrame:
        """
        Calculate change (delta) between baseline and shocked states
        
        Args:
            df: DataFrame with both baseline and shocked columns
            baseline_suffix: Suffix for baseline columns
            shocked_suffix: Suffix for shocked columns
            
        Returns:
            DataFrame with delta columns added
        """
        # Find baseline/shocked column pairs
        baseline_cols = [c for c in df.columns if c.endswith(baseline_suffix)]
        
        for baseline_col in baseline_cols:
            base_name = baseline_col.replace(baseline_suffix, '')
            shocked_col = base_name + shocked_suffix
            delta_col = base_name + '_delta'
            
            if shocked_col in df.columns:
                df[delta_col] = df[shocked_col] - df[baseline_col]
        
        return df
    
    def summary_statistics(self, df: pd.DataFrame) -> Dict:
        """
        Generate summary statistics for this shock
        
        Args:
            df: DataFrame after shock applied
            
        Returns:
            Dictionary of summary statistics
        """
        stats = {
            'shock_name': self.name,
            'n_households': len(df),
        }
        
        # Count exposed households
        exposed_cols = [c for c in df.columns if 'exposed' in c or 'renewing' in c]
        for col in exposed_cols:
            if col in df.columns:
                stats[f'n_{col}'] = df[col].sum()
                stats[f'pct_{col}'] = df[col].mean()
        
        # Delta metrics
        delta_cols = [c for c in df.columns if '_delta' in c]
        for col in delta_cols:
            stats[f'{col}_mean'] = df[col].mean()
            stats[f'{col}_median'] = df[col].median()
        
        return stats
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
