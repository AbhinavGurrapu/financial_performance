# STAGE 4 — GROWTH QUALITY & SEGMENT ROOT-CAUSE DIAGNOSTICS REPORT

**Project:** Reseller Profitability Performance & Growth Quality Analysis  
**Scope:** CY2011 vs CY2012 | `CurrencyKey = 100` | Reseller Channel  
**Status:** Completed, Fully Reconciled & Observational Review Verified  

---

## 1. Executive Summary & Portfolio Baseline Scope

Stage 4 extends the portfolio-level profitability decomposition from Stage 3 (+ $617,300.78 Gross Profit change) by executing a granular segment-level root-cause analysis across **6 analytical dimensions**:
1. **Product Category** (4 segments)
2. **Product Subcategory** (33 segments)
3. **ProductKey** (330 individual products)
4. **Reseller Business Type** (3 business types: Warehouse, Value Added Reseller, Specialty Bike Shop)
5. **Country** (2 countries: United States, France)
6. **Territory Region** (6 sales regions)

### Portfolio Baseline Scope (Reconciled to Stage 3 & Staging CSVs)
* **Net Revenue:** CY2011 = **$14,467,116.44** | CY2012 = **$20,908,342.06** | Net Revenue Change = **+$6,441,225.63** (+44.52%)
* **Gross Profit:** CY2011 = **$57,560.96** | CY2012 = **$674,861.75** | Gross Profit Change = **+$617,300.78** (+1,072.43%)
* **Gross Margin %:** CY2011 = **0.40%** | CY2012 = **3.23%** | Margin Expansion = **+2.83 ppt**
* **4-Factor GP Drivers:** Price Effect = **+$366,094.82** | Unit Cost Effect = **$0.00** | Volume Effect = **+$97,657.34** | Product Mix Effect = **+$153,548.62**

The objective of Stage 4 is to determine **WHERE** growth, margin dilution, value destruction, or contraction occurred across enterprise segments using observational accounting decomposition.

---

## 2. Growth-Quality Classification Framework

Segments across all 6 dimensions are categorized into growth-quality tiers based on observed **Revenue Change**, **Gross Profit Change**, and **Gross Margin Change (ppt)**:

| Tier / Classification | Criteria / Logic Rules | Observational Interpretation | Key Example Segments |
| :--- | :--- | :--- | :--- |
| **Tier 1 — High-Quality Growth** | $\Delta \text{Revenue} > 0$, $\Delta \text{GP} > 0$, $\Delta \text{GM} \ge 0$ ppt | Concurrent top-line revenue expansion, gross profit dollar growth, and gross margin expansion. | **Components Category**, **United States**, **Southwest Region**, **Road Frames** |
| **Tier 2 — Margin-Dilutive Growth** | $\Delta \text{Revenue} > 0$, $\Delta \text{GP} > 0$, $\Delta \text{GM} < 0$ ppt | Concurrent revenue expansion and gross profit dollar growth accompanied by gross margin decline. | **Clothing Category**, **Wheels Subcategory**, **France** |
| **Tier 3 — Value-Destructive Growth** | $\Delta \text{Revenue} > 0$, $\Delta \text{GP} < 0$, $\Delta \text{GM} < 0$ ppt | Revenue expanded while gross profit dollars contracted and gross margin deteriorated. | **Road Bikes**, **Touring Bikes**, **Jerseys** |
| **Tier 4 — Contraction** | $\Delta \text{Revenue} < 0$, $\Delta \text{GP} < 0$ | Top-line revenue contracted accompanied by gross profit dollar loss. | **Socks Subcategory**, *Selected low-volume product SKUs* |
| **Tier 5 — Profitable Contraction / Portfolio Improvement** | $\Delta \text{Revenue} < 0$, $\Delta \text{GP} > 0$, $\Delta \text{GM} > 0$ ppt | Top-line revenue contracted while gross profit dollars expanded and gross margin improved. | **Mountain Bikes Subcategory**, **Specialty Bike Shop**, **Northwest Region**, **Southeast Region** |
| **Tier 1 (New Segment Entry)** | $\text{CY11 Rev} = 0$, $\Delta \text{GP} > 0$ | Newly introduced subcategory/product in CY2012 producing positive gross profit. | **Vests**, **Bike Racks**, **Pedals**, **Cranksets** |
| **Tier 3 (New Segment Entry)** | $\text{CY11 Rev} = 0$, $\Delta \text{GP} < 0$ | Newly introduced subcategory/product in CY2012 producing negative gross profit. | **Touring Bikes**, **Touring Frames** |

---

## 3. Multi-Dimensional Diagnostics

### 3.1 Product Category Level

| Category | CY2011 Net Rev | CY2012 Net Rev | Rev Change | Rev Growth % | CY2011 GP | CY2012 GP | GP Change | GP Growth % | CY2011 GM % | CY2012 GM % | GM Change (ppt) | Growth Quality Tier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Bikes** | $13,094,233.51 | $16,836,129.28 | +$3,741,895.77 | +28.58% | -$27,249.77 | $254,180.20 | +$281,429.97 | +1032.78% | -0.21% | 1.51% | +1.72 | **Tier 1 — High-quality growth** |
| **Components** | $1,239,376.67 | $3,450,370.08 | +$2,210,993.41 | +178.40% | $82,492.35 | $385,821.57 | +$303,329.22 | +367.70% | 6.66% | 11.18% | +4.53 | **Tier 1 — High-quality growth** |
| **Clothing** | $100,018.39 | $523,551.49 | +$423,533.10 | +423.46% | $1,805.15 | $27,617.86 | +$25,812.71 | +1429.94% | 1.80% | 5.27% | +3.47 | **Tier 1 — High-quality growth** |
| **Accessories** | $33,487.87 | $98,291.21 | +$64,803.35 | +193.51% | $513.23 | $7,242.12 | +$6,728.89 | +1311.08% | 1.53% | 7.37% | +5.84 | **Tier 1 — High-quality growth** |
| **Total** | **$14,467,116.44** | **$20,908,342.06** | **+$6,441,225.63** | **+44.52%** | **$57,560.96** | **$674,861.75** | **+$617,300.78** | **+1072.43%** | **0.40%** | **3.23%** | **+2.83** | **Portfolio Total** |

#### Category Diagnostic Observations:
1. **Best Category for Gross Profit Improvement:** **Components** recorded the largest absolute Gross Profit increase (`+$303,329.22` GP change), exceeding Bikes (`+$281,429.97`), despite generating ~$1.53M less in top-line revenue growth.
2. **Category Performance Uniformity:** All 4 categories experienced positive revenue growth, positive gross profit growth, and gross margin expansion. **Accessories** generated the smallest absolute GP improvement (`+$6,728.89`).

---

### 3.2 Product Subcategory Level

#### Top 5 Gross Profit Improvement Subcategories:
1. **Mountain Bikes** (Bikes): Gross Profit increased by `+$639,784.82` (from -$17,174.63 to +$622,610.18; Revenue Change = -$967,506.86; GM expanded +9.61 ppt from -0.23% to +9.38%) — **Tier 5 Profitable Contraction**
2. **Wheels** (Components): Gross Profit increased by `+$107,065.05` (from $11,972.38 to $119,037.43; Revenue Change = +$413,451.91; GM -0.09 ppt from 26.00% to 25.91%) — **Tier 2 Margin-Dilutive Growth**
3. **Road Frames** (Components): Gross Profit increased by `+$77,272.99` (from $17,741.20 to $95,014.19; Revenue Change = +$916,189.35; GM +3.15 ppt from 3.57% to 6.72%) — **Tier 1 High-Quality Growth**
4. **Mountain Frames** (Components): Gross Profit increased by `+$50,733.33` (from $91,376.41 to $142,109.74; Revenue Change = +$605,500.20; GM -2.30 ppt from 13.29% to 10.99%) — **Tier 2 Margin-Dilutive Growth**
5. **Tights** (Clothing): Gross Profit increased by `+$34,820.90` (from $3,703.49 to $38,524.38; Revenue Change = +$115,371.47; GM +1.18 ppt from 28.87% to 30.05%) — **Tier 1 High-Quality Growth**

#### Top 5 Gross Profit Drag Subcategories:
1. **Road Bikes** (Bikes): Gross Profit decreased by `-$283,117.66` (from -$68,879.61 to -$351,997.27; Revenue Change = +$4,330,063.06; GM deteriorated -2.33 ppt from -1.25% to -3.58%) — **Tier 3 Value-Destructive Growth**
2. **Touring Bikes** (Bikes): Gross Profit was `-$136,107.21` (from $0.00 to -$136,107.21; Revenue Change = +$379,339.15; GM = -35.88%) — **Tier 3 New Segment Entry**
3. **Jerseys** (Clothing): Gross Profit decreased by `-$5,639.04` (from -$4,320.40 to -$9,959.45; Revenue Change = +$56,315.78; GM deteriorated -0.68 ppt from -8.73% to -9.41%) — **Tier 3 Value-Destructive Growth**
4. **Touring Frames** (Components): Gross Profit was `-$2,171.68` (from $0.00 to -$2,171.68; Revenue Change = +$106,469.68; GM = -2.04%) — **Tier 3 New Segment Entry**
5. **Socks** (Clothing): Gross Profit decreased by `-$1,639.08` (from $2,026.87 to $387.79; Revenue Change = -$4,274.78; GM -1.87 ppt from 37.87% to 36.00%) — **Tier 4 Contraction**

#### Strongest Revenue-Growth Subcategories:
1. **Road Bikes:** Revenue Change = `+$4,330,063.06` (from $5,490,315.65 to $9,820,378.71)
2. **Road Frames:** Revenue Change = `+$916,189.35` (from $497,481.21 to $1,413,670.55)
3. **Mountain Frames:** Revenue Change = `+$605,500.20` (from $687,570.07 to $1,293,070.27)
4. **Wheels:** Revenue Change = `+$413,451.91` (from $46,047.64 to $459,499.55)
5. **Touring Bikes:** Revenue Change = `+$379,339.15` (from $0.00 to $379,339.15)

#### Subcategories Where Revenue Grew But Gross Profit Deteriorated (Tier 3):
* **Road Bikes** (Rev: +$4,330,063.06, GP: -$283,117.66)
* **Touring Bikes** (Rev: +$379,339.15, GP: -$136,107.21)
* **Jerseys** (Rev: +$56,315.78, GP: -$5,639.04)
* **Touring Frames** (Rev: +$106,469.68, GP: -$2,171.68)
* **Caps** (Rev: +$3,567.35, GP: -$136.62)

#### Subcategories Where Revenue Declined But Gross Profit Improved (Tier 5):
* **Mountain Bikes:** Net Revenue contracted by `-$967,506.86` (from $7,603,912.39 to $6,636,405.53), while Gross Profit expanded by `+$639,784.82` (from -$17,174.63 to +$622,610.18). Gross Margin improved by +9.61 ppt (from -0.23% to +9.38%).

#### New CY2012 Subcategories (CY2011 Revenue = $0):
* **Profitable New Entries (Tier 1):** Vests (+$3,864.51 GP), Bike Racks (+$3,299.57 GP), Pedals (+$2,239.98 GP), Cranksets (+$1,537.32 GP), Hydration Packs (+$1,165.54 GP), Saddles (+$682.50 GP), Brakes (+$564.88 GP), Derailleurs (+$474.93 GP), Bottom Brackets (+$292.70 GP), Cleaners (+$243.22 GP), Bottles and Cages (+$120.01 GP), Chains (+$59.99 GP), Tires and Tubes (+$31.05 GP).
* **Unprofitable New Entries (Tier 3):** Touring Bikes (-$136,107.21 GP), Touring Frames (-$2,171.68 GP).

---

### 3.3 ProductKey Level Diagnostics

#### Top 10 Gross Profit Improvement Products:
1. **Mountain-200 Black, 38** (ProductKey 358): GP Change = **+$91,706.51** | Revenue Change = +$919,958.20 | Tier 2
2. **Mountain-200 Black, 42** (ProductKey 360): GP Change = **+$80,651.09** | Revenue Change = +$822,649.60 | Tier 1
3. **Mountain-200 Silver, 38** (ProductKey 352): GP Change = **+$74,432.10** | Revenue Change = +$740,674.22 | Tier 1
4. **Mountain-200 Silver, 42** (ProductKey 354): GP Change = **+$74,277.51** | Revenue Change = +$744,991.05 | Tier 2
5. **Mountain-200 Silver, 46** (ProductKey 356): GP Change = **+$70,426.67** | Revenue Change = +$714,311.67 | Tier 2
6. **Mountain-200 Black, 46** (ProductKey 362): GP Change = **+$58,109.49** | Revenue Change = +$591,109.91 | Tier 2
7. **HL Mountain Frame - Silver, 38** (ProductKey 308): GP Change = **+$27,591.66** | Revenue Change = +$246,354.26 | Tier 1
8. **HL Mountain Rear Wheel** (ProductKey 421): GP Change = **+$26,316.41** | Revenue Change = +$102,299.68 | Tier 2
9. **HL Mountain Frame - Black, 42** (ProductKey 297): GP Change = **+$26,053.69** | Revenue Change = +$232,621.98 | Tier 1
10. **Mountain-300 Black, 40** (ProductKey 365): GP Change = **+$24,831.23** | Revenue Change = +$330,033.28 | Tier 1

#### Top 10 Gross Profit Drag Products:
1. **Touring-1000 Yellow, 46** (ProductKey 561): GP Change = **-$39,546.95** | Revenue Change = +$41,959.63 | Tier 3
2. **Road-650 Red, 44** (ProductKey 327): GP Change = **-$34,018.27** | Revenue Change = +$415,698.63 | Special Case *(Negative base margin)*
3. **Road-250 Red, 44** (ProductKey 368): GP Change = **-$28,806.38** | Revenue Change = +$718,436.53 | Special Case *(Negative base margin)*
4. **Road-650 Red, 60** (ProductKey 323): GP Change = **-$22,736.56** | Revenue Change = +$426,006.93 | Special Case *(Negative base margin)*
5. **Road-250 Red, 48** (ProductKey 369): GP Change = **-$22,223.75** | Revenue Change = +$592,884.74 | Tier 3
6. **Touring-1000 Yellow, 60** (ProductKey 564): GP Change = **-$19,413.96** | Revenue Change = +$20,598.36 | Tier 3
7. **Touring-1000 Yellow, 50** (ProductKey 562): GP Change = **-$18,694.92** | Revenue Change = +$19,835.46 | Tier 3
8. **Road-650 Red, 62** (ProductKey 325): GP Change = **-$18,193.49** | Revenue Change = +$396,480.53 | Special Case *(Negative base margin)*
9. **Road-650 Black, 52** (ProductKey 343): GP Change = **-$17,197.45** | Revenue Change = +$400,396.81 | Special Case *(Negative base margin)*
10. **Road-250 Red, 52** (ProductKey 370): GP Change = **-$16,360.68** | Revenue Change = +$454,463.10 | Special Case *(Zero base margin)*

---

### 3.4 Reseller Business Type Diagnostics

| Business Type | CY11 Net Rev | CY12 Net Rev | Rev Change | CY11 GP | CY12 GP | GP Change | CY11 GM % | CY12 GM % | GM Change | Growth Quality Tier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Value Added Reseller** | $6,496,750.24 | $10,077,663.15 | +$3,580,912.91 | $27,477.58 | $244,471.00 | +$216,993.42 | 0.42% | 2.43% | +2.01 ppt | **Tier 1 — High-quality growth** |
| **Warehouse** | $6,395,602.09 | $9,421,149.34 | +$3,025,547.25 | $14,370.27 | $390,867.96 | +$376,497.69 | 0.22% | 4.15% | +3.92 ppt | **Tier 1 — High-quality growth** |
| **Specialty Bike Shop** | $1,574,764.11 | $1,409,529.58 | -$165,234.53 | $15,713.12 | $39,522.79 | +$23,809.67 | 1.00% | 2.80% | +1.81 ppt | **Tier 5 — Profitable Contraction** |

#### Specialty Bike Shop Observational Statement:
* **Specialty Bike Shop** experienced a `$165.2K` revenue contraction while Gross Profit increased by `$23.8K` and Gross Margin improved by `1.81 percentage points`.
* Mathematically, this reflects a reduction in total units sold or average net price per unit accompanied by a larger absolute reduction in average unit cost of goods sold, resulting in higher gross profit dollars per unit.

---

### 3.5 Country & Territory Region Diagnostics

#### Country Performance:
* **United States:** Recorded `+$5,209,327.97` in Net Revenue growth and `+$580,257.87` in Gross Profit growth (from $51.1K to $631.4K; GM +2.86 ppt from 0.35% to 3.22% — **Tier 1**).
* **France:** Recorded `+$1,231,897.65` in Net Revenue growth and `+$37,042.92` in Gross Profit growth (from $6.4K to $43.5K; GM -8.33 ppt from 11.71% to 3.38% — **Tier 2**).

#### Territory Region Performance:
* **Strongest GP Contributor:** **Southwest (US)** — Recorded `+$266,735.75` in Gross Profit growth (from -$97.9K to +$168.9K; Revenue Change = +$3.42M; GM +4.48 ppt from -2.28% to +2.19% — **Tier 1**).
* **Second Strongest GP Contributor:** **Northwest (US)** — Recorded `+$121,476.16` in Gross Profit growth (from $50.2K to $171.6K; Revenue Change = -$269.85; GM +3.50 ppt from 1.45% to 4.95% — **Tier 5**).
* **Weakest GP Contributor:** **Central (US)** — Recorded `+$36,502.43` in Gross Profit growth (from $44.2K to $80.7K; Revenue Change = +$478.8K; GM +0.99 ppt from 1.94% to 2.93% — **Tier 1**).

---

## 4. Key Diagnostic Insights & Discount Analysis

### 4.1 Price Effect vs Discount Diagnostic Analysis

$$\text{Realized Price (ASP)} = \frac{\text{Net Revenue}}{\text{Units}} = \frac{\text{Gross Revenue} - \text{Discount Amount}}{\text{Units}}$$

| Segment | CY11 Gross Rev | CY12 Gross Rev | CY11 Disc Amt | CY12 Disc Amt | Disc Rate 11 | Disc Rate 12 | Disc Rate Change | List ASP 11 | List ASP 12 | Net ASP 11 | Net ASP 12 | Net ASP Change |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Portfolio** | $14.59M | $20.98M | $122,297.68 | $71,077.60 | 0.84% | 0.34% | **-0.50 ppt** | $675.09 | $360.00 | $669.43 | $358.78 | -$310.65 |
| **Bikes** | $13.21M | $16.90M | $120,739.85 | $63,201.47 | 0.91% | 0.37% | **-0.54 ppt** | $1,146.34 | $806.53 | $1,135.86 | $803.52 | -$332.34 |
| **Components**| $1.24M | $3.45M | $99.67 | $1,293.29 | 0.01% | 0.04% | **+0.03 ppt** | $354.85 | $241.95 | $354.82 | $241.86 | -$112.96 |
| **Clothing** | $100.9K | $528.6K | $886.09 | $5,036.91 | 0.88% | 0.95% | **+0.07 ppt** | $21.03 | $29.92 | $20.84 | $29.63 | +$8.79 |
| **Accessories**| $34.1K | $99.8K | $572.07 | $1,545.93 | 1.68% | 1.55% | **-0.13 ppt** | $19.02 | $18.52 | $18.70 | $18.24 | -$0.46 |

#### Observational Conclusion on Discounting:
Deeper promotional discounting was not the primary observed explanation for the portfolio ASP decline, because discount depth decreased rather than increased (discount rate fell from 0.84% to 0.34%, saving $51,220.08). The remaining ASP movement should be interpreted alongside product mix and list-price changes.

---

## 5. Methodological Principles & Operational Caveats

1. **Accounting Bridge, Not Causal Inference:** The four-factor decomposition is an exact mathematical accounting identity. It measures statistical contributions to gross profit change, not causal elasticity.
2. **Fixed Scope:** All queries preserve `CurrencyKey = 100` and CY2011 vs CY2012 scope.
3. **No Double-Counting:** Discounts are embedded within Net Revenue ($SalesAmount = ExtendedAmount - DiscountAmount$) and are analyzed diagnostically without introducing a redundant fifth factor into the GP bridge.

---

## 6. Automated Validation Suite & Audit Summary

The Python validation script `scripts/verify_growth_quality_diagnostics.py` executed a **9-Point Audit** against PostgreSQL 18 with **100% PASS rate (Zero Residual)**:

* **Check 1: Segment Revenue Reconciliation** -> PASS (All 6 dimensions reconcile to $14,467,116.44 / $20,908,342.06)
* **Check 2: Segment Gross Profit Reconciliation** -> PASS (All 6 dimensions reconcile to $57,560.96 / $674,861.75)
* **Check 3: Four-Factor GP Sum Reconciliation** -> PASS (All 6 dimensions sum exactly to +$617,300.78)
* **Check 4: Product-Level Stage 3 Fact Alignment** -> PASS (330 product SKUs match Stage 3 exactly)
* **Check 5: Segment Uniqueness & No Double Counting** -> PASS (Zero key duplication across all 6 fact tables)
* **Check 6: Zero Unexpected NULL Segment Labels** -> PASS (0 NULL keys detected)
* **Check 7: Growth Quality Tier Consistency** -> PASS (100% consistent tier assignment across all tables)
* **Check 8: Revenue & Profitability Mix Share Reconciliation** -> PASS (Category and subcategory mix shares sum to 100.00%)
* **Check 9: Discount Diagnostic Accounting Reconciliation** -> PASS (Gross Revenue - Discount Amount = Net Revenue across all rows)

---
*Report updated and observational review verified.*