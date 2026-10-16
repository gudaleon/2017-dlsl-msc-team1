"""
AI Automation Unemployment Shock

Models labor market disruption from AI/automation:
- Occupation-specific displacement rates
- Wage suppression for remaining workers
- Skill-based vulnerability (routine vs non-routine tasks)
- Permanent vs temporary income loss
"""

import pandas as pd
import numpy as np
from typing import Dict
from .base_shock import BaseShock


class AIUnemploymentShock(BaseShock):
    """
    Models AI-driven unemployment and wage impacts
    
    Occupation Risk Tiers:
    - High Risk (50%+ displacement): Data entry, telemarketing, retail cashiers, truck drivers
    - Medium Risk (20-50%): Accounting clerks, paralegals, loan officers, customer service
    - Low Risk (<20%): Healthcare, skilled trades, creative professions, management
    """
    
    # Occupation displacement probabilities
    OCCUPATION_RISK = {
        'data_entry_clerk': 0.80,
        'telemarketer': 0.75,
        'retail_cashier': 0.70,
        'truck_driver': 0.60,
        'accounting_clerk': 0.55,
        'paralegal': 0.45,
        'loan_officer': 0.40,
        'customer_service': 0.35,
        'administrative': 0.30,
        'warehouse': 0.25,
        'teacher': 0.15,
        'nurse': 0.10,
        'electrician': 0.08,
        'manager': 0.05,
        'artist': 0.03,
    }
    
    def __init__(
        self,
        timeline: str = "5_year",  # '2_year', '5_year', '10_year'
        wage_suppression: float = 0.15,
        retraining_success_rate: float = 0.40
    ):
        super().__init__(
            name=f"ai_unemployment_{timeline}",
            description=f"AI automation shock ({timeline} timeline)"
        )
        
        self.timeline = timeline
        self.wage_suppression = wage_suppression
        self.retraining_success_rate = retraining_success_rate
        
        # Adjust displacement rates by timeline
        self.timeline_multiplier = {
            '2_year': 0.30,   # 30% of long-term risk realized
            '5_year': 0.60,   # 60% realized
            '10_year': 1.00   # Full risk realized
        }.get(timeline, 0.60)
    
    def apply_shock(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        print(f"\n=== Applying AI Unemployment Shock ({self.timeline}) ===")
        
        # Assign occupations
        if 'occupation' not in df.columns:
            df = self._assign_occupations(df)
        
        # Calculate displacement risk
        df['ai_displacement_risk'] = df['occupation'].map(self.OCCUPATION_RISK).fillna(0.10)
        df['ai_displacement_risk'] *= self.timeline_multiplier
        
        # Actual job loss
        df['ai_job_lost'] = np.random.random(len(df)) < df['ai_displacement_risk']
        
        # Income after shock
        df['income_shocked'] = df['annual_income'].copy()
        
        # Lost jobs: Some retrain successfully, others long-term unemployed
        retrained = df['ai_job_lost'] & (np.random.random(len(df)) < self.retraining_success_rate)
        long_term_unemployed = df['ai_job_lost'] & ~retrained
        
        # Retrained: 20% income loss (lower-skilled role)
        df.loc[retrained, 'income_shocked'] = df.loc[retrained, 'annual_income'] * 0.80
        
        # Long-term unemployed: Social assistance (~$15K/year)
        df.loc[long_term_unemployed, 'income_shocked'] = 15000
        
        # Workers who keep jobs: wage suppression due to labor surplus
        df.loc[~df['ai_job_lost'], 'income_shocked'] = (
            df.loc[~df['ai_job_lost'], 'annual_income'] * (1 - self.wage_suppression)
        )
        
        # Recalculate metrics
        df = self._recalculate_metrics(df)
        
        n_displaced = df['ai_job_lost'].sum()
        n_retrained = retrained.sum()
        
        print(f"✓ AI shock applied")
        print(f"  Jobs displaced: {n_displaced:,} ({n_displaced/len(df):.1%})")
        print(f"  Successfully retrained: {n_retrained:,} ({n_retrained/n_displaced:.1%} of displaced)")
        
        return df
    
    def _assign_occupations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Assign occupations based on Canadian labor force"""
        occupations = list(self.OCCUPATION_RISK.keys())
        
        # Approximate weights
        weights = [0.05, 0.02, 0.08, 0.04, 0.06, 0.02, 0.02, 0.10, 
                  0.12, 0.06, 0.08, 0.10, 0.05, 0.15, 0.05]
        
        df['occupation'] = np.random.choice(occupations, size=len(df), p=weights)
        return df
    
    def _recalculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Recalculate financial metrics"""
        df['disposable_income_shocked'] = df['income_shocked'] * 0.75
        df['residual_income_shocked'] = (
            df['disposable_income_shocked'] - df['annual_shelter_cost']
        )
        df['STIR_shocked'] = (
            (df['monthly_shelter_cost'] * 12) / df['income_shocked'].clip(lower=1)
        ).clip(upper=10)
        return df
    
    def get_shock_summary(self) -> Dict:
        return {
            'name': self.name,
            'timeline': self.timeline,
            'timeline_multiplier': self.timeline_multiplier,
            'wage_suppression': self.wage_suppression,
            'retraining_success_rate': self.retraining_success_rate
        }
