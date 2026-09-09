import os
import psycopg2
import sys

def main():
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST', 'localhost'),
        port=os.environ.get('PGPORT', 5432),
        user=os.environ.get('PGUSER', 'postgres'),
        dbname=os.environ.get('PGDATABASE', 'postgres'),
        password=os.environ.get('PGPASSWORD')
    )
    cur = conn.cursor()

    print("==================================================")
    print("PHASE 4 — ABT FULL RECONCILIATION & VALIDATION")
    print("==================================================")

    # A. Row Count Validation
    cur.execute("""
        SELECT COUNT(*) 
        FROM "FactResellerSales" f
        JOIN "DimDate" d ON f."OrderDateKey" = d."DateKey"
        WHERE f."CurrencyKey" = 100 AND d."CalendarYear" IN (2011, 2012);
    """)
    expected_rows = cur.fetchone()[0]

    cur.execute('SELECT COUNT(*) FROM "abt_reseller_sales";')
    actual_rows = cur.fetchone()[0]

    print(f"\nA. ROW COUNT CHECK:")
    print(f"  Expected Row Count (Fact Scope): {expected_rows}")
    print(f"  Actual Row Count (ABT Table):  {actual_rows}")
    assert expected_rows == actual_rows, f"FAIL: Row count mismatch! Expected {expected_rows}, got {actual_rows}"
    print("  STATUS: PASS")

    # B & G. Grain & Duplicate Check
    cur.execute("""
        SELECT COUNT(DISTINCT ("SalesOrderNumber", "SalesOrderLineNumber")) 
        FROM "abt_reseller_sales";
    """)
    distinct_grain_count = cur.fetchone()[0]

    cur.execute("""
        SELECT "SalesOrderNumber", "SalesOrderLineNumber", COUNT(*) 
        FROM "abt_reseller_sales" 
        GROUP BY "SalesOrderNumber", "SalesOrderLineNumber" 
        HAVING COUNT(*) > 1;
    """)
    duplicates = cur.fetchall()

    print(f"\nB & G. GRAIN & DUPLICATE CHECK:")
    print(f"  Total ABT Rows:           {actual_rows}")
    print(f"  Distinct Grain Keys:      {distinct_grain_count}")
    print(f"  Duplicate Grain Records: {len(duplicates)}")
    assert distinct_grain_count == actual_rows, "FAIL: Grain is not unique!"
    assert len(duplicates) == 0, "FAIL: Duplicate grain records found!"
    print("  STATUS: PASS")

    # C. Scope Check
    cur.execute('SELECT DISTINCT "CurrencyKey" FROM "abt_reseller_sales";')
    currencies = [r[0] for r in cur.fetchall()]

    cur.execute('SELECT DISTINCT "CalendarYear" FROM "abt_reseller_sales";')
    years = [r[0] for r in cur.fetchall()]

    print(f"\nC. SCOPE BOUNDARY CHECK:")
    print(f"  Distinct CurrencyKeys in ABT: {currencies}")
    print(f"  Distinct CalendarYears in ABT: {years}")
    assert currencies == [100], f"FAIL: Unexpected CurrencyKeys: {currencies}"
    assert sorted(years) == [2011, 2012], f"FAIL: Unexpected CalendarYears: {years}"
    print("  STATUS: PASS")

    # D. Join Integrity Check
    dim_fields = [
        "ResellerName", "BusinessType", "AnnualSales", 
        "SalesTerritoryRegion", "SalesTerritoryCountry",
        "ProductName", "Subcategory", "Category", 
        "CalendarMonth", "CalendarQuarter", "CalendarYear", "CalendarMonthNumber"
    ]
    null_counts = {}
    total_nulls = 0
    for field in dim_fields:
        cur.execute(f'SELECT COUNT(*) FROM "abt_reseller_sales" WHERE "{field}" IS NULL;')
        cnt = cur.fetchone()[0]
        null_counts[field] = cnt
        total_nulls += cnt

    print(f"\nD. JOIN INTEGRITY (NULL DIMENSION MAPPINGS):")
    for f_name, n_cnt in null_counts.items():
        print(f"  - Field '{f_name}': {n_cnt} NULLs")
    assert total_nulls == 0, f"FAIL: Found {total_nulls} NULL dimension mappings!"
    print("  STATUS: PASS (0 NULL dimension mappings)")

    # E. Financial Totals Reconciliation
    cur.execute("""
        SELECT 
            SUM(f."OrderQuantity")        AS total_qty,
            SUM(f."ExtendedAmount")       AS total_ext_amt,
            SUM(f."DiscountAmount")       AS total_disc_amt,
            SUM(f."SalesAmount")          AS total_sales_amt,
            SUM(f."TotalProductCost")     AS total_cost
        FROM "FactResellerSales" f
        JOIN "DimDate" d ON f."OrderDateKey" = d."DateKey"
        WHERE f."CurrencyKey" = 100 AND d."CalendarYear" IN (2011, 2012);
    """)
    src_tot = cur.fetchone()

    cur.execute("""
        SELECT 
            SUM("OrderQuantity")        AS total_qty,
            SUM("ExtendedAmount")       AS total_ext_amt,
            SUM("DiscountAmount")       AS total_disc_amt,
            SUM("SalesAmount")          AS total_sales_amt,
            SUM("TotalProductCost")     AS total_cost
        FROM "abt_reseller_sales";
    """)
    abt_tot = cur.fetchone()

    metrics = ["OrderQuantity", "ExtendedAmount", "DiscountAmount", "SalesAmount", "TotalProductCost"]
    print(f"\nE. FINANCIAL TOTALS RECONCILIATION:")
    print(f"  {'Metric':<20} | {'Source Fact Total':<20} | {'ABT Table Total':<20} | {'Variance':<15}")
    print("  " + "-" * 82)
    for idx, m in enumerate(metrics):
        s_val = float(src_tot[idx])
        a_val = float(abt_tot[idx])
        diff = abs(s_val - a_val)
        print(f"  {m:<20} | {s_val:<20,.4f} | {a_val:<20,.4f} | {diff:<15,.6f}")
        assert diff < 0.01, f"FAIL: Total mismatch for {m}! Source={s_val}, ABT={a_val}"
    print("  STATUS: PASS (Exact Financial Reconciliation)")

    # F. Derived Metric Mathematical Validation
    print(f"\nF. DERIVED METRIC MATHEMATICAL VALIDATION:")
    
    # 1. ExtendedAmount = OrderQuantity * UnitPrice
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("ExtendedAmount" - ("OrderQuantity" * "UnitPrice")) > 0.01;
    """)
    mismatches_ext = cur.fetchone()[0]
    print(f"  1. ExtendedAmount = OrderQuantity * UnitPrice Mismatches: {mismatches_ext}")
    assert mismatches_ext == 0, f"FAIL: ExtendedAmount equation mismatches: {mismatches_ext}"

    # 2. DiscountAmount = ExtendedAmount * UnitPriceDiscountPct
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("DiscountAmount" - ("ExtendedAmount" * "UnitPriceDiscountPct")) > 0.01;
    """)
    mismatches_disc = cur.fetchone()[0]
    print(f"  2. DiscountAmount = ExtendedAmount * UnitPriceDiscountPct Mismatches: {mismatches_disc}")
    assert mismatches_disc == 0, f"FAIL: DiscountAmount equation mismatches: {mismatches_disc}"

    # 3. SalesAmount = ExtendedAmount - DiscountAmount
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("SalesAmount" - ("ExtendedAmount" - "DiscountAmount")) > 0.01;
    """)
    mismatches_sales = cur.fetchone()[0]
    print(f"  3. SalesAmount = ExtendedAmount - DiscountAmount Mismatches: {mismatches_sales}")
    assert mismatches_sales == 0, f"FAIL: SalesAmount equation mismatches: {mismatches_sales}"

    # 4. TotalProductCost = ProductStandardCost * OrderQuantity
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("TotalProductCost" - ("ProductStandardCost" * "OrderQuantity")) > 0.01;
    """)
    mismatches_cost = cur.fetchone()[0]
    print(f"  4. TotalProductCost = ProductStandardCost * OrderQuantity Mismatches: {mismatches_cost}")
    assert mismatches_cost == 0, f"FAIL: TotalProductCost equation mismatches: {mismatches_cost}"

    # 5. GrossProfit = SalesAmount - TotalProductCost
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("GrossProfit" - ("SalesAmount" - "TotalProductCost")) > 0.01;
    """)
    mismatches_gp = cur.fetchone()[0]
    print(f"  5. GrossProfit = SalesAmount - TotalProductCost Mismatches: {mismatches_gp}")
    assert mismatches_gp == 0, f"FAIL: GrossProfit equation mismatches: {mismatches_gp}"

    # 6. GrossMarginPct = GrossProfit / SalesAmount
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("GrossMarginPct" - ("GrossProfit" / NULLIF("SalesAmount", 0))) > 0.0001;
    """)
    mismatches_gm = cur.fetchone()[0]
    print(f"  6. GrossMarginPct = GrossProfit / SalesAmount Mismatches: {mismatches_gm}")
    assert mismatches_gm == 0, f"FAIL: GrossMarginPct equation mismatches: {mismatches_gm}"

    # 7. RealizedUnitPrice = SalesAmount / OrderQuantity
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("RealizedUnitPrice" - ("SalesAmount" / NULLIF("OrderQuantity", 0))) > 0.0001;
    """)
    mismatches_rup = cur.fetchone()[0]
    print(f"  7. RealizedUnitPrice = SalesAmount / OrderQuantity Mismatches: {mismatches_rup}")
    assert mismatches_rup == 0, f"FAIL: RealizedUnitPrice equation mismatches: {mismatches_rup}"

    # 8. DiscountRatePct = DiscountAmount / ExtendedAmount
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("DiscountRatePct" - ("DiscountAmount" / NULLIF("ExtendedAmount", 0))) > 0.0001;
    """)
    mismatches_drp = cur.fetchone()[0]
    print(f"  8. DiscountRatePct = DiscountAmount / ExtendedAmount Mismatches: {mismatches_drp}")
    assert mismatches_drp == 0, f"FAIL: DiscountRatePct equation mismatches: {mismatches_drp}"

    # 9. UnitGrossProfit = RealizedUnitPrice - ProductStandardCost
    cur.execute("""
        SELECT COUNT(*) FROM "abt_reseller_sales"
        WHERE ABS("UnitGrossProfit" - ("RealizedUnitPrice" - "ProductStandardCost")) > 0.0001;
    """)
    mismatches_ugp = cur.fetchone()[0]
    print(f"  9. UnitGrossProfit = RealizedUnitPrice - ProductStandardCost Mismatches: {mismatches_ugp}")
    assert mismatches_ugp == 0, f"FAIL: UnitGrossProfit equation mismatches: {mismatches_ugp}"

    print("  STATUS: PASS (All Derived Equations Mathematically Validated)")

    print("\n==================================================")
    print("ALL PHASE 4 VALIDATIONS PASSED WITH 100% SUCCESS!")
    print("==================================================")

    conn.close()

if __name__ == "__main__":
    main()
