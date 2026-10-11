# CA-13 Housing Vulnerability Microsimulation

**From Shelter Ratios to Residual Income: A Disaggregate Analysis of Housing Hardship and Macroeconomic Shocks in Canada Using 2021 Census Microdata**

## Project Overview

This project implements a vectorized microsimulation engine to analyze housing vulnerability across Canadian households under various macroeconomic shock scenarios. Unlike traditional 30% shelter-cost-to-income ratio (STIR) metrics, this framework uses a **residual income approach** to identify households at risk of material deprivation.

### Key Innovation

- **Residual Income Framework**: Measures post-shelter income against Market Basket Measure (MBM) poverty thresholds
- **Dual-Shock Modeling**: Simultaneous mortgage renewal rate hikes and rental market inflation
- **Statistical Asset Imputation**: Links Survey of Financial Security (SFS) wealth data to Census households
- **Multi-Scenario Testing**: Flexible framework for modeling trade wars, AI unemployment, immigration-driven rent surges, and compound shocks
- **Demographic Stratification**: Tracks vulnerability across 7 high-risk cohorts

## Data Sources

### Primary Dataset
- **2021 Census Public Use Microdata File (PUMF)**: ~930,000 anonymized household records
  - Income, shelter costs, demographics, tenure, mobility

### Secondary Sources
- **Survey of Financial Security (SFS) 2023**: Assets, debts, net worth for statistical imputation
- **Survey of Household Spending (SHS) 2023**: Non-shelter expenditure patterns
- **Market Basket Measure (MBM) Thresholds**: Regional poverty lines by family size
- **Canadian Housing Survey (CHS) 2024**: Validation and calibration data
- **Bank of Canada Parameters**: Mortgage renewal schedules and rate shock scenarios

## Architecture

### Four-Step Pipeline

1. **Baseline Snapshot**
   - Load Census PUMF microdata
   - Calculate pre-shock STIR and residual income
   - Benchmark against MBM poverty lines

2. **Exposure Masks**
   - `is_renewing`: 20% of mortgagors facing rate resets
   - `is_market_exposed`: Recent movers (MOB5) facing unconstrained rent inflation
   - Cohort filters: Lone parents, seniors, newcomers, Indigenous, racialized, disabled, young renters

3. **Vectorized Shock Application**
   - Mortgage recalculation with shocked rates
   - Rent recalculation (market vs rent-controlled)
   - Income adjustments by shock scenario
   - Asset buffer depletion modeling

4. **Delta Analysis**
   - Threshold crossing counts
   - Liquidity buffer exhaustion timelines
   - Distributional impact metrics

### Shock Scenarios

#### Scenario 1: Mortgage Rate Shock
- Bank of Canada rate hikes (+400 bps)
- 5-year renewal waves (20% annual exposure)

#### Scenario 2: Trade War (Canada-USA)
- Export sector job losses (auto, lumber, agriculture)
- Regional concentration effects
- Income shocks by industry

#### Scenario 3: AI Automation Unemployment
- Occupation-specific displacement rates
- Middle-skill wage suppression
- Permanent vs temporary income loss

#### Scenario 4: Immigration-Driven Rent Surge
- Population growth → vacancy collapse
- CMA-specific rent inflation (Toronto, Vancouver)
- Differential impact on mobile vs sitting tenants

#### Scenario 5: Compound Shocks
- Multi-factor stress tests
- Worst-case scenario combinations

## Analytical Outputs

### Inequality Metrics
- **Residual Income Gini**: Post-shelter income inequality expansion
- **Disproportionality Index (DI)**: Cohort over-representation in distress
- **Depth of Poverty Gap (D)**: Dollar deficit below MBM survival line

### Key Deliverables
1. **Non-linear Elasticity Curves**: Tipping points where shocks cause exponential insolvency
2. **Policy Counterfactuals**: Universal allowances vs targeted transfers cost-effectiveness
3. **Liquidity Analysis**: Months-to-default by household type

## Installation

```bash
# Clone repository
git clone <repo-url>
cd ca13_housing_vulnerability

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Quick Start

```python
from ca13_housing_vulnerability import HousingVulnerabilityModel

# Initialize model with Census PUMF data
model = HousingVulnerabilityModel(census_path="data/raw/census_2021_hier_v2.csv")

# Run mortgage rate shock scenario
results = model.run_scenario(
    scenario="mortgage_rate_shock",
    rate_increase=400,  # basis points
    renewal_exposure=0.20
)

# Generate visualizations
results.plot_elasticity_curves()
results.plot_cohort_impacts()
```

### Advanced Usage

```python
# Statistical asset imputation
from ca13_housing_vulnerability.imputation import AssetImputer

imputer = AssetImputer(sfs_path="data/raw/SFS2023_PUMF_data.zip")
enriched_data = imputer.impute_assets(census_data, method="hot_deck")

# Custom shock scenario
from ca13_housing_vulnerability.shocks import CustomShock

shock = CustomShock(
    name="AI_unemployment",
    income_multipliers_by_occupation={
        "retail_sales": 0.70,  # 30% income loss
        "truck_drivers": 0.60,
        "data_entry": 0.50
    },
    rent_inflation=0.15
)

results = model.run_custom_shock(shock)
```

## Project Structure

```
ca13_housing_vulnerability/
├── data/
│   ├── raw/              # Original datasets (not tracked in git)
│   ├── processed/        # Cleaned and merged data
│   └── external/         # MBM thresholds, BoC parameters
├── src/
│   ├── data_loading/     # Census PUMF, SFS, SHS parsers
│   ├── imputation/       # Statistical asset matching
│   ├── shocks/           # Scenario implementations
│   ├── analytics/        # Inequality metrics, validation
│   └── policy/           # Counterfactual simulations
├── notebooks/            # Jupyter analysis notebooks
├── tests/                # Unit and integration tests
├── docs/                 # Documentation
├── config/               # Configuration files
└── outputs/              # Generated figures, tables, reports
```

## Data Access

Census PUMF and supplementary datasets are stored in Google Drive:
- **Core Data**: [Google Drive Link](https://drive.google.com/drive/folders/1SXZmm-RLQtPxKiD_Xc2oZ2xkHB0ePz1O)
- See `data/README_datasets.md` for detailed dataset descriptions

## Timeline

- **Weeks 1-2**: Data foundation and loading pipeline
- **Weeks 3-4**: Core shock simulation engine
- **Weeks 5-6**: Analytics and validation (hindcasting)
- **Weeks 7-9**: Policy simulations and counterfactuals
- **Weeks 10-12**: Deliverables, documentation, publication outputs

## Citation

If you use this code or methodology, please cite:

```
[Author Name]. (2026). From Shelter Ratios to Residual Income: A Disaggregate 
Analysis of Housing Hardship and Macroeconomic Shocks in Canada Using 2021 
Census Microdata. CA-13 Research Project.
```

## License

[To be determined - suggest MIT or Apache 2.0 for open-source policy research]

## Contact

[Add contact information]

## Acknowledgments

- Statistics Canada for Census PUMF and supplementary survey data
- CMHC for Housing Hardship framework and MBM thresholds
- Bank of Canada for mortgage renewal parameters
