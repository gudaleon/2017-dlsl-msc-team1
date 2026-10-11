"""Immigration-driven rent surge"""
import pandas as pd
from .base_shock import BaseShock

class ImmigrationRentSurgeShock(BaseShock):
    def __init__(self, rent_surge_pct: float = 0.25):
        super().__init__("immigration_rent", f"Immigration rent +{rent_surge_pct:.0%}")
        self.rent_surge = rent_surge_pct
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
    
    def get_shock_summary(self) -> dict:
        return {'name': self.name}
