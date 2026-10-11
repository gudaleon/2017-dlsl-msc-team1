"""Rent inflation shock"""
import pandas as pd
import numpy as np
from .base_shock import BaseShock

class RentInflationShock(BaseShock):
    def __init__(self, market_increase: float = 0.18):
        super().__init__("rent_inflation", f"Rent +{market_increase:.0%}")
        self.market_increase = market_increase
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
    
    def get_shock_summary(self) -> dict:
        return {'name': self.name, 'market_increase': self.market_increase}
