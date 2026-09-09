-- ============================================================================
-- STEP 14B — SCENARIO 3: TARGETED DISCOUNT REDUCTION
-- SQL Script: sql/07_what_if_discount_scenario.sql
--
-- Objective:
-- Calculate mechanical Gross Profit impact of reducing remaining line-item discounts
-- by 50% on selected high-discount subcategories (Accessories, Clothing).
-- Scope: CurrencyKey = 100 (USD), Calendar Year 2012.
-- ============================================================================

DROP VIEW IF EXISTS v_what_if_discount_scenario_summary CASCADE;
DROP VIEW IF EXISTS v_what_if_discount_scenario_subcategories CASCADE;
DROP VIEW IF EXISTS v_what_if_discount_subcategory_economics CASCADE;
DROP VIEW IF EXISTS v_what_if_discount_portfolio_baseline CASCADE;

-- 1. Baseline Portfolio View (CY2012 USD)
CREATE VIEW v_what_if_discount_portfolio_baseline AS
SELECT
    SUM("OrderQuantity") AS baseline_units,
    SUM("UnitPrice" * "OrderQuantity") AS baseline_gross_revenue,
    SUM("DiscountAmount") AS baseline_discount_amount,
    SUM("SalesAmount") AS baseline_net_revenue,
    SUM("TotalProductCost") AS baseline_total_cost,
    SUM("GrossProfit") AS baseline_gross_profit,
    (SUM("GrossProfit") / SUM("SalesAmount")) * 100.0 AS baseline_gross_margin_pct
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012;

-- 2. Subcategory Economics View (CY2012 USD)
CREATE VIEW v_what_if_discount_subcategory_economics AS
SELECT
    "Category" AS target_subcategory,
    SUM("OrderQuantity") AS cy2012_units,
    SUM("UnitPrice" * "OrderQuantity") AS gross_revenue,
    SUM("DiscountAmount") AS baseline_discount_amount,
    (SUM("DiscountAmount") / SUM("UnitPrice" * "OrderQuantity")) * 100.0 AS baseline_discount_rate_pct,
    SUM("SalesAmount") AS baseline_net_revenue,
    SUM("TotalProductCost") AS baseline_total_cost,
    SUM("GrossProfit") AS baseline_gross_profit,
    (SUM("GrossProfit") / SUM("SalesAmount")) * 100.0 AS baseline_gross_margin_pct
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 
  AND "CalendarYear" = 2012
  AND "Category" IN ('Accessories', 'Clothing')
GROUP BY "Category";

-- 3. Target Subcategories Breakdown View
CREATE VIEW v_what_if_discount_scenario_subcategories AS
SELECT
    target_subcategory,
    cy2012_units,
    gross_revenue,
    baseline_discount_rate_pct,
    baseline_discount_amount,
    baseline_discount_rate_pct * 0.50 AS scenario_discount_rate_pct,
    baseline_discount_amount * 0.50 AS scenario_discount_amount,
    baseline_discount_amount * 0.50 AS discount_savings,
    baseline_net_revenue,
    gross_revenue - (baseline_discount_amount * 0.50) AS scenario_net_revenue,
    baseline_discount_amount * 0.50 AS incremental_net_revenue,
    baseline_gross_profit,
    (gross_revenue - (baseline_discount_amount * 0.50)) - baseline_total_cost AS scenario_gross_profit,
    baseline_discount_amount * 0.50 AS incremental_gross_profit,
    baseline_gross_margin_pct,
    ((gross_revenue - (baseline_discount_amount * 0.50)) - baseline_total_cost) / (gross_revenue - (baseline_discount_amount * 0.50)) * 100.0 AS scenario_gross_margin_pct
FROM v_what_if_discount_subcategory_economics
ORDER BY target_subcategory;

-- 4. Overall Portfolio Scenario Summary View
CREATE VIEW v_what_if_discount_scenario_summary AS
WITH totals AS (
    SELECT
        SUM(baseline_discount_amount) AS baseline_target_discount_amount,
        SUM(scenario_discount_amount) AS scenario_target_discount_amount,
        SUM(discount_savings) AS total_discount_savings,
        SUM(incremental_net_revenue) AS total_incremental_net_revenue,
        SUM(incremental_gross_profit) AS total_incremental_gross_profit
    FROM v_what_if_discount_scenario_subcategories
)
SELECT
    b.baseline_net_revenue,
    b.baseline_gross_profit,
    b.baseline_gross_margin_pct,
    t.baseline_target_discount_amount,
    t.scenario_target_discount_amount,
    t.total_discount_savings AS discount_savings,
    t.total_incremental_net_revenue AS incremental_net_revenue,
    (b.baseline_net_revenue + t.total_discount_savings) AS scenario_net_revenue,
    t.total_incremental_gross_profit AS incremental_gross_profit,
    (b.baseline_gross_profit + t.total_discount_savings) AS scenario_gross_profit,
    ((b.baseline_gross_profit + t.total_discount_savings) / (b.baseline_net_revenue + t.total_discount_savings)) * 100.0 AS scenario_gross_margin_pct,
    (t.total_discount_savings / b.baseline_gross_profit) * 100.0 AS gross_profit_improvement_pct
FROM v_what_if_discount_portfolio_baseline b
CROSS JOIN totals t;
