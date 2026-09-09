-- ============================================================================
-- STEP 14B — SCENARIO 2: TARGETED PRICE REALIZATION
-- SQL Script: sql/06_what_if_price_scenario.sql
--
-- Objective:
-- Calculate mechanical Gross Profit impact of a 2% realized price increase on
-- value-destructive subcategories (Road Bikes, Touring Bikes).
-- Scope: CurrencyKey = 100 (USD), Calendar Year 2012.
-- ============================================================================

DROP VIEW IF EXISTS v_what_if_price_scenario_summary CASCADE;
DROP VIEW IF EXISTS v_what_if_price_scenario_subcategories CASCADE;
DROP VIEW IF EXISTS v_what_if_price_subcategory_economics CASCADE;
DROP VIEW IF EXISTS v_what_if_price_portfolio_baseline CASCADE;

-- 1. Baseline Portfolio View (CY2012 USD)
CREATE VIEW v_what_if_price_portfolio_baseline AS
SELECT
    SUM("OrderQuantity") AS baseline_units,
    SUM("SalesAmount") AS baseline_net_revenue,
    SUM("TotalProductCost") AS baseline_total_cost,
    SUM("GrossProfit") AS baseline_gross_profit,
    (SUM("GrossProfit") / SUM("SalesAmount")) * 100.0 AS baseline_gross_margin_pct
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012;

-- 2. Subcategory Economics View (CY2012 USD)
CREATE VIEW v_what_if_price_subcategory_economics AS
SELECT
    "Subcategory" AS target_subcategory,
    SUM("OrderQuantity") AS cy2012_units,
    SUM("SalesAmount") AS baseline_net_revenue,
    SUM("TotalProductCost") AS baseline_total_cost,
    SUM("GrossProfit") AS baseline_gross_profit,
    SUM("SalesAmount") / SUM("OrderQuantity") AS baseline_asp,
    SUM("TotalProductCost") / SUM("OrderQuantity") AS std_cost_per_unit,
    SUM("GrossProfit") / SUM("OrderQuantity") AS baseline_unit_gp,
    (SUM("GrossProfit") / SUM("SalesAmount")) * 100.0 AS baseline_gross_margin_pct
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 
  AND "CalendarYear" = 2012
  AND "Subcategory" IN ('Road Bikes', 'Touring Bikes')
GROUP BY "Subcategory";

-- 3. Target Subcategories Breakdown View
CREATE VIEW v_what_if_price_scenario_subcategories AS
SELECT
    target_subcategory,
    cy2012_units,
    0.02 AS price_increase_pct,
    baseline_asp,
    baseline_asp * 1.02 AS scenario_asp,
    baseline_unit_gp,
    (baseline_asp * 1.02) - std_cost_per_unit AS scenario_unit_gp,
    baseline_net_revenue,
    cy2012_units * (baseline_asp * 1.02) AS scenario_net_revenue,
    (cy2012_units * (baseline_asp * 1.02)) - baseline_net_revenue AS incremental_net_revenue,
    baseline_gross_profit,
    cy2012_units * ((baseline_asp * 1.02) - std_cost_per_unit) AS scenario_gross_profit,
    (cy2012_units * ((baseline_asp * 1.02) - std_cost_per_unit)) - baseline_gross_profit AS incremental_gross_profit,
    baseline_gross_margin_pct,
    (cy2012_units * ((baseline_asp * 1.02) - std_cost_per_unit)) / (cy2012_units * (baseline_asp * 1.02)) * 100.0 AS scenario_gross_margin_pct
FROM v_what_if_price_subcategory_economics
ORDER BY target_subcategory;

-- 4. Overall Portfolio Scenario Summary View
CREATE VIEW v_what_if_price_scenario_summary AS
WITH totals AS (
    SELECT
        SUM(incremental_net_revenue) AS total_incremental_net_revenue,
        SUM(incremental_gross_profit) AS total_incremental_gross_profit
    FROM v_what_if_price_scenario_subcategories
)
SELECT
    b.baseline_net_revenue,
    b.baseline_gross_profit,
    b.baseline_gross_margin_pct,
    t.total_incremental_net_revenue AS incremental_net_revenue,
    (b.baseline_net_revenue + t.total_incremental_net_revenue) AS scenario_net_revenue,
    t.total_incremental_gross_profit AS incremental_gross_profit,
    (b.baseline_gross_profit + t.total_incremental_gross_profit) AS scenario_gross_profit,
    ((b.baseline_gross_profit + t.total_incremental_gross_profit) / (b.baseline_net_revenue + t.total_incremental_net_revenue)) * 100.0 AS scenario_gross_margin_pct,
    (t.total_incremental_gross_profit / b.baseline_gross_profit) * 100.0 AS gross_profit_improvement_pct
FROM v_what_if_price_portfolio_baseline b
CROSS JOIN totals t;
