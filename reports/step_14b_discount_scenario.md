# Step 14B — Scenario 3: Targeted Discount Reduction

## Executive Summary

This report details **Scenario 3 (Targeted Discount Reduction)**, the third mechanical what-if sensitivity analysis performed on the validated **CY2012 USD** dataset (`CurrencyKey = 100`).

The scenario models the mechanical financial impact of reducing remaining line-item discounts by **50%** across all transaction lines in two selected high-discount subcategories: **Accessories** and **Clothing**.

### Key Financial Findings
- **Baseline CY2012 Net Revenue**: **$20,908,342.06**
- **Baseline CY2012 Gross Profit**: **$674,861.75**
- **Baseline CY2012 Gross Margin %**: **3.23%** (3.227715%)
- **Baseline Target Discount Amount**: **$6,582.84** ($1,545.93 Accessories + $5,036.91 Clothing)
- **Scenario Target Discount Amount**: **$3,291.42** ($772.97 Accessories + $2,518.46 Clothing)
- **Discount Savings**: **+$3,291.42**
- **Incremental Net Revenue**: **+$3,291.42**
- **Scenario Net Revenue**: **$20,911,633.49**
- **Incremental Gross Profit**: **+$3,291.42**
- **Scenario Gross Profit**: **$678,153.17**
- **Scenario Gross Margin %**: **3.24%** (3.242947%)
- **Gross Profit Improvement %**: **+0.49%** (+0.487718%)

---

## Scenario Objective & Scope

### Scope Boundaries
- **Dataset / Scope**: Reseller Sales (`abt_reseller_sales`), `CurrencyKey = 100` (USD), Calendar Year 2012 (`CalendarYear = 2012`).
- **Target Subcategories**:
  - **Accessories** (CY2012 Volume: 5,390 units; Baseline Gross Profit: $28,988.14)
  - **Clothing** (CY2012 Volume: 17,667 units; Baseline Gross Profit: $111,396.27)

### Core Assumptions & Controls
1. **Line-Item Discount Reduction**: Existing line-item discount rates are reduced by exactly **50%** across all lines in Accessories and Clothing (e.g., a 2.0% line discount becomes 1.0%).
2. **Actual Line-Level Discounts**: Modeled directly from actual CY2012 line-level discount amounts in `abt_reseller_sales` rather than applying an arbitrary generic portfolio discount rate.
3. **Constant Unit Volume & List Prices**: Unit volume (5,390 Accessories, 17,667 Clothing) and list prices (`UnitPrice`) remain strictly unchanged.
4. **Constant Standard Cost**: Standard product costs remain strictly unchanged.
5. **No Other Changes**: Discounts, prices, costs, and volumes for all other subcategories remain untouched.
6. **Accounting Sensitivity Framing**: This calculation is strictly a **mechanical accounting sensitivity test** assuming zero demand response for baseline calculation purposes. It is NOT a forecast, price elasticity model, or customer response prediction.

---

## Important Mathematical Identity Verification

Because unit volume ($Q$), list price ($P$), and standard unit cost ($C$) are held strictly constant:

$$	ext{Gross Revenue} = Q 	imes P$$
$$	ext{Net Revenue} = 	ext{Gross Revenue} - 	ext{Discount Amount}$$
$$	ext{Gross Profit} = 	ext{Net Revenue} - 	ext{COGS}$$

When discount amount is reduced by $\Delta 	ext{Discount}$:

$$\Delta 	ext{Net Revenue} = -\Delta 	ext{Discount Amount} = 	ext{Discount Savings}$$
$$\Delta 	ext{Gross Profit} = \Delta 	ext{Net Revenue} - \Delta 	ext{COGS} = 	ext{Discount Savings} - 0 = 	ext{Discount Savings}$$

### Empirical Identity Audit
$$	ext{Incremental Gross Profit} = 	ext{Incremental Net Revenue} = 	ext{Discount Savings} = +\$3,291.420650$$

- **Discount Savings**: **+$3,291.420650**
- **Incremental Net Revenue**: **+$3,291.420650**
- **Incremental Gross Profit**: **+$3,291.420650**
- **Identity Residual**: **$0.000000000000** (Exact zero residual verified across both subcategories and overall summary).

---

## Detailed Target Subcategory Breakdown

Reducing line-item discounts by 50% for Accessories and Clothing yields the following breakdown:

| Metric | Accessories (Target 1) | Clothing (Target 2) | Combined Target Total |
| :--- | :---: | :---: | :---: |
| **CY2012 Units** | 5,390 | 17,667 | **23,057** |
| **Gross Revenue ($)** | $99,843.96 | $528,588.37 | **$628,432.33** |
| **Baseline Discount Rate %** | 1.55% | 0.95% | **1.05%** |
| **Baseline Discount Amount ($)** | $1,545.93 | $5,036.91 | **$6,582.84** |
| **Scenario Discount Rate %** | **0.77%** | **0.48%** | **0.52%** |
| **Scenario Discount Amount ($)** | **$772.97** | **$2,518.46** | **$3,291.42** |
| **Discount Savings ($)** | **+$772.97** | **+$2,518.46** | **+$3,291.42** |
| **Baseline Net Revenue ($)** | $98,298.04 | $523,551.46 | **$621,849.49** |
| **Scenario Net Revenue ($)** | $99,071.00 | $526,069.91 | **$625,140.91** |
| **Incremental Net Revenue ($)** | **+$772.97** | **+$2,518.46** | **+$3,291.42** |
| **Baseline Gross Profit ($)** | $28,988.14 | $111,396.27 | **$140,384.42** |
| **Scenario Gross Profit ($)** | $29,761.11 | $113,914.73 | **$143,675.84** |
| **Incremental Gross Profit ($)** | **+$772.97** | **+$2,518.46** | **+$3,291.42** |
| **Baseline Gross Margin %** | 29.49% | 21.28% | **22.58%** |
| **Scenario Gross Margin %** | **30.04%** | **21.65%** | **22.98%** |

---

## Overall Portfolio Scenario Summary

Combining targeted discount reductions with baseline portfolio economics yields the overall scenario result:

| Metric | Baseline CY2012 | Scenario 3 Impact | Scenario 3 Total | Change (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Portfolio Units** | 58,276.00 | 0.00 | 58,276.00 | 0.00% |
| **Target Discount Amount** | $6,582.84 | **-$3,291.42** | $3,291.42 | -50.00% |
| **Discount Savings** | — | **+$3,291.42** | +$3,291.42 | — |
| **Net Revenue** | $20,908,342.06 | **+$3,291.42** | **$20,911,633.49** | +0.02% |
| **Gross Profit** | $674,861.75 | **+$3,291.42** | **$678,153.17** | **+0.49%** |
| **Gross Margin %** | 3.23% | **+0.015% pts** | **3.24%** | +0.47% |

---

## Automated Verification & Reconciliation Results

The automated script `scripts/verify_what_if_discount_scenario.py` executed 12 audit checks against PostgreSQL:
1. **Target Subcategory Existence**: Confirmed `Accessories` and `Clothing` exist in CY2012 USD data (`PASS`).
2. **Discount Rate Reduction Accuracy**: Verified scenario discount rate is exactly 50% of baseline rate (`PASS`).
3. **Volume Conservation**: Confirmed unit volumes remain strictly unchanged (`PASS`).
4. **Gross Revenue Conservation**: Confirmed list / gross revenue remains unchanged (`PASS`).
5. **Scenario Discount Calculation**: Verified scenario discount amount equals baseline discount amount $	imes 0.50$ (`PASS`).
6. **Discount Savings Calculation**: Verified discount savings equals baseline discount less scenario discount (`PASS`).
7. **Net Revenue Reconciliation**: Confirmed incremental Net Revenue equals discount savings (`PASS`).
8. **Mathematical Identity Verification**: Confirmed incremental Gross Profit = incremental Net Revenue = discount savings with $0.000000000000$ residual (`PASS`).
9. **Gross Profit Reconciliation**: Verified scenario Gross Profit equals baseline Gross Profit + discount savings ($674,861.75 + $3,291.42 = $678,153.17) (`PASS`).
10. **Gross Margin Consistency**: Verified scenario Gross Margin % ($678,153.17 / $20,911,633.49 = 3.242947%) matches formula (`PASS`).
11. **No Duplicate Rows**: Confirmed exactly 2 target rows and 1 summary row (`PASS`).
12. **Zero Residual Reconciliation**: All target metrics aggregate cleanly to summary metrics (`PASS`).

---

## Observational Conclusions

1. **Modest Financial Impact Due to Low Baseline Discounting**:
   In CY2012, reseller line-item discounts for Accessories (1.55%) and Clothing (0.95%) were already very low in absolute terms ($6,582.84 combined discount). Consequently, a 50% discount reduction yields **+$3,291.42** in incremental Gross Profit (+0.49% improvement).

2. **100% Gross Profit Conversion**:
   Because volume, list price, and standard cost are fixed, 100% of discount savings convert directly into Net Revenue and Gross Profit.

3. **Comparison Across Levers**:
   Compared to Scenario 1 (Mix Rebalancing: +$93.5k GP) and Scenario 2 (Targeted Price Realization: +$203.99k GP), Scenario 3 (Discount Reduction: +$3.29k GP) demonstrates that discount tightening in non-bike categories provides modest financial upside because these categories were not heavily discounted in CY2012.
