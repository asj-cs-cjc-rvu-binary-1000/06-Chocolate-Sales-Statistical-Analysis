import csv
import os
import re
from datetime import datetime, date

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.table import Table, TableStyleInfo

BASE = "/workspaces/06-Chocolate-Sales-Statistical-Analysis"
CSV_PATH = os.path.join(
    BASE, "data/processed/chocolate_sales_clean.csv"
)
XLSX_PATH = os.path.join(
    BASE, "excel/chocolate_sales_analysis.xlsx"
)

os.chdir(BASE)

# Columns that must remain text, even if they contain digits.
TEXT_COLUMNS = {
    "order_id", "product_id", "customer_id", "store_id"
}

def convert_value(header, value):
    if value is None or value == "":
        return None

    if header == "order_date":
        value = value.strip()
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(
                tzinfo=None
            )
        except ValueError:
            for fmt in (
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%m/%d/%Y",
                "%d/%m/%Y",
            ):
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    pass
            raise ValueError(f"Unrecognised order_date: {value}")

    if header in TEXT_COLUMNS:
        return value

    # Convert numeric-looking values to actual Excel numbers.
    cleaned = value.strip()
    if re.fullmatch(r"[-+]?\d+", cleaned):
        return int(cleaned)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\.\d+)", cleaned):
        return float(cleaned)

    return value


print("=" * 65)
print("PHASE 3 - TASK 2: IMPORT CLEANED DATASET")
print("=" * 65)

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(CSV_PATH)

if not os.path.exists(XLSX_PATH):
    raise FileNotFoundError(XLSX_PATH)

with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    records = list(reader)

if not headers:
    raise ValueError("The CSV file has no header row.")

if len(records) != 992:
    raise ValueError(
        f"Expected 992 records, found {len(records)}."
    )

wb = load_workbook(XLSX_PATH)
ws = wb["Clean_Data"]

# Clear existing contents and any old table definitions.
if ws.max_row:
    ws.delete_rows(1, ws.max_row)

for table_name in list(ws.tables.keys()):
    del ws.tables[table_name]

# Write column headings.
ws.append(headers)

for record in records:
    row = [
        convert_value(header, record.get(header))
        for header in headers
    ]
    ws.append(row)

# Header formatting.
for cell in ws[1]:
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(
        fill_type="solid", fgColor="1F4E78"
    )
    cell.alignment = Alignment(
        horizontal="center", vertical="center"
    )

ws.row_dimensions[1].height = 24
ws.freeze_panes = "A2"
ws.auto_filter.ref = ws.dimensions
ws.sheet_view.showGridLines = True

# Format dates, revenue, quantity, and other numeric columns.
for column_index, header in enumerate(headers, start=1):
    letter = ws.cell(row=1, column=column_index).column_letter

    if header == "order_date":
        for row_index in range(2, ws.max_row + 1):
            ws.cell(row_index, column_index).number_format = "dd-mmm-yyyy"

    elif header == "revenue":
        for row_index in range(2, ws.max_row + 1):
            ws.cell(row_index, column_index).number_format = '$#,##0.00'

    elif header == "quantity":
        for row_index in range(2, ws.max_row + 1):
            ws.cell(row_index, column_index).number_format = "0"

    # Set a readable width based on the column contents.
    max_length = len(str(header))
    for row_index in range(2, min(ws.max_row, 100) + 1):
        value = ws.cell(row_index, column_index).value
        if value is not None:
            max_length = max(max_length, len(str(value)))

    ws.column_dimensions[letter].width = min(max(max_length + 2, 12), 28)

# Add an Excel table so the imported data is easy to filter and sort.
last_column = ws.cell(1, len(headers)).column_letter
table_ref = f"A1:{last_column}{ws.max_row}"

table = Table(displayName="CleanSalesData", ref=table_ref)
table.tableStyleInfo = TableStyleInfo(
    name="TableStyleMedium2",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=False,
)
ws.add_table(table)

wb.save(XLSX_PATH)

# Reopen the saved workbook and verify the import.
check_wb = load_workbook(XLSX_PATH, data_only=False)
check_ws = check_wb["Clean_Data"]

print("Worksheet:", check_ws.title)
print("Imported columns:", check_ws.max_column)
print("Imported rows including header:", check_ws.max_row)
print("Imported data rows:", check_ws.max_row - 1)
print("CSV columns match worksheet:",
      [check_ws.cell(1, c).value
       for c in range(1, check_ws.max_column + 1)] == headers)
print("Excel table created:", "CleanSalesData" in check_ws.tables)

date_col = headers.index("order_date") + 1 if "order_date" in headers else None
revenue_col = headers.index("revenue") + 1 if "revenue" in headers else None
quantity_col = headers.index("quantity") + 1 if "quantity" in headers else None

if date_col:
    print("order_date stored as date:",
          isinstance(check_ws.cell(2, date_col).value, (datetime, date)))

if revenue_col:
    print("revenue stored as number:",
          isinstance(check_ws.cell(2, revenue_col).value, (int, float)))
    print("revenue number format:",
          check_ws.cell(2, revenue_col).number_format)

if quantity_col:
    print("quantity stored as number:",
          isinstance(check_ws.cell(2, quantity_col).value, (int, float)))
    print("quantity number format:",
          check_ws.cell(2, quantity_col).number_format)

assert check_ws.max_row == 993
assert check_ws.max_column == len(headers)
assert [check_ws.cell(1, c).value
        for c in range(1, check_ws.max_column + 1)] == headers
assert "CleanSalesData" in check_ws.tables
assert date_col and isinstance(
    check_ws.cell(2, date_col).value, (datetime, date)
)
assert revenue_col and isinstance(
    check_ws.cell(2, revenue_col).value, (int, float)
)
assert quantity_col and isinstance(
    check_ws.cell(2, quantity_col).value, (int, float)
)

print("\nALL DATA IMPORT CHECKS PASSED")