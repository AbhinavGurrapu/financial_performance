-- ============================================================================
-- AdventureWorks DW Data Loading Script for PostgreSQL 18
-- Uses client-side \copy with pipe delimiter (|) and empty string as NULL
-- ============================================================================

\set ON_ERROR_STOP on
\encoding UTF8

\echo '1/7 Loading DimDate (raw)...'
\copy "DimDate" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/DimDate.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '2/7 Loading DimProductCategory (raw)...'
\copy "DimProductCategory" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/DimProductCategory.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '3/7 Loading DimProductSubcategory (raw)...'
\copy "DimProductSubcategory" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/DimProductSubcategory.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '4/7 Loading DimProduct (sanitized staging copy - NUL bytes stripped)...'
\copy "DimProduct" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/staging/DimProduct_sanitized.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '5/7 Loading DimReseller (raw)...'
\copy "DimReseller" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/DimReseller.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '6/7 Loading DimSalesTerritory (raw)...'
\copy "DimSalesTerritory" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/DimSalesTerritory.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo '7/7 Loading FactResellerSales (raw)...'
\copy "FactResellerSales" FROM 'C:/Users/dell/OneDrive/Desktop/financial_performance/data/raw/FactResellerSales.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');
