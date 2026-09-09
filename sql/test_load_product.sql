\set ON_ERROR_STOP on
\encoding UTF8

-- Truncate just to be sure
TRUNCATE TABLE "DimProduct" CASCADE;

\echo 'Loading DimProduct with QUOTE ^ ...'
\copy "DimProduct" FROM 'C:/Users/dell/OneDrive/Desktop/project_3_financial_performance/data/staging/DimProduct_sanitized.csv' WITH (FORMAT csv, DELIMITER '|', NULL '', QUOTE '^', ENCODING 'UTF8');

\echo 'DimProduct loaded successfully.'
