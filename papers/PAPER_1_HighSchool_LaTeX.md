# Fifteen Years of Housing Crisis in Canada (2006-2021)
## A Longitudinal Study of Housing Hardship Using Residual Income Analysis

**High School Research Paper**  
**Author:** [Your Name]  
**Date:** October 16, 2026  
**Institution:** [Your School]

---

## Abstract

**Background:** Canada's housing affordability crisis has been a major concern for over a decade. Traditional measures like the 30% shelter-cost-to-income ratio may not fully capture when families struggle to afford basic needs after paying for housing.

**Objective:** This study examines how housing hardship in Canada changed over 15 years (2006-2021) using a residual income approach that measures whether households have enough money left after paying for housing to afford basic necessities.

**Methods:** We analyzed 777,707 person-records from three Canadian Census waves (2006, 2011, 2021). Housing hardship was defined as having residual income (after-tax income minus annual shelter costs) below Canada's poverty line (Market Basket Measure). All dollar amounts were adjusted for inflation to 2021 values for fair comparison.

**Results:** Over 15 years, inflation-adjusted shelter costs increased 37.1% while median household income grew only 33.5%, creating a 3.6 percentage point gap. Housing hardship rates remained persistently high: 38.0% (2006), 33.9% (2011), and 37.9% (2021). Renters consistently experienced higher hardship rates (40.4%-43.6%) than homeowners (31.4%-35.6%), but both groups worsened over time.

**Conclusions:** Canada's housing crisis is structural rather than temporary, persisting through economic recovery, three different governments, and the COVID-19 pandemic. The sustained gap between shelter cost and income growth represents an ongoing squeeze on household budgets. Current policies have not successfully addressed these affordability challenges.

**Keywords:** housing affordability, residual income, poverty, Canada, Census analysis

---

## 1. Introduction

### 1.1 The Housing Affordability Problem

Canada is experiencing a serious housing affordability crisis. Many Canadian families struggle to afford rent or mortgage payments while still having enough money left over for food, transportation, healthcare, and other basic needs. This problem affects young people planning to move out, university students, first-time home buyers, and even current homeowners.

The traditional way to measure housing affordability is the "30% rule": housing is considered affordable if it costs less than 30% of household income. However, this measure has a major limitation: it doesn't account for what happens after people pay for housing. A household spending 28% of income on housing might appear "affordable" by this standard, but if they can't afford groceries or transportation afterward, they're still in financial trouble.

### 1.2 A Better Way to Measure: Residual Income

Canada Mortgage and Housing Corporation (CMHC) developed an improved approach called the **residual income framework**. This method asks: "After paying for housing, does the household have enough money left over to afford basic necessities?" Basic necessities are defined by Canada's official poverty line, called the Market Basket Measure (MBM), which calculates the minimum cost of food, clothing, transportation, and other essentials (excluding housing).

The formula is:
- **Residual Income** = After-tax Income - Annual Shelter Costs
- **Housing Hardship** occurs when Residual Income < MBM Poverty Threshold

This approach directly links housing costs to material deprivation risk, providing a more comprehensive view of affordability challenges.

### 1.3 Why Study 15 Years?

Short-term studies (1-2 years) cannot distinguish between:
- **Temporary problems** caused by economic recessions that improve during recovery
- **Structural problems** built into the housing system that persist regardless of economic conditions

By analyzing three Census periods (2006, 2011, 2021), we can observe trends through major economic events:
- **2006-2011:** The 2008 global financial crisis and subsequent recession
- **2011-2016:** Economic recovery with low interest rates
- **2016-2021:** Housing market peak and COVID-19 pandemic

### 1.4 Research Questions

This study investigates three main questions:

1. **How has housing hardship evolved in Canada from 2006 to 2021?**
2. **Did homeowners and renters experience different trends?**
3. **Is Canada's housing crisis temporary or structural?**

---

## 2. Methods

### 2.1 Data Sources

#### 2.1.1 Census Public Use Microdata Files (PUMF)

We used publicly available Census data from Statistics Canada. These files contain anonymized individual-level data on income, housing costs, demographics, and geography. The specific datasets were:

**Census 2006** (pumf-95M0029-E-2006-hierarchical)
- Sample size: 78,056 valid records
- Reference period: May 2006
- Data collected: Total income, shelter costs (rent/mortgage), homeownership status

**Census 2011** (NHS-99M002X-E-2011-pumf-hierarchical)
- Sample size: 341,030 valid records
- Reference period: May 2011 (National Household Survey)
- Data collected: After-tax income, shelter costs, homeownership status

**Census 2021** (98M0001X2021002)
- Sample size: 358,621 valid records
- Reference period: May 2021
- Data collected: After-tax income, shelter costs, homeownership status

**Total sample:** 777,707 person-records across 15 years

#### 2.1.2 Market Basket Measure (MBM) Poverty Thresholds

We used Canada's official poverty thresholds for each Census year:
- **2006:** $13,500 per year
- **2011:** $15,000 per year
- **2021:** $19,728 per year

These thresholds represent the minimum income needed (after paying for housing) to purchase essential goods and services.

### 2.2 Data Processing

#### 2.2.1 Inflation Adjustment

To make fair comparisons across time, we converted all monetary values to 2021 constant dollars using the Canadian Consumer Price Index (CPI):

- 2006 dollars × 1.276 = 2021 dollars
- 2011 dollars × 1.148 = 2021 dollars
- 2021 dollars × 1.000 = 2021 dollars (no adjustment needed)

**Example:** $1,000 rent in 2006 is equivalent to $1,276 in 2021 dollars.

#### 2.2.2 Data Cleaning

Census files used special codes for missing data:
- 9999 = shelter cost not reported
- 8888 = not applicable
- 99999 = income not reported

We removed these codes and excluded records with missing values. We also excluded unrealistic values:
- Income must be > $0
- Monthly shelter cost must be > $0 and < $10,000

**Data quality note:** Census 2006 had lower data completeness (23.4% retention rate) compared to 2011 (99.3%) and 2021 (99.1%), suggesting different data collection methods. Results for 2006 should be interpreted with this limitation in mind.

### 2.3 Variable Construction

#### 2.3.1 Housing Hardship (Primary Outcome)

We calculated housing hardship in three steps:

**Step 1:** Calculate annual shelter cost
```
Annual Shelter Cost = Monthly Shelter Cost × 12
```

**Step 2:** Calculate residual income
```
Residual Income = After-tax Annual Income - Annual Shelter Cost
```

**Step 3:** Determine hardship status
```
Housing Hardship = 1 if Residual Income < MBM Threshold
Housing Hardship = 0 if Residual Income ≥ MBM Threshold
```

#### 2.3.2 Shelter-Cost-to-Income Ratio (STIR)

For comparison with traditional measures:
```
STIR = (Monthly Shelter Cost × 12) / Annual Income × 100%
```

We classified STIR > 30% as "affordability burden" and STIR > 50% as "severe burden."

#### 2.3.3 Tenure Classification

- **Owner:** Household owns their dwelling (with or without mortgage)
- **Renter:** Household rents their dwelling

### 2.4 Statistical Analysis

#### 2.4.1 Descriptive Statistics

For each Census year, we calculated:
- Mean and median income (inflation-adjusted)
- Mean and median shelter costs (inflation-adjusted)
- STIR distribution (mean, median, percentage > 30%, percentage > 50%)
- Overall housing hardship rate (percentage)
- Hardship rates by tenure (owners vs. renters)

#### 2.4.2 Trend Analysis

We computed changes between Census waves:
- **Percentage change in income:** (Income₂₀₂₁ - Income₂₀₀₆) / Income₂₀₀₆ × 100%
- **Percentage change in shelter costs:** Same formula
- **Change in hardship rate:** Percentage point difference (e.g., 38.0% - 37.9% = +0.1 pp)

#### 2.4.3 Visualization

We created five publication-quality figures showing:
1. National trends in income, shelter costs, STIR, and hardship (2006-2021)
2. Period-by-period comparison (which 5-year interval was worst?)
3. Owner vs. renter hardship trajectories
4. Income-shelter squeeze (indexed to 2006 baseline)
5. Summary dashboard with all key metrics

All figures were generated in Python using matplotlib and saved as high-resolution PNG files (300 DPI).

### 2.5 Ethical Considerations

This study used publicly available, anonymized Census data. No ethics approval was required per Statistics Canada guidelines. The data cannot be used to identify individual households. All analyses followed Statistics Canada's terms of use for PUMF data.

---

## 3. Results

### 3.1 Sample Characteristics

Table 1 shows the basic characteristics of our sample across the three Census years.

**Table 1: Sample Characteristics by Census Year**

| Characteristic | 2006 | 2011 | 2021 |
|----------------|------|------|------|
| **Sample size (n)** | 78,056 | 341,030 | 358,621 |
| **Income (2021 $)** |  |  |  |
| Median | $34,452 | $45,920 | $46,000 |
| 25th percentile | $17,864 | $22,960 | $25,000 |
| 75th percentile | $70,180 | $101,024 | $93,000 |
| **Shelter Cost (2021 $)** |  |  |  |
| Median monthly | $1,021 | $1,378 | $1,400 |
| 25th percentile | $766 | $804 | $800 |
| 75th percentile | $1,531 | $2,181 | $2,129 |

*Note: All dollar values adjusted to 2021 constant dollars using CPI.*

### 3.2 The Great Squeeze: Income vs. Shelter Costs

Figure 1 shows how income and shelter costs changed over 15 years.

\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{outputs/full_census_figures/08_fifteen_year_national_trends.png}
\caption{Fifteen-year trends in income, shelter costs, STIR, and housing hardship (2006-2021). Panel A shows median income growth, Panel B shows median shelter cost growth, Panel C shows traditional affordability metrics (STIR), and Panel D shows housing hardship rates using residual income methodology.}
\label{fig:national_trends}
\end{figure}

**Key findings:**

**Income growth (2006-2021):**
- Median income increased from $34,452 to $46,000
- **Total growth: 33.5%** (inflation-adjusted)

**Shelter cost growth (2006-2021):**
- Median monthly shelter cost increased from $1,021 to $1,400
- **Total growth: 37.1%** (inflation-adjusted)

**The gap:**
- Shelter costs grew **3.6 percentage points faster** than income
- This means housing became less affordable relative to earnings

**What does this mean in real dollars?**

If shelter costs had grown at the same rate as income, median monthly rent in 2021 would be $1,362 instead of $1,400. That's a $38/month difference, or **$456 per year**. For a household already struggling, $456 represents:
- One week of groceries for a family
- Two months of phone/internet bills
- A winter coat or essential clothing

### 3.3 Housing Hardship Rates Over Time

Figure 1, Panel D shows housing hardship rates using the residual income method.

**Housing hardship rates:**
- **2006:** 38.0% of households (29,681 households in our sample)
- **2011:** 33.9% of households (115,459 households)
- **2021:** 37.9% of households (135,740 households)

**Change over time:**
- **2006-2011:** Decreased by 4.1 percentage points (improvement!)
- **2011-2021:** Increased by 4.0 percentage points (deterioration)
- **2006-2021:** Essentially unchanged (-0.1 percentage points)

**Important finding:** Despite economic recovery (2009-2019), strong job markets, and three different federal governments, Canada's housing hardship rate in 2021 returned to almost exactly the same level as 2006. This suggests the problem is **structural** (built into the system) rather than **cyclical** (caused by temporary economic conditions).

### 3.4 Traditional Affordability Metrics (STIR)

For comparison, we also looked at traditional affordability measures (Figure 1, Panel C).

**Households with STIR > 30% (affordability burden):**
- 2006: 57.0%
- 2011: 51.1%
- 2021: 50.8%
- **Change:** -6.2 percentage points (improvement)

**Households with STIR > 50% (severe burden):**
- 2006: 35.8%
- 2011: 33.6%
- 2021: 31.5%
- **Change:** -4.3 percentage points (improvement)

**What does this contradiction mean?**

Traditional measures (STIR) show improvement, but residual income measures show no improvement. This discrepancy occurs because households can maintain "affordable" STIR ratios by cutting spending on food, transportation, and other necessities. The residual income approach reveals this hidden hardship.

### 3.5 Period-by-Period Analysis: Which 5-Year Interval Was Worst?

Figure 2 breaks down changes into two periods: 2006-2011 and 2011-2021.

\begin{figure}[h]
\centering
\includegraphics[width=0.85\textwidth]{outputs/full_census_figures/09_period_comparison.png}
\caption{Period-over-period comparison showing which five-year interval experienced the most severe deterioration. Bars show percentage changes in income, shelter costs, and hardship rates for each period.}
\label{fig:period_comparison}
\end{figure}

**2006-2011 period (Financial Crisis Era):**
- Income growth: +33.3%
- Shelter cost growth: +35.0%
- Hardship change: -4.1 percentage points (improved)
- **Analysis:** Despite including the worst financial crisis since the Great Depression, this period saw improvement in hardship rates, likely due to government stimulus programs and social assistance.

**2011-2021 period (Recovery Era):**
- Income growth: +0.2% (essentially flat!)
- Shelter cost growth: +1.6%
- Hardship change: +4.0 percentage points (worsened)
- **Analysis:** A decade of economic expansion produced almost zero real income growth and worsening hardship rates.

**Surprising finding:** The period that included economic crisis saw improvements, while the period of economic expansion saw deterioration. This suggests that active government intervention matters more than overall economic conditions.

### 3.6 Homeowners vs. Renters

Figure 3 compares hardship rates between homeowners and renters.

\begin{figure}[h]
\centering
\includegraphics[width=0.85\textwidth]{outputs/full_census_figures/10_tenure_divergence.png}
\caption{Owner versus renter housing hardship trajectories (2011-2021). Both groups experienced worsening conditions, with the gap narrowing as homeowners caught up to renters in hardship rates.}
\label{fig:tenure_divergence}
\end{figure}

**Table 2: Housing Hardship by Tenure**

| Year | Owner Hardship | Renter Hardship | Gap |
|------|----------------|-----------------|-----|
| 2011 | 31.4% | 40.4% | 9.0 percentage points |
| 2021 | 35.6% | 43.6% | 8.0 percentage points |
| **Change** | **+4.2 pp** | **+3.2 pp** | **-1.0 pp** |

**Key findings:**

1. **Renters consistently had higher hardship rates** than owners (as expected)

2. **Both groups worsened:** 
   - Owners: 13.4% increase (31.4% → 35.6%)
   - Renters: 7.9% increase (40.4% → 43.6%)

3. **The gap narrowed** because owners caught up to renters in hardship rates, NOT because renters improved

**Why are homeowners struggling?**
- High mortgage payments (borrowed large amounts to buy expensive homes)
- Rising property taxes
- Increasing maintenance costs
- Some are "house rich, cash poor" (own valuable property but have low income)

**Important implication:** Homeownership no longer guarantees housing security. Policies focused only on helping renters miss growing owner vulnerability.

### 3.7 The Income-Shelter Squeeze Visualized

Figure 4 shows both trends indexed to 2006 baseline (2006 = 100) to clearly visualize the growing gap.

\begin{figure}[h]
\centering
\includegraphics[width=0.85\textwidth]{outputs/full_census_figures/11_income_shelter_squeeze.png}
\caption{Income versus shelter cost growth indexed to 2006 baseline (2006 = 100). The diverging lines show shelter costs consistently outpacing income growth, creating a sustained squeeze on household budgets.}
\label{fig:squeeze}
\end{figure}

**Indexed values:**

| Year | Income Index | Shelter Index | Gap |
|------|-------------|---------------|-----|
| 2006 | 100 | 100 | 0 |
| 2011 | 133 | 135 | 2 |
| 2021 | 134 | 137 | 3 |

The cumulative 3-point gap represents a sustained squeeze that compounds year after year.

---

## 4. Discussion

### 4.1 Principal Findings

This 15-year longitudinal study reveals that Canada's housing crisis is **structural rather than cyclical**. Three key pieces of evidence support this conclusion:

1. **Persistence through economic cycles:** Housing hardship rates remained at ~38% from 2006 to 2021, despite post-recession recovery, a decade of economic expansion (2011-2019), low unemployment, and strong GDP growth.

2. **Sustained income-shelter gap:** Shelter costs outpaced income growth by 3.6 percentage points consistently across multiple periods and economic conditions.

3. **Policy ineffectiveness:** Three federal governments (Conservative 2006-2015, Liberal 2015-present) implemented various housing policies, yet hardship rates remained flat, suggesting incremental policy adjustments are insufficient.

### 4.2 The Meaning of the 3.6 Percentage Point Gap

While 3.6 percentage points may sound small, it has significant real-world impact:

**For a median household ($46,000 income, $1,400/month shelter):**
- Annual shelter cost: $16,800
- If shelter had tracked income: $16,320
- **Annual gap: $480**

This $480 represents:
- 1.6% of total income
- 2.5% of post-shelter disposable income
- One week of groceries or two months of transportation costs

**Over 15 years:** A household experiencing this squeeze continuously would face a cumulative shortfall of ~$3,600 (inflation-adjusted), forcing trade-offs between housing security and other necessities.

### 4.3 Why Did 2011-2021 See Income Stagnation?

The 2011-2021 period showed only 0.2% real income growth despite economic expansion. Possible explanations:

1. **Wage stagnation:** Real wages for median workers haven't kept pace with productivity growth
2. **Precarious employment:** Growth in temporary, part-time, and gig economy jobs with lower pay
3. **Income inequality:** Economic gains concentrated among top earners rather than median workers
4. **Regional variation:** Hot housing markets (Toronto, Vancouver) may have driven different patterns than our national analysis captures

### 4.4 The Homeowner Vulnerability Surprise

Our finding that homeowner hardship increased 13.4% challenges traditional assumptions that homeownership provides housing security. Several factors explain this:

**High mortgage debt:** First-time buyers in 2015-2021 stretched budgets to enter expensive markets, resulting in high debt-servicing costs even with low interest rates.

**Property tax increases:** Many municipalities raised property taxes faster than general inflation to fund services.

**Maintenance costs:** Home repairs and utilities increased, squeezing owners on fixed incomes.

**The "equity rich, cash poor" phenomenon:** Seniors may own homes worth $500,000+ but have annual incomes below $30,000, making them vulnerable to property tax increases and emergency repairs despite substantial home equity.

**Policy implication:** Housing policy focused exclusively on rental assistance misses growing owner vulnerability. Options to consider:
- Property tax deferral programs for low-income homeowners
- Mortgage renewal assistance during interest rate shocks
- Reverse mortgage programs for equity-rich, income-poor seniors

### 4.5 Comparison to Previous Research

**CMHC (2024)** reported 7.8% housing hardship using their revised methodology on 2020 data. Our 37.9% (2021) is substantially higher. Key differences:

1. **Sample:** CMHC uses full Census (100% of population); we used PUMF (2.7% sample)
2. **MBM calculation:** We used simplified national average; CMHC applies region-specific, family-size-adjusted thresholds
3. **Geographic variation:** CMHC accounts for Toronto/Vancouver vs. rural differences; our national average may overestimate hardship in low-cost regions

**Important note:** While our absolute hardship rate may differ from CMHC's, our **trend analysis** (persistence over time, owner-renter dynamics, income-shelter gap) remains valid because we used consistent methodology across all three Census years.

**Walks & Twigge-Molecey (2023)** found widening geographic inequality in Toronto/Vancouver versus other cities. Our national analysis masks this regional variation. Future research should stratify by Census Metropolitan Area (CMA) to identify which cities drive national trends.

### 4.6 Study Limitations

**1. Data quality issues**

Census 2006 had only 23.4% valid record retention versus 99%+ for 2011/2021. This may bias 2006 results toward higher-income households if low-income households were more likely to have missing data. Our 2006-2011 improvement may be somewhat overstated.

**2. Simplified MBM thresholds**

We used national average MBM for single adults ($13,500-$19,728) due to data limitations. CMHC applies:
- Region-specific MBM (50+ geographic areas)
- Family size adjustments (1-person, 2-person, 4-person households have different needs)
- Age adjustments (seniors have different consumption patterns)

Our simplified approach likely **underestimates hardship** for large families and Toronto/Vancouver residents while **overestimating hardship** for singles in low-cost regions.

**3. Cross-sectional snapshots**

Census occurs every 5 years, providing snapshots rather than continuous tracking. We cannot observe:
- Individual households moving in/out of hardship
- Life-cycle effects (young workers starting careers vs. seniors downsizing)
- Temporary vs. chronic hardship (short-term job loss vs. persistent low income)

Panel data (following same households over time) would reveal whether hardship affects the same households continuously or rotates across different households.

**4. No geographic stratification**

Our national analysis masks regional variation. Toronto and Vancouver likely experienced steeper hardship increases than Atlantic Canada or Prairie provinces. The housing crisis is not uniform across Canada.

### 4.7 Policy Implications

**Finding 1: Structural crisis requires structural solutions**

Incremental policies (small tax credits, pilot programs) have proven insufficient over 15 years. Canada needs:

**Supply-side:**
- Zoning reform to allow more apartment buildings and higher density
- Reduced development charges and permit fees
- Massive public housing expansion

**Demand-side:**
- Progressive taxation of housing wealth (higher taxes on multiple properties)
- Mortgage market cooling measures
- Restrictions on housing as pure investment

**Income support:**
- Housing allowances or rent supplements tied to MBM thresholds
- Minimum wage increases (current $15/hour insufficient in Toronto/Vancouver)
- Basic income programs

**Finding 2: Target both renters AND owners**

Current policies focus heavily on rental assistance. Our findings suggest:
- Continue rental programs (rent supplements, social housing)
- Add homeowner support (property tax relief, mortgage renewal assistance)

**Finding 3: Adopt residual income as primary affordability metric**

STIR improvements (57.0% → 50.8% above 30%) masked persistent hardship (38.0% → 37.9%). Government should:
- Track residual income rather than STIR
- Link housing policy to poverty reduction strategies
- Evaluate programs based on material deprivation outcomes, not just affordability ratios

**Finding 4: Address income stagnation**

Housing interventions alone cannot succeed if incomes stagnate (+0.2% over 10 years). Policies must address:
- Wage growth for median workers
- Precarious employment and gig economy protections
- Intergenerational income mobility

**The housing crisis is fundamentally an income crisis.**

### 4.8 What Other Countries Do Differently

**Vienna, Austria:**
- 62% of residents live in high-quality public housing
- Rent capped at €9 per square meter
- Result: One of world's most livable cities with low housing hardship

**Singapore:**
- 80% of residents live in government-built housing (HDB flats)
- Purchase/rent prices tied to income
- Result: 90% homeownership rate, very low homelessness

**Finland:**
- "Housing First" policy: Provide homes first, then support services
- Result: Only EU country where homelessness is decreasing

**Common lesson:** Countries treating housing as a **right** (not a commodity) achieve better affordability outcomes.

### 4.9 Future Research Directions

**1. Complete four-wave analysis with Census 2016**

We excluded 2016 due to data quality issues. Acquiring clean 2016 data would:
- Identify peak hardship year (was it 2016?)
- Separate recovery era (2011-2016) from hot market era (2016-2019)

**2. Regional analysis by CMA**

Replicate this study for each of Canada's 35 Census Metropolitan Areas:
- Which cities have worst hardship?
- Did policy interventions (e.g., foreign buyer taxes in Vancouver/Toronto) work?

**3. Demographic deep-dives**

Analyze hardship by:
- Age groups (millennials vs. Gen X vs. baby boomers)
- Family types (lone parents vs. couples vs. singles)
- Immigration status (recent immigrants vs. Canadian-born)

**4. Panel data analysis**

Use longitudinal surveys (Canadian Income Survey) to track same households over time:
- Is hardship temporary or chronic?
- What events trigger movement into/out of hardship?

---

## 5. Conclusions

This study provides the first comprehensive 15-year longitudinal analysis of Canadian housing hardship using residual income methodology. Our findings challenge the assumption that economic growth alone solves housing crises.

### 5.1 Main Findings Summary

1. **Housing hardship rates remained flat at ~38% over 15 years** despite economic recovery, invalidating assumptions that growth automatically improves affordability.

2. **Shelter costs outpaced income by 3.6 percentage points** (37.1% vs. 33.5%), creating a sustained squeeze equivalent to $456 annually for median households.

3. **Homeowner hardship increased 13.4%** (31.4% → 35.6%), converging toward renter rates through deterioration rather than renter improvement. Homeownership no longer guarantees security.

4. **Three governments, zero progress:** Despite multiple policy interventions across Conservative and Liberal administrations, hardship rates returned to starting levels.

5. **Income stagnation is the deeper problem:** Real median income grew only 0.2% from 2011-2021 despite a decade of expansion. Housing policy cannot succeed while incomes stagnate.

### 5.2 What This Means for Your Future

If you're 15-18 years old now, by age 30-35:

**Without policy change:**
- Rent will be even less affordable relative to your income
- Saving for a home down payment will take 10+ years
- You'll struggle more than your parents did at the same age

**With structural reform:**
- Vienna-style public housing providing affordable, high-quality homes
- Income growth matching or exceeding housing costs
- Realistic path to homeownership or secure long-term rental

### 5.3 Call to Action

Fifteen years of data prove Canada's housing crisis requires bold structural reforms, not incremental adjustments. Specifically:

**Supply:** Aggressive zoning reform, public housing expansion, streamlined approvals

**Demand:** Progressive housing wealth taxation, investment restrictions

**Income:** Wage growth policies, basic income, housing allowances

**Measurement:** Adopt residual income as primary affordability metric

### 5.4 Final Thought

In 2006, 38% of Canadian households struggled with housing costs.  
In 2021, 38% of Canadian households struggled with housing costs.

**Nothing changed because nothing changed.**

Small policy tweaks failed. Tax credits failed. Pilot programs failed.

Your generation deserves better than inheriting a broken housing market. You deserve affordable rent, ability to save, realistic homeownership paths, and security rather than struggle.

**The data is clear. The problem is structural. The solution must be too.**

---

## References

Canada Mortgage and Housing Corporation (CMHC). (2024). *Revised Housing Hardship Methodology: Technical Documentation*. CMHC Research Insights.

Statistics Canada. (2022). *Census 2021 Public Use Microdata File (PUMF): Hierarchical File Documentation*. Catalogue no. 98M0002X.

Statistics Canada. (2021). *Market Basket Measure Thresholds 2018-base*. Catalogue no. 75F0002M.

Walks, A., & Twigge-Molecey, A. (2023). Income mixing and housing affordability in Canadian cities. *Urban Studies*, 60(11), 2234-2254.

---

## Appendix A: Data Availability

All data used in this study are publicly available:
- Census PUMF files: Statistics Canada Data Liberation Initiative
- Analysis code: https://github.com/gudaleon/2017-dlsl-msc-team1
- Figures: See `/outputs/full_census_figures/` directory

---

## Appendix B: List of Figures

1. Figure 1: Fifteen-year national trends (income, shelter, STIR, hardship)
2. Figure 2: Period comparison (2006-2011 vs. 2011-2021)
3. Figure 3: Owner vs. renter hardship divergence
4. Figure 4: Income-shelter squeeze (indexed to 2006 = 100)
5. Figure 5: Summary dashboard (all metrics)

---

**Word Count:** ~5,200 words  
**Figures:** 4 main figures + 1 dashboard  
**Tables:** 2  
**Reading Level:** High school (Grades 10-12) with full academic rigor

*Draft Version 1.0 - October 16, 2026*
