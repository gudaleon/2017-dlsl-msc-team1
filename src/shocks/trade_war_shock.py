"""
Trade War Shock: Canada-USA trade disruption scenario

Models economic impacts of trade barriers between Canada and USA:
- Export sector job losses (auto, lumber, agriculture, manufacturing)
- Regional concentration effects (Ontario, Quebec, prairies)
- Income shocks by industry exposure
- Ripple effects on service sectors
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
from .base_shock import BaseShock


class TradeWarShock(BaseShock):
    """
    Models Canada-USA trade war impacts on household income
    
    Key Mechanisms:
    1. Direct job losses in export-dependent industries
    2. Wage suppression in affected sectors
    3. Regional concentration (auto belt, lumber regions)
    4. Secondary effects on service economy
    
    Scenarios:
    - Moderate: 10% tariff, gradual implementation
    - Severe: 25% tariff, immediate implementation
    - Extreme: Trade collapse, 50%+ disruption
    """
    
    # Industry exposure to US trade (% of output exported to USA)
    INDUSTRY_EXPOSURE = {
        'auto_manufacturing': 0.85,      # 85% of auto production exported to USA
        'lumber_forestry': 0.70,         # 70% to USA
        'agriculture': 0.60,             # 60% (grains, livestock)
        'oil_gas': 0.75,                 # 75% energy exports
        'manufacturing_general': 0.40,   # 40% general manufacturing
        'finance_services': 0.10,        # 10% (indirect exposure)
        'retail_hospitality': 0.05,      # 5% (minimal direct)
        'public_sector': 0.0             # No direct exposure
    }
    
    # Regional industry concentration
    REGIONAL_EXPOSURE = {
        'ON': {'auto_manufacturing': 0.15, 'manufacturing_general': 0.25},  # Ontario auto belt
        'QC': {'manufacturing_general': 0.20, 'lumber_forestry': 0.10},    # Quebec manufacturing
        'AB': {'oil_gas': 0.30, 'agriculture': 0.15},                       # Alberta energy
        'BC': {'lumber_forestry': 0.25, 'oil_gas': 0.10},                  # BC lumber
        'SK': {'agriculture': 0.30, 'oil_gas': 0.15},                       # Saskatchewan grains
        'MB': {'agriculture': 0.25, 'manufacturing_general': 0.10},         # Manitoba
    }
    
    def __init__(
        self,
        severity: str = "moderate",
        tariff_rate: float = 0.10,
        job_loss_rate: float = 0.15,
        wage_suppression: float = 0.10
    ):
        """
        Initialize trade war shock
        
        Args:
            severity: 'moderate', 'severe', or 'extreme'
            tariff_rate: Average tariff on Canadian exports (0.10 = 10%)
            job_loss_rate: Proportion of export-sector jobs lost
            wage_suppression: Wage reduction for workers who keep jobs
        """
        super().__init__(
            name=f"trade_war_{severity}",
            description=f"Canada-USA trade war ({severity} scenario, {tariff_rate:.0%} tariff)"
        )
        
        self.severity = severity
        self.tariff_rate = tariff_rate
        self.job_loss_rate = job_loss_rate
        self.wage_suppression = wage_suppression
        
        # Adjust parameters by severity
        if severity == "severe":
            self.tariff_rate = max(self.tariff_rate, 0.25)
            self.job_loss_rate = max(self.job_loss_rate, 0.25)
            self.wage_suppression = max(self.wage_suppression, 0.20)
        elif severity == "extreme":
            self.tariff_rate = max(self.tariff_rate, 0.50)
            self.job_loss_rate = max(self.job_loss_rate, 0.40)
            self.wage_suppression = max(self.wage_suppression, 0.35)
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply trade war income shock
        
        Steps:
        1. Assign industry to households (if not present)
        2. Calculate industry-specific income impacts
        3. Apply job loss probability
        4. Apply wage suppression to remaining workers
        5. Regional multiplier effects
        
        Args:
            df: DataFrame with household income data
            
        Returns:
            DataFrame with shocked income and exposure flags
        """
        df = df.copy()
        
        print(f"\n=== Applying {self.severity.upper()} Trade War Shock ===")
        print(f"  Tariff rate: {self.tariff_rate:.0%}")
        print(f"  Expected job losses: {self.job_loss_rate:.0%}")
        print(f"  Wage suppression: {self.wage_suppression:.0%}")
        
        # Assign industries if not present
        if 'industry' not in df.columns:
            df = self._assign_industries(df)
        
        # Assign provinces if not present
        if 'province' not in df.columns:
            df = self._assign_provinces(df)
        
        # Calculate baseline income
        if 'income_shocked' not in df.columns:
            df['income_shocked'] = df['annual_income'].copy()
        
        # Calculate exposure intensity by household
        df['trade_exposure'] = df.apply(
            lambda row: self._calculate_household_exposure(row),
            axis=1
        )
        
        # Apply job losses (binary outcome)
        job_loss_prob = df['trade_exposure'] * self.job_loss_rate
        df['trade_job_lost'] = np.random.random(len(df)) < job_loss_prob
        
        # Workers who lose jobs: income drops to unemployment insurance (~55% of wages, capped)
        df.loc[df['trade_job_lost'], 'income_shocked'] = (
            df.loc[df['trade_job_lost'], 'annual_income'] * 0.55
        ).clip(upper=30000)  # EI max ~$30K/year
        
        # Workers who keep jobs: wage suppression
        wage_impact = df['trade_exposure'] * self.wage_suppression
        df.loc[~df['trade_job_lost'], 'income_shocked'] = (
            df.loc[~df['trade_job_lost'], 'annual_income'] * (1 - wage_impact)
        )
        
        # Calculate income delta
        df['income_delta'] = df['income_shocked'] - df['annual_income']
        
        # Recalculate residual income and STIR
        df = self._recalculate_financial_metrics(df)
        
        # Summary
        n_job_loss = df['trade_job_lost'].sum()
        pct_job_loss = n_job_loss / len(df)
        avg_income_drop = df['income_delta'].mean()
        median_income_drop = df.loc[df['income_delta'] < 0, 'income_delta'].median()
        
        print(f"\n✓ Trade war shock applied")
        print(f"  Households with job loss: {n_job_loss:,} ({pct_job_loss:.1%})")
        print(f"  Average income change: ${avg_income_drop:,.0f}")
        print(f"  Median drop (affected): ${median_income_drop:,.0f}")
        
        self.applied = True
        return df
    
    def _assign_industries(self, df: pd.DataFrame) -> pd.DataFrame:
        """Assign industries to households based on Canadian labour force distribution"""
        industries = list(self.INDUSTRY_EXPOSURE.keys())
        
        # Approximate Canadian industry distribution
        industry_weights = [
            0.08,  # auto_manufacturing
            0.03,  # lumber_forestry
            0.02,  # agriculture
            0.05,  # oil_gas
            0.12,  # manufacturing_general
            0.25,  # finance_services
            0.25,  # retail_hospitality
            0.20   # public_sector
        ]
        
        df['industry'] = np.random.choice(
            industries,
            size=len(df),
            p=industry_weights
        )
        
        return df
    
    def _assign_provinces(self, df: pd.DataFrame) -> pd.DataFrame:
        """Assign provinces based on Canadian population distribution"""
        provinces = ['ON', 'QC', 'BC', 'AB', 'SK', 'MB', 'NS', 'NB', 'NL', 'PE']
        
        # Approximate population weights
        pop_weights = [0.38, 0.23, 0.13, 0.11, 0.03, 0.04, 0.03, 0.02, 0.02, 0.01]
        
        df['province'] = np.random.choice(
            provinces,
            size=len(df),
            p=pop_weights
        )
        
        return df
    
    def _calculate_household_exposure(self, row: pd.Series) -> float:
        """
        Calculate household-level trade exposure intensity
        
        Returns value between 0 (no exposure) and 1 (maximum exposure)
        """
        industry = row.get('industry', 'retail_hospitality')
        province = row.get('province', 'ON')
        
        # Base industry exposure
        base_exposure = self.INDUSTRY_EXPOSURE.get(industry, 0.05)
        
        # Regional multiplier
        regional_industries = self.REGIONAL_EXPOSURE.get(province, {})
        regional_multiplier = regional_industries.get(industry, 1.0)
        
        # Combined exposure (capped at 1.0)
        exposure = min(base_exposure * (1 + regional_multiplier), 1.0)
        
        return exposure
    
    def _recalculate_financial_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Recalculate STIR and residual income after income shock"""
        # After-tax income (assume 75% of gross after shock)
        df['disposable_income_shocked'] = df['income_shocked'] * 0.75
        
        # Residual income (shelter costs unchanged in trade war)
        df['residual_income_shocked'] = (
            df['disposable_income_shocked'] - df['annual_shelter_cost']
        )
        
        # STIR
        df['STIR_shocked'] = (
            (df['monthly_shelter_cost'] * 12) / df['income_shocked'].clip(lower=1)
        ).clip(upper=10)
        
        return df
    
    def get_shock_summary(self) -> Dict:
        """Return shock parameters as dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'severity': self.severity,
            'tariff_rate': self.tariff_rate,
            'job_loss_rate': self.job_loss_rate,
            'wage_suppression': self.wage_suppression,
            'affected_industries': list(self.INDUSTRY_EXPOSURE.keys())
        }


if __name__ == "__main__":
    # Test trade war shock
    print("=== Trade War Shock Test ===\n")
    
    # Create synthetic household data
    n = 1000
    np.random.seed(42)
    
    df = pd.DataFrame({
        'annual_income': np.random.lognormal(11.0, 0.8, n).clip(20000, 200000),
        'monthly_shelter_cost': np.random.lognormal(7.0, 0.5, n).clip(500, 4000),
    })
    
    df['annual_shelter_cost'] = df['monthly_shelter_cost'] * 12
    
    # Apply shocks at different severities
    for severity in ['moderate', 'severe', 'extreme']:
        shock = TradeWarShock(severity=severity)
        df_shocked = shock.apply_shock(df.copy())
        
        print(f"\n{'='*60}")
        print(f"Severity: {severity.upper()}")
        print(f"{'='*60}")
        summary = shock.summary_statistics(df_shocked)
        for key, val in summary.items():
            if isinstance(val, float):
                if val < 1:
                    print(f"  {key}: {val:.2%}")
                else:
                    print(f"  {key}: {val:,.1f}")
            else:
                print(f"  {key}: {val}")
