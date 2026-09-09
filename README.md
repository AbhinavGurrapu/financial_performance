# AdventureWorks Financial Performance & Profitability Analytics

This is a financial performance analytics project built using AdventureWorks reseller sales data in PostgreSQL and Python. Between Calendar Year 2011 (CY2011) and Calendar Year 2012 (CY2012), Net Revenue increased from $14.47M to $20.91M (+44.52%), while CY2012 Gross Profit reached $674.86K with a razor-thin Gross Margin of only 3.23%. The analysis investigates what drove revenue growth, whether top-line expansion translated into profitable growth, where value creation and destruction occurred across segments, and what mechanical improvement scenarios look like.

---

## 1. Business Questions

This project answers seven core business questions:
1. What changed in revenue, unit volume, selling price, Gross Profit, and Gross Margin between CY2011 and CY2012?
2. What drove top-line Net Revenue growth?
3. Did top-line revenue growth translate into profitable growth?
4. Which products, subcategories, categories, and business types created or destroyed Gross Profit?
5. What explains the major profitability differences across portfolio segments?
6. Which performance trends represent higher-quality versus lower-quality growth?
7. Which controllable decision levers show meaningful mechanical profit upside?

---

## 2. Analytical Approach

The analytical workflow follows a logical progression from historical diagnosis to sensitivity modeling:

**What Happened**  
$$\rightarrow$$ **Revenue Price/Volume/Mix Decomposition**  
$$\rightarrow$$ **Gross Profit Driver Decomposition**  
$$\rightarrow$$ **Growth-Quality & Segment Diagnostics**  
$$\rightarrow$$ **Mechanical What-If Scenarios**

- **Revenue Price-Volume-Mix (PVM) Decomposition**: Separates historical Net Revenue change into additive Price, Volume, and Mix effects using discrete index-number decomposition formulas.
- **Gross Profit Driver Decomposition**: Separates historical Gross Profit change into Price, Unit Cost, Volume, and Product Mix effects to isolate how margin structure evolved.
- **Segment Diagnostics**: Evaluates performance across product categories, subcategories, reseller business types, and sales territories to identify where profitable growth occurred and where profit was destroyed.
- **Mechanical What-If Scenarios**: Tests hypothetical accounting impacts under explicit fixed assumptions to quantify profit sensitivity across key decision levers.

*Note: PVM and Gross Profit driver calculations are descriptive accounting decompositions of historical variance rather than causal models of customer demand.*

---

## 3. Key Findings

### Revenue & Profitability
- **Net Revenue**: $14.47M $\rightarrow$ $20.91M (+$6.44M / +44.52%)
- **Gross Profit**: $57.56K $\rightarrow$ $674.86K (+$617.30K / +1,072.44%)
- **Gross Margin %**: 0.40% $\rightarrow$ 3.23% (+2.83 percentage points)
- **Unit Sales**: 21,611 units $\rightarrow$ 58,276 units (+169.66%)
- **Realized Average Selling Price (ASP)**: $669.43 $\rightarrow$ $358.78 (-46.41%)

### Revenue PVM
- **Price Effect**: +$366,094.82
- **Volume Effect**: +$24,544,760.73
- **Mix Effect**: -$18,469,629.93
- **Net Revenue Change**: +$6,441,225.63

Unit volume expansion was the primary positive driver of top-line growth, while a shift toward lower-priced items created a large negative mix offset. This PVM breakdown is an accounting decomposition rather than proof of causal customer substitution behavior.

### Gross Profit Drivers
- **Price Effect**: +$366,094.82
- **Unit Cost Effect**: $0.00
- **Volume Effect**: +$97,657.34
- **Product Mix Effect**: +$153,548.62
- **Total Gross Profit Change**: +$617,300.78

Unit costs remain static at the product level in this dataset, so the analysis does not claim observed manufacturing cost inflation.

### Growth Quality & Segment Findings
Comparing top-line revenue against gross profit contributions reveals major performance divergences across portfolio segments:

- **Components Category**: Generated +$303,329.22 in incremental Gross Profit (high-quality growth).
- **Bikes Category**: Generated +$281,429.97 in incremental Gross Profit overall, but contained severe internal segment divergence.
- **Road Bikes Subcategory**: Added +$4.33M in Net Revenue but destroyed -$283,117.66 in Gross Profit (negative unit gross margins).
- **Touring Bikes Subcategory**: Added +$379,339.15 in Net Revenue but destroyed -$136,107.21 in Gross Profit (severe negative unit gross margins).
- **Mountain Bikes Subcategory**: Net Revenue contracted by -$967,506.86, but Gross Profit expanded by +$639,784.82 due to strong margin expansion.
- **Specialty Bike Shop Channel**: Net Revenue contracted by -$165,234.53, yet Gross Profit increased by +$23,809.67 as gross margin expanded from 0.12% to 20.62%.

These findings demonstrate why evaluating top-line revenue growth alone is insufficient to assess business performance.

---

## 4. Mechanical What-If Scenarios

Three mechanical what-if scenarios were implemented to evaluate the profit sensitivity of controllable business levers. These calculations are hypothetical accounting sensitivity tests, **NOT** forecasts or predictive models.

| Scenario | Tested Assumption | Incremental Gross Profit | GP Improvement |
| :--- | :--- | ---: | ---: |
| **Product Mix** | Shift 5% of Road + Touring units to Mountain Bikes | +$93,547.97 | +13.86% |
| **Price Realization** | Increase realized price 2% for Road + Touring Bikes | +$203,994.37 | +30.23% |
| **Discount Reduction** | Reduce existing discounts 50% for Accessories + Clothing | +$3,291.42 | +0.49% |

*Important Note: The three scenarios use different intervention sizes, so their dollar impacts should not be interpreted as a normalized ranking of intrinsic lever effectiveness.*

Under the tested assumptions, targeted price realization produced the largest modeled Gross Profit impact (+$203.99K), product mix rebalancing was the second-largest (+$93.55K), while the tested discount reduction had limited upside (+$3.29K) because baseline discount dollars in Accessories and Clothing were already small ($6.58K combined).

- **Structural Limitation**: A 2% price realization increase improves Touring Bikes unit GP from -$246.57 to -$232.83, but leaves it deeply loss-making because standard cost ($933.78) remains far above realized price ($700.95).
- **Commercial Context**: Real-world implementation would require validating customer price sensitivity, commercial feasibility, production capacity, and channel dynamics.

---

## 5. Data & Scope

- **Data Source**: AdventureWorks DW reseller sales dataset
- **Fact Table**: `FactResellerSales`
- **Main Dimensions**: `DimProduct`, `DimProductSubcategory`, `DimProductCategory`, `DimReseller`, `DimSalesTerritory`, `DimDate`
- **Currency Scope**: `CurrencyKey = 100` (USD Reseller Sales)
- **Historical Comparison**: Calendar Year 2011 vs. Calendar Year 2012
- **What-If Baseline**: Calendar Year 2012
- **Database Engine**: PostgreSQL 18
- **Consolidated Modeling View**: `abt_reseller_sales` (Analytical Base Table)

*Product standard costs in this dataset are dataset-level standard costs rather than observed real-world manufacturing costs.*

---

## 6. Tech Stack

- **Database**: PostgreSQL 18
- **Query Language**: SQL / Common Table Expressions (CTEs) / Window Functions
- **Scripting & Analytics**: Python 3.10+
- **Data Manipulation**: `pandas`, `numpy`
- **Database Driver**: `psycopg2`
- **Version Control & Documentation**: Git, Markdown

---

## 7. Project Structure

```
financial_performance/
├── data/
│   └── staging/
├── sql/
│   ├── create_tables.sql
│   ├── load_data.sql
│   ├── create_abt.sql
│   ├── master_load_and_verify.sql
│   ├── 03_profitability_decomposition.sql
│   ├── 04_growth_quality_diagnostics.sql
│   ├── 05_what_if_mix_scenario.sql
│   ├── 06_what_if_price_scenario.sql
│   └── 07_what_if_discount_scenario.sql
├── scripts/
│   ├── sanitize_dimproduct.py
│   ├── verify_abt.py
│   ├── verify_profitability_decomposition.py
│   ├── verify_growth_quality_diagnostics.py
│   ├── verify_what_if_mix_scenario.py
│   ├── verify_what_if_price_scenario.py
│   └── verify_what_if_discount_scenario.py
├── reports/
│   ├── stage_3_profitability_decomposition.md
│   ├── stage_4_growth_quality_diagnostics.md
│   ├── step_14b_mix_scenario.md
│   ├── step_14b_price_scenario.md
│   ├── step_14b_discount_scenario.md
│   └── step_14c_comparison.md
├── notebooks/
├── archive/
└── README.md
```

---

## 8. Reproducibility

### Prerequisites
- PostgreSQL 18 installed locally with database user `postgres` and database `postgres`.
- Python 3.10+ environment with `pandas`, `numpy`, and `psycopg2`.

### Execution Workflow

1. **Sanitize Data File Quality**:
   ```bash
   python scripts/sanitize_dimproduct.py
   ```

2. **Load Raw Data & Execute Schema Assertions**:
   ```bash
   psql -U postgres -d postgres -f sql/master_load_and_verify.sql
   ```

3. **Build Consolidated Analytical Base Table (ABT)**:
   ```bash
   psql -U postgres -d postgres -f sql/create_abt.sql
   ```

4. **Verify ABT Quality Assertions**:
   ```bash
   python scripts/verify_abt.py
   ```

5. **Run Profitability Driver Decomposition Pipeline**:
   ```bash
   python scripts/verify_profitability_decomposition.py
   ```

6. **Run Growth Quality & Segment Diagnostics Pipeline**:
   ```bash
   python scripts/verify_growth_quality_diagnostics.py
   ```

7. **Run What-If Scenario Pipelines**:
   ```bash
   python scripts/verify_what_if_mix_scenario.py
   python scripts/verify_what_if_price_scenario.py
   python scripts/verify_what_if_discount_scenario.py
   ```

---

## 9. Methodological Notes

- **Accounting Decomposition**: PVM and Gross Profit driver models are descriptive accounting decompositions of variance. They partition historical performance into mathematical components and do not establish causal relationships.
- **New & Discontinued Products**: Handled using explicit baseline analytical conventions ($P_{11} = P_{12}$ and $C_{11} = C_{12}$ for new products; $Q_{12} = 0$ for discontinued products) to avoid undefined price/cost ratios while isolating volume and mix effects.
- **Dataset-Level Standard Costs**: Product costs are dataset-level standard costs provided in AdventureWorks DW rather than actual dynamic factory costs.
- **Mechanical Sensitivity Scenarios**: What-if scenarios test accounting sensitivity under static assumptions (e.g., fixed volume, fixed costs). They should be interpreted as theoretical sensitivity benchmarks, not forecasts of customer demand response.
