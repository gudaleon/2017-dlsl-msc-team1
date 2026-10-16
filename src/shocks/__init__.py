"""
Macroeconomic shock scenario modules
"""

from .base_shock import BaseShock
from .mortgage_shock import MortgageRateShock
from .rent_shock import RentInflationShock
from .trade_war_shock import TradeWarShock
from .ai_unemployment_shock import AIUnemploymentShock
from .immigration_shock import ImmigrationRentSurgeShock
from .compound_shock import CompoundShock

__all__ = [
    'BaseShock',
    'MortgageRateShock',
    'RentInflationShock',
    'TradeWarShock',
    'AIUnemploymentShock',
    'ImmigrationRentSurgeShock',
    'CompoundShock'
]
