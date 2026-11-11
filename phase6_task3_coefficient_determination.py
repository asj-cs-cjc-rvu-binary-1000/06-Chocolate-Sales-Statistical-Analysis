import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)
ws = wb["Correlation"]
clean = wb["Clean_Data"]

last_row = clean.max_row

quantity_range = f"Clean_Data!$F$2:$F${last_row}"
revenue_range = f"Clean_Data!$I$2:$I${last_row}"

# Coefficient of determination section.
ws["A17"] = "Coefficient of Determination (R²)"
ws["A18"] = "Calculation Method"
ws["B18"] = "Result"
ws["A19"] = "Squared Pearson Correlation (r²)"
ws["B19"] = "=B5^2"
ws["A20"] = "Excel RSQ Function"
ws["B20"] = f"=RSQ({revenue_range},{quantity_range})"
ws["A21"] = "R² as Percentage"
ws["B21"] = "=B19*100"
ws["A22"] = "Unexplained Variation (%)"
ws["B22"] = "=100-B21"

interpretation = (
    "Approximately 55.13% of the variation in revenue can be "
    "explained by the linear relationship with quantity sold. "
    "The remaining approximately 44.87% is not explained by "
    "this simple linear model and may be associated with other "
    "factors such as unit price, discounts, product type, and "
    "other transaction characteristics."
)

ws["A24"] = "Interpretation"
ws["A25"] = interpretation

# Formatting.
title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
thin = Side(style="thin", color="B7C9D6")

ws["A17"].font = Font(bold=True, color="FFFFFF")
ws["A17"].fill = title_fill
ws["A24"].font = Font(bold=True, color="FFFFFF")
ws["A24"].fill = title_fill

for row in (18, 19, 20, 21, 22):
    for col in (1, 2):
        cell = ws.cell(row, col)
        cell.border = Border(
            left=thin, right=thin, top=thin, bottom=thin
        )
        if row == 18:
            cell.font = Font(bold=True)
            cell.fill = header_fill
        elif col == 1:
            cell.font = Font(bold=True)

for cell in ("B19", "B20"):
    ws[cell].number_format = "0.0000"

for cell in ("B21", "B22"):
    ws[cell].number_format = '0.00"%"'

ws.merge_cells("A25:F27")
ws["A25"].alignment = Alignment(
    wrap_text=True,
    vertical="top"
)
ws.row_dimensions[25].height = 42
ws.row_dimensions[26].height = 25
ws.row_dimensions[27].height = 25

wb.save(WORKBOOK)
wb.close()

print("=" * 70)
print("PHASE 6 - TASK 3: COEFFICIENT OF DETERMINATION CREATED")
print("=" * 70)
print(f"Quantity range: {quantity_range}")
print(f"Revenue range : {revenue_range}")
print("Squared correlation formula: =B5^2")
print(f"RSQ formula: =RSQ({revenue_range},{quantity_range})")
print("R² percentage formula: =B19*100")
print("Unexplained variation formula: =100-B21")
print("\nExpected R²: approximately 0.5513")
print("Expected explained variation: approximately 55.13%")
print("Expected unexplained variation: approximately 44.87%")
print("\nWorkbook saved successfully.")
