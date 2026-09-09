import re

with open(r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\data\raw\instawdbdw.sql", "r", encoding="utf-8", errors="ignore") as f:
    sql_text = f.read()

with open(r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\sql\create_tables.sql", "r", encoding="utf-8", errors="ignore") as f:
    pg_text = f.read()

tables = ['DimDate', 'DimProductCategory', 'DimProductSubcategory', 'DimProduct', 'DimReseller', 'DimSalesTerritory', 'FactResellerSales']

def extract_cols_official(t):
    m = re.search(r'CREATE TABLE \[dbo\]\.\[\s*' + t + r'\s*\]\s*\((.*?)\)\s*(?:ON|ALTER|GO|WITH)', sql_text, re.DOTALL | re.IGNORECASE)
    if not m: return []
    cols = []
    for line in m.group(1).split('\n'):
        line = line.strip().rstrip(',')
        if not line or line.startswith('--'): continue
        col_m = re.match(r'\[(.*?)\]\s+(?:\[.*?\]|\w+)(?:\(.*?\))?(.*?)$', line)
        if col_m:
            col_name = col_m.group(1)
            rest = col_m.group(2)
            is_not_null = 'NOT NULL' in rest.upper()
            cols.append((col_name, is_not_null, line))
    return cols

def extract_cols_pg(t):
    m = re.search(r'CREATE TABLE \"' + t + r'\"\s*\((.*?)\);', pg_text, re.DOTALL | re.IGNORECASE)
    if not m: return []
    cols = []
    for line in m.group(1).split('\n'):
        line = line.strip().rstrip(',')
        if not line or line.startswith('--') or line.startswith('CONSTRAINT'): continue
        col_m = re.match(r'\"(.*?)\"\s+(.*)', line)
        if col_m:
            col_name = col_m.group(1)
            rest = col_m.group(2)
            is_not_null = 'NOT NULL' in rest.upper() or 'PRIMARY KEY' in rest.upper()
            cols.append((col_name, is_not_null, line))
    return cols

for t in tables:
    off = extract_cols_official(t)
    pg = extract_cols_pg(t)
    print("=" * 65)
    print(f"TABLE: {t}")
    print("=" * 65)
    off_dict = {c[0]: (c[1], c[2]) for c in off}
    pg_dict = {c[0]: (c[1], c[2]) for c in pg}
    
    mismatches = []
    for col, (off_nn, off_line) in off_dict.items():
        if col not in pg_dict:
            print(f"  MISSING IN PG: {col}")
            continue
        pg_nn, pg_line = pg_dict[col]
        if off_nn != pg_nn:
            mismatches.append((col, off_nn, pg_nn))
            print(f"  MISMATCH: {col:<28} | Official: {'NOT NULL' if off_nn else 'NULL'} ({off_line}) | PG: {'NOT NULL' if pg_nn else 'NULL'} ({pg_line})")
    if not mismatches:
        print("  All nullability constraints match perfectly!")
