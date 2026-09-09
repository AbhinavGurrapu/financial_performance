-- ============================================================================
-- AdventureWorks DW — Profitability Driver Decomposition Model
-- Model: 4-Factor Gross Profit Bridge (Price, Unit Cost, Volume, Product Mix)
-- Grain: ProductKey (330 Products across CY2011 and CY2012)
-- Analytical Scope: CurrencyKey = 100
-- ============================================================================

\set ON_ERROR_STOP on

DROP TABLE IF EXISTS "fact_profitability_decomposition_product" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_category" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_subcategory" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_business_type" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_country" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_territory_region" CASCADE;
DROP TABLE IF EXISTS "rollup_profitability_overall" CASCADE;

-- 1. Create Product-Level Profitability Decomposition Table
CREATE TABLE "fact_profitability_decomposition_product" AS
WITH portfolio_baseline AS (
    SELECT 
        SUM("SalesAmount" - "TotalProductCost") AS total_gp_11,
        SUM("OrderQuantity")                    AS total_units_11,
        (SUM("SalesAmount" - "TotalProductCost") / NULLIF(SUM("OrderQuantity"), 0)) AS baseline_avg_ugp
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2011
),
product_catalog AS (
    SELECT DISTINCT
        "ProductKey",
        "ProductName",
        "Subcategory",
        "Category"
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100
),
p_2011 AS (
    SELECT 
        "ProductKey",
        SUM("OrderQuantity")                    AS q11,
        SUM("SalesAmount")                       AS r11,
        SUM("TotalProductCost")                  AS c11_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2011
    GROUP BY "ProductKey"
),
p_2012 AS (
    SELECT 
        "ProductKey",
        SUM("OrderQuantity")                    AS q12,
        SUM("SalesAmount")                       AS r12,
        SUM("TotalProductCost")                  AS c12_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
    GROUP BY "ProductKey"
),
product_metrics AS (
    SELECT
        c."ProductKey",
        c."ProductName",
        c."Category",
        c."Subcategory",
        
        -- CY2011 Aggregates
        COALESCE(p11.q11, 0)                     AS q11,
        COALESCE(p11.r11, 0.0)                   AS r11,
        COALESCE(p11.c11_total, 0.0)             AS c11_total,
        (COALESCE(p11.r11, 0.0) - COALESCE(p11.c11_total, 0.0)) AS gp11,
        
        -- CY2012 Aggregates
        COALESCE(p12.q12, 0)                     AS q12,
        COALESCE(p12.r12, 0.0)                   AS r12,
        COALESCE(p12.c12_total, 0.0)             AS c12_total,
        (COALESCE(p12.r12, 0.0) - COALESCE(p12.c12_total, 0.0)) AS gp12,
        
        -- Unit Prices & Costs
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.r11 / p11.q11 ELSE 0.0 END AS p11,
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.c11_total / p11.q11 ELSE 0.0 END AS c11,
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN (p11.r11 - p11.c11_total) / p11.q11 ELSE 0.0 END AS ugp11,

        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.r12 / p12.q12 ELSE 0.0 END AS p12,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.c12_total / p12.q12 ELSE 0.0 END AS c12,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN (p12.r12 - p12.c12_total) / p12.q12 ELSE 0.0 END AS ugp12,

        -- Status
        CASE 
            WHEN COALESCE(p11.q11, 0) > 0 AND COALESCE(p12.q12, 0) > 0 THEN 'CONTINUING'
            WHEN COALESCE(p11.q11, 0) > 0 AND COALESCE(p12.q12, 0) = 0 THEN 'DISCONTINUED'
            WHEN COALESCE(p11.q11, 0) = 0 AND COALESCE(p12.q12, 0) > 0 THEN 'NEW'
        END AS product_status,

        b.baseline_avg_ugp
    FROM product_catalog c
    CROSS JOIN portfolio_baseline b
    LEFT JOIN p_2011 p11 ON c."ProductKey" = p11."ProductKey"
    LEFT JOIN p_2012 p12 ON c."ProductKey" = p12."ProductKey"
)
SELECT 
    m."ProductKey",
    m."ProductName",
    m."Category",
    m."Subcategory",
    m.product_status,
    m.q11,
    m.r11,
    m.c11_total,
    m.gp11,
    CASE WHEN m.r11 > 0 THEN m.gp11 / m.r11 ELSE 0.0 END AS gm11_pct,
    
    m.q12,
    m.r12,
    m.c12_total,
    m.gp12,
    CASE WHEN m.r12 > 0 THEN m.gp12 / m.r12 ELSE 0.0 END AS gm12_pct,
    
    (m.r12 - m.r11)                                     AS revenue_change,
    (m.gp12 - m.gp11)                                   AS gp_change,
    (CASE WHEN m.r12 > 0 THEN m.gp12 / m.r12 ELSE 0.0 END - CASE WHEN m.r11 > 0 THEN m.gp11 / m.r11 ELSE 0.0 END) AS gm_pct_change,

    m.p11,
    m.c11,
    m.ugp11,
    m.p12,
    m.c12,
    m.ugp12,
    m.baseline_avg_ugp,

    -- 1. PRICE EFFECT
    CASE 
        WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11)
        ELSE 0.0 
    END AS price_effect,

    -- 2. UNIT COST EFFECT
    CASE 
        WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12)
        ELSE 0.0 
    END AS unit_cost_effect,

    -- 3. VOLUME EFFECT
    (m.q12 - m.q11) * m.baseline_avg_ugp AS volume_effect,

    -- 4. PRODUCT MIX EFFECT
    CASE 
        WHEN m.product_status = 'NEW' THEN m.q12 * (m.ugp12 - m.baseline_avg_ugp)
        ELSE (m.q12 - m.q11) * (m.ugp11 - m.baseline_avg_ugp)
    END AS mix_effect,

    -- RECONCILIATION
    (
        CASE WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11) ELSE 0.0 END +
        CASE WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12) ELSE 0.0 END +
        ((m.q12 - m.q11) * m.baseline_avg_ugp) +
        CASE WHEN m.product_status = 'NEW' THEN m.q12 * (m.ugp12 - m.baseline_avg_ugp) ELSE (m.q12 - m.q11) * (m.ugp11 - m.baseline_avg_ugp) END
    ) AS reconciled_gp_change,

    (m.gp12 - m.gp11) - (
        CASE WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11) ELSE 0.0 END +
        CASE WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12) ELSE 0.0 END +
        ((m.q12 - m.q11) * m.baseline_avg_ugp) +
        CASE WHEN m.product_status = 'NEW' THEN m.q12 * (m.ugp12 - m.baseline_avg_ugp) ELSE (m.q12 - m.q11) * (m.ugp11 - m.baseline_avg_ugp) END
    ) AS residual
FROM product_metrics m;

ALTER TABLE "fact_profitability_decomposition_product"
ADD CONSTRAINT "PK_fact_profitability_decomposition_product" PRIMARY KEY ("ProductKey");


-- 2. Create Overall Summary Table
CREATE TABLE "rollup_profitability_overall" AS
SELECT 
    'Overall Portfolio'                                 AS segment_name,
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(reconciled_gp_change)                           AS reconciled_gp_change,
    SUM(residual)                                       AS residual
FROM "fact_profitability_decomposition_product";


-- 3. Create Product Category Rollup Table
CREATE TABLE "rollup_profitability_category" AS
SELECT 
    "Category",
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(reconciled_gp_change)                           AS reconciled_gp_change,
    SUM(residual)                                       AS residual
FROM "fact_profitability_decomposition_product"
GROUP BY "Category"
ORDER BY SUM(gp_change) DESC;


-- 4. Create Product Subcategory Rollup Table
CREATE TABLE "rollup_profitability_subcategory" AS
SELECT 
    "Category",
    "Subcategory",
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(reconciled_gp_change)                           AS reconciled_gp_change,
    SUM(residual)                                       AS residual
FROM "fact_profitability_decomposition_product"
GROUP BY "Category", "Subcategory"
ORDER BY SUM(gp_change) DESC;


-- 5. Create Reseller Business Type Rollup Table (Product-Segment Exact Decomposition)
CREATE TABLE "rollup_profitability_business_type" AS
WITH ps_catalog AS (
    SELECT DISTINCT "ProductKey", "BusinessType"
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100
),
ps_2011 AS (
    SELECT 
        "ProductKey",
        "BusinessType",
        SUM("OrderQuantity")                    AS q11,
        SUM("SalesAmount")                       AS r11,
        SUM("TotalProductCost")                  AS c11_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2011
    GROUP BY "ProductKey", "BusinessType"
),
ps_2012 AS (
    SELECT 
        "ProductKey",
        "BusinessType",
        SUM("OrderQuantity")                    AS q12,
        SUM("SalesAmount")                       AS r12,
        SUM("TotalProductCost")                  AS c12_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
    GROUP BY "ProductKey", "BusinessType"
),
ps_metrics AS (
    SELECT 
        c."ProductKey",
        c."BusinessType",
        COALESCE(p11.q11, 0)                     AS q11,
        COALESCE(p11.r11, 0.0)                   AS r11,
        COALESCE(p11.c11_total, 0.0)             AS c11_total,
        COALESCE(p12.q12, 0)                     AS q12,
        COALESCE(p12.r12, 0.0)                   AS r12,
        COALESCE(p12.c12_total, 0.0)             AS c12_total,
        
        glob.product_status,
        glob.p11                                 AS p11_glob,
        glob.c11                                 AS c11_glob,
        glob.ugp11                               AS ugp11_glob,
        glob.p12                                 AS p12_glob,
        glob.c12                                 AS c12_glob,
        glob.ugp12                               AS ugp12_glob,
        glob.baseline_avg_ugp,

        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.r11 / p11.q11 ELSE glob.p11 END AS p11,
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.c11_total / p11.q11 ELSE glob.c11 END AS c11,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.r12 / p12.q12 ELSE glob.p12 END AS p12,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.c12_total / p12.q12 ELSE glob.c12 END AS c12
    FROM ps_catalog c
    JOIN "fact_profitability_decomposition_product" glob ON c."ProductKey" = glob."ProductKey"
    LEFT JOIN ps_2011 p11 ON c."ProductKey" = p11."ProductKey" AND c."BusinessType" = p11."BusinessType"
    LEFT JOIN ps_2012 p12 ON c."ProductKey" = p12."ProductKey" AND c."BusinessType" = p12."BusinessType"
),
ps_effects AS (
    SELECT 
        m."BusinessType",
        m.q11,
        m.r11,
        (m.r11 - m.c11_total) AS gp11,
        m.q12,
        m.r12,
        (m.r12 - m.c12_total) AS gp12,
        (m.r12 - m.r11) AS revenue_change,
        ((m.r12 - m.c12_total) - (m.r11 - m.c11_total)) AS gp_change,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11)
            ELSE 0.0
        END AS price_effect,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12)
            ELSE 0.0
        END AS unit_cost_effect,

        (m.q12 - m.q11) * m.baseline_avg_ugp AS volume_effect,

        CASE 
            WHEN m.product_status = 'NEW' THEN m.q12 * ((m.p12 - m.c12) - m.baseline_avg_ugp)
            ELSE (m.q12 - m.q11) * ((m.p11 - m.c11) - m.baseline_avg_ugp)
        END AS mix_effect
    FROM ps_metrics m
)
SELECT 
    "BusinessType",
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(price_effect + unit_cost_effect + volume_effect + mix_effect) AS reconciled_gp_change,
    SUM(gp_change - (price_effect + unit_cost_effect + volume_effect + mix_effect)) AS residual
FROM ps_effects
GROUP BY "BusinessType"
ORDER BY SUM(gp_change) DESC;


-- 6. Create Country Rollup Table (Product-Segment Exact Decomposition)
CREATE TABLE "rollup_profitability_country" AS
WITH ps_catalog AS (
    SELECT DISTINCT "ProductKey", "SalesTerritoryCountry" AS "Country"
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100
),
ps_2011 AS (
    SELECT 
        "ProductKey",
        "SalesTerritoryCountry"                 AS "Country",
        SUM("OrderQuantity")                    AS q11,
        SUM("SalesAmount")                       AS r11,
        SUM("TotalProductCost")                  AS c11_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2011
    GROUP BY "ProductKey", "SalesTerritoryCountry"
),
ps_2012 AS (
    SELECT 
        "ProductKey",
        "SalesTerritoryCountry"                 AS "Country",
        SUM("OrderQuantity")                    AS q12,
        SUM("SalesAmount")                       AS r12,
        SUM("TotalProductCost")                  AS c12_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
    GROUP BY "ProductKey", "SalesTerritoryCountry"
),
ps_metrics AS (
    SELECT 
        c."ProductKey",
        c."Country",
        COALESCE(p11.q11, 0)                     AS q11,
        COALESCE(p11.r11, 0.0)                   AS r11,
        COALESCE(p11.c11_total, 0.0)             AS c11_total,
        COALESCE(p12.q12, 0)                     AS q12,
        COALESCE(p12.r12, 0.0)                   AS r12,
        COALESCE(p12.c12_total, 0.0)             AS c12_total,
        
        glob.product_status,
        glob.p11                                 AS p11_glob,
        glob.c11                                 AS c11_glob,
        glob.p12                                 AS p12_glob,
        glob.c12                                 AS c12_glob,
        glob.baseline_avg_ugp,

        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.r11 / p11.q11 ELSE glob.p11 END AS p11,
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.c11_total / p11.q11 ELSE glob.c11 END AS c11,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.r12 / p12.q12 ELSE glob.p12 END AS p12,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.c12_total / p12.q12 ELSE glob.c12 END AS c12
    FROM ps_catalog c
    JOIN "fact_profitability_decomposition_product" glob ON c."ProductKey" = glob."ProductKey"
    LEFT JOIN ps_2011 p11 ON c."ProductKey" = p11."ProductKey" AND c."Country" = p11."Country"
    LEFT JOIN ps_2012 p12 ON c."ProductKey" = p12."ProductKey" AND c."Country" = p12."Country"
),
ps_effects AS (
    SELECT 
        m."Country",
        m.q11,
        m.r11,
        (m.r11 - m.c11_total) AS gp11,
        m.q12,
        m.r12,
        (m.r12 - m.c12_total) AS gp12,
        (m.r12 - m.r11) AS revenue_change,
        ((m.r12 - m.c12_total) - (m.r11 - m.c11_total)) AS gp_change,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11)
            ELSE 0.0
        END AS price_effect,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12)
            ELSE 0.0
        END AS unit_cost_effect,

        (m.q12 - m.q11) * m.baseline_avg_ugp AS volume_effect,

        CASE 
            WHEN m.product_status = 'NEW' THEN m.q12 * ((m.p12 - m.c12) - m.baseline_avg_ugp)
            ELSE (m.q12 - m.q11) * ((m.p11 - m.c11) - m.baseline_avg_ugp)
        END AS mix_effect
    FROM ps_metrics m
)
SELECT 
    "Country",
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(price_effect + unit_cost_effect + volume_effect + mix_effect) AS reconciled_gp_change,
    SUM(gp_change - (price_effect + unit_cost_effect + volume_effect + mix_effect)) AS residual
FROM ps_effects
GROUP BY "Country"
ORDER BY SUM(gp_change) DESC;


-- 7. Create Territory Region Rollup Table (Product-Segment Exact Decomposition)
CREATE TABLE "rollup_profitability_territory_region" AS
WITH ps_catalog AS (
    SELECT DISTINCT "ProductKey", "SalesTerritoryCountry" AS "Country", "SalesTerritoryRegion" AS "TerritoryRegion"
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100
),
ps_2011 AS (
    SELECT 
        "ProductKey",
        "SalesTerritoryCountry"                 AS "Country",
        "SalesTerritoryRegion"                  AS "TerritoryRegion",
        SUM("OrderQuantity")                    AS q11,
        SUM("SalesAmount")                       AS r11,
        SUM("TotalProductCost")                  AS c11_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2011
    GROUP BY "ProductKey", "SalesTerritoryCountry", "SalesTerritoryRegion"
),
ps_2012 AS (
    SELECT 
        "ProductKey",
        "SalesTerritoryCountry"                 AS "Country",
        "SalesTerritoryRegion"                  AS "TerritoryRegion",
        SUM("OrderQuantity")                    AS q12,
        SUM("SalesAmount")                       AS r12,
        SUM("TotalProductCost")                  AS c12_total
    FROM "abt_reseller_sales"
    WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
    GROUP BY "ProductKey", "SalesTerritoryCountry", "SalesTerritoryRegion"
),
ps_metrics AS (
    SELECT 
        c."ProductKey",
        c."Country",
        c."TerritoryRegion",
        COALESCE(p11.q11, 0)                     AS q11,
        COALESCE(p11.r11, 0.0)                   AS r11,
        COALESCE(p11.c11_total, 0.0)             AS c11_total,
        COALESCE(p12.q12, 0)                     AS q12,
        COALESCE(p12.r12, 0.0)                   AS r12,
        COALESCE(p12.c12_total, 0.0)             AS c12_total,
        
        glob.product_status,
        glob.p11                                 AS p11_glob,
        glob.c11                                 AS c11_glob,
        glob.p12                                 AS p12_glob,
        glob.c12                                 AS c12_glob,
        glob.baseline_avg_ugp,

        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.r11 / p11.q11 ELSE glob.p11 END AS p11,
        CASE WHEN COALESCE(p11.q11, 0) > 0 THEN p11.c11_total / p11.q11 ELSE glob.c11 END AS c11,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.r12 / p12.q12 ELSE glob.p12 END AS p12,
        CASE WHEN COALESCE(p12.q12, 0) > 0 THEN p12.c12_total / p12.q12 ELSE glob.c12 END AS c12
    FROM ps_catalog c
    JOIN "fact_profitability_decomposition_product" glob ON c."ProductKey" = glob."ProductKey"
    LEFT JOIN ps_2011 p11 ON c."ProductKey" = p11."ProductKey" AND c."Country" = p11."Country" AND c."TerritoryRegion" = p11."TerritoryRegion"
    LEFT JOIN ps_2012 p12 ON c."ProductKey" = p12."ProductKey" AND c."Country" = p12."Country" AND c."TerritoryRegion" = p12."TerritoryRegion"
),
ps_effects AS (
    SELECT 
        m."Country",
        m."TerritoryRegion",
        m.q11,
        m.r11,
        (m.r11 - m.c11_total) AS gp11,
        m.q12,
        m.r12,
        (m.r12 - m.c12_total) AS gp12,
        (m.r12 - m.r11) AS revenue_change,
        ((m.r12 - m.c12_total) - (m.r11 - m.c11_total)) AS gp_change,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.p12 - m.p11)
            ELSE 0.0
        END AS price_effect,

        CASE 
            WHEN m.product_status = 'CONTINUING' THEN m.q12 * (m.c11 - m.c12)
            ELSE 0.0
        END AS unit_cost_effect,

        (m.q12 - m.q11) * m.baseline_avg_ugp AS volume_effect,

        CASE 
            WHEN m.product_status = 'NEW' THEN m.q12 * ((m.p12 - m.c12) - m.baseline_avg_ugp)
            ELSE (m.q12 - m.q11) * ((m.p11 - m.c11) - m.baseline_avg_ugp)
        END AS mix_effect
    FROM ps_metrics m
)
SELECT 
    "Country",
    "TerritoryRegion",
    SUM(q11)                                            AS q11,
    SUM(r11)                                            AS r11,
    SUM(gp11)                                           AS gp11,
    SUM(gp11) / NULLIF(SUM(r11), 0)                     AS gm11_pct,
    SUM(q12)                                            AS q12,
    SUM(r12)                                            AS r12,
    SUM(gp12)                                           AS gp12,
    SUM(gp12) / NULLIF(SUM(r12), 0)                     AS gm12_pct,
    SUM(revenue_change)                                 AS revenue_change,
    SUM(gp_change)                                      AS gp_change,
    (SUM(gp12) / NULLIF(SUM(r12), 0) - SUM(gp11) / NULLIF(SUM(r11), 0)) AS gm_pct_change,
    SUM(price_effect)                                   AS price_effect,
    SUM(unit_cost_effect)                               AS unit_cost_effect,
    SUM(volume_effect)                                  AS volume_effect,
    SUM(mix_effect)                                     AS mix_effect,
    SUM(price_effect + unit_cost_effect + volume_effect + mix_effect) AS reconciled_gp_change,
    SUM(gp_change - (price_effect + unit_cost_effect + volume_effect + mix_effect)) AS residual
FROM ps_effects
GROUP BY "Country", "TerritoryRegion"
ORDER BY SUM(gp_change) DESC;
