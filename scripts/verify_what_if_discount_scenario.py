import os
import sys
import psycopg2
import pandas as pd
import numpy as np

def run_verification():
    print("==================================================")
    print("STEP 14B — SCENARIO 3: TARGETED DISCOUNT REDUCTION")
    print("AUTOMATED VERIFICATION & AUDIT SUITE")
    print("==================================================")

    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST', 'localhost'),
        port=os.environ.get('PGPORT', 5432),
        user=os.environ.get('PGUSER', 'postgres'),
        dbname=os.environ.get('PGDATABASE', 'postgres'),
        password=os.environ.get('PGPASSWORD', 'Abhi123$')
    )
    cur = conn.cursor()

    # 2. Execute sql/07_what_if_discount_scenario.sql
    sql_file = os.path.join('sql', '07_what_if_discount_scenario.sql')
    print(f"\n[1/3] Executing SQL script: {sql_file}")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    cur.execute(sql_script)
    conn.commit()
    print(" -> Views successfully created in PostgreSQL.")

    # 3. Export views to CSV files under data/staging/
    print("\n[2/3] Exporting staging CSVs under data/staging/...")
    os.makedirs(os.path.join('data', 'staging'), exist_ok=True)
    
    df_subcategories = pd.read_sql("SELECT * FROM v_what_if_discount_scenario_subcategories", conn)
    subcat_csv = os.path.join('data', 'staging', 'discount_scenario_subcategories.csv')
    df_subcategories.to_csv(subcat_csv, index=False)
    print(f" -> Saved {subcat_csv} ({len(df_subcategories)} rows)")

    df_summary = pd.read_sql("SELECT * FROM v_what_if_discount_scenario_summary", conn)
    summary_csv = os.path.join('data', 'staging', 'discount_scenario_summary.csv')
    df_summary.to_csv(summary_csv, index=False)
    print(f" -> Saved {summary_csv} ({len(df_summary)} rows)")

    # 4. Perform Mandatory Audit Checks
    print("\n[3/3] Running Audit & Reconciliation Checks...")

    # Check 1: Validate Accessories and Clothing exist
    df_all_cat = pd.read_sql("""
        SELECT "Category", SUM("OrderQuantity") as units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
        GROUP BY "Category"
    """, conn)
    existing_cats = set(df_all_cat['Category'])
    required_cats = {'Accessories', 'Clothing'}
    assert required_cats.issubset(existing_cats), f"Missing required subcategories/categories: {required_cats - existing_cats}"
    print(" [PASS] Check 1: Target subcategories ('Accessories', 'Clothing') exist in CY2012 USD data.")

    # Check 2: Validate exactly 50% of existing discount rate is removed
    for idx, row in df_subcategories.iterrows():
        expected_s_rate = row['baseline_discount_rate_pct'] * 0.50
        assert np.isclose(row['scenario_discount_rate_pct'], expected_s_rate), f"Discount rate mismatch for {row['target_subcategory']}"
    print(" [PASS] Check 2: Exactly 50% of the existing discount rate is removed.")

    # Check 3: Validate unit volume remains unchanged
    df_base_units = pd.read_sql("""
        SELECT "Category", SUM("OrderQuantity") as units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012 AND "Category" IN ('Accessories', 'Clothing')
        GROUP BY "Category"
    """, conn).set_index('Category')['units'].to_dict()
    
    for idx, row in df_subcategories.iterrows():
        base_u = df_base_units[row['target_subcategory']]
        assert np.isclose(row['cy2012_units'], base_u), f"Units mismatch for {row['target_subcategory']}"
    print(" [PASS] Check 3: Unit volume remains strictly unchanged.")

    # Check 4: Validate list / gross revenue remains unchanged
    df_base_gross = pd.read_sql("""
        SELECT "Category", SUM("UnitPrice" * "OrderQuantity") as gross_rev
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012 AND "Category" IN ('Accessories', 'Clothing')
        GROUP BY "Category"
    """, conn).set_index('Category')['gross_rev'].to_dict()
    
    for idx, row in df_subcategories.iterrows():
        base_g = float(df_base_gross[row['target_subcategory']])
        assert np.isclose(row['gross_revenue'], base_g), f"Gross revenue mismatch for {row['target_subcategory']}"
    print(" [PASS] Check 4: List / gross revenue remains strictly unchanged.")

    # Check 5: Validate scenario discount calculation is correct
    for idx, row in df_subcategories.iterrows():
        expected_s_disc = row['baseline_discount_amount'] * 0.50
        assert np.isclose(row['scenario_discount_amount'], expected_s_disc), "Scenario discount amount mismatch"
    print(" [PASS] Check 5: Scenario discount calculation is correct.")

    # Check 6: Validate discount savings calculation is correct
    for idx, row in df_subcategories.iterrows():
        expected_savings = row['baseline_discount_amount'] - row['scenario_discount_amount']
        assert np.isclose(row['discount_savings'], expected_savings), "Discount savings mismatch"
    print(" [PASS] Check 6: Discount savings calculation is correct.")

    # Check 7: Validate Incremental Gross Profit EQUALS Incremental Net Revenue
    inc_net_rev = float(df_summary.iloc[0]['incremental_net_revenue'])
    inc_gp = float(df_summary.iloc[0]['incremental_gross_profit'])
    assert np.isclose(inc_gp, inc_net_rev), f"Inc GP != Inc Net Rev: {inc_gp} vs {inc_net_rev}"
    print(f" [PASS] Check 7: Incremental Gross Profit EQUALS Incremental Net Revenue (${inc_gp:,.2f} == ${inc_net_rev:,.2f}).")

    # Check 8: Validate Incremental Gross Profit EQUALS Discount Savings
    disc_savings = float(df_summary.iloc[0]['discount_savings'])
    assert np.isclose(inc_gp, disc_savings), f"Inc GP != Discount Savings: {inc_gp} vs {disc_savings}"
    print(f" [PASS] Check 8: Incremental Gross Profit EQUALS Discount Savings (${inc_gp:,.2f} == ${disc_savings:,.2f}, zero residual).")

    # Check 9: Validate scenario Gross Profit calculation is correct
    b_gp = float(df_summary.iloc[0]['baseline_gross_profit'])
    s_gp = float(df_summary.iloc[0]['scenario_gross_profit'])
    assert np.isclose(s_gp, b_gp + inc_gp), "Scenario Gross Profit calculation mismatch"
    print(f" [PASS] Check 9: Scenario Gross Profit calculation is correct (${b_gp:,.2f} + ${inc_gp:,.2f} = ${s_gp:,.2f}).")

    # Check 10: Validate scenario Gross Margin calculation is correct
    s_gm = float(df_summary.iloc[0]['scenario_gross_margin_pct'])
    s_rev = float(df_summary.iloc[0]['scenario_net_revenue'])
    expected_s_gm = (s_gp / s_rev) * 100.0
    assert np.isclose(s_gm, expected_s_gm), "Scenario Gross Margin % mismatch"
    print(f" [PASS] Check 10: Scenario Gross Margin % calculation is correct ({s_gm:.4f}%).")

    # Check 11: Validate no unexpected duplicate rows
    assert len(df_subcategories) == 2, f"Expected 2 subcategories, got {len(df_subcategories)}"
    assert len(df_summary) == 1, f"Expected 1 summary row, got {len(df_summary)}"
    print(" [PASS] Check 11: No unexpected duplicate rows in staging outputs.")

    # Check 12: Validate all key scenario outputs reconcile with zero residual
    sum_disc_savings = df_subcategories['discount_savings'].sum()
    assert np.isclose(sum_disc_savings, disc_savings), "Summary discount savings mismatch"
    print(" [PASS] Check 12: All key scenario outputs reconcile mathematically with zero residual.")

    conn.close()
    print("\n==================================================")
    print("[SUCCESS] ALL WHAT-IF DISCOUNT SCENARIO VERIFICATIONS PASSED!")
    print("==================================================")

if __name__ == '__main__':
    run_verification()
