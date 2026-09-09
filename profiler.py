import pandas as pd
import os

base_dir = r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance"

# Load data
print("Loading data...")
df_date = pd.read_csv(os.path.join(base_dir, r"data\raw\DimDate.csv"), sep='|', header=None, names=[
    "DateKey", "FullDateAlternateKey", "DayNumberOfWeek", "EnglishDayNameOfWeek",
    "SpanishDayNameOfWeek", "FrenchDayNameOfWeek", "DayNumberOfMonth", "DayNumberOfYear",
    "WeekNumberOfYear", "EnglishMonthName", "SpanishMonthName", "FrenchMonthName",
    "MonthNumberOfYear", "CalendarQuarter", "CalendarYear", "CalendarSemester",
    "FiscalQuarter", "FiscalYear", "FiscalSemester"
])

df_prod_cat = pd.read_csv(os.path.join(base_dir, r"data\raw\DimProductCategory.csv"), sep='|', header=None, names=[
    "ProductCategoryKey", "ProductCategoryAlternateKey", "EnglishProductCategoryName",
    "SpanishProductCategoryName", "FrenchProductCategoryName"
])

df_prod_sub = pd.read_csv(os.path.join(base_dir, r"data\raw\DimProductSubcategory.csv"), sep='|', header=None, names=[
    "ProductSubcategoryKey", "ProductSubcategoryAlternateKey", "EnglishProductSubcategoryName",
    "SpanishProductSubcategoryName", "FrenchProductSubcategoryName", "ProductCategoryKey"
])

df_prod = pd.read_csv(os.path.join(base_dir, r"data\staging\DimProduct_sanitized.csv"), sep='|', header=None, names=[
    "ProductKey", "ProductAlternateKey", "ProductSubcategoryKey", "WeightUnitMeasureCode",
    "SizeUnitMeasureCode", "EnglishProductName", "SpanishProductName", "FrenchProductName",
    "StandardCost", "FinishedGoodsFlag", "Color", "SafetyStockLevel", "ReorderPoint",
    "ListPrice", "Size", "SizeRange", "Weight", "DaysToManufacture", "ProductLine",
    "DealerPrice", "Class", "Style", "ModelName", "LargePhoto", "EnglishDescription",
    "FrenchDescription", "ChineseDescription", "ArabicDescription", "HebrewDescription",
    "ThaiDescription", "GermanDescription", "JapaneseDescription", "TurkishDescription",
    "StartDate", "EndDate", "Status"
])

df_reseller = pd.read_csv(os.path.join(base_dir, r"data\raw\DimReseller.csv"), sep='|', header=None, names=[
    "ResellerKey", "GeographyKey", "ResellerAlternateKey", "Phone", "BusinessType",
    "ResellerName", "NumberEmployees", "OrderFrequency", "OrderMonth", "FirstOrderYear",
    "LastOrderYear", "ProductLine", "AddressLine1", "AddressLine2", "AnnualSales",
    "BankName", "MinPaymentType", "MinPaymentAmount", "AnnualRevenue", "YearOpened"
])

df_terr = pd.read_csv(os.path.join(base_dir, r"data\raw\DimSalesTerritory.csv"), sep='|', header=None, names=[
    "SalesTerritoryKey", "SalesTerritoryAlternateKey", "SalesTerritoryRegion",
    "SalesTerritoryCountry", "SalesTerritoryGroup", "SalesTerritoryImage"
])

df_fact = pd.read_csv(os.path.join(base_dir, r"data\raw\FactResellerSales.csv"), sep='|', header=None, names=[
    "ProductKey", "OrderDateKey", "DueDateKey", "ShipDateKey", "ResellerKey",
    "EmployeeKey", "PromotionKey", "CurrencyKey", "SalesTerritoryKey",
    "SalesOrderNumber", "SalesOrderLineNumber", "RevisionNumber", "OrderQuantity",
    "UnitPrice", "ExtendedAmount", "UnitPriceDiscountPct", "DiscountAmount",
    "ProductStandardCost", "TotalProductCost", "SalesAmount", "TaxAmt", "Freight",
    "CarrierTrackingNumber", "CustomerPONumber", "OrderDate", "DueDate", "ShipDate"
])

print("\n--- 4. Orphaned FK Values ---")
orphans_date = df_fact[~df_fact['OrderDateKey'].isin(df_date['DateKey'])]
print(f"Fact -> DimDate (OrderDateKey) Orphans: {len(orphans_date)}")

orphans_prod = df_fact[~df_fact['ProductKey'].isin(df_prod['ProductKey'])]
print(f"Fact -> DimProduct (ProductKey) Orphans: {len(orphans_prod)}")

orphans_res = df_fact[~df_fact['ResellerKey'].isin(df_reseller['ResellerKey'])]
print(f"Fact -> DimReseller (ResellerKey) Orphans: {len(orphans_res)}")

orphans_terr = df_fact[~df_fact['SalesTerritoryKey'].isin(df_terr['SalesTerritoryKey'])]
print(f"Fact -> DimSalesTerritory (SalesTerritoryKey) Orphans: {len(orphans_terr)}")

orphans_subcat = df_prod[~df_prod['ProductSubcategoryKey'].isin(df_prod_sub['ProductSubcategoryKey']) & df_prod['ProductSubcategoryKey'].notnull()]
print(f"DimProduct -> DimProductSubcategory (ProductSubcategoryKey) Orphans: {len(orphans_subcat)}")

orphans_cat = df_prod_sub[~df_prod_sub['ProductCategoryKey'].isin(df_prod_cat['ProductCategoryKey']) & df_prod_sub['ProductCategoryKey'].notnull()]
print(f"DimProductSubcategory -> DimProductCategory (ProductCategoryKey) Orphans: {len(orphans_cat)}")


print("\n--- 5. Fact Table Date Coverage ---")
df_fact['OrderDate'] = pd.to_datetime(df_fact['OrderDate'])
print(f"Min OrderDate: {df_fact['OrderDate'].min()}")
print(f"Max OrderDate: {df_fact['OrderDate'].max()}")
print(f"Min OrderDateKey: {df_fact['OrderDateKey'].min()}")
print(f"Max OrderDateKey: {df_fact['OrderDateKey'].max()}")


print("\n--- 6, 7, 8. Fact Table Year Summaries ---")
df_fact['CalendarYear'] = df_fact['OrderDate'].dt.year
df_fact['CalendarMonth'] = df_fact['OrderDate'].dt.month

yearly_stats = df_fact.groupby('CalendarYear').agg(
    distinct_dates=('OrderDate', 'nunique'),
    min_date=('OrderDate', 'min'),
    max_date=('OrderDate', 'max'),
    distinct_orders=('SalesOrderNumber', 'nunique'),
    units_sold=('OrderQuantity', 'sum'),
    sales_amount=('SalesAmount', 'sum'),
    distinct_months=('CalendarMonth', 'nunique')
).reset_index()

for idx, row in yearly_stats.iterrows():
    print(f"\nYear: {row['CalendarYear']}")
    print(f"Distinct Dates: {row['distinct_dates']}")
    print(f"Min Date: {row['min_date']}")
    print(f"Max Date: {row['max_date']}")
    print(f"Distinct Orders: {row['distinct_orders']}")
    print(f"Units Sold: {row['units_sold']}")
    print(f"Sales Amount: {row['sales_amount']}")
    print(f"Distinct Months: {row['distinct_months']}")


print("\n--- 10. Fact Table Grain (SalesOrderNumber + SalesOrderLineNumber) ---")
grain_check = df_fact.duplicated(subset=['SalesOrderNumber', 'SalesOrderLineNumber']).sum()
print(f"Duplicates on (SalesOrderNumber, SalesOrderLineNumber): {grain_check}")

print("\n--- 11. Fact Table Grain (SalesOrderNumber) ---")
order_check = df_fact.duplicated(subset=['SalesOrderNumber']).sum()
print(f"Duplicates on (SalesOrderNumber) only: {order_check}")
