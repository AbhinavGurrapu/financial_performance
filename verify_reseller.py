import pandas as pd

try:
    df = pd.read_csv(r'C:\Users\dell\OneDrive\Desktop\project_3_financial_performance\data\raw\DimReseller.csv', sep='|', header=None, nrows=1)
    print("DimReseller cols:", len(df.columns))
    print(df.head())
except Exception as e:
    print('Error:', e)
