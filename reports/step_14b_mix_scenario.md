# Step 14B — Scenario 1: Product Mix Rebalancing

## Executive Summary

This report presents **Scenario 1 (Product Mix Rebalancing)**, the first mechanical what-if sensitivity analysis performed on the validated **CY2012 USD** dataset (`CurrencyKey = 100`).

The scenario models the mechanical Gross Profit impact of shifting **5% of CY2012 unit volume** away from two heavily value-destructive subcategories (**Road Bikes** and **Touring Bikes**) toward a highly profitable target subcategory (**Mountain Bikes**).

### Key Financial Findings
- **Baseline CY2012 Net Revenue**: **$20,908,342.06**
- **Baseline CY2012 Gross Profit**: **$674,861.75**
- **Baseline CY2012 Gross Margin %**: **3.23%** (3.227715%)
- **Total Units Shifted**: **722.40 units** (694.80 from Road Bikes, 27.60 from Touring Bikes)
- **Net Revenue Impact**: **+$227,006.99** (Revenue gained in Mountain Bikes less revenue lost in Road/Touring Bikes)
- **Incremental Gross Profit**: **+$93,547.97**
- **Scenario Gross Profit**: **$768,409.72**
- **Scenario Gross Margin %**: **3.64%** (3.635661%)
- **Gross Profit Improvement %**: **+13.86%** (+13.861798%)

---

## Scenario Objective & Scope

### Scope Boundaries
- **Dataset / Scope**: Reseller Sales (`abt_reseller_sales`), `CurrencyKey = 100` (USD), Calendar Year 2012 (`CalendarYear = 2012`).
- **Source Subcategories**:
  - **Road Bikes** (CY2012 Volume: 13,896 units; Gross Profit: -$351,997.27)
  - **Touring Bikes** (CY2012 Volume: 552 units; Gross Profit: -$136,107.21)
- **Target Subcategory**:
  - **Mountain Bikes** (CY2012 Volume: 6,505 units; Gross Profit: +$622,610.18)

### Core Assumptions & Controls
1. **Shift Percentage**: Exactly **5%** of CY2012 units are shifted from **each** source subcategory into Mountain Bikes.
2. **Constant Portfolio Volume**: Total portfolio volume is strictly conserved at **58,276 units** (722.40 units removed from source subcategories and added to Mountain Bikes).
3. **Unchanged Unit Pricing & Costs**: Realized price per unit, standard cost per unit, and discount rates remain unchanged for all products.
4. **Target Economics**: Mountain Bikes contains multiple products; per instructions, Mountain Bikes economics are modeled using its CY2012 weighted-average realized price ($1,020.20/unit) and weighted-average standard cost ($924.49/unit).
5. **No Elasticity / Commercial Execution Overhead**: This is a **mechanical accounting sensitivity test**, NOT a forecast, demand model, or commercial prediction.

---

## Unit-Level Subcategory Economics (CY2012 USD)

The table below outlines the underlying CY2012 unit-level economics for the source and target subcategories:

| Subcategory | CY2012 Units | Net Revenue ($) | Total Cost ($) | Gross Profit ($) | Realized Price / Unit ($) | Std Cost / Unit ($) | Unit GP ($) | Unit GM % |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Road Bikes** (Source 1) | 13,896 | $9,820,379.11 | $10,172,376.37 | -$351,997.27 | $706.71 | $732.04 | -$25.33 | -3.58% |
| **Touring Bikes** (Source 2) | 552 | $379,339.15 | $515,446.36 | -$136,107.21 | $687.21 | $933.78 | -$246.57 | -35.88% |
| **Mountain Bikes** (Target) | 6,505 | $6,636,404.79 | $6,013,794.61 | +$622,610.18 | $1,020.20 | $924.49 | +$95.71 | +9.38% |

---

## Detailed Source Subcategory Breakdown

Shifting 5% of CY2012 units from each source subcategory to Mountain Bikes produces the following breakdown:

| Source Subcategory | CY2012 Units | Shift % | Units Shifted | Source Unit GP ($) | Target Unit GP ($) | GP Lost / Eliminated ($) | GP Gained in Target ($) | Net Incremental GP ($) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Road Bikes** | 13,896.0 | 5.0% | 694.80 | -$25.33 | +$95.71 | -$17,599.86 | +$66,501.08 | **+$84,100.95** |
| **Touring Bikes** | 552.0 | 5.0% | 27.60 | -$246.57 | +$95.71 | -$6,805.36 | +$2,641.67 | **+$9,447.03** |
| **Total / Weighted** | **14,448.0** | **5.0%** | **722.40** | **-$29.56** | **+$95.71** | **-$24,405.22** | **+$69,142.75** | **+$93,547.97** |

### Mechanics of the Incremental GP
- **Road Bikes Shift (694.80 units)**:
  - Removing 694.80 loss-making Road Bike units eliminates **$17,599.86** of Gross Profit loss.
  - Selling 694.80 units of Mountain Bikes generates **$66,501.08** of Gross Profit.
  - Net Incremental GP = $66,501.08 - (-$17,599.86) = **+$84,100.95**.
- **Touring Bikes Shift (27.60 units)**:
  - Removing 27.60 severely loss-making Touring Bike units eliminates **$6,805.36** of Gross Profit loss.
  - Selling 27.60 units of Mountain Bikes generates **$2,641.67** of Gross Profit.
  - Net Incremental GP = $2,641.67 - (-$6,805.36) = **+$9,447.03**.

---

## Overall Scenario Summary

Combining the source subcategory shifts with the baseline portfolio economics yields the overall scenario result:

| Metric | Baseline CY2012 | Scenario 1 Impact | Scenario 1 Total | Change (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Portfolio Units** | 58,276.00 | 0.00 | 58,276.00 | 0.00% |
| **Total Units Shifted** | — | 722.40 | 722.40 | — |
| **Net Revenue** | $20,908,342.06 | +$227,006.99 | $21,135,349.05 | +1.09% |
| **Gross Profit** | $674,861.75 | +$93,547.97 | $768,409.72 | **+13.86%** |
| **Gross Margin %** | 3.23% | +0.41% pts | **3.64%** | +12.64% |

---

## Automated Verification & Reconciliation Results

The automated script `scripts/verify_what_if_mix_scenario.py` ran 8 rigorous checks against PostgreSQL:
1. **Subcategory Existence**: Verified that `Road Bikes`, `Touring Bikes`, and `Mountain Bikes` exist in CY2012 USD reseller sales (`PASS`).
2. **Shift Volume Accuracy**: Verified that shifted units are exactly 5.0% of source units (694.80 Road Bikes, 27.60 Touring Bikes) (`PASS`).
3. **Volume Conservation**: Verified that total portfolio volume remains strictly 58,276 units (`PASS`).
4. **Revenue Reconciliation**: Verified scenario net revenue equals baseline revenue + net revenue impact ($20,908,342.06 + $227,006.99 = $21,135,349.05) (`PASS`).
5. **Gross Profit Reconciliation**: Verified scenario Gross Profit equals baseline Gross Profit + incremental Gross Profit ($674,861.75 + $93,547.97 = $768,409.72) (`PASS`).
6. **Gross Margin Consistency**: Verified scenario Gross Margin % ($768,409.72 / $21,135,349.05 = 3.635661%) matches formula (`PASS`).
7. **No Duplicate Rows**: Confirmed exactly 2 source subcategory rows and 1 summary row (`PASS`).
8. **Mathematical Integrity**: Reconciled subcategory totals to summary metrics with zero residual (`PASS`).

---

## Observational Conclusions

1. **High Profit Leverage from Negative Margin Elimination**:
   Shifting just 5% of unit volume (722.40 units out of 58,276 total portfolio units, or 1.24% of portfolio volume) increases overall portfolio Gross Profit by **+13.86%** (+$93.5k). This high multiplier occurs because eliminating negative unit margins provides a dual benefit: eliminating losses while capturing positive gross margin.

2. **Road Bikes Dominates Absolute GP Impact**:
   Because Road Bikes has large CY2012 volume (13,896 units), shifting 5% yields 694.80 units and **$84,100.95** in incremental GP (89.9% of the total scenario gain).

3. **Touring Bikes Has Extreme Unit Drag**:
   Although Touring Bikes represents only 27.60 shifted units, its severe negative unit GP (-$246.57/unit) means removing those 27.60 units eliminates $6.8k of gross loss, generating **$9,447.03** in incremental GP.

4. **Accounting Sensitivity Context**:
   This test establishes the theoretical upper bound of mix rebalancing without price or cost alterations. Commercial execution would require evaluating production capacity, dealer demand, and cannibalization risk.
