import csv
import os

base_dir = r"C:\Users\dell\OneDrive\Desktop\project_3_financial_performance"
raw_dir = os.path.join(base_dir, "data", "raw")
staging_dir = os.path.join(base_dir, "data", "staging")

tables = {
    "DimDate": {
        "file": os.path.join(raw_dir, "DimDate.csv"),
        "columns": [
            "DateKey", "FullDateAlternateKey", "DayNumberOfWeek", "EnglishDayNameOfWeek",
            "SpanishDayNameOfWeek", "FrenchDayNameOfWeek", "DayNumberOfMonth", "DayNumberOfYear",
            "WeekNumberOfYear", "EnglishMonthName", "SpanishMonthName", "FrenchMonthName",
            "MonthNumberOfYear", "CalendarQuarter", "CalendarYear", "CalendarSemester",
            "FiscalQuarter", "FiscalYear", "FiscalSemester"
        ]
    },
    "DimProductCategory": {
        "file": os.path.join(raw_dir, "DimProductCategory.csv"),
        "columns": [
            "ProductCategoryKey", "ProductCategoryAlternateKey", "EnglishProductCategoryName",
            "SpanishProductCategoryName", "FrenchProductCategoryName"
        ]
    },
    "DimProductSubcategory": {
        "file": os.path.join(raw_dir, "DimProductSubcategory.csv"),
        "columns": [
            "ProductSubcategoryKey", "ProductSubcategoryAlternateKey", "EnglishProductSubcategoryName",
            "SpanishProductSubcategoryName", "FrenchProductSubcategoryName", "ProductCategoryKey"
        ]
    },
    "DimProduct": {
        "file": os.path.join(staging_dir, "DimProduct_sanitized.csv"),
        "columns": [
            "ProductKey", "ProductAlternateKey", "ProductSubcategoryKey", "WeightUnitMeasureCode",
            "SizeUnitMeasureCode", "EnglishProductName", "SpanishProductName", "FrenchProductName",
            "StandardCost", "FinishedGoodsFlag", "Color", "SafetyStockLevel", "ReorderPoint",
            "ListPrice", "Size", "SizeRange", "Weight", "DaysToManufacture", "ProductLine",
            "DealerPrice", "Class", "Style", "ModelName", "LargePhoto", "EnglishDescription",
            "FrenchDescription", "ChineseDescription", "ArabicDescription", "HebrewDescription",
            "ThaiDescription", "GermanDescription", "JapaneseDescription", "TurkishDescription",
            "StartDate", "EndDate", "Status"
        ]
    },
    "DimReseller": {
        "file": os.path.join(raw_dir, "DimReseller.csv"),
        "columns": [
            "ResellerKey", "GeographyKey", "ResellerAlternateKey", "Phone", "BusinessType",
            "ResellerName", "NumberEmployees", "OrderFrequency", "OrderMonth", "FirstOrderYear",
            "LastOrderYear", "ProductLine", "AddressLine1", "AddressLine2", "AnnualSales",
            "BankName", "MinPaymentType", "MinPaymentAmount", "AnnualRevenue", "YearOpened"
        ]
    },
    "DimSalesTerritory": {
        "file": os.path.join(raw_dir, "DimSalesTerritory.csv"),
        "columns": [
            "SalesTerritoryKey", "SalesTerritoryAlternateKey", "SalesTerritoryRegion",
            "SalesTerritoryCountry", "SalesTerritoryGroup", "SalesTerritoryImage"
        ]
    },
    "FactResellerSales": {
        "file": os.path.join(raw_dir, "FactResellerSales.csv"),
        "columns": [
            "ProductKey", "OrderDateKey", "DueDateKey", "ShipDateKey", "ResellerKey",
            "EmployeeKey", "PromotionKey", "CurrencyKey", "SalesTerritoryKey",
            "SalesOrderNumber", "SalesOrderLineNumber", "RevisionNumber", "OrderQuantity",
            "UnitPrice", "ExtendedAmount", "UnitPriceDiscountPct", "DiscountAmount",
            "ProductStandardCost", "TotalProductCost", "SalesAmount", "TaxAmt", "Freight",
            "CarrierTrackingNumber", "CustomerPONumber", "OrderDate", "DueDate", "ShipDate"
        ]
    }
}

for table_name, table_info in tables.items():
    file_path = table_info["file"]
    expected_cols = len(table_info["columns"])
    print(f"\n--- Auditing {table_name} ---")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
        
    with open(file_path, "r", encoding="utf-8") as f:
        # In PostgreSQL COPY WITH (FORMAT csv), quotes are handled, but let's just do a basic split first to see
        # Alternatively use csv reader. We'll use csv reader.
        reader = csv.reader(f, delimiter="|")
        max_lengths = {i: 0 for i in range(expected_cols)}
        max_val = {i: "" for i in range(expected_cols)}
        row_count = 0
        malformed_lines = 0
        for line_num, row in enumerate(reader, 1):
            row_count += 1
            if len(row) != expected_cols:
                if malformed_lines < 5:
                    print(f"Line {line_num}: Expected {expected_cols} columns, got {len(row)}")
                malformed_lines += 1
            
            for i, val in enumerate(row):
                if i < expected_cols:
                    if len(val) > max_lengths[i]:
                        max_lengths[i] = len(val)
                        max_val[i] = val
                        
        print(f"Total Rows: {row_count}")
        if malformed_lines > 0:
            print(f"Malformed Lines: {malformed_lines}")
            
        print("Max String Lengths:")
        for i in range(expected_cols):
            if max_lengths[i] > 0:
                print(f"  {table_info['columns'][i]}: {max_lengths[i]}")
