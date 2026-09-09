# Financial Performance Analysis & Profitability Driver Decomposition

An end-to-end enterprise data engineering and financial analytics project built on the **AdventureWorks Data Warehouse** dataset. This repository implements automated data ingestion, data quality sanitization, Analytical Base Table (ABT) modeling, and a mathematically exact **4-Factor Gross Profit Driver Decomposition** (Price, Unit Cost, Volume, Product Mix) across 330 reseller products between CY2011 and CY2012.

---

## Executive Overview & Business Problem

Between Calendar Year 2011 (CY2011) and Calendar Year 2012 (CY2012), AdventureWorks Reseller Gross Profit expanded significantly from **,560.96** to **,861.75** — representing a total Gross Profit change of **+,300.78** (+1,072.44%). 

The primary business objective is to isolate and quantify the exact commercial drivers behind this profit growth:
1. **Price Effect**: How much profit growth was driven by realized price adjustments ( = \text{Net Revenue} / \text{Units}$)?
2. **Unit Cost Effect**: How much profit change was driven by underlying standard product cost shifts?
3. **Volume Effect**: How much profit growth was driven by total unit growth valued at baseline portfolio margins?
4. **Product Mix Effect**: How much profit growth was driven by portfolio rebalancing toward higher-margin products?

---

## Key Analytical Results

| Profitability Driver | Dollar Impact ($) | % Contribution | Primary Business Insight |
| :--- | :--- | :--- | :--- |
| **Price Effect** | **+,094.82** | **59.31%** | Realized price growth driven by lower average discount rates across core bike models. |
| **Unit Cost Effect** | **.00** | **0.00%** | Product Standard Cost per unit remained constant across both years in source data. |
| **Volume Effect** | **+,657.34** | **15.82%** | Total unit volume expansion from 21,611 to 58,276 units valued at baseline UGP (.6635/unit). |
| **Product Mix Effect** | **+,548.62** | **24.87%** | Strategic portfolio mix shift toward higher-margin Components and high-margin Touring subcategories. |
| **Reconciled Gross Profit Change** | **+,300.78** | **100.00%** | **100% Exact Reconciliation (Zero Unexplained Residual)** |

---

## Project Structure

`	ext
financial_performance/
│
├── data/
│   ├── raw/                        # Raw DW CSV files & database backups (Excluded from Git)
│   └── staging/                    # Sanitized staging files & Stage 3 output CSVs
│
├── sql/
│   ├── create_tables.sql           # PostgreSQL DDL table schema definitions
│   ├── load_data.sql               # Client-side \copy data ingestion script
│   ├── create_abt.sql              # ABT creation script (abt_reseller_sales)
│   ├── master_load_and_verify.sql  # Master pipeline setup, data load & 0-orphan assertion script
│   └── 03_profitability_decomposition.sql # Product-level 4-factor Gross Profit bridge & rollups
│
├── scripts/
│   ├── sanitize_dimproduct.py      # Data pipeline script (strips NUL bytes from raw DimProduct.csv)
│   ├── verify_abt.py               # Core ABT quality verification script (7-phase assertion)
│   ├── verify_profitability_decomposition.py # Executable 15-point automated validation suite
│   │
│   └── data_quality/               # Reusable Data Quality & Profiling Suite
│       ├── financial_profiler.py   # Statistical profiler for ranges, types, and summary metrics
│       ├── profiler.py              # Profiler for shape and NULL count analysis
│       ├── audit_nulls.py          # NULL distribution auditor across raw CSVs
│       ├── audit_csvs.py           # Delimiter, line count, and byte size auditor
│       ├── check_null_conflicts.py # Compares empty strings against NOT NULL DDL constraints
│       ├── compare_schemas.py      # Compares SQL Server DDL with PostgreSQL DDL
│       ├── investigate_anomalies.py# Financial & price discount anomaly detection script
│       └── schema_summary.py       # DDL schema primary key and column parser
│
├── archive/
│   └── data_loading_debug/         # Historical one-off debugging & troubleshooting scripts
│       ├── check_chars.py
│       ├── check_dimproduct.py
│       ├── check_dimproduct_cols.py
│       ├── check_nul_bytes.py
│       ├── test_db.py
│       ├── test_load_product.sql
│       ├── verify.py
│       └── verify_reseller.py
│
├── notebooks/                      # Exploratory Jupyter notebooks
│
├── reports/                        # Executive methodology notes & stage reports
│   ├── abt_notes.md                # ABT design & grain specification
│   ├── data_loading_notes.md       # Data ingestion & schema design notes
│   └── stage_3_profitability_decomposition.md # Stage 3 full analytical report & validation results
│
├── .gitignore                      # Git ignore rules for data backups, caches, and secrets
└── README.md                       # Executive project documentation & pipeline guide
`

---

## Data Scope & Methodology

### Data Scope
- **Source Database**: AdventureWorks Data Warehouse (PostgreSQL 18)
- **Analytical Table**: bt_reseller_sales
- **Scope Boundary**: CurrencyKey = 100 (USD Reseller Sales)
- **Timeframe Scope**: Calendar Year 2011 vs. Calendar Year 2012
- **Analytical Grain**: ProductKey (330 unique products across both years)

### Methodological Conventions & Non-Double-Counting Safeguards
- **Realized Selling Price**:  = \text{Net Revenue} / \text{Units} = \text{SalesAmount} / \text{OrderQuantity}$. Because Realized Price already incorporates discounts, discounting is NOT added as a fifth factor to the main Gross Profit bridge.
- **New Products ({11} = 0, Q_{12} > 0$)**: Evaluated using {11} = P_{12}$ and {11} = C_{12}$ as analytical conventions, attributing margin gain to Volume Effect ({12} \times \overline{UGP}_{11}$) and Product Mix Effect ({12} \times (UGP_{12} - \overline{UGP}_{11})$).
- **Discontinued Products ({11} > 0, Q_{12} = 0$)**: Evaluated using {12} = 0$ and {12} = 0$, attributing margin loss to Volume Effect ($-Q_{11} \times \overline{UGP}_{11}$) and Product Mix Effect ($-Q_{11} \times (UGP_{11} - \overline{UGP}_{11})$).

---

## Reproducibility & Pipeline Execution Guide

### Prerequisites
- **Database**: PostgreSQL 18
- **Environment**: Python 3.10+ (pandas, 
umpy, psycopg2)

### Step-by-Step Execution

1. **Sanitize Data Quality**:
   `ash
   python scripts/sanitize_dimproduct.py
   `

2. **Run Master Database Load & Verification**:
   `ash
   psql -U postgres -d postgres -f sql/master_load_and_verify.sql
   `

3. **Build Analytical Base Table (ABT)**:
   `ash
   psql -U postgres -d postgres -f sql/create_abt.sql
   `

4. **Run Core ABT Verification Suite**:
   `ash
   python scripts/verify_abt.py
   `

5. **Execute Profitability Decomposition & 15-Point Validation Suite**:
   `ash
   python scripts/verify_profitability_decomposition.py
   `

---

## Analytical Disclaimers

> [!NOTE]
> **Descriptive Accounting Decomposition**:
> Price-Volume-Mix and profitability driver decomposition are descriptive mathematical/accounting decompositions. They isolate accounting variance and do not establish causal economic relationships.

> [!NOTE]
> **Cost Proxy**:
> Product Standard Cost is used as the Cost of Goods Sold (COGS) proxy for this analysis.
