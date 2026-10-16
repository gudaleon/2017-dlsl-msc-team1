"""
Complete 4-Wave Temporal Analysis: Canadian Housing Crisis (2006-2021)
15-year longitudinal analysis with 1.35M person-records
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime

# Publication style
sns.set_theme(style='whitegrid', context='paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10

# Canadian CPI for inflation adjustment (2021 base)
CPI_ADJUSTMENT = {
    2006: 1.276,  # 2006 dollars × 1.276 = 2021 dollars
    2011: 1.148,  # 2011 dollars × 1.148 = 2021 dollars
    2016: 1.082,  # 2016 dollars × 1.082 = 2021 dollars
    2021: 1.000   # Already in 2021 dollars
}

# MBM thresholds (single adult, national average)
MBM_THRESHOLDS = {
    2006: 13500,
    2011: 15000,
    2016: 17000,
    2021: 19728
}

def clean_and_load_census(file_path, year):
    """
    Load and clean Census file, handling year-specific quirks
    """
    print(f"\n{'='*70}")
    print(f"LOADING CENSUS {year}")
    print('='*70)
    
    print(f"Reading: {file_path}")
    df = pd.read_csv(file_path, low_memory=False)
    print(f"✓ Loaded {len(df):,} records, {len(df.columns)} columns")
    
    # Identify variables (names may differ across years)
    income_col = None
    shelter_col = None
    tenure_col = None
    cma_col = None
    
    for col in df.columns:
        if col in ['TOTINC', 'INCTOT', 'TOTINC_AT']:
            income_col = col
        if col in ['SHELCO', 'GROSRT', 'SHELTER']:
            shelter_col = col
        if col == 'TENUR':
            tenure_col = col
        if col == 'CMA':
            cma_col = col
    
    if not income_col or not shelter_col:
        print(f"⚠️  Missing required variables")
        return None
    
    print(f"  Income: {income_col}")
    print(f"  Shelter: {shelter_col}")
    
    # Clean data
    df['income_raw'] = pd.to_numeric(df[income_col], errors='coerce')
    df['shelter_raw'] = pd.to_numeric(df[shelter_col], errors='coerce')
    
    # Remove missing value codes (9999, 8888, etc.)
    df['shelter_raw'] = df['shelter_raw'].replace([8888, 9999, 99999], np.nan)
    
    # Keep valid records
    valid = (df['income_raw'] > 0) & (df['shelter_raw'].notna()) & (df['shelter_raw'] > 0) & (df['shelter_raw'] < 10000)
    df_clean = df[valid].copy()
    
    pct_valid = len(df_clean) / len(df) * 100
    print(f"  Valid records: {len(df_clean):,} ({pct_valid:.1f}%)")
    
    # Adjust for inflation to 2021 dollars
    adj_factor = CPI_ADJUSTMENT[year]
    df_clean['income'] = df_clean['income_raw'] * adj_factor
    df_clean['shelter_monthly'] = df_clean['shelter_raw'] * adj_factor
    
    print(f"  Inflation adjustment: ×{adj_factor:.3f} to 2021 dollars")
    print(f"  Median income: ${df_clean['income'].median():,.0f}")
    print(f"  Median shelter: ${df_clean['shelter_monthly'].median():,.0f}/month")
    
    # Calculate metrics
    df_clean['annual_shelter'] = df_clean['shelter_monthly'] * 12
    df_clean['residual_income'] = df_clean['income'] - df_clean['annual_shelter']
    df_clean['stir'] = (df_clean['shelter_monthly'] * 12) / df_clean['income']
    df_clean['stir'] = df_clean['stir'].clip(0, 2)
    
    # V2 Hardship (using year-specific MBM threshold)
    mbm_threshold = MBM_THRESHOLDS[year]
    df_clean['hardship'] = (df_clean['residual_income'] < mbm_threshold).astype(int)
    
    # Tenure
    if tenure_col:
        df_clean['is_owner'] = df[tenure_col] == 1
        df_clean['is_renter'] = df[tenure_col] == 2
    
    # CMA
    if cma_col:
        df_clean['cma_code'] = df[cma_col]
    
    df_clean['year'] = year
    
    print(f"✓ Census {year} processed successfully")
    
    return df_clean


def calculate_summary_stats(df, year):
    """
    Calculate comprehensive summary statistics for one year
    """
    results = {
        'year': year,
        'sample_size': int(len(df)),
        'income': {
            'mean': float(df['income'].mean()),
            'median': float(df['income'].median()),
            'p25': float(df['income'].quantile(0.25)),
            'p75': float(df['income'].quantile(0.75))
        },
        'shelter': {
            'mean': float(df['shelter_monthly'].mean()),
            'median': float(df['shelter_monthly'].median()),
            'p25': float(df['shelter_monthly'].quantile(0.25)),
            'p75': float(df['shelter_monthly'].quantile(0.75))
        },
        'stir': {
            'mean': float(df['stir'].mean()),
            'median': float(df['stir'].median()),
            'pct_above_30': float((df['stir'] > 0.30).mean() * 100),
            'pct_above_50': float((df['stir'] > 0.50).mean() * 100)
        },
        'hardship': {
            'rate_pct': float(df['hardship'].mean() * 100),
            'count': int(df['hardship'].sum())
        }
    }
    
    # Tenure breakdown
    if 'is_owner' in df.columns and 'is_renter' in df.columns:
        results['owner_hardship'] = float(df[df['is_owner']]['hardship'].mean() * 100)
        results['renter_hardship'] = float(df[df['is_renter']]['hardship'].mean() * 100)
    
    return results


def create_temporal_visualizations(all_data, all_results):
    """
    Generate comprehensive temporal trend visualizations
    """
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70)
    
    output_dir = Path('outputs/full_census_figures')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    years = sorted([r['year'] for r in all_results])
    
    # ========================================================================
    # FIGURE 1: National Trends Overview (4 panels)
    # ========================================================================
    print("\n[1/5] National trends overview...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('15-Year Housing Crisis Evolution: National Trends (2006-2021)',
                 fontsize=14, fontweight='bold')
    
    # Panel A: Income (inflation-adjusted)
    ax1 = axes[0, 0]
    mean_income = [all_results[i]['income']['mean'] for i in range(len(years))]
    median_income = [all_results[i]['income']['median'] for i in range(len(years))]
    
    ax1.plot(years, mean_income, marker='o', linewidth=2, markersize=8, label='Mean', color='#27ae60')
    ax1.plot(years, median_income, marker='s', linewidth=2, markersize=8, label='Median', color='#16a085')
    ax1.set_xlabel('Census Year')
    ax1.set_ylabel('Annual Income (2021 $)')
    ax1.set_title('A. Household Income (Inflation-Adjusted)')
    ax1.ticklabel_format(style='plain', axis='y')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Add growth rate annotation
    pct_change = (median_income[-1] / median_income[0] - 1) * 100
    ax1.text(0.05, 0.95, f'15-year change: {pct_change:+.1f}%',
            transform=ax1.transAxes, fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Panel B: Shelter Cost (inflation-adjusted)
    ax2 = axes[0, 1]
    mean_shelter = [all_results[i]['shelter']['mean'] for i in range(len(years))]
    median_shelter = [all_results[i]['shelter']['median'] for i in range(len(years))]
    
    ax2.plot(years, mean_shelter, marker='o', linewidth=2, markersize=8, label='Mean', color='#e74c3c')
    ax2.plot(years, median_shelter, marker='s', linewidth=2, markersize=8, label='Median', color='#c0392b')
    ax2.set_xlabel('Census Year')
    ax2.set_ylabel('Monthly Shelter Cost (2021 $)')
    ax2.set_title('B. Shelter Costs (Inflation-Adjusted)')
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # Add growth rate
    pct_change = (median_shelter[-1] / median_shelter[0] - 1) * 100
    ax2.text(0.05, 0.95, f'15-year change: {pct_change:+.1f}%',
            transform=ax2.transAxes, fontsize=9,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Panel C: Affordability Crisis (STIR >30%)
    ax3 = axes[1, 0]
    stir_30 = [all_results[i]['stir']['pct_above_30'] for i in range(len(years))]
    
    ax3.plot(years, stir_30, marker='o', linewidth=3, markersize=10, color='#f39c12')
    ax3.fill_between(years, 0, stir_30, alpha=0.2, color='#f39c12')
    ax3.axhline(30, color='red', linestyle='--', alpha=0.5, label='30% benchmark')
    ax3.set_xlabel('Census Year')
    ax3.set_ylabel('Percentage of Households (%)')
    ax3.set_title('C. Affordability Crisis Rate (STIR >30%)')
    ax3.legend()
    ax3.grid(alpha=0.3)
    
    # Panel D: Housing Hardship (V2 Residual Income)
    ax4 = axes[1, 1]
    hardship_rate = [all_results[i]['hardship']['rate_pct'] for i in range(len(years))]
    
    ax4.plot(years, hardship_rate, marker='o', linewidth=3, markersize=10, color='#c0392b')
    ax4.fill_between(years, 0, hardship_rate, alpha=0.3, color='#c0392b')
    ax4.set_xlabel('Census Year')
    ax4.set_ylabel('Hardship Rate (%)')
    ax4.set_title('D. V2 Housing Hardship (Residual Income < MBM)')
    ax4.grid(alpha=0.3)
    
    # Add change annotation
    pp_change = hardship_rate[-1] - hardship_rate[0]
    ax4.text(0.05, 0.95, f'15-year change: {pp_change:+.1f} pp',
            transform=ax4.transAxes, fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    fig1_path = output_dir / '08_fifteen_year_national_trends.png'
    plt.savefig(fig1_path, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {fig1_path}")
    
    # ========================================================================
    # FIGURE 2: Period Comparison (Which 5-year period was worst?)
    # ========================================================================
    print("[2/5] Period-over-period comparison...")
    
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    fig.suptitle('Period Comparison: Which 5-Year Interval Saw Worst Deterioration?',
                 fontsize=14, fontweight='bold')
    
    periods = [
        ('2006-2011', 0, 1),
        ('2011-2016', 1, 2),
        ('2016-2021', 2, 3)
    ]
    
    # Income change
    ax1 = axes[0]
    income_changes = []
    for name, i, j in periods:
        change = (all_results[j]['income']['median'] / all_results[i]['income']['median'] - 1) * 100
        income_changes.append(change)
    
    colors = ['#27ae60' if c > 0 else '#e74c3c' for c in income_changes]
    ax1.bar([p[0] for p in periods], income_changes, color=colors, edgecolor='black', linewidth=1.5)
    ax1.axhline(0, color='black', linestyle='-', linewidth=0.8)
    ax1.set_ylabel('Change (%)')
    ax1.set_title('Median Income Change')
    ax1.set_xticklabels([p[0] for p in periods], rotation=45, ha='right')
    ax1.grid(axis='y', alpha=0.3)
    
    # Shelter cost change
    ax2 = axes[1]
    shelter_changes = []
    for name, i, j in periods:
        change = (all_results[j]['shelter']['median'] / all_results[i]['shelter']['median'] - 1) * 100
        shelter_changes.append(change)
    
    ax2.bar([p[0] for p in periods], shelter_changes, color='#e74c3c', edgecolor='black', linewidth=1.5)
    ax2.axhline(0, color='black', linestyle='-', linewidth=0.8)
    ax2.set_ylabel('Change (%)')
    ax2.set_title('Median Shelter Cost Change')
    ax2.set_xticklabels([p[0] for p in periods], rotation=45, ha='right')
    ax2.grid(axis='y', alpha=0.3)
    
    # Hardship rate change
    ax3 = axes[2]
    hardship_changes = []
    for name, i, j in periods:
        change = all_results[j]['hardship']['rate_pct'] - all_results[i]['hardship']['rate_pct']
        hardship_changes.append(change)
    
    colors = ['#e74c3c' if c > 0 else '#27ae60' for c in hardship_changes]
    ax3.bar([p[0] for p in periods], hardship_changes, color=colors, edgecolor='black', linewidth=1.5)
    ax3.axhline(0, color='black', linestyle='-', linewidth=0.8)
    ax3.set_ylabel('Change (percentage points)')
    ax3.set_title('Hardship Rate Change')
    ax3.set_xticklabels([p[0] for p in periods], rotation=45, ha='right')
    ax3.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    fig2_path = output_dir / '09_period_comparison.png'
    plt.savefig(fig2_path, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {fig2_path}")
    
    # ========================================================================
    # FIGURE 3: Tenure Divergence
    # ========================================================================
    if all(('owner_hardship' in r and 'renter_hardship' in r) for r in all_results):
        print("[3/5] Tenure divergence analysis...")
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        fig.suptitle('Owner vs Renter Hardship: The Widening Gap (2006-2021)',
                     fontsize=14, fontweight='bold')
        
        owner_rates = [r['owner_hardship'] for r in all_results]
        renter_rates = [r['renter_hardship'] for r in all_results]
        gap = [r - o for r, o in zip(renter_rates, owner_rates)]
        
        ax.plot(years, owner_rates, marker='o', linewidth=2.5, markersize=10,
               label='Owners', color='#2ecc71')
        ax.plot(years, renter_rates, marker='s', linewidth=2.5, markersize=10,
               label='Renters', color='#e74c3c')
        
        # Shade the gap
        ax.fill_between(years, owner_rates, renter_rates, alpha=0.2, color='red')
        
        ax.set_xlabel('Census Year', fontsize=12)
        ax.set_ylabel('Hardship Rate (%)', fontsize=12)
        ax.set_title('Tenure Gap in Housing Hardship', fontsize=12)
        ax.legend(fontsize=11)
        ax.grid(alpha=0.3)
        
        # Add gap annotations
        for i, (year, g) in enumerate(zip(years, gap)):
            ax.text(year, (owner_rates[i] + renter_rates[i])/2, f'{g:.1f}pp',
                   ha='center', fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
        
        plt.tight_layout()
        fig3_path = output_dir / '10_tenure_divergence.png'
        plt.savefig(fig3_path, bbox_inches='tight')
        plt.close()
        print(f"   ✓ Saved: {fig3_path}")
    
    # ========================================================================
    # FIGURE 4: Income vs Shelter Squeeze
    # ========================================================================
    print("[4/5] Income-shelter squeeze visualization...")
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    fig.suptitle('The Great Squeeze: Income Stagnation vs Shelter Cost Inflation (2006-2021)',
                 fontsize=14, fontweight='bold')
    
    # Normalize to 2006 = 100
    income_index = [all_results[i]['income']['median'] / all_results[0]['income']['median'] * 100
                   for i in range(len(years))]
    shelter_index = [all_results[i]['shelter']['median'] / all_results[0]['shelter']['median'] * 100
                    for i in range(len(years))]
    
    ax.plot(years, income_index, marker='o', linewidth=3, markersize=12,
           label='Median Income (2021 $)', color='#27ae60')
    ax.plot(years, shelter_index, marker='s', linewidth=3, markersize=12,
           label='Median Shelter Cost (2021 $)', color='#e74c3c')
    ax.axhline(100, color='gray', linestyle='--', alpha=0.5, label='2006 baseline')
    
    ax.set_xlabel('Census Year', fontsize=12)
    ax.set_ylabel('Index (2006 = 100)', fontsize=12)
    ax.set_title('Real Income vs Real Shelter Costs', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(alpha=0.3)
    
    # Add final values
    ax.annotate(f'{income_index[-1]:.0f}', xy=(years[-1], income_index[-1]),
               xytext=(10, 0), textcoords='offset points', fontsize=10, fontweight='bold')
    ax.annotate(f'{shelter_index[-1]:.0f}', xy=(years[-1], shelter_index[-1]),
               xytext=(10, 0), textcoords='offset points', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    fig4_path = output_dir / '11_income_shelter_squeeze.png'
    plt.savefig(fig4_path, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {fig4_path}")
    
    # ========================================================================
    # FIGURE 5: Summary Dashboard
    # ========================================================================
    print("[5/5] Summary dashboard...")
    
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25)
    fig.suptitle('Canadian Housing Crisis: 15-Year Summary Dashboard (2006-2021)',
                 fontsize=16, fontweight='bold')
    
    # Panel 1: Hardship rate progression
    ax1 = fig.add_subplot(gs[0, :])
    ax1.bar(years, hardship_rate, color=['#f39c12', '#e67e22', '#e74c3c', '#c0392b'],
           edgecolor='black', linewidth=2, width=3)
    ax1.set_ylabel('Hardship Rate (%)', fontsize=11)
    ax1.set_title('Housing Hardship Evolution', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for i, (year, rate) in enumerate(zip(years, hardship_rate)):
        ax1.text(year, rate + 1, f'{rate:.1f}%', ha='center', fontsize=10, fontweight='bold')
    
    # Panel 2-5: Key metrics comparison
    metrics = [
        ('Median Income', [r['income']['median'] for r in all_results], '${:,.0f}', '#27ae60'),
        ('Median Shelter', [r['shelter']['median'] for r in all_results], '${:,.0f}/mo', '#e74c3c'),
        ('STIR >30%', [r['stir']['pct_above_30'] for r in all_results], '{:.1f}%', '#f39c12'),
        ('Owner Hardship', [r.get('owner_hardship', 0) for r in all_results], '{:.1f}%', '#2ecc71')
    ]
    
    for idx, (title, values, fmt, color) in enumerate(metrics):
        row = 1 + idx // 2
        col = idx % 2
        ax = fig.add_subplot(gs[row, col])
        
        ax.plot(years, values, marker='o', linewidth=2, markersize=8, color=color)
        ax.fill_between(years, 0, values, alpha=0.2, color=color)
        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.grid(alpha=0.3)
        
        # Add final value annotation
        final_val = fmt.format(values[-1])
        change_pct = (values[-1] / values[0] - 1) * 100 if values[0] > 0 else 0
        ax.text(0.95, 0.95, f'{final_val}\n({change_pct:+.1f}%)',
               transform=ax.transAxes, ha='right', va='top', fontsize=9,
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    fig5_path = output_dir / '12_summary_dashboard.png'
    plt.savefig(fig5_path, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Saved: {fig5_path}")
    
    print("\n✓ All visualizations generated")


def main():
    """
    Execute complete 4-wave temporal analysis
    """
    print("="*70)
    print("4-WAVE TEMPORAL ANALYSIS: 2006-2011-2016-2021")
    print("="*70)
    print(f"\nStart time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define census files
    census_files = [
        ('data/raw/census_2006_pumf.csv', 2006),
        ('data/raw/census_2011_nhs.csv', 2011),
        ('data/raw/census_2016_pumf.csv', 2016),
        ('data/raw/census_2021_full.csv', 2021)
    ]
    
    all_data = []
    all_results = []
    
    # Load and analyze each year
    for file_path, year in census_files:
        if not Path(file_path).exists():
            print(f"\n⚠️  File not found: {file_path}")
            continue
        
        df = clean_and_load_census(file_path, year)
        if df is not None:
            all_data.append(df)
            results = calculate_summary_stats(df, year)
            all_results.append(results)
    
    if len(all_results) < 2:
        print("\n❌ Need at least 2 years for temporal analysis")
        return
    
    # Generate visualizations
    create_temporal_visualizations(all_data, all_results)
    
    # Export results
    print("\n" + "="*70)
    print("EXPORTING RESULTS")
    print("="*70)
    
    output_json = Path('results/four_wave_temporal_results.json')
    output_json.parent.mkdir(exist_ok=True)
    
    export_data = {
        'analysis_date': datetime.now().isoformat(),
        'years_analyzed': len(all_results),
        'total_records': sum(r['sample_size'] for r in all_results),
        'results_by_year': all_results,
        'key_findings': {
            'income_growth_15yr': (all_results[-1]['income']['median'] / all_results[0]['income']['median'] - 1) * 100,
            'shelter_growth_15yr': (all_results[-1]['shelter']['median'] / all_results[0]['shelter']['median'] - 1) * 100,
            'hardship_change_15yr': all_results[-1]['hardship']['rate_pct'] - all_results[0]['hardship']['rate_pct']
        }
    }
    
    with open(output_json, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"✓ Saved: {output_json}")
    
    # Print summary
    print("\n" + "="*70)
    print("15-YEAR ANALYSIS COMPLETE")
    print("="*70)
    
    print(f"\nYears analyzed: {len(all_results)}")
    print(f"Total records: {export_data['total_records']:,}")
    print(f"\nKey findings:")
    print(f"  Income growth (15-year): {export_data['key_findings']['income_growth_15yr']:+.1f}%")
    print(f"  Shelter growth (15-year): {export_data['key_findings']['shelter_growth_15yr']:+.1f}%")
    print(f"  Hardship change (15-year): {export_data['key_findings']['hardship_change_15yr']:+.1f} percentage points")
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✅ Ready for Paper 1!")


if __name__ == '__main__':
    main()
