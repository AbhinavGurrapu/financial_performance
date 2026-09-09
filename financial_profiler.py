import pandas as pd
import numpy as np
import os

base_dir = r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance"

# Load fact data
df_fact = pd.read_csv(os.path.join(base_dir, r"data\raw\FactResellerSales.csv"), sep='|', header=None, names=[
    "ProductKey", "OrderDateKey", "DueDateKey", "ShipDateKey", "ResellerKey",
    "EmployeeKey", "PromotionKey", "CurrencyKey", "SalesTerritoryKey",
    "SalesOrderNumber", "SalesOrderLineNumber", "RevisionNumber", "OrderQuantity",
    "UnitPrice", "ExtendedAmount", "UnitPriceDiscountPct", "DiscountAmount",
    "ProductStandardCost", "TotalProductCost", "SalesAmount", "TaxAmt", "Freight",
    "CarrierTrackingNumber", "CustomerPONumber", "OrderDate", "DueDate", "ShipDate"
])

# Load dimension data for product categories
df_prod = pd.read_csv(os.path.join(base_dir, r"data\staging\DimProduct_sanitized.csv"), sep='|', header=None, usecols=[0, 2], names=["ProductKey", "ProductSubcategoryKey"])
df_sub = pd.read_csv(os.path.join(base_dir, r"data\raw\DimProductSubcategory.csv"), sep='|', header=None, usecols=[0, 2, 5], names=["ProductSubcategoryKey", "SubcategoryName", "ProductCategoryKey"])
df_cat = pd.read_csv(os.path.join(base_dir, r"data\raw\DimProductCategory.csv"), sep='|', header=None, usecols=[0, 2], names=["ProductCategoryKey", "CategoryName"])

# Merge products
df_prod = df_prod.merge(df_sub, on="ProductSubcategoryKey", how="left").merge(df_cat, on="ProductCategoryKey", how="left")

# Process fact table
df_fact['OrderDate'] = pd.to_datetime(df_fact['OrderDate'])
df_fact['Year'] = df_fact['OrderDate'].dt.year

# 1. Financial Equation Validation (All rows)
print("=== 1. FINANCIAL EQUATION VALIDATION ===")
df_eq = df_fact.copy()
# ExtAmt = Qty * UnitPrice
diff1 = np.abs(df_eq['ExtendedAmount'] - (df_eq['OrderQuantity'] * df_eq['UnitPrice']))
# DiscAmt = ExtAmt * DiscountPct
diff2 = np.abs(df_eq['DiscountAmount'] - (df_eq['ExtendedAmount'] * df_eq['UnitPriceDiscountPct']))
# SalesAmt = ExtAmt - DiscAmt
diff3 = np.abs(df_eq['SalesAmount'] - (df_eq['ExtendedAmount'] - df_eq['DiscountAmount']))
# TotalCost = StdCost * Qty
diff4 = np.abs(df_eq['TotalProductCost'] - (df_eq['ProductStandardCost'] * df_eq['OrderQuantity']))

tol = 0.01  # tolerance for floating point rounding (cents)
for name, diff in [("ExtAmt = Qty*Price", diff1), ("DiscAmt = ExtAmt*Pct", diff2), 
                   ("SalesAmt = ExtAmt-DiscAmt", diff3), ("TotalCost = StdCost*Qty", diff4)]:
    mismatches = (diff > tol).sum()
    max_diff = diff.max()
    print(f"{name}: Tested={len(df_eq)}, Mismatches (>0.01)={mismatches}, Max Diff={max_diff:.6f}")


# Scope down to CurrencyKey = 100 and Years 2011, 2012
df_scope = df_fact[(df_fact['CurrencyKey'] == 100) & (df_fact['Year'].isin([2011, 2012]))].copy()
df_scope = df_scope.merge(df_prod, on="ProductKey", how="left")

# 2. Quantity / Price / Cost Quality
print("\n=== 2. QUANTITY / PRICE / COST QUALITY ===")
total_scope = len(df_scope)
print(f"Total rows in scope: {total_scope}")
for col in ['OrderQuantity', 'UnitPrice', 'ProductStandardCost', 'SalesAmount', 'TotalProductCost']:
    zeros = (df_scope[col] == 0).sum()
    negs = (df_scope[col] < 0).sum()
    print(f"{col}: Zeros={zeros} ({zeros/total_scope:.2%}), Negatives={negs} ({negs/total_scope:.2%})")

# 3. Discount Profile
print("\n=== 3. DISCOUNT PROFILE ===")
for yr in [2011, 2012]:
    dy = df_scope[df_scope['Year'] == yr]
    tot = len(dy)
    zero_disc = (dy['DiscountAmount'] == 0).sum()
    non_zero = tot - zero_disc
    pct_disc = non_zero / tot
    min_pct = dy[dy['DiscountAmount'] > 0]['UnitPriceDiscountPct'].min() if non_zero > 0 else 0
    max_pct = dy['UnitPriceDiscountPct'].max()
    avg_pct = dy['UnitPriceDiscountPct'].mean()
    wt_rate = dy['DiscountAmount'].sum() / dy['ExtendedAmount'].sum() if dy['ExtendedAmount'].sum() > 0 else 0
    
    print(f"\nYear {yr}:")
    print(f"Rows: {tot}, Zero Disc: {zero_disc}, Non-Zero: {non_zero} ({pct_disc:.2%})")
    print(f"Min Pct: {min_pct:.2%}, Max Pct: {max_pct:.2%}, Avg Pct: {avg_pct:.2%}, Wtd Rate: {wt_rate:.2%}")
    print(f"Common Discount Pcts:")
    print(dy['UnitPriceDiscountPct'].value_counts().head(5))

# Discount behavior by category/subcategory (both years together)
print("\nDiscount Behavior by Category/Subcategory (2011-2012 USD):")
disc_cat = df_scope.groupby(['CategoryName', 'SubcategoryName']).agg(
    Rows=('ProductKey', 'count'),
    DiscRows=('DiscountAmount', lambda x: (x > 0).sum()),
    WtdRate=('DiscountAmount', lambda x: x.sum() / df_scope.loc[x.index, 'ExtendedAmount'].sum())
).reset_index()
disc_cat['PctDiscounted'] = disc_cat['DiscRows'] / disc_cat['Rows']
print(disc_cat.to_string(index=False))

# 4. Product Mix Profile
print("\n=== 4. PRODUCT MIX PROFILE ===")
total_units = df_scope['OrderQuantity'].sum()
total_rev = df_scope['SalesAmount'].sum()

mix = df_scope.groupby(['CategoryName', 'SubcategoryName']).agg(
    units=('OrderQuantity', 'sum'),
    net_rev=('SalesAmount', 'sum'),
    cogs=('TotalProductCost', 'sum')
).reset_index()
mix['gp'] = mix['net_rev'] - mix['cogs']
mix['gm_pct'] = np.where(mix['net_rev'] > 0, mix['gp'] / mix['net_rev'], 0)
mix['unit_share'] = mix['units'] / total_units
mix['rev_share'] = mix['net_rev'] / total_rev
print(mix.to_string(index=False))

# 5. Baseline Financial Summary
print("\n=== 5. BASELINE FINANCIAL SUMMARY ===")
base = df_scope.groupby('Year').agg(
    ext_rev=('ExtendedAmount', 'sum'),
    disc_amt=('DiscountAmount', 'sum'),
    net_rev=('SalesAmount', 'sum'),
    cogs=('TotalProductCost', 'sum')
)
base['gp'] = base['net_rev'] - base['cogs']
base['gm_pct'] = base['gp'] / base['net_rev']

for yr in [2011, 2012]:
    print(f"\nCY{yr}:")
    print(f"Ext Rev: ${base.loc[yr, 'ext_rev']:,.2f}")
    print(f"Discount: ${base.loc[yr, 'disc_amt']:,.2f}")
    print(f"Net Rev: ${base.loc[yr, 'net_rev']:,.2f}")
    print(f"COGS: ${base.loc[yr, 'cogs']:,.2f}")
    print(f"GP: ${base.loc[yr, 'gp']:,.2f}")
    print(f"GM%: {base.loc[yr, 'gm_pct']:.2%}")

if 2011 in base.index and 2012 in base.index:
    yoy_rev = (base.loc[2012, 'net_rev'] - base.loc[2011, 'net_rev']) / base.loc[2011, 'net_rev']
    yoy_cogs = (base.loc[2012, 'cogs'] - base.loc[2011, 'cogs']) / base.loc[2011, 'cogs']
    yoy_gp = (base.loc[2012, 'gp'] - base.loc[2011, 'gp']) / base.loc[2011, 'gp']
    pt_gm = base.loc[2012, 'gm_pct'] - base.loc[2011, 'gm_pct']
    print("\nYoY Changes (2012 vs 2011):")
    print(f"Net Rev Change: {yoy_rev:.2%}")
    print(f"COGS Change: {yoy_cogs:.2%}")
    print(f"GP Change: {yoy_gp:.2%}")
    print(f"GM% Change: {pt_gm*100:.2f} pts")
