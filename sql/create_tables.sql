-- ============================================================================
-- AdventureWorks DW Schema Creation for PostgreSQL 18
-- Tables: DimDate, DimProductCategory, DimProductSubcategory, DimProduct,
--         DimReseller, DimSalesTerritory, FactResellerSales
-- ============================================================================

\set ON_ERROR_STOP on

-- Drop tables in reverse dependency order
DROP TABLE IF EXISTS "FactResellerSales" CASCADE;
DROP TABLE IF EXISTS "DimProduct" CASCADE;
DROP TABLE IF EXISTS "DimProductSubcategory" CASCADE;
DROP TABLE IF EXISTS "DimProductCategory" CASCADE;
DROP TABLE IF EXISTS "DimReseller" CASCADE;
DROP TABLE IF EXISTS "DimSalesTerritory" CASCADE;
DROP TABLE IF EXISTS "DimDate" CASCADE;

-- 1. DimDate (19 columns)
CREATE TABLE "DimDate" (
    "DateKey"               INTEGER NOT NULL PRIMARY KEY,
    "FullDateAlternateKey"  DATE NOT NULL,
    "DayNumberOfWeek"       SMALLINT NOT NULL,
    "EnglishDayNameOfWeek"  VARCHAR(10) NOT NULL,
    "SpanishDayNameOfWeek"  VARCHAR(10) NOT NULL,
    "FrenchDayNameOfWeek"   VARCHAR(10) NOT NULL,
    "DayNumberOfMonth"      SMALLINT NOT NULL,
    "DayNumberOfYear"       SMALLINT NOT NULL,
    "WeekNumberOfYear"      SMALLINT NOT NULL,
    "EnglishMonthName"      VARCHAR(10) NOT NULL,
    "SpanishMonthName"      VARCHAR(10) NOT NULL,
    "FrenchMonthName"       VARCHAR(10) NOT NULL,
    "MonthNumberOfYear"     SMALLINT NOT NULL,
    "CalendarQuarter"       SMALLINT NOT NULL,
    "CalendarYear"          SMALLINT NOT NULL,
    "CalendarSemester"      SMALLINT NOT NULL,
    "FiscalQuarter"         SMALLINT NOT NULL,
    "FiscalYear"            SMALLINT NOT NULL,
    "FiscalSemester"        SMALLINT NOT NULL
);

-- 2. DimProductCategory (5 columns)
CREATE TABLE "DimProductCategory" (
    "ProductCategoryKey"          INTEGER NOT NULL PRIMARY KEY,
    "ProductCategoryAlternateKey" INTEGER,
    "EnglishProductCategoryName"  VARCHAR(50) NOT NULL,
    "SpanishProductCategoryName"  VARCHAR(50) NOT NULL,
    "FrenchProductCategoryName"   VARCHAR(50) NOT NULL
);

-- 3. DimProductSubcategory (6 columns)
CREATE TABLE "DimProductSubcategory" (
    "ProductSubcategoryKey"          INTEGER NOT NULL PRIMARY KEY,
    "ProductSubcategoryAlternateKey" INTEGER,
    "EnglishProductSubcategoryName"  VARCHAR(50) NOT NULL,
    "SpanishProductSubcategoryName"  VARCHAR(50) NOT NULL,
    "FrenchProductSubcategoryName"   VARCHAR(50) NOT NULL,
    "ProductCategoryKey"             INTEGER REFERENCES "DimProductCategory"("ProductCategoryKey")
);

-- 4. DimProduct (36 columns)
CREATE TABLE "DimProduct" (
    "ProductKey"                    INTEGER NOT NULL PRIMARY KEY,
    "ProductAlternateKey"           VARCHAR(25),
    "ProductSubcategoryKey"         INTEGER REFERENCES "DimProductSubcategory"("ProductSubcategoryKey"),
    "WeightUnitMeasureCode"         CHAR(3),
    "SizeUnitMeasureCode"           CHAR(3),
    "EnglishProductName"            VARCHAR(50) NOT NULL,
    "SpanishProductName"            VARCHAR(50),
    "FrenchProductName"             VARCHAR(50),
    "StandardCost"                  NUMERIC(19,4),
    "FinishedGoodsFlag"             SMALLINT NOT NULL,
    "Color"                         VARCHAR(15) NOT NULL,
    "SafetyStockLevel"              SMALLINT,
    "ReorderPoint"                  SMALLINT,
    "ListPrice"                     NUMERIC(19,4),
    "Size"                          VARCHAR(50),
    "SizeRange"                     VARCHAR(50),
    "Weight"                        DOUBLE PRECISION,
    "DaysToManufacture"             INTEGER,
    "ProductLine"                   CHAR(2),
    "DealerPrice"                   NUMERIC(19,4),
    "Class"                         CHAR(2),
    "Style"                         CHAR(2),
    "ModelName"                     VARCHAR(50),
    "LargePhoto"                    TEXT,
    "EnglishDescription"            VARCHAR(400),
    "FrenchDescription"             VARCHAR(400),
    "ChineseDescription"            VARCHAR(400),
    "ArabicDescription"             VARCHAR(400),
    "HebrewDescription"             VARCHAR(400),
    "ThaiDescription"               VARCHAR(400),
    "GermanDescription"             VARCHAR(400),
    "JapaneseDescription"           VARCHAR(400),
    "TurkishDescription"            VARCHAR(400),
    "StartDate"                     TIMESTAMP,
    "EndDate"                       TIMESTAMP,
    "Status"                        VARCHAR(7)
);

-- 5. DimReseller (20 columns)
CREATE TABLE "DimReseller" (
    "ResellerKey"           INTEGER NOT NULL PRIMARY KEY,
    "GeographyKey"          INTEGER,
    "ResellerAlternateKey"  VARCHAR(15),
    "Phone"                 VARCHAR(25),
    "BusinessType"          VARCHAR(20) NOT NULL,
    "ResellerName"          VARCHAR(50) NOT NULL,
    "NumberEmployees"       INTEGER,
    "OrderFrequency"        CHAR(1),
    "OrderMonth"            SMALLINT,
    "FirstOrderYear"        INTEGER,
    "LastOrderYear"         INTEGER,
    "ProductLine"           VARCHAR(50),
    "AddressLine1"          VARCHAR(60),
    "AddressLine2"          VARCHAR(60),
    "AnnualSales"           NUMERIC(19,4),
    "BankName"              VARCHAR(50),
    "MinPaymentType"        SMALLINT,
    "MinPaymentAmount"      NUMERIC(19,4),
    "AnnualRevenue"         NUMERIC(19,4),
    "YearOpened"            INTEGER
);

-- 6. DimSalesTerritory (6 columns)
CREATE TABLE "DimSalesTerritory" (
    "SalesTerritoryKey"          INTEGER NOT NULL PRIMARY KEY,
    "SalesTerritoryAlternateKey" INTEGER,
    "SalesTerritoryRegion"       VARCHAR(50) NOT NULL,
    "SalesTerritoryCountry"      VARCHAR(50) NOT NULL,
    "SalesTerritoryGroup"        VARCHAR(50),
    "SalesTerritoryImage"        TEXT
);

-- 7. FactResellerSales (27 columns)
CREATE TABLE "FactResellerSales" (
    "ProductKey"                INTEGER NOT NULL REFERENCES "DimProduct"("ProductKey"),
    "OrderDateKey"              INTEGER NOT NULL REFERENCES "DimDate"("DateKey"),
    "DueDateKey"                INTEGER NOT NULL REFERENCES "DimDate"("DateKey"),
    "ShipDateKey"               INTEGER NOT NULL REFERENCES "DimDate"("DateKey"),
    "ResellerKey"               INTEGER NOT NULL REFERENCES "DimReseller"("ResellerKey"),
    "EmployeeKey"               INTEGER NOT NULL,
    "PromotionKey"              INTEGER NOT NULL,
    "CurrencyKey"               INTEGER NOT NULL,
    "SalesTerritoryKey"         INTEGER NOT NULL REFERENCES "DimSalesTerritory"("SalesTerritoryKey"),
    "SalesOrderNumber"          VARCHAR(20) NOT NULL,
    "SalesOrderLineNumber"      SMALLINT NOT NULL,
    "RevisionNumber"            SMALLINT,
    "OrderQuantity"             SMALLINT,
    "UnitPrice"                 NUMERIC(19,4),
    "ExtendedAmount"            NUMERIC(19,4),
    "UnitPriceDiscountPct"      DOUBLE PRECISION,
    "DiscountAmount"            DOUBLE PRECISION,
    "ProductStandardCost"       NUMERIC(19,4),
    "TotalProductCost"          NUMERIC(19,4),
    "SalesAmount"               NUMERIC(19,4),
    "TaxAmt"                    NUMERIC(19,4),
    "Freight"                   NUMERIC(19,4),
    "CarrierTrackingNumber"     VARCHAR(25),
    "CustomerPONumber"          VARCHAR(25),
    "OrderDate"                 TIMESTAMP,
    "DueDate"                   TIMESTAMP,
    "ShipDate"                  TIMESTAMP,
    CONSTRAINT "PK_FactResellerSales" PRIMARY KEY ("SalesOrderNumber", "SalesOrderLineNumber")
);
