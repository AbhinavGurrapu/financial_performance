path = r"C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw\DimProduct.csv"

cols = [
    'ProductKey', 'ProductAlternateKey', 'ProductSubcategoryKey', 'WeightUnitMeasureCode',
    'SizeUnitMeasureCode', 'EnglishProductName', 'SpanishProductName', 'FrenchProductName',
    'StandardCost', 'FinishedGoodsFlag', 'Color', 'SafetyStockLevel', 'ReorderPoint',
    'ListPrice', 'Size', 'SizeRange', 'Weight', 'DaysToManufacture', 'ProductLine',
    'DealerPrice', 'Class', 'Style', 'ModelName', 'LargePhoto', 'EnglishDescription',
    'FrenchDescription', 'ChineseDescription', 'ArabicDescription', 'HebrewDescription',
    'ThaiDescription', 'GermanDescription', 'JapaneseDescription', 'TurkishDescription',
    'StartDate', 'EndDate', 'Status'
]

col_nul_counts = {c: 0 for c in cols}

with open(path, "rb") as f:
    for line_idx, line in enumerate(f):
        parts = line.rstrip(b"\r\n").split(b"|")
        for c_idx, p in enumerate(parts):
            if b"\x00" in p:
                col_nul_counts[cols[c_idx]] += p.count(b"\x00")

for c, count in col_nul_counts.items():
    if count > 0:
        print(f"Column '{c}': {count} NUL bytes")
