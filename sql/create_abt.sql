-- ============================================================================
-- AdventureWorks DW — Analytical Base Table (ABT) Creation Script
-- Table: abt_reseller_sales
-- Grain: SalesOrderNumber + SalesOrderLineNumber
-- Analytical Scope: CurrencyKey = 100 AND CalendarYear IN (2011, 2012)
-- ============================================================================

\set ON_ERROR_STOP on

DROP TABLE IF EXISTS "abt_reseller_sales" CASCADE;

CREATE TABLE "abt_reseller_sales" AS
SELECT
    -- TIME
    f."OrderDate",
    d."CalendarYear",
    d."EnglishMonthName"            AS "CalendarMonth",
    d."MonthNumberOfYear"           AS "CalendarMonthNumber",
    d."CalendarQuarter",

    -- ORDER
    f."SalesOrderNumber",
    f."SalesOrderLineNumber",

    -- RESELLER
    f."ResellerKey",
    r."ResellerName",
    r."BusinessType",
    r."AnnualSales",

    -- GEOGRAPHY
    f."SalesTerritoryKey",
    st."SalesTerritoryRegion",
    st."SalesTerritoryCountry",

    -- PRODUCT
    f."ProductKey",
    p."EnglishProductName"          AS "ProductName",
    p."ProductSubcategoryKey",
    ps."EnglishProductSubcategoryName" AS "Subcategory",
    ps."ProductCategoryKey",
    pc."EnglishProductCategoryName" AS "Category",

    -- SCOPE METADATA
    f."CurrencyKey",

    -- SOURCE COMMERCIAL / FINANCIAL FIELDS
    f."OrderQuantity",
    f."UnitPrice",
    f."UnitPriceDiscountPct",
    f."ExtendedAmount",
    f."DiscountAmount",
    f."SalesAmount",
    f."ProductStandardCost",
    f."TotalProductCost",

    -- DERIVED FIELDS
    (f."SalesAmount" / NULLIF(f."OrderQuantity", 0))                             AS "RealizedUnitPrice",
    (f."SalesAmount" - f."TotalProductCost")                                     AS "GrossProfit",
    ((f."SalesAmount" - f."TotalProductCost") / NULLIF(f."SalesAmount", 0))       AS "GrossMarginPct",
    (f."DiscountAmount" / NULLIF(f."ExtendedAmount", 0))                         AS "DiscountRatePct",
    ((f."SalesAmount" / NULLIF(f."OrderQuantity", 0)) - f."ProductStandardCost") AS "UnitGrossProfit"

FROM "FactResellerSales" f
JOIN "DimDate" d 
  ON f."OrderDateKey" = d."DateKey"
JOIN "DimProduct" p 
  ON f."ProductKey" = p."ProductKey"
JOIN "DimProductSubcategory" ps 
  ON p."ProductSubcategoryKey" = ps."ProductSubcategoryKey"
JOIN "DimProductCategory" pc 
  ON ps."ProductCategoryKey" = pc."ProductCategoryKey"
JOIN "DimReseller" r 
  ON f."ResellerKey" = r."ResellerKey"
JOIN "DimSalesTerritory" st 
  ON f."SalesTerritoryKey" = st."SalesTerritoryKey"
WHERE f."CurrencyKey" = 100
  AND d."CalendarYear" IN (2011, 2012);

-- Add primary key constraint on grain
ALTER TABLE "abt_reseller_sales" 
ADD CONSTRAINT "PK_abt_reseller_sales" PRIMARY KEY ("SalesOrderNumber", "SalesOrderLineNumber");
