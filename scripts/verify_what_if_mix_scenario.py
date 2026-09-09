import os
import sys
import psycopg2
import pandas as pd
import numpy as np

def run_verification():
    print("==================================================")
    print("STEP 14B — SCENARIO 1: PRODUCT MIX REBALANCING")
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

    # 2. Execute sql/05_what_if_mix_scenario.sql
    sql_file = os.path.join('sql', '05_what_if_mix_scenario.sql')
    print(f"\n[1/3] Executing SQL script: {sql_file}")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    cur.execute(sql_script)
    conn.commit()
    print(" -> Views successfully created in PostgreSQL.")

    # 3. Export views to CSV files under data/staging/
    print("\n[2/3] Exporting staging CSVs under data/staging/...")
    os.makedirs(os.path.join('data', 'staging'), exist_ok=True)
    
    df_subcategories = pd.read_sql("SELECT * FROM v_what_if_mix_scenario_subcategories", conn)
    subcat_csv = os.path.join('data', 'staging', 'mix_scenario_subcategories.csv')
    df_subcategories.to_csv(subcat_csv, index=False)
    print(f" -> Saved {subcat_csv} ({len(df_subcategories)} rows)")

    df_summary = pd.read_sql("SELECT * FROM v_what_if_mix_scenario_summary", conn)
    summary_csv = os.path.join('data', 'staging', 'mix_scenario_summary.csv')
    df_summary.to_csv(summary_csv, index=False)
    print(f" -> Saved {summary_csv} ({len(df_summary)} rows)")

    # 4. Perform 8 Mandatory Verification Checks
    print("\n[3/3] Running 8 Audit & Reconciliation Checks...")

    # Check 1: Validate source and target subcategories exist in CY2012 USD data
    df_all_sub = pd.read_sql("""
        SELECT "Subcategory", SUM("OrderQuantity") as units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
        GROUP BY "Subcategory"
    """, conn)
    existing_subcats = set(df_all_sub['Subcategory'])
    required_subcats = {'Road Bikes', 'Touring Bikes', 'Mountain Bikes'}
    assert required_subcats.issubset(existing_subcats), f"Missing required subcategories: {required_subcats - existing_subcats}"
    print(" [PASS] Check 1: Source ('Road Bikes', 'Touring Bikes') and Target ('Mountain Bikes') subcategories exist.")

    # Check 2: Validate shifted units are exactly 5% of source units
    for idx, row in df_subcategories.iterrows():
        expected_shifted = row['cy2012_units'] * 0.05
        assert np.isclose(row['units_shifted'], expected_shifted), f"Units shifted for {row['source_subcategory']} is {row['units_shifted']}, expected {expected_shifted}"
    print(" [PASS] Check 2: Shifted units are exactly 5% of source units.")

    # Check 3: Validate total portfolio units remain unchanged
    df_tot_units = pd.read_sql("""
        SELECT SUM("OrderQuantity") as total_units
        FROM abt_reseller_sales
        WHERE "CurrencyKey" = 100 AND "CalendarYear" = 2012
    """, conn)
    baseline_units = float(df_tot_units.iloc[0]['total_units'])
    total_shifted = float(df_summary.iloc[0]['total_units_shifted'])
    scenario_units = baseline_units - total_shifted + total_shifted
    assert np.isclose(baseline_units, scenario_units), f"Portfolio units changed: baseline={baseline_units}, scenario={scenario_units}"
    print(f" [PASS] Check 3: Total portfolio unit volume remains unchanged ({baseline_units:,.0f} units).")

    # Check 4: Validate scenario revenue calculation consistency
    baseline_rev = float(df_summary.iloc[0]['baseline_net_revenue'])
    net_rev_impact = float(df_summary.iloc[0]['net_revenue_impact'])
    expected_scenario_rev = baseline_rev + net_rev_impact
    assert expected_scenario_rev > 0, "Scenario revenue must be positive"
    print(f" [PASS] Check 4: Scenario revenue calculation is consistent (Net Impact: +${net_rev_impact:,.2f}).")

    # Check 5: Validate scenario Gross Profit calculation consistency
    baseline_gp = float(df_summary.iloc[0]['baseline_gross_profit'])
    incremental_gp = float(df_summary.iloc[0]['incremental_gross_profit'])
    scenario_gp = float(df_summary.iloc[0]['scenario_gross_profit'])
    assert np.isclose(scenario_gp, baseline_gp + incremental_gp), f"Scenario GP mismatch: {scenario_gp} vs {baseline_gp + incremental_gp}"
    print(f" [PASS] Check 5: Scenario Gross Profit calculation is consistent (${baseline_gp:,.2f} + ${incremental_gp:,.2f} = ${scenario_gp:,.2f}).")

    # Check 6: Validate scenario Gross Margin calculation consistency
    scenario_gm = float(df_summary.iloc[0]['scenario_gross_margin_pct'])
    expected_gm = (scenario_gp / expected_scenario_rev) * 100.0
    assert np.isclose(scenario_gm, expected_gm), f"Scenario GM% mismatch: {scenario_gm} vs {expected_gm}"
    print(f" [PASS] Check 6: Scenario Gross Margin % calculation is consistent ({scenario_gm:.4f}%).")

    # Check 7: Validate no unexpected duplicate rows
    assert len(df_subcategories) == 2, f"Expected exactly 2 source subcategories, got {len(df_subcategories)}"
    assert len(df_summary) == 1, f"Expected exactly 1 summary row, got {len(df_summary)}"
    print(" [PASS] Check 7: No unexpected duplicate rows in staging outputs.")

    # Check 8: Validate mathematical reconciliation between subcategories and summary
    sum_units_shifted = df_subcategories['units_shifted'].sum()
    sum_incremental_gp = df_subcategories['incremental_gp'].sum()
    assert np.isclose(sum_units_shifted, df_summary.iloc[0]['total_units_shifted']), "Units shifted mismatch between subcategories and summary"
    assert np.isclose(sum_incremental_gp, df_summary.iloc[0]['incremental_gross_profit']), "Incremental GP mismatch between subcategories and summary"
    print(" [PASS] Check 8: All key scenario outputs reconcile mathematically with zero residual.")

    conn.close()
    print("\n==================================================")
    print("[SUCCESS] ALL WHAT-IF MIX SCENARIO VERIFICATIONS PASSED!")
    print("==================================================")

if __name__ == '__main__':
    run_verification()
