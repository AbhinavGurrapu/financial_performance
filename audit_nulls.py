import re
import csv
import os

base_dir = r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance"

tables = {
    "DimDate": r"data\raw\DimDate.csv",
    "DimProductCategory": r"data\raw\DimProductCategory.csv",
    "DimProductSubcategory": r"data\raw\DimProductSubcategory.csv",
    "DimProduct": r"data\staging\DimProduct_sanitized.csv",
    "DimReseller": r"data\raw\DimReseller.csv",
    "DimSalesTerritory": r"data\raw\DimSalesTerritory.csv",
    "FactResellerSales": r"data\raw\FactResellerSales.csv"
}

with open(os.path.join(base_dir, "sql", "create_tables.sql"), "r", encoding="utf-8") as f:
    sql = f.read()

# Extract table definitions
table_defs = {}
for match in re.finditer(r'CREATE TABLE "([^"]+)" \((.*?)\);', sql, re.DOTALL):
    table_name = match.group(1)
    cols = []
    lines = match.group(2).split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('--') or line.startswith('CONSTRAINT'): continue
        
        m_col = re.match(r'"([^"]+)"\s+(.+)', line)
        if m_col:
            col_name = m_col.group(1)
            is_not_null = 'NOT NULL' in m_col.group(2).upper()
            if 'PRIMARY KEY' in m_col.group(2).upper() or 'REFERENCES' in m_col.group(2).upper():
                if 'NOT NULL' not in m_col.group(2).upper():
                    pass # PRIMARY KEY implies NOT NULL
            
            # just store if it has NOT NULL text
            cols.append({"name": col_name, "not_null": 'NOT NULL' in m_col.group(2).upper() or 'PRIMARY KEY' in m_col.group(2).upper()})

    table_defs[table_name] = cols

# Verify empty strings in NOT NULL columns
for tname, cols in table_defs.items():
    file_path = os.path.join(base_dir, tables[tname])
    not_null_indices = [i for i, c in enumerate(cols) if c["not_null"]]
    
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="|")
        for line_num, row in enumerate(reader, 1):
            if len(row) != len(cols): continue
            for i in not_null_indices:
                if row[i].strip() == "":
                    print(f"{tname} Line {line_num}: Column {cols[i]['name']} is NOT NULL but contains empty string!")

print("NOT NULL scan complete.")
