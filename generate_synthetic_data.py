"""
Generate synthetic Census data for testing V2 baseline pipeline
"""
import numpy as np
import pandas as pd
from pathlib import Path

print("="*60)
print("GENERATING SYNTHETIC CENSUS DATA FOR DEMO")
print("="*60)

np.random.seed(42)

# Generate households first
n_households = 3000
households = []

for hh_id in range(1, n_households + 1):
    hh_size = np.random.choice([1, 2, 3, 4, 5], p=[0.28, 0.33, 0.15, 0.15, 0.09])
    
    # Household-level attributes
    shelco = int(np.random.gamma(3, 400))
    cma = np.random.choice([462, 535, 825, 835, 933, 999], p=[0.15, 0.25, 0.1, 0.08, 0.12, 0.3])
    pr = np.random.choice([24, 35, 48, 59, 70], p=[0.25, 0.38, 0.12, 0.15, 0.1])
    weight = np.random.randint(10, 200)
    
    # Decide economic family structure
    if hh_size == 1:
        n_families = 1
    elif np.random.random() < 0.85:
        n_families = 1
    else:
        n_families = 2
    
    # Generate persons
    persons_added = 0
    for ef_idx in range(n_families):
        ef_id = hh_id * 100 + ef_idx
        
        if n_families == 1:
            family_size = hh_size
        else:
            family_size = max(1, hh_size // n_families)
        
        # Economic family disposable income (same for all members)
        efdimbm = int(np.random.gamma(5, 10000))
        
        for person_idx in range(family_size):
            if persons_added >= hh_size:
                break
                
            pp_id = hh_id * 10 + persons_added + 1
            
            # Person attributes
            agegrp = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8], p=[0.05, 0.05, 0.08, 0.15, 0.20, 0.22, 0.15, 0.10])
            
            # Total income (N/A for children)
            if agegrp <= 2:  # Age 0-14
                totinc = 99_999_999
            else:
                totinc = int(np.random.gamma(5, 8000))
            
            # EF_RP: 1=reference, 2=member
            if person_idx == 0:
                ef_rp = 1
            else:
                ef_rp = 2
            
            # PRIHM
            prihm = 1 if persons_added == 0 else 2
            
            tenur = np.random.choice([1, 2, 3], p=[0.65, 0.08, 0.27])
            
            households.append({
                'HH_ID': hh_id,
                'PP_ID': pp_id,
                'EF_ID': ef_id,
                'EF_RP': ef_rp,
                'PRIHM': prihm,
                'AGEGRP': agegrp,
                'TOTINC': totinc,
                'EFDIMBM_2018': efdimbm,
                'SHELCO': shelco,
                'TENUR': tenur,
                'CMA': cma,
                'PR': pr,
                'WEIGHT': weight,
            })
            
            persons_added += 1

# Add some unattached persons in multi-person households
for _ in range(200):
    hh_id = np.random.randint(1, n_households + 1)
    pp_id = 90000 + _
    
    households.append({
        'HH_ID': hh_id,
        'PP_ID': pp_id,
        'EF_ID': 99900 + _,
        'EF_RP': 3,  # Unattached
        'PRIHM': 2,
        'AGEGRP': np.random.choice([5, 6, 7, 8]),
        'TOTINC': int(np.random.gamma(4, 7000)),
        'EFDIMBM_2018': int(np.random.gamma(4, 6500)),
        'SHELCO': int(np.random.gamma(3, 400)),
        'TENUR': np.random.choice([1, 2, 3]),
        'CMA': np.random.choice([462, 535, 825, 835, 933, 999]),
        'PR': np.random.choice([24, 35, 48, 59, 70]),
        'WEIGHT': np.random.randint(10, 200),
    })

person_df = pd.DataFrame(households)

print(f"\n✓ Generated {len(person_df):,} person records")
print(f"  Unique households: {person_df['HH_ID'].nunique():,}")
print(f"  Unique economic families: {person_df['EF_ID'].nunique():,}")
print(f"  Persons in families: {(person_df['EF_RP'] != 3).sum():,}")
print(f"  Unattached persons: {(person_df['EF_RP'] == 3).sum():,}")

# Save
Path('data/raw').mkdir(parents=True, exist_ok=True)
person_df.to_csv('data/raw/synthetic_census.csv', index=False)
print(f"\n✓ Saved to data/raw/synthetic_census.csv")

print("\n" + "="*60)
print("SYNTHETIC DATA READY")
print("="*60)
