-- ============================================================================
-- Complete Master Script: Create Schema, Load Data, and Assert Verification
-- ============================================================================

\set ON_ERROR_STOP on

\echo '==================================================='
\echo 'STEP 1: RESETTING AND CREATING TABLES'
\echo '==================================================='
\i 'C:/Users/dell/OneDrive/Desktop/financial_performance/sql/create_tables.sql'

\echo ''
\echo '==================================================='
\echo 'STEP 2: LOADING DATA FILES'
\echo '==================================================='
\i 'C:/Users/dell/OneDrive/Desktop/financial_performance/sql/load_data.sql'

\echo ''
\echo '==================================================='
\echo 'STEP 3: ASSERTIVE VERIFICATION'
\echo '==================================================='

-- 3A. Display table summary
SELECT 
    t.table_name,
    t.actual_count,
    t.expected_count,
    CASE WHEN t.actual_count = t.expected_count THEN 'PASS' ELSE 'FAIL' END AS status
FROM (
    SELECT 'DimDate' AS table_name, COUNT(*) AS actual_count, 3652 AS expected_count FROM "DimDate"
    UNION ALL
    SELECT 'DimProductCategory', COUNT(*), 4 FROM "DimProductCategory"
    UNION ALL
    SELECT 'DimProductSubcategory', COUNT(*), 37 FROM "DimProductSubcategory"
    UNION ALL
    SELECT 'DimProduct', COUNT(*), 606 FROM "DimProduct"
    UNION ALL
    SELECT 'DimReseller', COUNT(*), 701 FROM "DimReseller"
    UNION ALL
    SELECT 'DimSalesTerritory', COUNT(*), 11 FROM "DimSalesTerritory"
    UNION ALL
    SELECT 'FactResellerSales', COUNT(*), 60855 FROM "FactResellerSales"
) t
ORDER BY t.table_name;

-- 3B. Assertive verification block: raises hard exception if any table count mismatches
DO $$
DECLARE
    v_date_count INT;
    v_cat_count INT;
    v_subcat_count INT;
    v_prod_count INT;
    v_reseller_count INT;
    v_terr_count INT;
    v_sales_count INT;
    v_orphan_prod INT;
    v_orphan_date INT;
    v_orphan_reseller INT;
    v_orphan_terr INT;
BEGIN
    SELECT COUNT(*) INTO v_date_count FROM "DimDate";
    SELECT COUNT(*) INTO v_cat_count FROM "DimProductCategory";
    SELECT COUNT(*) INTO v_subcat_count FROM "DimProductSubcategory";
    SELECT COUNT(*) INTO v_prod_count FROM "DimProduct";
    SELECT COUNT(*) INTO v_reseller_count FROM "DimReseller";
    SELECT COUNT(*) INTO v_terr_count FROM "DimSalesTerritory";
    SELECT COUNT(*) INTO v_sales_count FROM "FactResellerSales";

    IF v_date_count <> 3652 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimDate expected 3652 rows, found %', v_date_count;
    END IF;
    IF v_cat_count <> 4 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimProductCategory expected 4 rows, found %', v_cat_count;
    END IF;
    IF v_subcat_count <> 37 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimProductSubcategory expected 37 rows, found %', v_subcat_count;
    END IF;
    IF v_prod_count <> 606 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimProduct expected 606 rows, found %', v_prod_count;
    END IF;
    IF v_reseller_count <> 701 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimReseller expected 701 rows, found %', v_reseller_count;
    END IF;
    IF v_terr_count <> 11 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: DimSalesTerritory expected 11 rows, found %', v_terr_count;
    END IF;
    IF v_sales_count <> 60855 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: FactResellerSales expected 60855 rows, found %', v_sales_count;
    END IF;

    -- Check for orphaned foreign keys in FactResellerSales
    SELECT COUNT(*) INTO v_orphan_prod
    FROM "FactResellerSales" f LEFT JOIN "DimProduct" p ON f."ProductKey" = p."ProductKey"
    WHERE p."ProductKey" IS NULL;

    SELECT COUNT(*) INTO v_orphan_date
    FROM "FactResellerSales" f LEFT JOIN "DimDate" d ON f."OrderDateKey" = d."DateKey"
    WHERE d."DateKey" IS NULL;

    SELECT COUNT(*) INTO v_orphan_reseller
    FROM "FactResellerSales" f LEFT JOIN "DimReseller" r ON f."ResellerKey" = r."ResellerKey"
    WHERE r."ResellerKey" IS NULL;

    SELECT COUNT(*) INTO v_orphan_terr
    FROM "FactResellerSales" f LEFT JOIN "DimSalesTerritory" t ON f."SalesTerritoryKey" = t."SalesTerritoryKey"
    WHERE t."SalesTerritoryKey" IS NULL;

    IF v_orphan_prod > 0 OR v_orphan_date > 0 OR v_orphan_reseller > 0 OR v_orphan_terr > 0 THEN
        RAISE EXCEPTION 'ASSERTION FAILED: Orphaned foreign keys detected in FactResellerSales!';
    END IF;

    RAISE NOTICE '===================================================';
    RAISE NOTICE 'SUCCESS: ALL 7 TABLES LOADED AND FULLY VALIDATED!';
    RAISE NOTICE '===================================================';
END $$;

\echo ''
\echo '==================================================='
\echo 'STEP 4: FACT TABLE DATE RANGE CHECK'
\echo '==================================================='
SELECT 
    MIN("OrderDate") AS min_order_date,
    MAX("OrderDate") AS max_order_date,
    MIN("OrderDateKey") AS min_order_date_key,
    MAX("OrderDateKey") AS max_order_date_key,
    COUNT(DISTINCT "SalesOrderNumber") AS distinct_orders,
    SUM("OrderQuantity") AS total_units_sold,
    SUM("SalesAmount") AS total_sales_amount
FROM "FactResellerSales";
