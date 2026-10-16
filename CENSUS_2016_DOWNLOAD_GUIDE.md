# Census 2016 PUMF Download Guide

## What You Need for Temporal Analysis

To compare 2016 vs 2021 and show how housing crisis evolved, you need:

### 1. Census 2016 PUMF - Hierarchical File
**What it is:**
- Public Use Microdata File from 2016 Census
- Similar structure to 2021 PUMF we already have
- ~450,000 person records (2016 had larger sample)
- 100+ variables: income, shelter costs, demographics

**Official Source:**
- Statistics Canada Data Liberation Initiative (DLI)
- Requires university/institution access
- Catalogue: 98M0001X2016002

**Alternative Sources:**
1. **Your Google Drive** (if you have it)
2. **Statistics Canada Open Data Portal** (some PUMFs are public)
3. **University library DLI access** (most comprehensive)

### 2. MBM Thresholds 2016
**What it is:**
- Market Basket Measure poverty lines for 2016
- Regional thresholds (50+ CMAs)
- By family size and composition

**Source:**
- Statistics Canada Catalogue 75F0002M
- Table: Market Basket Measure Thresholds (2008-base for 2016, or 2018-base adjusted)

---

## Census 2016 PUMF Structure (Expected)

Similar to 2021 but different variable names:

| Category | 2021 Variable | 2016 Variable | Notes |
|----------|---------------|---------------|-------|
| Household ID | `HH_ID` | `HHLDID` or similar | May differ |
| Total income | `TOTINC` | `TOTINC` | Check codebook |
| After-tax income | `EFATINC` | `EFATINC` | Economic family |
| Shelter costs | `SHELCO` | `SHELCO` | Monthly amount |
| Tenure | `TENUR` | `TENUR` | 1=Owner, 2=Renter |
| CMA | `CMA` | `CMA` | Geographic code |
| Province | `PR` | `PR` | Province code |

**Important:** Variable names may change between Census years. Always check the codebook!

---

## Recommended Approach

### Step 1: Check Your Google Drive
Do you have Census 2016 PUMF in your drive already?
- Look for files like `census_2016_hier.csv` or similar
- Size: ~150-200 MB (compressed) or ~500 MB (uncompressed)

### Step 2: If Not Available, Options:

**Option A: Request from Statistics Canada**
- Free through Data Liberation Initiative (DLI)
- Requires institutional access (university)
- Usually 1-2 week turnaround

**Option B: Use DLI Through University**
- If you're affiliated with a Canadian university
- Access through library portal
- Instant download

**Option C: Use Public Extracts**
- Some smaller Census 2016 extracts available publicly
- May not have full hierarchical structure
- Good for proof-of-concept

---

## What We'll Do Once You Have 2016 Data

### Temporal Analysis Pipeline

1. **Load Census 2016 PUMF**
   ```python
   df_2016 = loader.load_census_pumf('data/raw/census_2016_hier.csv')
   ```

2. **Calculate V2 Hardship (2016)**
   - Same residual income framework
   - Use 2016 MBM thresholds
   - Get 2016 baseline hardship rate

3. **Compare 2016 vs 2021**
   - National change in hardship rate
   - CMA-level changes (which cities got worse?)
   - Demographic shifts (age groups, family types)

4. **Spatial Visualization**
   - Heat maps showing hardship by CMA
   - Change maps (green = improving, red = worsening)
   - Top 10 worst/best performing cities

5. **Generate Paper 1 Figures**
   - Figure 1: National trend 2016→2021
   - Figure 2: CMA comparison (bar chart)
   - Figure 3: Heat map of change
   - Figure 4: Demographic breakdown

---

## Expected Key Findings (Hypotheses to Test)

Based on your "collapsing country" observation:

### Hypothesis 1: National Worsening
**2016 vs 2021 hardship rate increase**
- Expect: +3-5 percentage points nationally
- Driven by: Stagnant incomes + rising rents

### Hypothesis 2: Toronto & Vancouver Hit Hardest
**Hot market CMAs deteriorate fastest**
- Toronto: Expect +8-12 pp increase
- Vancouver: Expect +10-15 pp increase
- Calgary: May improve (oil price recovery)

### Hypothesis 3: Renters Bear the Brunt
**Tenure gap widens**
- Renter hardship: Expect +10-15 pp
- Owner hardship: Expect +2-4 pp (mortgage renewal shock starts 2022+)

### Hypothesis 4: Youth Crisis Deepens
**Age stratification**
- 25-34 age group: Expect largest increase
- 65+ seniors: May worsen due to fixed incomes vs inflation

---

## Timeline

**Immediate Actions:**
1. ✅ Check your Google Drive for Census 2016 PUMF
2. ✅ If you have it, share the link (like you did for 2021)
3. ✅ If not, I'll guide you through DLI access

**Once 2016 Data Acquired (Same Day):**
- Load and validate data (~10 minutes)
- Run V2 analysis on 2016 (~5 minutes)
- Generate 2016 vs 2021 comparison (~15 minutes)
- Create spatial visualizations (~20 minutes)
- Export results for Paper 1 (~10 minutes)

**Total Time:** ~1 hour to get full temporal analysis ready

---

## Example Research Questions (Paper 1)

With 2016 + 2021 data, you can answer:

1. **"How much worse is Canada's housing crisis in 2021 vs 2016?"**
   - National hardship rate change
   - Number of NEW households in crisis

2. **"Which cities are collapsing fastest?"**
   - CMA rankings by hardship rate increase
   - Toronto vs Vancouver vs Montreal

3. **"Who got hit hardest?"**
   - Renters vs owners
   - Young vs old
   - Families vs singles

4. **"Did any cities improve?"**
   - Identify positive outliers
   - What policies did they implement?

5. **"What's the trajectory?"**
   - If trend continues, what's 2026 projection?
   - When does crisis become catastrophic?

---

## Next Steps

**Tell me:**
1. Do you have Census 2016 PUMF in your Google Drive?
2. If yes → Share the link, I'll download immediately
3. If no → Do you have university DLI access? I'll guide you through request

**Once we have 2016 data:**
- I'll run the temporal analysis immediately
- Generate all Paper 1 figures
- Create draft outline with key findings

This will give you a **strong, simpler paper** using V2 only (no assets), focused on the spatial-temporal story of Canada's worsening housing crisis from 2016 to 2021.

---

## Pro Tip: Start with V2 (Simpler) Paper

**Why this is smart:**
1. ✅ Faster to publish (simpler methodology)
2. ✅ Easier to explain (high school → policy audiences)
3. ✅ Still novel (residual income framework underutilized)
4. ✅ Establishes your expertise in the field
5. ✅ Sets up Paper 2 (complex V3 + shocks) as natural extension

**Then Paper 2 builds on Paper 1:**
- "In our previous work (Paper 1), we showed housing crisis worsening 2016-2021"
- "Here we extend that analysis with asset augmentation and shock scenarios"
- Reviewers will see you as established researcher in this domain

**Smart publication strategy!** 🎯
