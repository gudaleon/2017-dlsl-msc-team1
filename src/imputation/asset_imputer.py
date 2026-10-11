"""
Statistical imputation of liquid assets from SFS to Census PUMF households

Implements statistical matching (hot-deck imputation) to link asset/debt data
from Survey of Financial Security onto Census households based on demographic
and income characteristics.
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, Literal


class AssetImputer:
    """
    Imputes liquid assets and debt onto Census households using SFS profiles
    
    Methods:
    - Hot-deck imputation: Match to nearest SFS donor within strata
    - Parametric imputation: Sample from estimated distributions
    - Fractional assignment: Probabilistic matching across donors
    """
    
    def __init__(self, sfs_data: pd.DataFrame, method: str = "hot_deck"):
        """
        Initialize asset imputer
        
        Args:
            sfs_data: SFS DataFrame with asset/debt variables
            method: Imputation method ('hot_deck', 'parametric', 'fractional')
        """
        self.sfs_data = sfs_data
        self.method = method
        
        # Prepare SFS matching keys
        self._prepare_sfs_matching_keys()
    
    def _prepare_sfs_matching_keys(self):
        """Prepare SFS data for statistical matching"""
        df = self.sfs_data.copy()
        
        # Calculate income decile if not present
        if 'income_decile' not in df.columns:
            if 'income_sfs' in df.columns:
                df['income_decile'] = pd.qcut(
                    df['income_sfs'], 
                    q=10, 
                    labels=False, 
                    duplicates='drop'
                ) + 1
        
        # Ensure tenure is available
        if 'tenure' not in df.columns:
            df['tenure'] = 2  # Default to renter
        
        self.sfs_data_prepared = df
    
    def impute_assets(
        self, 
        census_df: pd.DataFrame,
        matching_vars: Optional[list] = None
    ) -> pd.DataFrame:
        """
        Impute liquid assets onto Census households
        
        Args:
            census_df: Census DataFrame with income, tenure, demographics
            matching_vars: List of variables to match on (default: income_decile, tenure)
            
        Returns:
            Census DataFrame with added asset columns
        """
        df = census_df.copy()
        
        # Default matching variables
        if matching_vars is None:
            matching_vars = ['income_decile', 'tenure']
        
        # Calculate income decile for Census data if not present
        if 'income_decile' not in df.columns:
            if 'annual_income' in df.columns:
                df['income_decile'] = pd.qcut(
                    df['annual_income'],
                    q=10,
                    labels=False,
                    duplicates='drop'
                ) + 1
        
        # Ensure tenure variables
        if 'tenure' not in df.columns:
            # Derive from is_owner/is_renter if available
            if 'is_owner' in df.columns:
                df['tenure'] = np.where(df['is_owner'], 1, 2)
            else:
                df['tenure'] = 2  # Default to renter
        
        print(f"\n=== Imputing Assets via {self.method.upper()} Method ===")
        print(f"  Census records: {len(df):,}")
        print(f"  SFS donor pool: {len(self.sfs_data_prepared):,}")
        print(f"  Matching on: {matching_vars}")
        
        if self.method == "hot_deck":
            df = self._hot_deck_imputation(df, matching_vars)
        elif self.method == "parametric":
            df = self._parametric_imputation(df, matching_vars)
        else:
            raise ValueError(f"Unknown imputation method: {self.method}")
        
        # Calculate months-to-default metric
        df = self._calculate_months_to_default(df)
        
        return df
    
    def _hot_deck_imputation(
        self, 
        census_df: pd.DataFrame, 
        matching_vars: list
    ) -> pd.DataFrame:
        """
        Hot-deck imputation: Match each Census household to nearest SFS donor
        
        Within each strata (e.g., income_decile × tenure), randomly sample
        a donor household from SFS and copy their asset values.
        """
        df = census_df.copy()
        
        # Initialize asset columns
        df['liquid_assets_imputed'] = 0.0
        df['total_debt_imputed'] = 0.0
        df['net_worth_imputed'] = 0.0
        
        # Create stratification key
        sfs = self.sfs_data_prepared.copy()
        
        # Match within strata
        for decile in range(1, 11):
            for tenure in [1, 2]:
                # Census households in this stratum
                census_mask = (
                    (df['income_decile'] == decile) & 
                    (df['tenure'] == tenure)
                )
                n_census = census_mask.sum()
                
                if n_census == 0:
                    continue
                
                # SFS donors in this stratum
                sfs_mask = (
                    (sfs['income_decile'] == decile) & 
                    (sfs['tenure'] == tenure)
                )
                sfs_donors = sfs[sfs_mask]
                
                if len(sfs_donors) == 0:
                    # No donors available - use overall decile mean
                    fallback = sfs[sfs['income_decile'] == decile]
                    if len(fallback) > 0:
                        sfs_donors = fallback
                    else:
                        continue
                
                # Random sampling with replacement
                sampled_donors = sfs_donors.sample(n=n_census, replace=True)
                
                # Assign imputed values
                df.loc[census_mask, 'liquid_assets_imputed'] = sampled_donors['liquid_assets'].values
                df.loc[census_mask, 'total_debt_imputed'] = sampled_donors['total_debt'].values if 'total_debt' in sampled_donors else 0
                df.loc[census_mask, 'net_worth_imputed'] = sampled_donors['net_worth'].values if 'net_worth' in sampled_donors else 0
        
        print(f"✓ Hot-deck imputation complete")
        print(f"  Mean imputed liquid assets: ${df['liquid_assets_imputed'].mean():,.0f}")
        print(f"  Median imputed liquid assets: ${df['liquid_assets_imputed'].median():,.0f}")
        print(f"  % with <$5K liquid: {(df['liquid_assets_imputed'] < 5000).mean():.1%}")
        
        return df
    
    def _parametric_imputation(
        self,
        census_df: pd.DataFrame,
        matching_vars: list
    ) -> pd.DataFrame:
        """
        Parametric imputation: Sample from estimated distributions
        
        Estimate lognormal distributions for assets within each stratum,
        then draw random samples for Census households.
        """
        df = census_df.copy()
        
        # Calculate distribution parameters from SFS
        sfs = self.sfs_data_prepared
        
        params = sfs.groupby(matching_vars)['liquid_assets'].agg([
            ('mean', 'mean'),
            ('std', 'std'),
            ('count', 'count')
        ]).reset_index()
        
        # Initialize columns
        df['liquid_assets_imputed'] = 0.0
        
        # Impute within each stratum
        for _, row in params.iterrows():
            # Match Census households to this stratum
            mask = True
            for var in matching_vars:
                mask = mask & (df[var] == row[var])
            
            n = mask.sum()
            if n == 0:
                continue
            
            # Sample from lognormal distribution
            mean_log = np.log(row['mean']**2 / np.sqrt(row['std']**2 + row['mean']**2))
            std_log = np.sqrt(np.log(1 + row['std']**2 / row['mean']**2))
            
            samples = np.random.lognormal(mean_log, std_log, size=n).clip(0, 1e6)
            df.loc[mask, 'liquid_assets_imputed'] = samples
        
        print(f"✓ Parametric imputation complete")
        
        return df
    
    def _calculate_months_to_default(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate months until liquidity exhaustion
        
        Months to Default = Liquid Assets / |Monthly Residual Income Deficit|
        
        Only relevant for households with negative residual income
        """
        # Monthly residual income (baseline)
        if 'residual_income_baseline' in df.columns:
            df['monthly_residual_income'] = df['residual_income_baseline'] / 12
        else:
            df['monthly_residual_income'] = 0
        
        # For households with deficit
        has_deficit = df['monthly_residual_income'] < 0
        
        df['months_to_default'] = np.inf  # Default: infinite (solvent)
        
        df.loc[has_deficit, 'months_to_default'] = (
            df.loc[has_deficit, 'liquid_assets_imputed'] / 
            df.loc[has_deficit, 'monthly_residual_income'].abs()
        )
        
        # Cap at 120 months (10 years)
        df['months_to_default'] = df['months_to_default'].clip(0, 120)
        
        # Categorize
        df['liquidity_category'] = pd.cut(
            df['months_to_default'],
            bins=[0, 3, 6, 12, 24, 120],
            labels=['<3mo', '3-6mo', '6-12mo', '1-2yr', '>2yr']
        )
        
        n_deficit = has_deficit.sum()
        if n_deficit > 0:
            print(f"\n=== Liquidity Buffer Analysis ===")
            print(f"  Households with deficit: {n_deficit:,} ({n_deficit/len(df):.1%})")
            print(f"  Mean months to default: {df.loc[has_deficit, 'months_to_default'].mean():.1f}")
            print(f"  Immediately insolvent (<3mo): {(df['liquidity_category'] == '<3mo').sum():,}")
        
        return df


if __name__ == "__main__":
    # Test asset imputation
    from ..data_loading.sfs_loader import SFSLoader
    from ..data_loading.census_loader import CensusLoader
    
    print("=== Asset Imputation Test ===\n")
    
    # Create synthetic SFS data
    sfs_loader = SFSLoader()
    sfs_data = sfs_loader._create_synthetic_sfs(n=3000)
    
    # Create synthetic Census data
    census_loader = CensusLoader()
    census_data = census_loader._create_synthetic_baseline(pd.DataFrame({'_': range(1000)}))
    
    # Impute assets
    imputer = AssetImputer(sfs_data, method="hot_deck")
    enriched = imputer.impute_assets(census_data)
    
    print("\n=== Results ===")
    print(f"Enriched dataset shape: {enriched.shape}")
    print(f"New columns: {[c for c in enriched.columns if 'imputed' in c]}")
