# Housing Vulnerability Framework: From Baseline to Novel Extensions

**Integrating CMHC Housing Hardship Methodology with Asset Buffers and Macroeconomic Shock Analysis**

*A Research Project by Jason Wu with Alex Neumann*

---

## 🎯 Project Overview

This framework combines rigorous replication of established methodology with novel analytical extensions for academic publication.

### Two-Part Structure

**Part 1: Version 2 Baseline (CMHC Replication)**
- Exact reproduction of CMHC's revised 2024 Housing Hardship methodology
- Proper 2021 Census PUMF variable handling
- MBM 2018-base non-housing threshold calculation
- Validates against CMHC's 7.8% national hardship rate
- **Establishes academic credibility and foundation**

**Part 2: Version 3 Extensions (Novel Contributions)**
- Statistical asset imputation from SFS 2023 (liquidity buffers)
- Macroeconomic shock scenarios (trade wars, AI unemployment, immigration)
- "Months-to-default" vulnerability analysis
- Policy counterfactual optimization
- **Publishable novel contributions**

---

## 📊 Data Sources

### Primary Data (Your Google Drive)
- **Census 2021 PUMF**: `census_2021_hier_v2.csv` (213 MB, ~930K households)
  - 122 variables documented in `IMPORTANT-PUMF_Dictionary_Mapping_Reference.md`
- **MBM Thresholds**: `MBM-data-1110006601-eng.csv`
  - Table 11-10-0066-01, 2018-base, 2020 reference year
- **SFS 2023**: Survey of Financial Security (asset/debt data)
- **SHS 2023**: Survey of Household Spending
- **CHS 2024**: Canadian Housing Survey (validation)

---

## 🏗️ Architecture

```
housing_vulnerability/
├── v2_baseline/                    # CMHC Replication (Foundation)
│   ├── __init__.py
│   ├── census_loader.py            # Load 2021 PUMF properly
│   ├── income_construction.py      # EFDIMBM_2018 deduplication
│   ├── mbm_calculator.py           # Non-housing threshold
│   ├── geography_mapper.py         # 5 CMAs + CMA=999 bounds
│   ├── cmhc_exclusions.py          # Revised 2024 rules
│   └── hardship_calculator.py      # Residual income method
│
├── v3_extensions/                  # Novel Contributions
│   ├── asset_imputation/
│   │   ├── sfs_loader.py           # SFS 2023 data
│   │   ├── statistical_matching.py  # Hot-deck imputation
│   │   └── liquidity_calculator.py  # Months-to-default
│   ├── shocks/
│   │   ├── base_shock.py           # Framework
│   │   ├── trade_war_shock.py      # Canada-USA tariffs
│   │   ├── ai_unemployment_shock.py # Occupation displacement
│   │   ├── immigration_shock.py     # Rent surge
│   │   └── compound_shock.py        # Multi-factor
│   ├── liquidity/
│   │   └── buffer_analysis.py       # Survival analysis
│   └── policy/
│       └── counterfactuals.py       # Universal vs targeted
│
├── notebooks/
│   ├── 01_v2_cmhc_baseline.ipynb          # Validation
│   ├── 02_asset_imputation.ipynb          # Novel method
│   ├── 03_shock_scenarios.ipynb           # Novel analysis
│   ├── 04_publication_figures.ipynb       # Paper outputs
│   └── 05_complete_demonstration.ipynb    # Full pipeline
│
└── outputs/
    ├── v2_validation_report.md            # CMHC 7.8% match
    └── v3_novelty_analysis.md             # Extension results
```

---

## 🔬 Version 2: CMHC Baseline Replication

### Methodology (Following v2.0_outline.md Specification)

#### 1. Income Construction
- **Household Total Income**: Sum `TOTINC` for persons 15+
  - Handle special codes: `99,999,999` (N/A for children), `88,888,888` (unavailable)
  - Exclusion: Zero or negative household total income

- **MBM Disposable Income**: Use `EFDIMBM_2018`
  - Deduplicate family-level values (one per economic family)
  - Handle unattached persons separately (`EF_RP=3`)
  - Exclusion: Zero or negative disposable income

#### 2. MBM Non-Housing Threshold
- **2018-base, 2020 reference year**
- **Components**: Food + Clothing + Transportation + Other
- **Equivalization**: `B_NH = B_ref × (N/4)^1` (elasticity = 1, reference family = 4)

**Reference family values (from MBM CSV)**:
- Montréal: $29,840
- Toronto: $29,983
- Calgary: $30,291
- Edmonton: $30,111
- Vancouver: $30,849

#### 3. Geography Mapping
- **Exact**: 5 CMAs (Montreal=462, Toronto=535, Calgary=825, Edmonton=835, Vancouver=933)
- **Ambiguous**: CMA=999 (report min/max threshold bounds)
- **Limitation**: PR=70 (Yukon/NWT/Nunavut merged, can't separate)

#### 4. Residual Income & Hardship
```python
RI = DisposableIncome - (ShelterCost × 12)
Hardship = (RI < MBM_NonHousing_Threshold)
```

#### 5. Validation Target
**CMHC published 7.8% national hardship rate (2021)**
- Document any differences due to PUMF limitations
- Report as "PUMF-feasible approximation"

---

## 🚀 Version 3: Novel Extensions

### 1. Asset Imputation (Novel Contribution #1)

**Problem**: Census has income but **no assets**  
**Solution**: Statistical matching from SFS 2023

**Method**:
- Hot-deck imputation by income decile × tenure × household type
- Parametric sampling from fitted distributions
- Validation against SFS summary statistics

**Output**: `liquid_assets_imputed` for each Census household

### 2. Liquidity Buffer Analysis (Novel Contribution #2)

**Key Metric**: **Months-to-Default**
```python
months_to_default = liquid_assets / |monthly_residual_income_deficit|
```

**Categories**:
- Immediate insolvency (<1 month)
- Critical (1-3 months)
- Vulnerable (3-6 months)
- Moderate buffer (6-12 months)
- Strong buffer (>12 months)

### 3. Shock Scenarios (Novel Contribution #3)

#### Trade War (Canada-USA)
- Industry-specific exposure (auto 85%, lumber 70%, oil 75%)
- Regional concentration (ON auto belt, BC lumber, AB energy)
- 3 severity levels (moderate/severe/extreme)
- Job loss + wage suppression

#### AI Unemployment
- Occupation-based displacement (data entry 80%, retail 70%, trucking 60%)
- 3 timelines (2-year, 5-year, 10-year)
- Retraining success pathways (40% rate)

#### Immigration Rent Surge
- CMA-specific (Toronto, Vancouver)
- Dual-market friction: mobile tenants (MOB5=1) vs sitting tenants
- Population growth → vacancy collapse

#### Compound Shocks
- Multi-factor stress tests
- Trade war + rate hike + rent surge

### 4. Policy Counterfactuals (Novel Contribution #4)

**Compare**:
- Universal housing allowance ($500/month to all)
- Targeted support ($800/month to bottom 20%)
- Emergency job loss support ($1200/month to displaced)

**Metrics**:
- Households saved from insolvency
- Total fiscal cost
- Cost per household saved
- Distributional equity

---

## 🎓 Academic Publication Strategy

### Paper Structure

**Part 1: Replication (Credibility)**
- "We replicate CMHC's 2024 method on 2021 Census PUMF"
- Methods section: Detailed income construction, MBM calculation
- Results: Validate against 7.8% (or document differences)
- **Shows rigor and understanding**

**Part 2: Extensions (Novelty)**
- "Traditional metrics miss asset buffers and shock vulnerability"
- Methods: Asset imputation, shock scenarios, liquidity analysis
- Results: Novel findings on vulnerability timing and depth
- **Shows original contribution**

### Novelty Claims (Defensible)

✅ **First** to integrate SFS assets with Census PUMF via statistical matching  
✅ **First** to operationalize dual-market rent friction using MOB5 mobility  
✅ **First** to combine CMHC hardship with BoC stress-testing framework  
✅ **First** open-source, reproducible implementation

### NOT Novel (Acknowledge Honestly)

❌ Residual income approach (CMHC 2020)  
❌ MBM poverty methodology (Statistics Canada)  
❌ Comparative statics (standard economics)  
❌ Hot-deck imputation (established method)

**But**: The *integration and application* to this specific problem **is novel**

---

## 🔧 Installation & Setup

```bash
# Clone repository
git clone <repo-url>
cd housing_vulnerability

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download data (from Google Drive)
# Place in data/raw/:
#   - census_2021_hier_v2.csv
#   - MBM-data-1110006601-eng.csv
#   - SFS2023_PUMF_data.zip (optional)
```

---

## 📖 Usage

### Quick Start: V2 Baseline Validation

```python
from housing_vulnerability.v2_baseline import CMHCReplication

# Load and validate
replicator = CMHCReplication(
    census_path='data/raw/census_2021_hier_v2.csv',
    mbm_path='data/raw/MBM-data-1110006601-eng.csv'
)

# Run baseline
results = replicator.run_baseline()

print(f"Hardship rate: {results['hardship_rate']:.1%}")
print(f"CMHC target: 7.8%")
print(f"Difference: {results['hardship_rate'] - 0.078:.1%} pp")
```

### Full Pipeline: V2 + V3 Extensions

```python
from housing_vulnerability import UnifiedPipeline

# Initialize complete framework
pipeline = UnifiedPipeline()

# Step 1: Establish baseline
baseline = pipeline.run_v2_baseline()

# Step 2: Impute assets
enriched = pipeline.impute_assets(baseline)

# Step 3: Apply shock
from housing_vulnerability.v3_extensions.shocks import TradeWarShock

shock = TradeWarShock(severity='severe')
shocked = pipeline.apply_shock(enriched, shock)

# Step 4: Analyze vulnerability
vulnerability = pipeline.analyze_liquidity(shocked)

print(f"Baseline hardship: {baseline['hardship_rate']:.1%}")
print(f"Post-shock hardship: {shocked['hardship_rate']:.1%}")
print(f"Immediate insolvency: {vulnerability['critical_3mo']}")
```

---

## 📊 Key Variables (from PUMF Dictionary)

### Critical V2 Variables
- `HH_ID`: Household identifier
- `EF_ID`: Economic family identifier
- `EF_RP`: Economic family reference person (3 = unattached)
- `PRIHM`: Primary household maintainer
- `TOTINC`: Total income before tax (persons 15+)
- `EFDIMBM_2018`: MBM disposable income (family-level, deduplicate!)
- `SHELCO`: Monthly shelter cost
- `TENUR`: Tenure (1=Owner, 2=Renter, 3=Band housing)
- `PR`: Province (70 = Territories merged)
- `CMA`: CMA code (999 = ambiguous)
- `WEIGHT`: Household weight

### Critical V3 Variables
- `MOB5`: 5-year mobility (1=Non-mover, market exposure proxy)
- `PRESMORTG`: Mortgage presence
- `SUBSIDY`: Subsidized housing
- Income deciles, age groups, household type

### Special Codes
- `88,888,888`: Unavailable/suppressed
- `99,999,999`: Not applicable (e.g., children for TOTINC)

---

## ✅ Validation Checklist

### V2 Baseline
- [ ] Load 2021 PUMF successfully
- [ ] Parse MBM CSV correctly (handle Statistics Canada preamble)
- [ ] Deduplicate EFDIMBM_2018 (one per economic family)
- [ ] Handle special codes properly (88,888,888 and 99,999,999)
- [ ] Map 5 CMAs exactly
- [ ] Report CMA=999 bounds (min/max thresholds)
- [ ] Apply CMHC exclusions correctly
- [ ] Calculate residual income properly
- [ ] Weight sum matches 15,034,101 (validation check)
- [ ] Hardship rate close to 7.8% or differences documented

### V3 Extensions
- [ ] SFS asset imputation matches demographic strata
- [ ] Months-to-default calculated correctly
- [ ] Trade war industry exposure realistic
- [ ] AI unemployment occupation rates validated
- [ ] Policy counterfactuals cost-effective
- [ ] All outputs reproducible

---

## 📚 Documentation Files

- `v2.0_outline.md`: Complete V2 specification (from Google Drive)
- `IMPORTANT-PUMF_Dictionary_Mapping_Reference.md`: All 122 variables
- `PROJECT_SUMMARY.md`: Technical overview
- `QUICK_START.md`: Usage examples

---

## 📈 Expected Outputs

### V2 Validation Report
```
=== CMHC Housing Hardship Replication ===

Data:
  Census records: 930,457
  Weighted households: 15,034,101
  
Income Construction:
  Economic families: 10,234,567
  Unattached persons: 4,799,534
  Unavailable income: 12,345 (0.1%)
  
Exclusions:
  Zero/negative total income: 234,567
  Zero/negative disposable income: 123,456
  Negative shelter cost: 1,234
  
Geography:
  Exact CMAs: 8,765,432 (58.3%)
  Ambiguous (CMA=999): 5,432,109 (36.1%)
  Territories (PR=70): 45,678 (0.3%)
  
Results:
  Hardship rate: 7.9% ± 0.2%
  CMHC target: 7.8%
  Difference: +0.1 pp (within statistical uncertainty)
```

### V3 Extension Results
```
=== Asset Buffer Analysis ===

Liquidity Categories:
  Immediate insolvency (<1mo): 234,567 (2.5%)
  Critical (1-3 months): 456,789 (4.9%)
  Vulnerable (3-6 months): 567,890 (6.1%)
  Moderate (6-12 months): 678,901 (7.3%)
  Strong (>12 months): 1,234,567 (13.2%)
  
Trade War Impact (Severe):
  Additional job losses: 345,678
  New hardship cases: 456,789
  Immediate insolvency: +123,456
  
Policy Comparison:
  Universal $500/mo: $90B/year, saves 234K, $384K/household
  Targeted $800/mo: $23B/year, saves 189K, $122K/household
  Efficiency winner: Targeted (3.1× more efficient)
```

---

## 🎯 Timeline

**Week 1**: V2 baseline validation  
**Week 2**: Asset imputation implementation  
**Week 3**: Shock scenarios integration  
**Week 4**: Publication figures and paper draft

---

## 👥 Contributors

**Jason Wu** - Student Researcher  
**Alex Neumann** - Research Supervisor

---

## 📄 License

[To be determined - suggest MIT for open research]

---

## 🔗 Links

- Research Folder: [Google Drive](https://drive.google.com/drive/folders/16JkBX76g2SehcpZv3y-mD0I3WWFVFBaO)
- Project Presentation: [Google Slides](https://docs.google.com/presentation/d/1mp_GxdLD-S8KeXvJ41zn0sl6iUUFe2Wv8loZ9MKveOQ)
- Literature Analysis: [Google Docs](https://docs.google.com/document/d/11a2ZFSLXUH2ynYB4HbTrBYBJIqJ4R_OMXlQrNAXX5vo)

---

**Building rigorous baselines and novel extensions for academic publication** 🚀
