"""
Survey of Financial Security (SFS) 2023 loader for asset imputation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Tuple
import zipfile


class SFSLoader:
    """
    Loads Survey of Financial Security 2023 PUMF
    
    Purpose: Statistical imputation of liquid assets onto Census households
    
    Key SFS Variables:
    - Assets: Liquid savings, investments, RRSP/TFSA
    - Debts: Mortgage balance, credit card, lines of credit
    - Net worth: Total assets - total debts
    - Demographics: Age, income, household type (for matching)
    """
    
    def __init__(self):
        self.data: Optional[pd.DataFrame] = None
        self.asset_profiles: Optional[pd.DataFrame] = None
        
    def load_sfs_pumf(self, file_path: str) -> pd.DataFrame:
        """
        Load SFS 2023 PUMF from ZIP file
        
        Args:
            file_path: Path to SFS2023_PUMF_data.zip
            
        Returns:
            DataFrame with SFS microdata
        """
        print(f"Loading SFS 2023 PUMF from: {file_path}")
        
        try:
            # SFS PUMFs typically come as zipped CSV or SAS files
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # List files in ZIP
                file_list = zip_ref.namelist()
                print(f"  Files in archive: {file_list}")
                
                # Find the main data file (usually .csv or .txt)
                data_file = [f for f in file_list if f.endswith(('.csv', '.txt', '.dat'))][0]
                
                with zip_ref.open(data_file) as f:
                    df = pd.read_csv(f, low_memory=False)
            
            print(f"✓ Loaded {len(df):,} SFS records")
            print(f"  Columns: {len(df.columns)}")
            
            self.data = df
            return df
            
        except FileNotFoundError:
            print(f"✗ File not found: {file_path}")
            print("  SFS 2023 PUMF should be downloaded from Statistics Canada")
            # Create synthetic data for demonstration
            return self._create_synthetic_sfs()
    
    def _create_synthetic_sfs(self, n: int = 5000) -> pd.DataFrame:
        """
        Create synthetic SFS-like data for demonstration
        
        Args:
            n: Number of synthetic households
            
        Returns:
            DataFrame with synthetic asset/debt data
        """
        print("Creating synthetic SFS data for demonstration...")
        
        np.random.seed(42)
        
        # Income distribution (matches Census for statistical matching)
        income = np.random.lognormal(mean=11.0, sigma=0.8, size=n).clip(10000, 500000)
        
        # Age groups
        age = np.random.choice([25, 35, 45, 55, 65, 75], size=n, 
                              p=[0.15, 0.20, 0.20, 0.20, 0.15, 0.10])
        
        # Household type
        hhtype = np.random.choice([1, 2, 3], size=n, p=[0.30, 0.50, 0.20])
        # 1=Single, 2=Couple, 3=Family with children
        
        # Liquid assets (correlated with income and age)
        income_factor = income / 50000
        age_factor = age / 50
        base_liquid = 5000 * income_factor * age_factor
        noise = np.random.lognormal(0, 1.5, size=n)
        liquid_assets = (base_liquid * noise).clip(0, 500000)
        
        # Total debt (higher for younger, high-income)
        age_debt_factor = (80 - age) / 50  # Younger = more debt
        base_debt = 50000 * income_factor * age_debt_factor
        debt = (base_debt * np.random.lognormal(0, 1.0, size=n)).clip(0, 1000000)
        
        # Net worth
        net_worth = liquid_assets - debt
        
        # Tenure
        tenure = np.random.choice([1, 2], size=n, p=[0.40, 0.60])  # 1=Owner, 2=Renter
        
        df = pd.DataFrame({
            'income_sfs': income,
            'age_group': age,
            'hhtype': hhtype,
            'tenure': tenure,
            'liquid_assets': liquid_assets,
            'total_debt': debt,
            'net_worth': net_worth,
            'has_rrsp': liquid_assets > 10000,
            'weight': 1.0  # Survey weights
        })
        
        print(f"✓ Created {len(df):,} synthetic SFS records")
        print(f"  Mean liquid assets: ${df['liquid_assets'].mean():,.0f}")
        print(f"  Median liquid assets: ${df['liquid_assets'].median():,.0f}")
        print(f"  % with <$5K liquid: {(df['liquid_assets'] < 5000).mean():.1%}")
        
        self.data = df
        return df
    
    def create_asset_profiles(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Create asset distribution profiles by demographic strata
        
        For statistical matching to Census households
        
        Args:
            df: SFS DataFrame (uses self.data if None)
            
        Returns:
            DataFrame with asset distribution parameters by strata
        """
        if df is None:
            if self.data is None:
                df = self._create_synthetic_sfs()
            else:
                df = self.data
        
        print("\n=== Creating Asset Distribution Profiles ===")
        
        # Group by demographic characteristics that exist in both SFS and Census
        # Income deciles, age groups, household type, tenure
        
        # Calculate income deciles
        df['income_decile'] = pd.qcut(df['income_sfs'], q=10, labels=False, duplicates='drop') + 1
        
        # Create stratification keys
        profiles = df.groupby(['income_decile', 'tenure']).agg({
            'liquid_assets': ['mean', 'median', 'std', 'count'],
            'total_debt': ['mean', 'median'],
            'net_worth': ['mean', 'median']
        }).reset_index()
        
        profiles.columns = ['_'.join(col).strip('_') for col in profiles.columns.values]
        
        print(f"✓ Created {len(profiles)} asset profiles")
        print("\nSample profiles (income decile 1 vs 10):")
        if len(profiles) > 0:
            print(f"  Decile 1: Median liquid = ${profiles.iloc[0]['liquid_assets_median']:,.0f}")
            print(f"  Decile 10: Median liquid = ${profiles.iloc[-1]['liquid_assets_median']:,.0f}")
        
        self.asset_profiles = profiles
        return profiles
    
    def get_asset_distribution(self, income_decile: int, tenure: int) -> Dict[str, float]:
        """
        Get asset distribution parameters for a specific strata
        
        Args:
            income_decile: Income decile (1-10)
            tenure: 1=Owner, 2=Renter
            
        Returns:
            Dictionary with distribution parameters
        """
        if self.asset_profiles is None:
            self.create_asset_profiles()
        
        match = self.asset_profiles[
            (self.asset_profiles['income_decile'] == income_decile) &
            (self.asset_profiles['tenure'] == tenure)
        ]
        
        if len(match) == 0:
            # Return fallback values
            return {
                'liquid_assets_mean': 10000,
                'liquid_assets_std': 5000,
                'total_debt_mean': 20000
            }
        
        row = match.iloc[0]
        return {
            'liquid_assets_mean': row['liquid_assets_mean'],
            'liquid_assets_median': row['liquid_assets_median'],
            'liquid_assets_std': row['liquid_assets_std'],
            'total_debt_mean': row['total_debt_mean']
        }


if __name__ == "__main__":
    # Test SFS loader
    loader = SFSLoader()
    
    print("=== SFS 2023 PUMF Loader ===\n")
    
    # Try to load or create synthetic data
    df = loader._create_synthetic_sfs(n=5000)
    
    # Create asset profiles
    profiles = loader.create_asset_profiles(df)
    
    print("\n=== Asset Profile Examples ===")
    print("\nLow-income renter (Decile 1, Tenure=Renter):")
    params = loader.get_asset_distribution(income_decile=1, tenure=2)
    for key, val in params.items():
        print(f"  {key}: ${val:,.0f}")
    
    print("\nHigh-income owner (Decile 10, Tenure=Owner):")
    params = loader.get_asset_distribution(income_decile=10, tenure=1)
    for key, val in params.items():
        print(f"  {key}: ${val:,.0f}")
