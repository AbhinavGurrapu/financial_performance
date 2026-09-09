import os

csv_files = [
    'FactResellerSales.csv',
    'DimProduct.csv',
    'DimProductSubcategory.csv',
    'DimProductCategory.csv',
    'DimReseller.csv',
    'DimSalesTerritory.csv',
    'DimDate.csv'
]

raw_dir = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw"

for fname in csv_files:
    fpath = os.path.join(raw_dir, fname)
    with open(fpath, "rb") as f:
        content = f.read()
    nul_count = content.count(b"\x00")
    print(f"{fname:<28}: {len(content):>10} bytes, {nul_count:>6} NUL (0x00) bytes")
