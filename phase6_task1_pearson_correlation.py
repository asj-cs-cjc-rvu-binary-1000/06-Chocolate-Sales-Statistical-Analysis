import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)

clean = wb["Clean_Data"]
ws = wb["Correlation"]

# Identify the actual data ranges.
last_row = clean.max_row
quantity_range = f"Clean_Data!$F$2:$F${last_row}"
revenue_range = f"Clean_Data!$I$2:$I${last_row}"

# Create the Pearson correlation section.
ws["A3"] = "Pearson's Correlation Coefficient"
ws["A4"] = "Statistic"
ws["B4"] = "Value"
ws["A5"] = "Pearson's r"
ws["B5"] = f"=CORREL({quantity_range},{revenue_range})"

# Formatting.
title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
thin_gray = Side(style="thin", color="B7C9D6")

ws["A3"].font = Font(bold=True, color="FFFFFF", size=12)
ws["A3"].fill = title_fill

for cell in ws[4][:2]:
    cell.font = Font(bold=True)
    cell.fill = header_fill
    cell.border = Border(
        left=thin_gray, right=thin_gray,
        top=thin_gray, bottom=thin_gray
    )
    cell.alignment = Alignment(horizontal="center")

for cell in ws[5][:2]:
    cell.border = Border(
        left=thin_gray, right=thin_gray,
        top=thin_gray, bottom=thin_gray
    )

ws["B5"].number_format = "0.0000"
ws["A5"].font = Font(bold=True)
ws["B5"].font = Font(bold=True, color="008000")

ws.column_dimensions["A"].width = 38
ws.column_dimensions["B"].width = 18

wb.save(WORKBOOK)
wb.close()

print("=" * 70)
print("PHASE 6 - TASK 1: PEARSON CORRELATION FORMULA CREATED")
print("=" * 70)
print(f"Quantity range : {quantity_range}")
print(f"Revenue range  : {revenue_range}")
print("Formula cell   : Correlation!B5")
print(f"Excel formula  : =CORREL({quantity_range},{revenue_range})")
print("Workbook saved successfully.")
