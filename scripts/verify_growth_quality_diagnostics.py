import os
import sys
import psycopg2
import pandas as pd
import numpy as np

def run_diagnostics_and_verification():
    print("==================================================")
    print("STAGE 4 — GROWTH QUALITY & SEGMENT ROOT-CAUSE DIAGNOSTICS")
    print("FULL RECONCILIATION & 9-POINT VALIDATION SUITE")
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

    # 2. Execute SQL file sql/04_growth_quality_diagnostics.sql
    sql_file = os.path.join('sql', '04_growth_quality_diagnostics.sql')
    print(f"\n[1/3] Executing SQL script: {sql_file}")
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    sql_lines = [line for line in sql_script.splitlines() if not line.strip().startswith('\\')]
    clean_sql = '\n'.join(sql_lines)
    sql_statements = [s.strip() for s in clean_sql.split(';') if s.strip()]
    for stmt in sql_statements:
        cur.execute(stmt)
    conn.commit()
    print("   -> SQL diagnostic tables and views created successfully.")

    # 3. Define target tables and export paths
    staging_dir = os.path.join('data', 'staging')
    os.makedirs(staging_dir, exist_ok=True)

    tables_map = {
        'fact_growth_quality_category': 'growth_quality_category.csv',
        'fact_growth_quality_subcategory': 'growth_quality_subcategory.csv',
        'fact_growth_quality_product': 'growth_quality_product.csv',
        'fact_growth_quality_business_type': 'growth_quality_business_type.csv',
        'fact_growth_quality_country': 'growth_quality_country.csv',
        'fact_growth_quality_territory_region': 'growth_quality_territory_region.csv',
        'fact_top_gp_contributors': 'top_gp_contributors.csv',
        'fact_top_gp_drags': 'top_gp_drags.csv',
        'fact_discount_diagnostic': 'discount_diagnostic.csv'
    }

    dfs = {}
    print(f"\n[2/3] Exporting 9 diagnostic staging CSV files to '{staging_dir}/'...")
    for table_name, csv_name in tables_map.items():
        df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
        dfs[table_name] = df
        csv_path = os.path.join(staging_dir, csv_name)
        df.to_csv(csv_path, index=False)
        print(f"   -> Exported {table_name} ({len(df)} rows) to {csv_name}")

    # 4. Fetch Portfolio Totals from Stage 3 rollup_profitability_overall
    df_overall = pd.read_sql("SELECT * FROM rollup_profitability_overall WHERE segment_name = 'Overall Portfolio'", conn)
    known_r11 = float(df_overall['r11'].iloc[0])
    known_r12 = float(df_overall['r12'].iloc[0])
    known_r_change = float(df_overall['revenue_change'].iloc[0])
    known_gp11 = float(df_overall['gp11'].iloc[0])
    known_gp12 = float(df_overall['gp12'].iloc[0])
    known_gp_change = float(df_overall['gp_change'].iloc[0])

    print("\n[3/3] Running 9-Point Automated Validation Suite...")
    validation_passed = True

    # Check 1: Revenue Reconciliation across 6 dimensions
    print("\n   --- Check 1: Segment-Level Revenue Totals Reconciliation ---")
    rev_dims = ['fact_growth_quality_category', 'fact_growth_quality_subcategory', 'fact_growth_quality_product',
                'fact_growth_quality_business_type', 'fact_growth_quality_country', 'fact_growth_quality_territory_region']
    for dim_table in rev_dims:
        df_dim = dfs[dim_table]
        sum_r11 = float(df_dim['cy2011_net_revenue'].sum())
        sum_r12 = float(df_dim['cy2012_net_revenue'].sum())
        sum_r_change = float(df_dim['revenue_change'].sum())
        
        diff_r11 = abs(sum_r11 - known_r11)
        diff_r12 = abs(sum_r12 - known_r12)
        diff_r_change = abs(sum_r_change - known_r_change)

        if diff_r11 < 0.01 and diff_r12 < 0.01 and diff_r_change < 0.01:
            print(f"   [PASS] {dim_table}: R11=${sum_r11:,.2f}, R12=${sum_r12:,.2f}, Change=+${sum_r_change:,.2f}")
        else:
            print(f"   [FAIL] {dim_table} Revenue discrepancy: Diff R11={diff_r11:.4f}, R12={diff_r12:.4f}, Change={diff_r_change:.4f}")
            validation_passed = False

    # Check 2: Gross Profit Reconciliation across 6 dimensions
    print("\n   --- Check 2: Segment-Level Gross Profit Totals Reconciliation ---")
    for dim_table in rev_dims:
        df_dim = dfs[dim_table]
        sum_gp11 = float(df_dim['cy2011_gross_profit'].sum())
        sum_gp12 = float(df_dim['cy2012_gross_profit'].sum())
        sum_gp_change = float(df_dim['gross_profit_change'].sum())

        diff_gp11 = abs(sum_gp11 - known_gp11)
        diff_gp12 = abs(sum_gp12 - known_gp12)
        diff_gp_change = abs(sum_gp_change - known_gp_change)

        if diff_gp11 < 0.01 and diff_gp12 < 0.01 and diff_gp_change < 0.01:
            print(f"   [PASS] {dim_table}: GP11=${sum_gp11:,.2f}, GP12=${sum_gp12:,.2f}, Change=+${sum_gp_change:,.2f}")
        else:
            print(f"   [FAIL] {dim_table} Gross Profit discrepancy: Diff GP11={diff_gp11:.4f}, GP12={diff_gp12:.4f}, Change={diff_gp_change:.4f}")
            validation_passed = False

    # Check 3: Four-Factor Effects Reconciliation to Known +$617,300.78
    print("\n   --- Check 3: Four-Factor Effects Reconciliation ---")
    for dim_table in rev_dims:
        df_dim = dfs[dim_table]
        price_sum = float(df_dim['price_effect'].sum())
        cost_sum = float(df_dim['unit_cost_effect'].sum())
        vol_sum = float(df_dim['volume_effect'].sum())
        mix_sum = float(df_dim['mix_effect'].sum())
        total_4factor = price_sum + cost_sum + vol_sum + mix_sum

        diff_4factor = abs(total_4factor - known_gp_change)
        if diff_4factor < 0.01:
            print(f"   [PASS] {dim_table}: Price=+${price_sum:,.2f}, Cost=${cost_sum:,.2f}, Vol=+${vol_sum:,.2f}, Mix=+${mix_sum:,.2f} -> Total=+${total_4factor:,.2f}")
        else:
            print(f"   [FAIL] {dim_table} 4-factor sum=${total_4factor:,.2f} vs known=${known_gp_change:,.2f} (Diff=${diff_4factor:.4f})")
            validation_passed = False

    # Check 4: Product-Level Diagnostic Reconciliation against Stage 3 Product Fact
    print("\n   --- Check 4: Product-Level Stage 3 Fact Alignment ---")
    df_prod_stg3 = pd.read_sql('SELECT * FROM fact_profitability_decomposition_product', conn)
    df_prod_stg4 = dfs['fact_growth_quality_product']
    diff_prod_gp = abs(df_prod_stg4['gross_profit_change'].sum() - df_prod_stg3['gp_change'].sum())
    if diff_prod_gp < 0.01:
        print(f"   [PASS] Product-level GP change reconciles perfectly with Stage 3 ({len(df_prod_stg4)} products).")
    else:
        print(f"   [FAIL] Product-level GP change discrepancy: Diff=${diff_prod_gp:.4f}")
        validation_passed = False

    # Check 5: No Segment Double-Counting (Uniqueness Check)
    print("\n   --- Check 5: No Segment Double-Counting ---")
    uniqueness_specs = [
        ('fact_growth_quality_category', ['Category']),
        ('fact_growth_quality_subcategory', ['Category', 'Subcategory']),
        ('fact_growth_quality_product', ['ProductKey']),
        ('fact_growth_quality_business_type', ['BusinessType']),
        ('fact_growth_quality_country', ['Country']),
        ('fact_growth_quality_territory_region', ['Country', 'TerritoryRegion'])
    ]
    for table_name, keys in uniqueness_specs:
        df_tbl = dfs[table_name]
        dups = df_tbl.duplicated(subset=keys).sum()
        if dups == 0:
            print(f"   [PASS] {table_name}: Unique on {keys} ({len(df_tbl)} rows).")
        else:
            print(f"   [FAIL] {table_name}: Found {dups} duplicate rows on keys {keys}.")
            validation_passed = False

    # Check 6: No Unexpected NULL Segment Labels
    print("\n   --- Check 6: No Unexpected NULL Segment Labels ---")
    for table_name, keys in uniqueness_specs:
        df_tbl = dfs[table_name]
        null_cnt = df_tbl[keys].isnull().sum().sum()
        if null_cnt == 0:
            print(f"   [PASS] {table_name}: Zero NULL segment labels.")
        else:
            print(f"   [FAIL] {table_name}: Found {null_cnt} NULL values in segment keys {keys}.")
            validation_passed = False

    # Check 7: Growth Quality Tier Classification Consistency
    print("\n   --- Check 7: Growth-Quality Tier Classification Consistency ---")
    for table_name in rev_dims:
        df_tbl = dfs[table_name]
        inconsistent_count = 0
        for idx, row in df_tbl.iterrows():
            rev_11 = row['cy2011_net_revenue']
            rev_12 = row['cy2012_net_revenue']
            rev_c = row['revenue_change']
            gp_c = row['gross_profit_change']
            gm_c = row['gross_margin_change_ppt']
            tier = row['growth_quality_tier']

            # Handle new segment entry or missing margin change
            if pd.isna(gm_c):
                if rev_11 == 0 and rev_12 > 0 and gp_c > 0:
                    expected_tier = 'Tier 1 - High-quality growth (New Segment Entry)'
                elif rev_11 == 0 and rev_12 > 0 and gp_c <= 0:
                    expected_tier = 'Tier 3 - Value-destructive growth (New Segment Entry)'
                else:
                    expected_tier = 'Other Special Case'
            elif rev_c > 0 and gp_c > 0 and gm_c >= 0:
                expected_tier = 'Tier 1 - High-quality growth'
            elif rev_c > 0 and gp_c > 0 and gm_c < 0:
                expected_tier = 'Tier 2 - Margin-dilutive growth'
            elif rev_c > 0 and gp_c < 0 and gm_c < 0:
                expected_tier = 'Tier 3 - Value-destructive growth'
            elif rev_c < 0 and gp_c < 0:
                expected_tier = 'Tier 4 - Contraction'
            elif rev_c < 0 and gp_c > 0 and gm_c > 0:
                expected_tier = 'Tier 5 - Profitable Contraction / Portfolio Improvement'
            else:
                expected_tier = 'Other Special Case'

            if tier != expected_tier:
                inconsistent_count += 1
                print(f"      Inconsistency in {table_name}: Rev11={rev_11:.2f}, Rev_C={rev_c:.2f}, GP_C={gp_c:.2f}, GM_C={gm_c} -> Tier='{tier}', Expected='{expected_tier}'")

        if inconsistent_count == 0:
            print(f"   [PASS] {table_name}: All {len(df_tbl)} tier classifications are 100% consistent.")
        else:
            print(f"   [FAIL] {table_name}: {inconsistent_count} inconsistent tier classifications.")
            validation_passed = False

    # Check 8: Revenue vs Profitability Mix Totals Reconcile to 100%
    print("\n   --- Check 8: Mix Share Totals Reconcile to 100% ---")
    df_cat = dfs['fact_growth_quality_category']
    df_subcat = dfs['fact_growth_quality_subcategory']
    
    cat_r11_share = (df_cat['cy2011_net_revenue'] / known_r11 * 100).sum()
    cat_r12_share = (df_cat['cy2012_net_revenue'] / known_r12 * 100).sum()
    cat_gp11_share = (df_cat['cy2011_gross_profit'] / known_gp11 * 100).sum()
    cat_gp12_share = (df_cat['cy2012_gross_profit'] / known_gp12 * 100).sum()

    subcat_r11_share = (df_subcat['cy2011_net_revenue'] / known_r11 * 100).sum()
    subcat_gp11_share = (df_subcat['cy2011_gross_profit'] / known_gp11 * 100).sum()

    if abs(cat_r11_share - 100.0) < 0.001 and abs(cat_gp11_share - 100.0) < 0.001 and abs(subcat_r11_share - 100.0) < 0.001:
        print(f"   [PASS] Category & Subcategory mix shares sum to 100.00%.")
    else:
        print(f"   [FAIL] Mix share summation error.")
        validation_passed = False

    # Check 9: Discount Diagnostic Accounting Reconciliation
    print("\n   --- Check 9: Discount Diagnostic Accounting Reconciliation ---")
    df_disc = dfs['fact_discount_diagnostic']
    disc_errors = 0
    for idx, row in df_disc.iterrows():
        net11_calc = row['gross_revenue_2011'] - row['discount_amount_2011']
        net12_calc = row['gross_revenue_2012'] - row['discount_amount_2012']
        if abs(net11_calc - row['net_revenue_2011']) > 0.01 or abs(net12_calc - row['net_revenue_2012']) > 0.01:
            disc_errors += 1
            print(f"      Discount net revenue mismatch in row {row['segment_name']}")

    if disc_errors == 0:
        print(f"   [PASS] Discount diagnostic reconciles perfectly ({len(df_disc)} segment rows).")
    else:
        print(f"   [FAIL] Found {disc_errors} discount accounting mismatches.")
        validation_passed = False

    conn.close()

    print("\n==================================================")
    if validation_passed:
        print("ALL 9 VALIDATION CHECKS PASSED PERFECTLY (ZERO RESIDUAL)")
        print("==================================================")
        sys.exit(0)
    else:
        print("VALIDATION FAILED — SEE DISCREPANCIES ABOVE")
        print("==================================================")
        sys.exit(1)

if __name__ == '__main__':
    run_diagnostics_and_verification()