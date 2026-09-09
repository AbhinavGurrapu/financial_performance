# Step 14B — Scenario 2: Targeted Price Realization

## Executive Summary

This report details **Scenario 2 (Targeted Price Realization)**, the second mechanical what-if sensitivity analysis performed on the validated **CY2012 USD** dataset (`CurrencyKey = 100`).

The scenario models the mechanical financial impact of a **2% increase in realized selling price (ASP)** across all units sold in the portfolio's two value-destructive subcategories: **Road Bikes** and **Touring Bikes**.

### Key Financial Findings
- **Baseline CY2012 Net Revenue**: **$20,908,342.06**
- **Baseline CY2012 Gross Profit**: **$674,861.75**
- **Baseline CY2012 Gross Margin %**: **3.23%** (3.227715%)
- **Incremental Net Revenue**: **+$203,994.37** (+$196,407.58 from Road Bikes, +$7,586.78 from Touring Bikes)
- **Scenario Net Revenue**: **$21,112,336.43**
- **Incremental Gross Profit**: **+$203,994.37**
- **Scenario Gross Profit**: **$878,856.11**
- **Scenario Gross Margin %**: **4.16%** (4.162761%)
- **Gross Profit Improvement %**: **+30.23%** (+30.227579%)

---

## Scenario Objective & Scope

### Scope Boundaries
- **Dataset / Scope**: Reseller Sales (`abt_reseller_sales`), `CurrencyKey = 100` (USD), Calendar Year 2012 (`CalendarYear = 2012`).
- **Target Subcategories**:
  - **Road Bikes** (CY2012 Volume: 13,896 units; Baseline Gross Profit: -$351,997.27)
  - **Touring Bikes** (CY2012 Volume: 552 units; Baseline Gross Profit: -$136,107.21)

### Core Assumptions & Controls
1. **Targeted Price Adjustment**: Realized Average Selling Price (ASP) is increased by exactly **2%** for all units in Road Bikes and Touring Bikes.
2. **Constant Unit Volume**: Unit sales remain strictly constant (13,896 Road Bikes and 552 Touring Bikes). Total portfolio volume is unchanged at 58,276 units.
3. **Constant Standard Cost**: Standard unit costs remain strictly constant ($732.04/unit for Road Bikes, $933.78/unit for Touring Bikes).
4. **Unchanged Product Mix**: Product mix within each subcategory remains unchanged.
5. **No Other Changes**: Prices, costs, and volumes for all other subcategories remain untouched.
6. **Accounting Sensitivity Framing**: This calculation is strictly a **mechanical accounting sensitivity test** assuming zero price elasticity for baseline calculation purposes. It is NOT a commercial forecast, price demand model, or customer response estimate.

---

## Important Mathematical Identity Verification

Because unit volume ($Q$) and standard cost per unit ($C$) are held strictly constant:

$$	ext{Net Revenue} = Q 	imes 	ext{ASP}$$
$$	ext{Cost of Goods Sold} = Q 	imes C$$
$$	ext{Gross Profit} = (Q 	imes 	ext{ASP}) - (Q 	imes C) = 	ext{Net Revenue} - 	ext{COGS}$$

Taking the differential with respect to realized ASP when volume $Q$ and unit cost $C$ are fixed:

$$\Delta 	ext{Gross Profit} = \Delta 	ext{Net Revenue} - \Delta 	ext{COGS} = \Delta 	ext{Net Revenue} - 0 = \Delta 	ext{Net Revenue}$$

### Empirical Identity Audit
- **Incremental Net Revenue**: **+$203,994.365248**
- **Incremental Gross Profit**: **+$203,994.365248**
- **Identity Residual**: **$0.000000000000** (Exact zero residual verified across both subcategories and overall summary).

---

## Detailed Target Subcategory Breakdown

Applying a 2% realized price increase to Road Bikes and Touring Bikes yields the following subcategory breakdown:

| Metric | Road Bikes (Target 1) | Touring Bikes (Target 2) | Combined Target Total |
| :--- | :---: | :---: | :---: |
| **CY2012 Units** | 13,896 | 552 | **14,448** |
| **Price Adjustment %** | +2.0% | +2.0% | **+2.0%** |
| **Baseline Realized ASP ($)** | $706.71 | $687.21 | **$705.96** |
| **Scenario Realized ASP ($)** | $720.84 | $700.95 | **$720.08** |
| **Baseline Unit GP ($)** | -$25.33 | -$246.57 | **-$33.79** |
| **Scenario Unit GP ($)** | -$11.20 | -$232.83 | **-$19.68** |
| **Baseline Net Revenue ($)** | $9,820,379.11 | $379,339.15 | **$10,199,718.25** |
| **Scenario Net Revenue ($)** | $10,016,786.69 | $386,925.93 | **$10,403,712.62** |
| **Incremental Net Revenue ($)** | **+$196,407.58** | **+$7,586.78** | **+$203,994.37** |
| **Baseline Gross Profit ($)** | -$351,997.27 | -$136,107.21 | **-$488,104.48** |
| **Scenario Gross Profit ($)** | -$155,589.68 | -$128,520.43 | **-$284,110.11** |
| **Incremental Gross Profit ($)** | **+$196,407.58** | **+$7,586.78** | **+$203,994.37** |
| **Baseline Gross Margin %** | -3.58% | -35.88% | **-4.79%** |
| **Scenario Gross Margin %** | **-1.55%** | **-33.22%** | **-2.73%** |

---

## Overall Portfolio Scenario Summary

Combining the targeted subcategory price adjustments with the baseline portfolio economics yields the overall scenario result:

| Metric | Baseline CY2012 | Scenario 2 Impact | Scenario 2 Total | Change (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Portfolio Units** | 58,276.00 | 0.00 | 58,276.00 | 0.00% |
| **Net Revenue** | $20,908,342.06 | **+$203,994.37** | **$21,112,336.43** | +0.98% |
| **Gross Profit** | $674,861.75 | **+$203,994.37** | **$878,856.11** | **+30.23%** |
| **Gross Margin %** | 3.23% | **+0.94% pts** | **4.16%** | +28.97% |

---

## Automated Verification & Reconciliation Results

The automated script `scripts/verify_what_if_price_scenario.py` executed 9 rigorous audit checks against PostgreSQL:
1. **Target Subcategory Existence**: Confirmed `Road Bikes` and `Touring Bikes` exist in CY2012 USD data (`PASS`).
2. **Price Realization Accuracy**: Verified scenario ASP equals baseline ASP $	imes 1.02$ for both subcategories (`PASS`).
3. **Volume Conservation**: Confirmed unit volumes remain strictly unchanged (`PASS`).
4. **Revenue Reconciliation**: Verified scenario net revenue equals baseline revenue + incremental net revenue ($20,908,342.06 + $203,994.37 = $21,112,336.43) (`PASS`).
5. **Mathematical Identity Verification**: Confirmed incremental Gross Profit equals incremental Net Revenue with $0.000000000000$ residual (`PASS`).
6. **Gross Profit Reconciliation**: Verified scenario Gross Profit equals baseline Gross Profit + incremental Gross Profit ($674,861.75 + $203,994.37 = $878,856.11) (`PASS`).
7. **Gross Margin Consistency**: Verified scenario Gross Margin % ($878,856.11 / $21,112,336.43 = 4.162761%) matches formula (`PASS`).
8. **No Duplicate Rows**: Confirmed exactly 2 subcategory rows and 1 summary row (`PASS`).
9. **Zero Residual Reconciliation**: All subcategory metrics aggregate cleanly to summary metrics (`PASS`).

---

## Observational Conclusions

1. **Substantial Leverage on Low Baseline Margin**:
   Because baseline portfolio Gross Profit is small ($674.9k on $20.9M revenue, or 3.23% margin), a modest 2% price increase on just two subcategories (representing 48.8% of portfolio revenue) yields a **+30.23% increase in portfolio Gross Profit** (+$203.99k).

2. **Road Bikes Account for 96.3% of Scenario Gain**:
   Due to its high volume (13,896 units) and revenue ($9.82M), Road Bikes contributes **$196,407.58** of the $203,994.37 incremental Gross Profit. Its unit loss shrinks from -$25.33/unit to -$11.20/unit.

3. **Touring Bikes Remains Deeply Loss-Making**:
   While a 2% price realization increase adds $7,586.78 in revenue and profit, Touring Bikes' standard unit cost ($933.78) is so far above its price ($700.95) that its unit GP remains severely negative (-$232.83/unit vs -$246.57 baseline). Price realization alone cannot solve Touring Bikes' negative margin without cost restructuring or major repositioning.

4. **100% Gross Profit Flow-Through**:
   Holding volume and cost fixed ensures that 100% of price realization gains drop directly to Gross Profit.
