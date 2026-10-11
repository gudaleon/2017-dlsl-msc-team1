"""Compound multi-factor shock"""
import pandas as pd
from .base_shock import BaseShock

class CompoundShock(BaseShock):
    def __init__(self, shocks: list):
        super().__init__("compound", "Multi-factor shock")
        self.shocks = shocks
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        for shock in self.shocks:
            df = shock.apply_shock(df)
        return df
    
    def get_shock_summary(self) -> dict:
        return {'name': self.name, 'component_shocks': len(self.shocks)}
