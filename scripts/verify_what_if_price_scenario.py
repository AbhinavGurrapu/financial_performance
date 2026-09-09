import os
import sys
import psycopg2
import pandas as pd
import numpy as np

def run_verification():
    print("==================================================")
    print("STEP 14B — SCENARIO 2: TARGETED PRICE REALIZATION")
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

    # 2. Execute sql/06_what_if_price_scenario.sql
    sql_file = os.path.join('sql', '06_what_if_price_scenario.sql')
    print(f"\n[1/3] Executing SQL script: {sql_file}")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    cur.execute(sql_script)
    conn.commit()
    print(" -> Views successfully created in PostgreSQL.")

    # 3. Export views to CSV files under data/staging/
    print("\n[2/3] Exporting staging CSVs under data/staging/...")
    os.makedirs(os.path.join('data', 'staging'), exist_ok=True)
    
    df_subcategories = pd.read_sql("SELECT * FROM v_what_if_price_scenario_subcategories", conn)
    subcat_csv = os.path.join('data', 'staging', 'price_scenario_subcategories.csv')
    df_subcategories.to_csv(subcat_csv, index=False)
    print(f" -> Saved {subcat_csv} ({len(df_subcategories)} rows)")

    df_summary = pd.read_sql("SELECT * FROM v_what_if_price_scenario_summary", conn)
    summary_csv = os.path.join('data', 'staging', 'price_scenario_summary.csv')
    df_summary.to_csv(summary_csv, index=False)
    print(f" -> Saved {summary_csv} ({len(df_summary)} rows)")

    # 4. Perform 9 Mandatory Audit Checks
    print("\n[3/3] Running Audit & Reconciliation Checks...")

    # Check 1: Validate Road Bikes and Touring Bikes exist in CY2012 USD data
    df_all_sub = pd.read_sql("""
        SELECT "Subcategory", SUM("OrderQuantity") as units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
        GROUP BY "Subcategory"
    """, conn)
    existing_subcats = set(df_all_sub['Subcategory'])
    required_subcats = {'Road Bikes', 'Touring Bikes'}
    assert required_subcats.issubset(existing_subcats), f"Missing required subcategories: {required_subcats - existing_subcats}"
    print(" [PASS] Check 1: Target subcategories ('Road Bikes', 'Touring Bikes') exist in CY2012 USD data.")

    # Check 2: Validate exactly 2% price increase is applied
    for idx, row in df_subcategories.iterrows():
        expected_s_asp = row['baseline_asp'] * 1.02
        assert np.isclose(row['scenario_asp'], expected_s_asp), f"Scenario ASP for {row['target_subcategory']} mismatch"
    print(" [PASS] Check 2: Exactly 2% price increase is applied to realized ASPs.")

    # Check 3: Validate unit volume remains unchanged
    df_base_sub_units = pd.read_sql("""
        SELECT "Subcategory", SUM("OrderQuantity") as units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012 AND "Subcategory" IN ('Road Bikes', 'Touring Bikes')
        GROUP BY "Subcategory"
    """, conn).set_index('Subcategory')['units'].to_dict()
    
    for idx, row in df_subcategories.iterrows():
        base_units = df_base_sub_units[row['target_subcategory']]
        assert np.isclose(row['cy2012_units'], base_units), f"Units mismatch for {row['target_subcategory']}"
    print(" [PASS] Check 3: Unit volume remains strictly unchanged.")

    # Check 4: Validate scenario revenue calculation is correct
    for idx, row in df_subcategories.iterrows():
        expected_s_rev = row['cy2012_units'] * row['scenario_asp']
        assert np.isclose(row['scenario_net_revenue'], expected_s_rev), "Subcategory scenario revenue mismatch"
    
    b_rev = float(df_summary.iloc[0]['baseline_net_revenue'])
    inc_rev = float(df_summary.iloc[0]['incremental_net_revenue'])
    s_rev = float(df_summary.iloc[0]['scenario_net_revenue'])
    assert np.isclose(s_rev, b_rev + inc_rev), "Portfolio scenario revenue mismatch"
    print(f" [PASS] Check 4: Scenario revenue calculation is correct (Incremental Net Rev: +${inc_rev:,.2f}).")

    # Check 5: Validate Incremental Gross Profit EQUALS Incremental Net Revenue
    inc_gp = float(df_summary.iloc[0]['incremental_gross_profit'])
    diff = abs(inc_rev - inc_gp)
    assert np.isclose(inc_rev, inc_gp), f"Incremental GP != Incremental Net Rev diff={diff}"
    for idx, row in df_subcategories.iterrows():
        sub_inc_rev = row['incremental_net_revenue']
        sub_inc_gp = row['incremental_gross_profit']
        assert np.isclose(sub_inc_rev, sub_inc_gp), f"Subcategory Inc GP != Inc Rev for {row['target_subcategory']}"
    print(f" [PASS] Check 5: Incremental Gross Profit EQUALS Incremental Net Revenue (${inc_gp:,.2f} == ${inc_rev:,.2f}, zero residual).")

    # Check 6: Validate scenario Gross Profit calculation is correct
    b_gp = float(df_summary.iloc[0]['baseline_gross_profit'])
    s_gp = float(df_summary.iloc[0]['scenario_gross_profit'])
    assert np.isclose(s_gp, b_gp + inc_gp), "Portfolio scenario Gross Profit mismatch"
    print(f" [PASS] Check 6: Scenario Gross Profit calculation is correct (${b_gp:,.2f} + ${inc_gp:,.2f} = ${s_gp:,.2f}).")

    # Check 7: Validate scenario Gross Margin calculation is correct
    s_gm = float(df_summary.iloc[0]['scenario_gross_margin_pct'])
    expected_s_gm = (s_gp / s_rev) * 100.0
    assert np.isclose(s_gm, expected_s_gm), "Scenario Gross Margin % mismatch"
    print(f" [PASS] Check 7: Scenario Gross Margin % calculation is correct ({s_gm:.4f}%).")

    # Check 8: Validate no unexpected duplicate rows
    assert len(df_subcategories) == 2, f"Expected 2 subcategories, got {len(df_subcategories)}"
    assert len(df_summary) == 1, f"Expected 1 summary row, got {len(df_summary)}"
    print(" [PASS] Check 8: No unexpected duplicate rows in staging outputs.")

    # Check 9: Validate all key scenario outputs reconcile with zero residual
    sum_inc_rev = df_subcategories['incremental_net_revenue'].sum()
    sum_inc_gp = df_subcategories['incremental_gross_profit'].sum()
    assert np.isclose(sum_inc_rev, inc_rev), "Summary incremental revenue mismatch"
    assert np.isclose(sum_inc_gp, inc_gp), "Summary incremental GP mismatch"
    print(" [PASS] Check 9: All key scenario outputs reconcile mathematically with zero residual.")

    conn.close()
    print("\n==================================================")
    print("[SUCCESS] ALL WHAT-IF PRICE SCENARIO VERIFICATIONS PASSED!")
    print("==================================================")

if __name__ == '__main__':
    run_verification()
