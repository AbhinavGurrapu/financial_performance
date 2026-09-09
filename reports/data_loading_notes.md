# AdventureWorks DW — Data Loading & Architecture Notes

**Project:** Financial Performance & Profitability Diagnostic Analytics  
**Database Engine:** PostgreSQL 18  
**Source Dataset:** Official Microsoft AdventureWorks DW Azure Synapse / SQL DW CSV Distribution  
**Location of Untouched Raw Files:** `C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\data\raw\`  
**Temporary Staging Artifact:** `C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\data\staging\DimProduct_sanitized.csv`

---

## 1. Connection & Execution Architecture

- **Host:** `localhost`
- **Port:** `5432`
- **User:** `postgres`
- **Client Executable:** `C:\Program Files\PostgreSQL\18\bin\psql.exe`
- **Authentication:** Standard interactive prompt via client terminal (no credentials stored on disk or in persistent environment variables).
- **Master Orchestrator:** `C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\sql\master_load_and_verify.sql`

---

## 2. Root Cause Analysis: Initial Load Failure

During the first loading run, 5 of 7 tables loaded with 100% success (`DimDate`, `DimProductCategory`, `DimProductSubcategory`, `DimReseller`, `DimSalesTerritory`). However, `DimProduct` and `FactResellerSales` reported 0 rows.

### A. The NUL-Byte Anomaly in DimProduct.csv
- Detailed byte-level inspection of `DimProduct.csv` revealed **574 literal ASCII NUL (`0x00`) bytes**:
  - `SpanishProductName` (Column 7): 287 occurrences of `\x00`
  - `FrenchProductName` (Column 8): 287 occurrences of `\x00`
- **Mechanism of Failure:** PostgreSQL and its client library (`libpq`) are written in C, where strings are null-terminated (`\0`). When `psql`'s `\copy` read the NUL bytes, string buffer routines treated `\0` as string termination, truncating lines mid-row at column 6. The remainder of the line was read as the start of the next row with trailing delimiters, causing PostgreSQL to abort with:  
  `ERROR: extra data after last expected column - COPY DimProduct, line 1`.

### B. Cascading Failure on FactResellerSales
- `FactResellerSales.csv` contains zero NUL bytes and is completely valid.
- However, `FactResellerSales` enforces a foreign key constraint referencing `DimProduct("ProductKey")`. Because `DimProduct` failed to load, `FactResellerSales` immediately aborted on its first insert (`Key (ProductKey)=(349) is not present in table "DimProduct"`).

### C. Orchestration Script Bug
- The initial load script lacked `\set ON_ERROR_STOP on`. By default, `psql` continued execution despite errors.
- A hardcoded `\echo 'All 7 tables loaded successfully.'` statement executed unconditionally.
- The verification query was purely passive (`SELECT actual, expected`) rather than programmatic and assertive.

---

## 3. Pre-Flight Audit & Second Load Failure: `VARCHAR(400)` Overflow

During the second load attempt, `DimProduct` failed again on line 483: `value too long for type character varying(400)`.

A comprehensive Pre-Flight Audit phase was initiated consisting of detailed Python-based validation over all 7 raw datasets and PostgreSQL table definitions:
1. **Max String Length Audit:** Analysed true max string lengths across all character columns. Example max lengths discovered in `DimProduct.csv`:
   - `EnglishDescription`: 221 chars
   - `FrenchDescription`: 269 chars
   - `GermanDescription`: 318 chars
   None exceeded the specified `VARCHAR(400)` limit.
2. **Empty String NOT NULL Violations Audit:** Ensured every column listed as `NOT NULL` in the DDL strictly matched actual valid data in the CSVs. 0 violations were found.
3. **Delimiter Tracking and Missing Column Search:** Verified all rows in all CSVs contained the correct number of delimiters.

### The Real Culprit: Unescaped Quotes Swallowing Delimiters
- Line 483 of `DimProduct` contained the string: `Carries 4 bikes securely; steel construction, fits 2" receiver hitch.`
- The PostgreSQL `\copy` command was using `FORMAT csv`. The CSV specification strictly requires quoting characters (such as `"`) to be escaped.
- Because `"` appeared raw and unescaped, PostgreSQL initiated an unintended quoting block spanning across multiple columns and lines, ignoring any internal pipe `|` delimiters until it eventually hit another `"`. This resulted in a massive concatenated string exceeding the 400-character limit, throwing the `VARCHAR(400)` overflow error.

---

## 4. Resolution & Hardening Approach

1. **Untouched Raw Files:** All official source CSVs in `data\raw\` remain completely untouched and unmutated.
2. **Temporary Staging Sanitization:** A Python script (`sanitize_dimproduct.py`) extracted `DimProduct.csv` into `data\staging\DimProduct_sanitized.csv` by removing only the 574 `0x00` bytes. Exactly 606 rows with 35 pipe delimiters each were verified.
3. **Fail-Fast Enforcement:** Enabled `\set ON_ERROR_STOP on` across all SQL scripts (`create_tables.sql`, `load_data.sql`, `master_load_and_verify.sql`).
4. **Minimal Schema Correction:** Relaxed artificial `NOT NULL` constraints on `SpanishProductName` and `FrenchProductName` in `DimProduct`. The original SQL Server source satisfied `NOT NULL` with `CHAR(0)` for untranslated fields, which in PostgreSQL translates semantically and correctly to SQL `NULL` under `NULL ''`.
5. **Safe Quote Specification:** Added `QUOTE '^'` to all `\copy` routines in `load_data.sql`. A thorough Python scan (`check_chars.py`) confirmed that the Caret (`^`) does NOT exist in any of the 7 source datasets, making it an invincible, failure-proof substitute quote character that prevents unescaped literal quotes from merging columns.
6. **Assertive PL/pgSQL Verification:** The master script includes a strict PL/pgSQL validation block that compares each table's actual row count against the expected count and checks for orphaned foreign keys in `FactResellerSales`. If any count mismatches, a fatal `RAISE EXCEPTION` halts the pipeline and reports failure.

---

## 5. Expected Row Counts

| Table Name | Source File | Expected Row Count | Verification Status |
| :--- | :--- | :--- | :--- |
| `DimDate` | `data\raw\DimDate.csv` | 3,652 | Pending |
| `DimProductCategory` | `data\raw\DimProductCategory.csv` | 4 | Pending |
| `DimProductSubcategory` | `data\raw\DimProductSubcategory.csv` | 37 | Pending |
| `DimProduct` | `data\staging\DimProduct_sanitized.csv` | 606 | Pending |
| `DimReseller` | `data\raw\DimReseller.csv` | 701 | Pending |
| `DimSalesTerritory` | `data\raw\DimSalesTerritory.csv` | 11 | Pending |
| `FactResellerSales` | `data\raw\FactResellerSales.csv` | 60,855 | Pending |

---

## 6. Decision Log Updates

- **DECISION 1:** Official source CSVs in `data\raw\` are permanently locked as pristine, immutable source data.
- **DECISION 2:** The temporary staging copy (`DimProduct_sanitized.csv`) is preserved in `data\staging\` solely for reproducible automated loads, documented as a deterministic NUL-byte filter of the raw source.
- **DECISION 3:** PostgreSQL 18 is locked as the working database, utilizing strict DDL constraints and assertive validation before any diagnostic analytics begin.
- **DECISION 4:** Due to the unstructured, delimiter-agnostic nature of the Microsoft raw export files, safe load processes MUST explicitly declare a dedicated `QUOTE '^'` character distinct from standard quotes.
