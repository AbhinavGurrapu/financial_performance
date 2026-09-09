import os

raw_dir = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw"
staging_file = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\staging\DimProduct_sanitized.csv"

# Let's inspect each table and see which columns actually have empty strings (NULLs) in the CSVs
# and compare with what's defined as NOT NULL in create_tables.sql!

files = {
    'DimDate': (os.path.join(raw_dir, 'DimDate.csv'), 19),
    'DimProductCategory': (os.path.join(raw_dir, 'DimProductCategory.csv'), 5),
    'DimProductSubcategory': (os.path.join(raw_dir, 'DimProductSubcategory.csv'), 6),
    'DimProduct': (staging_file, 36),
    'DimReseller': (os.path.join(raw_dir, 'DimReseller.csv'), 20),
    'DimSalesTerritory': (os.path.join(raw_dir, 'DimSalesTerritory.csv'), 6),
    'FactResellerSales': (os.path.join(raw_dir, 'FactResellerSales.csv'), 27)
}

# Read create_tables.sql to get our NOT NULL columns
with open(r"C:\Users\dell\OneDrive\Desktop\financial_performance\sql\create_tables.sql", "r", encoding="utf-8") as f:
    sql = f.read()

import re

for t, (fpath, num_cols) in files.items():
    # find table in create_tables.sql
    m = re.search(r'CREATE TABLE \"' + t + r'\"\s*\((.*?)\);', sql, re.DOTALL | re.IGNORECASE)
    pg_cols = []
    if m:
        for l in m.group(1).split('\n'):
            l = l.strip().rstrip(',')
            if not l or l.startswith('--') or l.startswith('CONSTRAINT'): continue
            col_m = re.match(r'\"(.*?)\"\s+(.*)', l)
            if col_m:
                cname = col_m.group(1)
                is_nn = 'NOT NULL' in l.upper() or 'PRIMARY KEY' in l.upper()
                pg_cols.append((cname, is_nn))
    
    # Check CSV for empty fields
    col_empty_counts = [0] * num_cols
    total_rows = 0
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            total_rows += 1
            parts = line.rstrip('\r\n').split('|')
            for i, p in enumerate(parts):
                if p == '' or p == '\x00':
                    col_empty_counts[i] += 1
    
    print("=" * 65)
    print(f"TABLE: {t} (Total Rows: {total_rows}, Columns: {len(pg_cols)})")
    print("=" * 65)
    for i, (cname, is_nn) in enumerate(pg_cols):
        empty_cnt = col_empty_counts[i]
        if is_nn and empty_cnt > 0:
            print(f"  CRITICAL CONFLICT: Col {i+1:2d} \"{cname}\" is NOT NULL in PG, but has {empty_cnt} empty/NULL rows in CSV!")
        elif is_nn:
            print(f"  OK (NOT NULL):     Col {i+1:2d} \"{cname}\" has 0 empty rows.")
        elif empty_cnt > 0:
            print(f"  OK (NULLable):     Col {i+1:2d} \"{cname}\" has {empty_cnt} empty rows.")
        else:
            print(f"  OK (NULLable):     Col {i+1:2d} \"{cname}\" has 0 empty rows (all populated).")
