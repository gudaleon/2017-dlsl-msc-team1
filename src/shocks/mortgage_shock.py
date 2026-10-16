"""Mortgage rate shock - basic implementation"""
import pandas as pd
import numpy as np
from .base_shock import BaseShock

class MortgageRateShock(BaseShock):
    def __init__(self, rate_increase_bps: int = 400):
        super().__init__("mortgage_rate", f"Mortgage rate +{rate_increase_bps}bps")
        self.rate_increase = rate_increase_bps / 10000
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['is_renewing'] = False
        if 'is_owner' in df.columns:
            owners = df['is_owner']
            df.loc[owners, 'is_renewing'] = np.random.random(owners.sum()) < 0.20
        return df
    
    def get_shock_summary(self) -> dict:
        return {'name': self.name, 'rate_increase_bps': int(self.rate_increase * 10000)}
