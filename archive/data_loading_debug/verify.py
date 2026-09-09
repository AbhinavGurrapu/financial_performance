import pandas as pd
import sys

columns = [
    'ProductKey', 'OrderDateKey', 'DueDateKey', 'ShipDateKey', 'ResellerKey', 
    'EmployeeKey', 'PromotionKey', 'CurrencyKey', 'SalesTerritoryKey', 
    'SalesOrderNumber', 'SalesOrderLineNumber', 'RevisionNumber', 
    'OrderQuantity', 'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 
    'DiscountAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount', 
    'TaxAmt', 'Freight', 'CarrierTrackingNumber', 'CustomerPONumber', 
    'OrderDate', 'DueDate', 'ShipDate'
]

try:
    df = pd.read_csv(r'C:\Users\dell\OneDrive\Desktop\financial_performance\data\raw\FactResellerSales.csv', sep='|', names=columns, nrows=5)
    print(df[['SalesOrderNumber', 'ProductKey', 'OrderQuantity', 'UnitPrice', 'ExtendedAmount', 'UnitPriceDiscountPct', 'DiscountAmount', 'ProductStandardCost', 'TotalProductCost', 'SalesAmount']])
except Exception as e:
    print('Error:', e)
