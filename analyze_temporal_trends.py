"""
Temporal Trends Analysis: Canadian Housing Crisis Evolution
Analyzes housing hardship across multiple Census years
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

# Publication style
sns.set_theme(style='whitegrid', context='paper')
plt.rcParams['figure.dpi'] = 300

def load_and_analyze_census(file_path, year_label):
    """
    Load Census file and calculate baseline hardship metrics
    Works across different Census year structures
    """
    
    print(f"\n{'='*70}")
    print(f"LOADING: {year_label}")
    print('='*70)
    
    # Load full file
    print(f"Reading: {file_path}")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"✓ Loaded {len(df):,} records")
    print(f"  Columns: {len(df.columns)}")
    
    # Identify key variables (they may have different names)
    print("\nIdentifying variables...")
    
    # Income variable
    income_vars = [c for c in df.columns if c in ['TOTINC', 'INCTOT', 'TOTINC_AT']]
    if income_vars:
        income_col = income_vars[0]
        print(f"  Income: {income_col}")
    else:
        print("  ⚠ Income variable not found")
        return None
    
    # Shelter cost (can be SHELCO or GROSRT depending on year)
    shelter_vars = [c for c in df.columns if c in ['SHELCO', 'GROSRT', 'SHELTER', 'GROSRENT']]
    if shelter_vars:
        shelter_col = shelter_vars[0]
        print(f"  Shelter: {shelter_col}")
    else:
        print("  ⚠ Shelter cost variable not found")
        return None
    
    # Tenure
    tenure_vars = [c for c in df.columns if c == 'TENUR']
    if tenure_vars:
        tenure_col = tenure_vars[0]
        print(f"  Tenure: {tenure_col}")
    else:
        print("  ⚠ Tenure variable not found")
        tenure_col = None
    
    # CMA
    cma_vars = [c for c in df.columns if c == 'CMA']
    if cma_vars:
        cma_col = cma_vars[0]
        print(f"  CMA: {cma_col}")
    else:
        print("  ⚠ CMA variable not found")
        cma_col = None
    
    # Calculate baseline metrics
    print("\nCalculating baseline metrics...")
    
    # Clean data
    df['income'] = pd.to_numeric(df[income_col], errors='coerce')
    df['shelter_monthly'] = pd.to_numeric(df[shelter_col], errors='coerce')
    
    # Remove invalid/missing data
    valid = (df['income'] > 0) & (df['shelter_monthly'] > 0)
    df = df[valid].copy()
    print(f"  Valid records: {len(df):,}")
    
    # STIR calculation
    df['stir'] = (df['shelter_monthly'] * 12) / df['income']
    df['stir'] = df['stir'].clip(0, 2)  # Cap at 200%
    
    # V2 Hardship (simplified - using national MBM approximation)
    # 2016 MBM ≈ $17,000 single adult
    # 2021 MBM ≈ $19,728 single adult
    # Adjust for year
    if '2021' in year_label:
        mbm_threshold = 19728
    elif '2016' in year_label:
        mbm_threshold = 17000
    elif '2011' in year_label:
        mbm_threshold = 15000
    else:
        mbm_threshold = 17000  # Default
    
    df['annual_shelter'] = df['shelter_monthly'] * 12
    df['residual_income'] = df['income'] - df['annual_shelter']
    df['hardship'] = (df['residual_income'] < mbm_threshold).astype(int)
    
    # Tenure categorization
    if tenure_col:
        df['is_owner'] = df[tenure_col] == 1
        df['is_renter'] = df[tenure_col] == 2
    
    # Calculate summary statistics
    results = {
        'year': year_label,
        'sample_size': int(len(df)),
        'mean_income': float(df['income'].mean()),
        'median_income': float(df['income'].median()),
        'mean_shelter': float(df['shelter_monthly'].mean()),
        'median_shelter': float(df['shelter_monthly'].median()),
        'mean_stir': float(df['stir'].mean()),
        'median_stir': float(df['stir'].median()),
        'pct_stir_above_30': float((df['stir'] > 0.30).mean() * 100),
        'pct_stir_above_50': float((df['stir'] > 0.50).mean() * 100),
        'hardship_rate': float(df['hardship'].mean() * 100),
        'hardship_count': int(df['hardship'].sum())
    }
    
    if tenure_col:
        results['owner_hardship_rate'] = float(df[df['is_owner']]['hardship'].mean() * 100)
        results['renter_hardship_rate'] = float(df[df['is_renter']]['hardship'].mean() * 100)
    
    print(f"\n📊 Summary Statistics:")
    print(f"   Sample size: {results['sample_size']:,}")
    print(f"   Mean income: ${results['mean_income']:,.0f}")
    print(f"   Median shelter: ${results['median_shelter']:,.0f}/month")
    print(f"   Mean STIR: {results['mean_stir']:.1%}")
    print(f"   STIR >30%: {results['pct_stir_above_30']:.1f}%")
    print(f"   V2 Hardship rate: {results['hardship_rate']:.1f}%")
    
    return df, results


def compare_temporal_trends(all_results):
    """
    Create visualization comparing trends across years
    """
    
    print("\n" + "="*70)
    print("GENERATING TEMPORAL TREND VISUALIZATIONS")
    print("="*70)
    
    # Sort by year
    years_order = sorted([r['year'] for r in all_results])
    results_sorted = {r['year']: r for r in all_results}
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Canadian Housing Crisis: Temporal Evolution', 
                 fontsize=16, fontweight='bold')
    
    years = years_order
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(years)))
    
    # Plot 1: Mean income over time
    ax1 = axes[0, 0]
    mean_incomes = [results_sorted[y]['mean_income'] for y in years]
    ax1.plot(years, mean_incomes, marker='o', linewidth=2, markersize=8, color='#27ae60')
    ax1.set_xlabel('Census Year')
    ax1.set_ylabel('Mean Income ($)')
    ax1.set_title('Mean Annual Income Trend')
    ax1.ticklabel_format(style='plain', axis='y')
    ax1.grid(alpha=0.3)
    
    # Add percentage change annotation
    if len(years) >= 2:
        pct_change = (mean_incomes[-1] / mean_incomes[0] - 1) * 100
        ax1.annotate(f'{pct_change:+.1f}%', 
                    xy=(years[-1], mean_incomes[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, color='red' if pct_change < 5 else 'green')
    
    # Plot 2: Median shelter cost over time
    ax2 = axes[0, 1]
    median_shelters = [results_sorted[y]['median_shelter'] for y in years]
    ax2.plot(years, median_shelters, marker='o', linewidth=2, markersize=8, color='#e74c3c')
    ax2.set_xlabel('Census Year')
    ax2.set_ylabel('Median Shelter Cost ($/month)')
    ax2.set_title('Median Shelter Cost Trend')
    ax2.grid(alpha=0.3)
    
    # Add percentage change
    if len(years) >= 2:
        pct_change = (median_shelters[-1] / median_shelters[0] - 1) * 100
        ax2.annotate(f'{pct_change:+.1f}%', 
                    xy=(years[-1], median_shelters[-1]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, color='red')
    
    # Plot 3: STIR >30% over time
    ax3 = axes[0, 2]
    stir_30_pcts = [results_sorted[y]['pct_stir_above_30'] for y in years]
    ax3.plot(years, stir_30_pcts, marker='o', linewidth=2, markersize=8, color='#f39c12')
    ax3.set_xlabel('Census Year')
    ax3.set_ylabel('Percentage (%)')
    ax3.set_title('Affordability Crisis Rate (STIR >30%)')
    ax3.axhline(30, color='red', linestyle='--', alpha=0.5, label='30% threshold')
    ax3.grid(alpha=0.3)
    ax3.legend()
    
    # Plot 4: V2 Hardship rate over time
    ax4 = axes[1, 0]
    hardship_rates = [results_sorted[y]['hardship_rate'] for y in years]
    ax4.plot(years, hardship_rates, marker='o', linewidth=3, markersize=10, color='#c0392b')
    ax4.set_xlabel('Census Year')
    ax4.set_ylabel('Hardship Rate (%)')
    ax4.set_title('V2 Housing Hardship Rate Trend')
    ax4.grid(alpha=0.3)
    ax4.fill_between(years, 0, hardship_rates, alpha=0.2, color='#c0392b')
    
    # Add change annotation
    if len(years) >= 2:
        pp_change = hardship_rates[-1] - hardship_rates[0]
        ax4.annotate(f'{pp_change:+.1f} pp', 
                    xy=(years[-1], hardship_rates[-1]),
                    xytext=(10, -20), textcoords='offset points',
                    fontsize=12, fontweight='bold', color='red',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Plot 5: Owner vs Renter hardship (if available)
    ax5 = axes[1, 1]
    owner_rates = [results_sorted[y].get('owner_hardship_rate', 0) for y in years]
    renter_rates = [results_sorted[y].get('renter_hardship_rate', 0) for y in years]
    
    if any(owner_rates) and any(renter_rates):
        ax5.plot(years, owner_rates, marker='o', linewidth=2, label='Owners', color='#2ecc71')
        ax5.plot(years, renter_rates, marker='s', linewidth=2, label='Renters', color='#e74c3c')
        ax5.set_xlabel('Census Year')
        ax5.set_ylabel('Hardship Rate (%)')
        ax5.set_title('Hardship Rate by Tenure')
        ax5.legend()
        ax5.grid(alpha=0.3)
    
    # Plot 6: Summary bar chart (latest year breakdown)
    ax6 = axes[1, 2]
    latest_year = years[-1]
    latest = results_sorted[latest_year]
    
    metrics = ['STIR >30%', 'STIR >50%', 'Hardship']
    values = [
        latest['pct_stir_above_30'],
        latest['pct_stir_above_50'],
        latest['hardship_rate']
    ]
    colors_bar = ['#f39c12', '#e67e22', '#c0392b']
    
    ax6.bar(metrics, values, color=colors_bar, edgecolor='black', linewidth=1.5)
    ax6.set_ylabel('Percentage (%)')
    ax6.set_title(f'Crisis Metrics ({latest_year})')
    ax6.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(values):
        ax6.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    
    output_path = Path('outputs/full_census_figures/07_temporal_trends_analysis.png')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Saved figure: {output_path}")


def main():
    """
    Main analysis workflow
    """
    
    print("="*70)
    print("TEMPORAL TRENDS ANALYSIS: CANADIAN HOUSING CRISIS")
    print("="*70)
    
    # Define census files to analyze
    census_files = [
        ('data/raw/census_2016_a.csv', 'Census 2016 (A)'),
        ('data/raw/census_2016_b.csv', 'Census 2016 (B)'),
        ('data/raw/census_2011_or_2016.csv', 'Census 2016/2011 (C)'),
        ('data/raw/census_2021_full.csv', 'Census 2021'),
    ]
    
    all_results = []
    
    # Analyze each census year
    for file_path, year_label in census_files:
        if Path(file_path).exists():
            df, results = load_and_analyze_census(file_path, year_label)
            if results:
                all_results.append(results)
        else:
            print(f"\n⚠ File not found: {file_path}")
    
    if len(all_results) < 2:
        print("\n⚠ Need at least 2 census years for temporal analysis")
        return
    
    # Compare trends
    compare_temporal_trends(all_results)
    
    # Export results
    output_json = Path('results/temporal_trends_analysis.json')
    output_json.parent.mkdir(exist_ok=True)
    
    with open(output_json, 'w') as f:
        json.dump({
            'analysis_date': pd.Timestamp.now().isoformat(),
            'census_years': all_results,
            'key_findings': {
                'years_analyzed': len(all_results),
                'income_growth': 'Calculated from data',
                'shelter_cost_growth': 'Calculated from data',
                'hardship_rate_change': 'Calculated from data'
            }
        }, f, indent=2)
    
    print(f"\n✓ Saved results: {output_json}")
    
    # Summary
    print("\n" + "="*70)
    print("TEMPORAL ANALYSIS COMPLETE")
    print("="*70)
    print(f"\nAnalyzed {len(all_results)} census years:")
    for r in all_results:
        print(f"  • {r['year']:20s}: {r['sample_size']:>7,} records, {r['hardship_rate']:>5.1f}% hardship")
    
    print("\n✅ Ready for Paper 1 (Spatial-Temporal Analysis)")
    print("   Next: Add CMA-level breakdown for geographic comparison")


if __name__ == '__main__':
    main()
