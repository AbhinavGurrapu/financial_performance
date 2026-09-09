-- ============================================================================
-- STEP 14B — SCENARIO 1: PRODUCT MIX REBALANCING
-- SQL Script: sql/05_what_if_mix_scenario.sql
--
-- Objective:
-- Calculate mechanical Gross Profit impact of shifting 5% of CY2012 unit volume
-- from value-destructive subcategories (Road Bikes, Touring Bikes) toward a
-- higher-profit target subcategory (Mountain Bikes).
-- Scope: CurrencyKey = 100 (USD), Calendar Year 2012.
-- ============================================================================

DROP VIEW IF EXISTS v_what_if_mix_scenario_summary CASCADE;
DROP VIEW IF EXISTS v_what_if_mix_scenario_subcategories CASCADE;
DROP VIEW IF EXISTS v_what_if_mix_subcategory_economics CASCADE;
DROP VIEW IF EXISTS v_what_if_mix_portfolio_baseline CASCADE;

-- 1. Baseline Portfolio View (CY2012 USD)
CREATE VIEW v_what_if_mix_portfolio_baseline AS
SELECT
    SUM("OrderQuantity") AS baseline_units,
    SUM("SalesAmount") AS baseline_net_revenue,
    SUM("TotalProductCost") AS baseline_total_cost,
    SUM("GrossProfit") AS baseline_gross_profit,
    (SUM("GrossProfit") / SUM("SalesAmount")) * 100.0 AS baseline_gross_margin_pct
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012;

-- 2. Subcategory Economics View (CY2012 USD)
CREATE VIEW v_what_if_mix_subcategory_economics AS
SELECT
    "Subcategory" AS subcategory,
    SUM("OrderQuantity") AS cy2012_units,
    SUM("SalesAmount") AS cy2012_net_revenue,
    SUM("TotalProductCost") AS cy2012_total_cost,
    SUM("GrossProfit") AS cy2012_gross_profit,
    SUM("SalesAmount") / SUM("OrderQuantity") AS realized_rev_per_unit,
    SUM("TotalProductCost") / SUM("OrderQuantity") AS std_cost_per_unit,
    SUM("GrossProfit") / SUM("OrderQuantity") AS unit_gross_profit
FROM abt_reseller_sales
WHERE "CurrencyKey" = 100 
  AND "CalendarYear" = 2012
  AND "Subcategory" IN ('Road Bikes', 'Touring Bikes', 'Mountain Bikes')
GROUP BY "Subcategory";

-- 3. Source & Target Breakdown View
CREATE VIEW v_what_if_mix_scenario_subcategories AS
WITH target_econ AS (
    SELECT 
        realized_rev_per_unit AS target_rev_per_unit,
        std_cost_per_unit AS target_cost_per_unit,
        unit_gross_profit AS target_unit_gp
    FROM v_what_if_mix_subcategory_economics
    WHERE subcategory = 'Mountain Bikes'
)
SELECT
    src.subcategory AS source_subcategory,
    src.cy2012_units,
    0.05 AS shift_pct,
    src.cy2012_units * 0.05 AS units_shifted,
    src.realized_rev_per_unit AS source_rev_per_unit,
    src.std_cost_per_unit AS source_cost_per_unit,
    src.unit_gross_profit AS source_unit_gp,
    tgt.target_rev_per_unit,
    tgt.target_cost_per_unit,
    tgt.target_unit_gp,
    (src.cy2012_units * 0.05) * src.realized_rev_per_unit AS revenue_lost,
    (src.cy2012_units * 0.05) * src.std_cost_per_unit AS cost_saved,
    (src.cy2012_units * 0.05) * src.unit_gross_profit AS gp_lost,
    (src.cy2012_units * 0.05) * tgt.target_rev_per_unit AS revenue_gained,
    (src.cy2012_units * 0.05) * tgt.target_cost_per_unit AS cost_added,
    (src.cy2012_units * 0.05) * tgt.target_unit_gp AS gp_gained,
    (src.cy2012_units * 0.05) * (tgt.target_unit_gp - src.unit_gross_profit) AS incremental_gp
FROM v_what_if_mix_subcategory_economics src
CROSS JOIN target_econ tgt
WHERE src.subcategory IN ('Road Bikes', 'Touring Bikes')
ORDER BY src.subcategory;

-- 4. Overall Scenario Summary View
CREATE VIEW v_what_if_mix_scenario_summary AS
WITH totals AS (
    SELECT
        SUM(units_shifted) AS total_units_shifted,
        SUM(revenue_lost) AS total_revenue_lost,
        SUM(cost_saved) AS total_cost_saved,
        SUM(gp_lost) AS total_gp_lost,
        SUM(revenue_gained) AS total_revenue_gained,
        SUM(cost_added) AS total_cost_added,
        SUM(gp_gained) AS total_gp_gained,
        SUM(incremental_gp) AS total_incremental_gp
    FROM v_what_if_mix_scenario_subcategories
)
SELECT
    b.baseline_net_revenue,
    b.baseline_gross_profit,
    b.baseline_gross_margin_pct,
    t.total_units_shifted,
    (t.total_revenue_gained - t.total_revenue_lost) AS net_revenue_impact,
    t.total_incremental_gp AS incremental_gross_profit,
    (b.baseline_gross_profit + t.total_incremental_gp) AS scenario_gross_profit,
    ((b.baseline_gross_profit + t.total_incremental_gp) / (b.baseline_net_revenue + (t.total_revenue_gained - t.total_revenue_lost))) * 100.0 AS scenario_gross_margin_pct,
    ((t.total_incremental_gp) / b.baseline_gross_profit) * 100.0 AS gross_profit_improvement_pct
FROM v_what_if_mix_portfolio_baseline b
CROSS JOIN totals t;
