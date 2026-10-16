"""
Full Analysis Pipeline for CA-13 Housing Vulnerability Study
Runs complete V2+V3 analysis on 361,915 person Census PUMF
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from data_loading.census_loader import CensusLoader
from data_loading.sfs_loader import SFSLoader
from imputation.asset_imputer import AssetImputer

def run_full_analysis():
    """Execute complete V2 + V3 pipeline on full Census data"""
    
    print("="*70)
    print("CA-13 HOUSING VULNERABILITY FULL ANALYSIS")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # ========================================================================
    # PHASE 1: Load Full Census PUMF
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 1: Loading Full Census 2021 PUMF")
    print("="*70)
    
    census_path = 'data/raw/census_2021_full.csv'
    loader = CensusLoader()
    
    print(f"\nLoading: {census_path}")
    df = loader.load_census_pumf(census_path)
    
    print(f"\n✓ Loaded {len(df):,} person records")
    print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # ========================================================================
    # PHASE 2: Calculate Baseline Metrics
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 2: Calculating Baseline Housing Metrics")
    print("="*70)
    
    df = loader.calculate_baseline_metrics(df)
    
    # Quick baseline stats
    if 'STIR' in df.columns:
        print("\nBaseline STIR Distribution:")
        print(f"  Mean: {df['STIR'].mean():.3f}")
        print(f"  Median: {df['STIR'].median():.3f}")
        print(f"  >30% (affordability threshold): {(df['STIR'] > 0.30).sum():,} ({(df['STIR'] > 0.30).mean()*100:.1f}%)")
    
    # ========================================================================
    # PHASE 3: Load SFS and Impute Assets
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 3: Asset Imputation from Survey of Financial Security")
    print("="*70)
    
    # Check if SFS synthetic file exists
    sfs_path = Path('data/raw/sfs_synthetic.csv')
    if not sfs_path.exists():
        print("\n⚠ Creating synthetic SFS data (real SFS not available yet)")
        sfs_loader = SFSLoader()
        sfs_data = sfs_loader._create_synthetic_sfs(n=5000)
    else:
        print(f"\nLoading SFS from: {sfs_path}")
        sfs_data = pd.read_csv(sfs_path)
    
    print(f"✓ SFS sample size: {len(sfs_data):,} households")
    
    # Impute assets
    print("\nImputing liquid assets to Census households...")
    imputer = AssetImputer(sfs_data)
    df_enriched = imputer.impute_assets(df)
    
    # Check imputation results
    if 'liquid_assets_imputed' in df_enriched.columns:
        print("\n✓ Asset imputation complete")
        print(f"  Mean liquid assets: ${df_enriched['liquid_assets_imputed'].mean():,.0f}")
        print(f"  Median liquid assets: ${df_enriched['liquid_assets_imputed'].median():,.0f}")
        print(f"  Zero assets: {(df_enriched['liquid_assets_imputed'] == 0).sum():,} ({(df_enriched['liquid_assets_imputed'] == 0).mean()*100:.1f}%)")
    
    # ========================================================================
    # PHASE 4: MBM Threshold Matching (Simplified for now)
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 4: MBM Threshold Matching")
    print("="*70)
    
    # Use simplified national MBM threshold for demonstration
    # Real implementation would use config/mbm_thresholds_2018_2020.csv
    national_mbm_single = 19728  # 2020 reference person
    
    # Simple family size adjustment (actual MBM uses detailed equivalization)
    df_enriched['family_size'] = 1  # Placeholder - would come from Census EF structure
    df_enriched['mbm_threshold'] = national_mbm_single * np.sqrt(df_enriched['family_size'])
    
    print(f"\n✓ MBM thresholds assigned")
    print(f"  Mean threshold: ${df_enriched['mbm_threshold'].mean():,.0f}")
    
    # ========================================================================
    # PHASE 5: Hardship Calculation (V2 Baseline)
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 5: V2 Housing Hardship (CMHC Residual Income)")
    print("="*70)
    
    # Calculate residual income
    # Residual Income = After-tax Income - (12 * Monthly Shelter Cost)
    
    # Get income and shelter cost columns (exact names depend on Census PUMF structure)
    income_col = None
    shelter_col = None
    
    for col in df_enriched.columns:
        if 'income' in col.lower() or 'totinc' in col.lower():
            income_col = col
        if 'shelter' in col.lower() or 'shelco' in col.lower():
            shelter_col = col
    
    if income_col and shelter_col:
        # Calculate residual income
        df_enriched['annual_shelter_cost'] = df_enriched[shelter_col] * 12
        df_enriched['residual_income'] = df_enriched[income_col] - df_enriched['annual_shelter_cost']
        
        # V2 Hardship flag: Residual income < MBM threshold
        df_enriched['v2_hardship'] = (df_enriched['residual_income'] < df_enriched['mbm_threshold']).astype(int)
        
        print(f"\n✓ V2 hardship calculation complete")
        print(f"  Hardship rate: {df_enriched['v2_hardship'].mean()*100:.2f}%")
        print(f"  Households in hardship: {df_enriched['v2_hardship'].sum():,}")
    else:
        print("\n⚠ Could not identify income/shelter columns - skipping hardship calc")
        df_enriched['residual_income'] = 0
        df_enriched['v2_hardship'] = 0
    
    # ========================================================================
    # PHASE 6: Liquidity Analysis (V3 Asset-Augmented)
    # ========================================================================
    print("\n" + "="*70)
    print("PHASE 6: V3 Liquidity Buffer Analysis")
    print("="*70)
    
    # Calculate monthly deficit for hardship households
    df_enriched['monthly_deficit'] = np.maximum(
        0, 
        (df_enriched['mbm_threshold'] - df_enriched['residual_income']) / 12
    )
    
    # Calculate months to default (avoid division by zero)
    df_enriched['months_to_default'] = np.where(
        df_enriched['monthly_deficit'] > 0,
        df_enriched['liquid_assets_imputed'] / df_enriched['monthly_deficit'],
        999  # No deficit = no risk
    )
    
    # Cap at 24 months for analysis
    df_enriched['months_to_default'] = np.minimum(df_enriched['months_to_default'], 24)
    
    # Categorize liquidity risk
    def categorize_liquidity(months):
        if months == 0:
            return 'Zero buffer'
        elif months < 3:
            return '<3 months'
        elif months < 6:
            return '3-6 months'
        elif months < 12:
            return '6-12 months'
        else:
            return '>12 months'
    
    df_enriched['liquidity_category'] = df_enriched['months_to_default'].apply(categorize_liquidity)
    
    print("\n✓ Liquidity analysis complete")
    print("\nLiquidity Distribution (hardship households only):")
    hardship_only = df_enriched[df_enriched['v2_hardship'] == 1]
    if len(hardship_only) > 0:
        liquidity_dist = hardship_only['liquidity_category'].value_counts(normalize=True).sort_index()
        for cat, pct in liquidity_dist.items():
            print(f"  {cat:>15}: {pct*100:>5.1f}%")
    
    # ========================================================================
    # PHASE 7: Summary Statistics
    # ========================================================================
    print("\n" + "="*70)
    print("FINAL RESULTS SUMMARY")
    print("="*70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'sample_size': len(df_enriched),
        'baseline': {
            'mean_stir': float(df_enriched.get('STIR', pd.Series([np.nan])).mean()),
            'pct_stir_above_30': float((df_enriched.get('STIR', pd.Series([0])) > 0.30).mean() * 100)
        },
        'v2_hardship': {
            'rate_pct': float(df_enriched['v2_hardship'].mean() * 100),
            'count': int(df_enriched['v2_hardship'].sum()),
            'mean_residual_income': float(df_enriched['residual_income'].mean())
        },
        'v3_assets': {
            'mean_liquid_assets': float(df_enriched['liquid_assets_imputed'].mean()),
            'median_liquid_assets': float(df_enriched['liquid_assets_imputed'].median()),
            'pct_zero_assets': float((df_enriched['liquid_assets_imputed'] == 0).mean() * 100)
        },
        'liquidity_risk': {}
    }
    
    if len(hardship_only) > 0:
        for cat in ['Zero buffer', '<3 months', '3-6 months', '6-12 months', '>12 months']:
            count = (hardship_only['liquidity_category'] == cat).sum()
            pct = (hardship_only['liquidity_category'] == cat).mean() * 100
            results['liquidity_risk'][cat] = {
                'count': int(count),
                'pct_of_hardship': float(pct)
            }
    
    print("\n📊 KEY FINDINGS:")
    print(f"   Sample size: {results['sample_size']:,} persons")
    print(f"   V2 hardship rate: {results['v2_hardship']['rate_pct']:.2f}%")
    print(f"   Mean liquid assets: ${results['v3_assets']['mean_liquid_assets']:,.0f}")
    print(f"   Households with zero buffer: {results['liquidity_risk'].get('Zero buffer', {}).get('count', 0):,}")
    
    # ========================================================================
    # PHASE 8: Save Results
    # ========================================================================
    print("\n" + "="*70)
    print("SAVING RESULTS")
    print("="*70)
    
    output_dir = Path('results/full_census_362k')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save enriched data (compressed)
    output_file = output_dir / 'census_enriched_full.parquet'
    print(f"\nSaving enriched data to: {output_file}")
    df_enriched.to_parquet(output_file, compression='gzip', index=False)
    print(f"✓ Saved {len(df_enriched):,} records ({output_file.stat().st_size / 1024**2:.1f} MB)")
    
    # Save summary JSON
    json_file = output_dir / 'analysis_results.json'
    with open(json_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Saved summary to: {json_file}")
    
    # Save sample preview
    preview_file = output_dir / 'preview_first_1000.csv'
    df_enriched.head(1000).to_csv(preview_file, index=False)
    print(f"✓ Saved preview to: {preview_file}")
    
    print("\n" + "="*70)
    print("✓ ANALYSIS COMPLETE")
    print("="*70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nResults saved to: {output_dir.absolute()}")
    print("\nNext steps:")
    print("  1. Review results/full_census_362k/analysis_results.json")
    print("  2. Generate publication figures")
    print("  3. Run macroeconomic shock scenarios")
    print("  4. Create comprehensive report")
    
    return df_enriched, results


if __name__ == '__main__':
    df_final, results = run_full_analysis()
