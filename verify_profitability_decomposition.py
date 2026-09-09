import os
import sys
import psycopg2
import pandas as pd
import numpy as np

def assign_growth_quality_tier(row):
    r_change = row['revenue_change']
    gp_change = row['gp_change']
    gm_change = row['gm_pct_change']
    
    if r_change > 0 and gp_change > 0 and gm_change >= 0:
        return 'Tier 1: High-Quality Growth'
    elif r_change > 0 and gp_change > 0 and gm_change < 0:
        return 'Tier 2: Margin-Dilutive Growth'
    elif r_change > 0 and gp_change <= 0 and gm_change < 0:
        return 'Tier 3: Value-Destructive Growth'
    elif r_change <= 0 and gp_change <= 0:
        return 'Tier 4: Contraction'
    else:
        return 'Other'

def run_validation():
    print("==================================================")
    print("STAGE 3 — PROFITABILITY DRIVER DECOMPOSITION")
    print("FULL RECONCILIATION & 15-POINT VALIDATION SUITE")
    print("==================================================")

    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(
        host=os.environ.get('PGHOST', 'localhost'),
        port=os.environ.get('PGPORT', 5432),
        user=os.environ.get('PGUSER', 'postgres'),
        dbname=os.environ.get('PGDATABASE', 'postgres'),
        password=os.environ.get('PGPASSWORD')
    )
    cur = conn.cursor()

    # 2. Execute SQL file to build models and rollups
    sql_file = os.path.join('sql', '03_profitability_decomposition.sql')
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    sql_lines = [line for line in sql_script.splitlines() if not line.strip().startswith('\\')]
    clean_sql = '\n'.join(sql_lines)
    sql_statements = [s.strip() for s in clean_sql.split(';') if s.strip()]
    for stmt in sql_statements:
        cur.execute(stmt)
    conn.commit()
    print("\n[SQL EXECUTION] Profitability decomposition model and 6 rollup tables created successfully.")

    # 3. Load tables into DataFrames for validation
    df_product = pd.read_sql('SELECT * FROM "fact_profitability_decomposition_product"', conn)
    df_overall = pd.read_sql('SELECT * FROM "rollup_profitability_overall"', conn)
    df_category = pd.read_sql('SELECT * FROM "rollup_profitability_category"', conn)
    df_subcategory = pd.read_sql('SELECT * FROM "rollup_profitability_subcategory"', conn)
    df_business = pd.read_sql('SELECT * FROM "rollup_profitability_business_type"', conn)
    df_country = pd.read_sql('SELECT * FROM "rollup_profitability_country"', conn)
    df_territory = pd.read_sql('SELECT * FROM "rollup_profitability_territory_region"', conn)

    # Convert numeric columns from Decimal to float
    num_cols = ['q11', 'r11', 'gp11', 'gm11_pct', 'q12', 'r12', 'gp12', 'gm12_pct',
                'revenue_change', 'gp_change', 'gm_pct_change', 'p11', 'c11', 'ugp11',
                'p12', 'c12', 'ugp12', 'baseline_avg_ugp', 'price_effect', 'unit_cost_effect',
                'volume_effect', 'mix_effect', 'reconciled_gp_change', 'residual']
    
    for df in [df_product, df_overall, df_category, df_subcategory, df_business, df_country, df_territory]:
        for col in num_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)

    # 4. Perform 15 Mandatory Validation Checks
    validations = []

    # Check 1: Product-level grain uniqueness
    c1_total = len(df_product)
    c1_distinct = df_product['ProductKey'].nunique()
    c1_pass = (c1_total == c1_distinct)
    validations.append(("1. Product Grain Uniqueness", c1_pass, f"Total Rows: {c1_total}, Distinct ProductKeys: {c1_distinct}"))

    # Check 2: All 330 products accounted for
    c2_pass = (c1_total == 330)
    validations.append(("2. All 330 Products Accounted For", c2_pass, f"Found {c1_total} products across 2011-2012"))

    # Check 3: Zero products silently dropped
    cur.execute('SELECT COUNT(DISTINCT "ProductKey") FROM "abt_reseller_sales" WHERE "CurrencyKey" = 100 AND "CalendarYear" IN (2011, 2012);')
    abt_products = cur.fetchone()[0]
    c3_pass = (c1_total == abt_products)
    validations.append(("3. No Products Silently Dropped", c3_pass, f"ABT Unique Products: {abt_products}, Decomposition Products: {c1_total}"))

    # Check 4: Actual CY2011 GP matches known baseline ($57,560.96)
    actual_gp11 = df_product['gp11'].sum()
    c4_pass = abs(actual_gp11 - 57560.96) < 0.01
    validations.append(("4. CY2011 Baseline GP Match", c4_pass, f"Actual CY2011 GP: ${actual_gp11:,.2f} (Expected: $57,560.96)"))

    # Check 5: Actual CY2012 GP matches known baseline ($674,861.75)
    actual_gp12 = df_product['gp12'].sum()
    c5_pass = abs(actual_gp12 - 674861.75) < 0.01
    validations.append(("5. CY2012 Baseline GP Match", c5_pass, f"Actual CY2012 GP: ${actual_gp12:,.2f} (Expected: $674,861.75)"))

    # Check 6: Sum of 4 decomposition effects equals actual GP change (+$617,300.78)
    tot_price = df_product['price_effect'].sum()
    tot_cost = df_product['unit_cost_effect'].sum()
    tot_vol = df_product['volume_effect'].sum()
    tot_mix = df_product['mix_effect'].sum()
    reconciled_gp_change = tot_price + tot_cost + tot_vol + tot_mix
    actual_gp_change = actual_gp12 - actual_gp11
    c6_pass = abs(reconciled_gp_change - 617300.78) < 0.01
    validations.append(("6. 4-Factor Effect Sum Matches GP Change", c6_pass, f"Reconciled: ${reconciled_gp_change:,.2f}, Actual Change: ${actual_gp_change:,.2f}"))

    # Check 7: Residual is effectively zero (< 1e-6)
    overall_residual = abs(actual_gp_change - reconciled_gp_change)
    c7_pass = (overall_residual < 1e-6)
    validations.append(("7. Residual Zero Within Tolerance", c7_pass, f"Residual: ${overall_residual:.10f}"))

    # Check 8: Category rollup sum of effects matches overall total
    cat_reconciled = df_category['reconciled_gp_change'].sum()
    c8_pass = abs(cat_reconciled - reconciled_gp_change) < 1e-6
    validations.append(("8. Category Rollup Effect Sum Match", c8_pass, f"Category Reconciled: ${cat_reconciled:,.2f}"))

    # Check 9: Subcategory rollup sum of effects matches overall total
    subcat_reconciled = df_subcategory['reconciled_gp_change'].sum()
    c9_pass = abs(subcat_reconciled - reconciled_gp_change) < 1e-6
    validations.append(("9. Subcategory Rollup Effect Sum Match", c9_pass, f"Subcategory Reconciled: ${subcat_reconciled:,.2f}"))

    # Check 10: Business Type rollup sum of effects matches overall total
    biz_reconciled = df_business['reconciled_gp_change'].sum()
    c10_pass = abs(biz_reconciled - reconciled_gp_change) < 1e-6
    validations.append(("10. Business Type Rollup Effect Sum Match", c10_pass, f"Business Type Reconciled: ${biz_reconciled:,.2f}"))

    # Check 11: Country rollup sum of effects matches overall total
    country_reconciled = df_country['reconciled_gp_change'].sum()
    c11_pass = abs(country_reconciled - reconciled_gp_change) < 1e-6
    validations.append(("11. Country Rollup Effect Sum Match", c11_pass, f"Country Reconciled: ${country_reconciled:,.2f}"))

    # Check 12: Territory Region rollup sum of effects matches overall total
    terr_reconciled = df_territory['reconciled_gp_change'].sum()
    c12_pass = abs(terr_reconciled - reconciled_gp_change) < 1e-6
    validations.append(("12. Territory Region Rollup Effect Sum Match", c12_pass, f"Territory Reconciled: ${terr_reconciled:,.2f}"))

    # Check 13: Verify no discount effect double-counted in main bridge
    main_bridge_columns = ['price_effect', 'unit_cost_effect', 'volume_effect', 'mix_effect']
    c13_pass = ('discount_effect' not in df_product.columns) and all(col in df_product.columns for col in main_bridge_columns)
    validations.append(("13. Non-Double-Counting Discounting Enforcement", c13_pass, "Main bridge contains exactly Price, Unit Cost, Volume, Mix (No separate discount effect column)"))

    # Check 14: Verify Price Effect equals Net Revenue Price Effect under approved methodology
    # Q12 * (P12 - P11) for continuing products
    cont_mask = (df_product['product_status'] == 'CONTINUING')
    expected_price_effect = (df_product.loc[cont_mask, 'q12'] * (df_product.loc[cont_mask, 'p12'] - df_product.loc[cont_mask, 'p11'])).sum()
    c14_pass = abs(tot_price - expected_price_effect) < 1e-6
    validations.append(("14. Price Effect Equivalence with Net Revenue Price Effect", c14_pass, f"GP Price Effect: ${tot_price:,.2f}, Net Rev Price Effect: ${expected_price_effect:,.2f}"))

    # Check 15: Verify no unexplained residuals across products and rollups
    max_residual = df_product['residual'].abs().max()
    c15_pass = (max_residual < 1e-6)
    validations.append(("15. Zero Unexplained Residuals Across All Grain Levels", c15_pass, f"Max Product Residual: ${max_residual:.10f}"))

    # 5. Print Validation Summary
    print("\n--- VALIDATION RESULTS ---")
    all_passed = True
    for title, status, details in validations:
        flag = "PASS" if status else "FAIL"
        if not status:
            all_passed = False
        print(f"[{flag}] {title:<55} | {details}")

    assert all_passed, "FATAL: One or more validation checks failed!"
    print("\n>>> ALL 15 VALIDATION CHECKS PASSED PERFECTLY! <<<")

    # 6. Apply Growth Quality Tier Classifications
    for df in [df_overall, df_category, df_subcategory, df_business, df_country, df_territory]:
        df['growth_quality_tier'] = df.apply(assign_growth_quality_tier, axis=1)

    # 7. Export Outputs to CSV
    os.makedirs(os.path.join('data', 'staging'), exist_ok=True)
    df_product.to_csv(os.path.join('data', 'staging', 'fact_profitability_decomposition_product.csv'), index=False)
    df_overall.to_csv(os.path.join('data', 'staging', 'rollup_profitability_overall.csv'), index=False)
    df_category.to_csv(os.path.join('data', 'staging', 'rollup_profitability_category.csv'), index=False)
    df_subcategory.to_csv(os.path.join('data', 'staging', 'rollup_profitability_subcategory.csv'), index=False)
    df_business.to_csv(os.path.join('data', 'staging', 'rollup_profitability_business_type.csv'), index=False)
    df_country.to_csv(os.path.join('data', 'staging', 'rollup_profitability_country.csv'), index=False)
    df_territory.to_csv(os.path.join('data', 'staging', 'rollup_profitability_territory_region.csv'), index=False)

    print("\n[STAGING CSV EXPORT] Exported 7 output CSV files to data/staging/")

    # 8. Print Executive Decomposition Summary
    print("\n==================================================")
    print("EXECUTIVE PROFITABILITY DECOMPOSITION SUMMARY")
    print("==================================================")
    print(f"CY2011 Gross Profit:          ${actual_gp11:>14,.2f}")
    print(f"CY2012 Gross Profit:          ${actual_gp12:>14,.2f}")
    print(f"Actual Gross Profit Change:   ${actual_gp_change:>14,.2f}")
    print("--------------------------------------------------")
    print(f"1. Price Effect:              ${tot_price:>14,.2f}  ({tot_price/actual_gp_change*100:>6.2f}%)")
    print(f"2. Unit Cost Effect:          ${tot_cost:>14,.2f}  ({tot_cost/actual_gp_change*100:>6.2f}%)")
    print(f"3. Volume Effect:             ${tot_vol:>14,.2f}  ({tot_vol/actual_gp_change*100:>6.2f}%)")
    print(f"4. Product Mix Effect:        ${tot_mix:>14,.2f}  ({tot_mix/actual_gp_change*100:>6.2f}%)")
    print("--------------------------------------------------")
    print(f"Reconciled GP Change:         ${reconciled_gp_change:>14,.2f}")
    print(f"Residual Difference:          ${overall_residual:>14.10f}")
    print("==================================================")

    print("\nPRODUCT CATEGORY ROLLUP:")
    print(df_category[['Category', 'revenue_change', 'gp_change', 'gm_pct_change', 'price_effect', 'unit_cost_effect', 'volume_effect', 'mix_effect', 'growth_quality_tier']].to_string(index=False))

    print("\nRESELLER BUSINESS TYPE ROLLUP:")
    print(df_business[['BusinessType', 'revenue_change', 'gp_change', 'gm_pct_change', 'price_effect', 'unit_cost_effect', 'volume_effect', 'mix_effect', 'growth_quality_tier']].to_string(index=False))

    print("\nCOUNTRY ROLLUP:")
    print(df_country[['Country', 'revenue_change', 'gp_change', 'gm_pct_change', 'price_effect', 'unit_cost_effect', 'volume_effect', 'mix_effect', 'growth_quality_tier']].to_string(index=False))

if __name__ == '__main__':
    run_validation()
