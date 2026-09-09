import pandas as pd
import os

base_dir = r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance"

df_fact = pd.read_csv(os.path.join(base_dir, r"data\raw\FactResellerSales.csv"), sep='|', header=None, names=[
    "ProductKey", "OrderDateKey", "DueDateKey", "ShipDateKey", "ResellerKey",
    "EmployeeKey", "PromotionKey", "CurrencyKey", "SalesTerritoryKey",
    "SalesOrderNumber", "SalesOrderLineNumber", "RevisionNumber", "OrderQuantity",
    "UnitPrice", "ExtendedAmount", "UnitPriceDiscountPct", "DiscountAmount",
    "ProductStandardCost", "TotalProductCost", "SalesAmount", "TaxAmt", "Freight",
    "CarrierTrackingNumber", "CustomerPONumber", "OrderDate", "DueDate", "ShipDate"
])

df_date = pd.read_csv(os.path.join(base_dir, r"data\raw\DimDate.csv"), sep='|', header=None, names=[
    "DateKey", "FullDateAlternateKey", "DayNumberOfWeek", "EnglishDayNameOfWeek",
    "SpanishDayNameOfWeek", "FrenchDayNameOfWeek", "DayNumberOfMonth", "DayNumberOfYear",
    "WeekNumberOfYear", "EnglishMonthName", "SpanishMonthName", "FrenchMonthName",
    "MonthNumberOfYear", "CalendarQuarter", "CalendarYear", "CalendarSemester",
    "FiscalQuarter", "FiscalYear", "FiscalSemester"
])

df_fact['OrderDate'] = pd.to_datetime(df_fact['OrderDate'])
df_fact['Year'] = df_fact['OrderDate'].dt.year
df_fact['Month'] = df_fact['OrderDate'].dt.month

print("--- PART A ---")
for y in sorted(df_fact['Year'].unique()):
    months = sorted(df_fact[df_fact['Year'] == y]['Month'].unique())
    print(f"CY{y} Transaction Months: {months}")

print("\n--- CY2011 Detail ---")
y2011 = df_fact[df_fact['Year'] == 2011]
agg2011 = y2011.groupby('Month').agg(
    tx_dates=('OrderDate', 'nunique'),
    orders=('SalesOrderNumber', 'nunique'),
    fact_rows=('ProductKey', 'count'),
    units=('OrderQuantity', 'sum'),
    sales=('SalesAmount', 'sum')
).reset_index()
print(agg2011)

print("\n--- CY2012 Detail ---")
y2012 = df_fact[df_fact['Year'] == 2012]
agg2012 = y2012.groupby('Month').agg(
    tx_dates=('OrderDate', 'nunique'),
    orders=('SalesOrderNumber', 'nunique'),
    fact_rows=('ProductKey', 'count'),
    units=('OrderQuantity', 'sum'),
    sales=('SalesAmount', 'sum')
).reset_index()
print(agg2012)

print("\n--- DimDate Check ---")
print(f"Total rows in DimDate: {len(df_date)}")
print(f"Min Date: {df_date['FullDateAlternateKey'].min()}")
print(f"Max Date: {df_date['FullDateAlternateKey'].max()}")
# check if any date is missing between min and max
min_d = pd.to_datetime(df_date['FullDateAlternateKey'].min())
max_d = pd.to_datetime(df_date['FullDateAlternateKey'].max())
expected_days = (max_d - min_d).days + 1
print(f"Expected days: {expected_days}, Actual distinct dates: {df_date['FullDateAlternateKey'].nunique()}")


print("\n--- PART B ---")
print("Distinct CurrencyKeys in FactResellerSales:")
print(df_fact['CurrencyKey'].unique())

for ck in df_fact['CurrencyKey'].unique():
    subset = df_fact[df_fact['CurrencyKey'] == ck]
    print(f"\nCurrencyKey {ck}:")
    print(f"Fact rows: {len(subset)}")
    print(f"Distinct orders: {subset['SalesOrderNumber'].nunique()}")
    print(f"Units: {subset['OrderQuantity'].sum()}")
    print(f"SalesAmount: {subset['SalesAmount'].sum()}")
    print(f"Years represented: {sorted(subset['Year'].unique())}")
