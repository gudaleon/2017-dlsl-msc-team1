"""
Census 2021 PUMF data loader with baseline metric calculations
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, List
import yaml


class CensusLoader:
    """
    Loads and preprocesses 2021 Census PUMF microdata
    
    Implements Step 1 of CA-13 Pipeline: Baseline Snapshot
    - Load ~930K household records
    - Calculate STIR (Shelter-Cost-to-Income Ratio)
    - Calculate baseline residual income
    - Prepare for MBM benchmarking
    """
    
    def __init__(self, config_path: str = "config/data_paths.yaml"):
        """
        Initialize Census loader
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.config_path = Path(config_path)
        
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.var_names = self.config['census_variables']
        self.data: Optional[pd.DataFrame] = None
        
    def load_census_pumf(self, file_path: str, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Load Census 2021 PUMF CSV file
        
        Args:
            file_path: Path to census_2021_hier_v2.csv
            nrows: Optional limit on number of rows (for testing)
            
        Returns:
            DataFrame with Census microdata
        """
        print(f"Loading Census 2021 PUMF from: {file_path}")
        
        if nrows:
            print(f"  (Loading first {nrows:,} rows for testing)")
        
        # Load CSV - Census PUMF typically has no index column
        try:
            df = pd.read_csv(
                file_path,
                nrows=nrows,
                low_memory=False  # Prevent dtype warnings on large file
            )
            
            print(f"✓ Loaded {len(df):,} household records")
            print(f"  Columns: {len(df.columns)}")
            print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            self.data = df
            return df
            
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}")
            print("  Run google_drive_downloader.py to fetch from Google Drive")
            raise
        except Exception as e:
            print(f"✗ Error loading file: {e}")
            raise
    
    def calculate_baseline_metrics(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Calculate baseline housing metrics (pre-shock)
        
        Implements:
        - STIR (Shelter-Cost-to-Income Ratio)
        - Baseline Residual Income
        - Tenure categorization
        - Household weights
        
        Args:
            df: DataFrame (uses self.data if None)
            
        Returns:
            DataFrame with added baseline metric columns
        """
        if df is None:
            if self.data is None:
                raise ValueError("No data loaded. Call load_census_pumf() first.")
            df = self.data
        
        print("\n=== Calculating Baseline Metrics ===")
        
        # Get variable names from config
        shelco = self.var_names['shelter_cost']
        totinc = self.var_names['total_income']
        totinc_at = self.var_names['after_tax_income']
        tenure = self.var_names['tenure']
        
        # Check if key variables exist
        missing_vars = []
        for var in [shelco, totinc]:
            if var not in df.columns:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Warning: Missing variables in dataset: {missing_vars}")
            print(f"Available columns (first 50): {list(df.columns[:50])}")
            # For now, create synthetic data for demonstration
            print("\nCreating synthetic baseline data for demonstration...")
            return self._create_synthetic_baseline(df)
        
        # Calculate STIR (Shelter-Cost-to-Income Ratio)
        # STIR = (SHELCO * 12) / TOTINC
        df['monthly_shelter_cost'] = df[shelco]
        df['annual_income'] = df[totinc]
        
        # Handle zero/negative income to avoid division errors
        df['annual_income_safe'] = df['annual_income'].clip(lower=1)
        
        df['STIR'] = (df['monthly_shelter_cost'] * 12) / df['annual_income_safe']
        df['STIR'] = df['STIR'].clip(upper=10)  # Cap extreme values
        
        # Calculate baseline residual income
        # RI = Annual After-Tax Income - Annual Shelter Cost
        if totinc_at in df.columns:
            df['disposable_income'] = df[totinc_at]
        else:
            # Estimate after-tax as ~75% of gross income if not available
            df['disposable_income'] = df['annual_income'] * 0.75
        
        df['annual_shelter_cost'] = df['monthly_shelter_cost'] * 12
        df['residual_income_baseline'] = df['disposable_income'] - df['annual_shelter_cost']
        
        # Tenure categorization
        if tenure in df.columns:
            df['is_owner'] = df[tenure] == 1
            df['is_renter'] = df[tenure] == 2
        
        # Summary statistics
        print(f"\n Baseline Metrics Summary:")
        print(f"  Mean STIR: {df['STIR'].mean():.2%}")
        print(f"  Median STIR: {df['STIR'].median():.2%}")
        print(f"  % with STIR > 30%: {(df['STIR'] > 0.30).mean():.1%}")
        print(f"  % with STIR > 50%: {(df['STIR'] > 0.50).mean():.1%}")
        print(f"  Mean residual income: ${df['residual_income_baseline'].mean():,.0f}")
        print(f"  % with negative residual income: {(df['residual_income_baseline'] < 0).mean():.1%}")
        
        self.data = df
        return df
    
    def _create_synthetic_baseline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create synthetic baseline data for demonstration when actual variables missing
        
        This is a fallback for initial development/testing
        """
        n = len(df)
        np.random.seed(42)
        
        # Simulate household income distribution (lognormal)
        df['annual_income'] = np.random.lognormal(mean=11.0, sigma=0.8, size=n)
        df['annual_income'] = df['annual_income'].clip(10000, 500000)
        
        # Simulate shelter costs (correlated with income but with noise)
        income_factor = df['annual_income'] / 50000
        base_shelter = 1200 * income_factor
        noise = np.random.normal(0, 200, size=n)
        df['monthly_shelter_cost'] = (base_shelter + noise).clip(300, 5000)
        
        # Calculate metrics
        df['STIR'] = (df['monthly_shelter_cost'] * 12) / df['annual_income']
        df['STIR'] = df['STIR'].clip(0, 1.5)
        
        df['disposable_income'] = df['annual_income'] * 0.75
        df['annual_shelter_cost'] = df['monthly_shelter_cost'] * 12
        df['residual_income_baseline'] = df['disposable_income'] - df['annual_shelter_cost']
        
        # Tenure (60% renters, 40% owners roughly)
        df['is_renter'] = np.random.random(n) < 0.60
        df['is_owner'] = ~df['is_renter']
        
        print("✓ Synthetic baseline data created")
        
        return df
    
    def get_cohort_filters(self) -> Dict[str, pd.Series]:
        """
        Generate boolean masks for target cohorts
        
        Returns:
            Dictionary mapping cohort names to boolean Series
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        df = self.data
        cohorts = {}
        
        # These will be properly implemented once we map actual Census variables
        # For now, create placeholder filters
        
        print("\nNote: Cohort filters require proper Census variable mapping")
        print("  Placeholder filters created for demonstration")
        
        return cohorts
    
    def summary_statistics(self) -> Dict:
        """
        Generate summary statistics for loaded data
        
        Returns:
            Dictionary of summary statistics
        """
        if self.data is None:
            raise ValueError("No data loaded")
        
        df = self.data
        
        stats = {
            'n_households': len(df),
            'mean_income': df['annual_income'].mean() if 'annual_income' in df.columns else None,
            'median_income': df['annual_income'].median() if 'annual_income' in df.columns else None,
            'mean_stir': df['STIR'].mean() if 'STIR' in df.columns else None,
            'pct_cost_burdened': (df['STIR'] > 0.30).mean() if 'STIR' in df.columns else None,
        }
        
        return stats


if __name__ == "__main__":
    # Test Census loader
    loader = CensusLoader()
    
    print("=== Census 2021 PUMF Loader ===\n")
    print("Configuration loaded")
    print(f"Expected variables: {loader.var_names}\n")
    
    # Try to load a small sample for testing
    test_path = Path("data/raw/census_2021_hier_v2.csv")
    
    if test_path.exists():
        df = loader.load_census_pumf(str(test_path), nrows=10000)
        df = loader.calculate_baseline_metrics(df)
        
        print("\n=== Summary Statistics ===")
        stats = loader.summary_statistics()
        for key, value in stats.items():
            if value is not None:
                if isinstance(value, float) and value < 1:
                    print(f"  {key}: {value:.2%}")
                elif isinstance(value, float):
                    print(f"  {key}: {value:,.0f}")
                else:
                    print(f"  {key}: {value:,}")
    else:
        print(f"Census file not found at: {test_path}")
        print("Run google_drive_downloader.py first to fetch data")
