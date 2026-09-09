import sys, os
base_dir = r'C:\Users\dell\OneDrive\Desktop\financial_performance'
files = [
    r'data\raw\DimDate.csv',
    r'data\raw\DimProductCategory.csv',
    r'data\raw\DimProductSubcategory.csv',
    r'data\staging\DimProduct_sanitized.csv',
    r'data\raw\DimReseller.csv',
    r'data\raw\DimSalesTerritory.csv',
    r'data\raw\FactResellerSales.csv'
]
chars = set()
for f in files:
    path = os.path.join(base_dir, f)
    with open(path, 'rb') as f_in:
        content = f_in.read()
        chars.update(content)

print(f'Quote (") present: {34 in chars}')
print(f'Backslash (\\) present: {92 in chars}')
print(f'Backtick (`) present: {96 in chars}')
print(f'Tilde (~) present: {126 in chars}')
print(f'Caret (^) present: {94 in chars}')
print(f'0x02 present: {2 in chars}')
print(f'0x01 present: {1 in chars}')
print(f'0x07 present: {7 in chars}')
