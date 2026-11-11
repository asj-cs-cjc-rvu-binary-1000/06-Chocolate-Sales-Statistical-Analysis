import os
import statistics
import math
import openpyxl

from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)
ws_data = wb["Clean_Data"]
ws_calc = wb["Calculations"]
ws_desc = wb["Descriptive_Stats"]

quantity = [
    float(ws_data.cell(row, 6).value)
    for row in range(2, 994)
]

revenue = [
    float(ws_data.cell(row, 9).value)
    for row in range(2, 994)
]

data = {
    "Quantity": quantity,
    "Revenue": revenue
}

results = {}

for variable, values in data.items():
    mean_value = statistics.mean(values)
    sd_value = statistics.stdev(values)
    cv_value = (sd_value / mean_value) * 100

    results[variable] = {
        "mean": mean_value,
        "sd": sd_value,
        "cv": cv_value
    }

print("=" * 70)
print("PHASE 5 - TASK 4: COEFFICIENT OF VARIATION")
print("=" * 70)

for variable, result in results.items():
    print(f"\n{variable}")
    print(f"Mean: {result['mean']:.4f}")
    print(f"Sample SD: {result['sd']:.4f}")
    print(f"CV: {result['cv']:.4f}%")

    assert result["mean"] > 0
    assert result["sd"] > 0
    assert result["cv"] > 0

# Identify the Calculations sheet CV rows.
print("\nEXISTING CALCULATIONS SHEET CV ENTRIES")

for row in range(1, ws_calc.max_row + 1):
    label = ws_calc.cell(row, 1).value

    if isinstance(label, str) and "coefficient" in label.lower():
        print(
            "Row:", row,
            "| Quantity:", ws_calc.cell(row, 2).value,
            "| Revenue:", ws_calc.cell(row, 3).value
        )

# Find the existing CV row, if present.
cv_rows = [
    row for row in range(1, ws_calc.max_row + 1)
    if isinstance(ws_calc.cell(row, 1).value, str)
    and "coefficient" in ws_calc.cell(row, 1).value.lower()
]

assert len(cv_rows) == 1, (
    "Expected exactly one existing CV row in Calculations."
)

cv_row = cv_rows[0]

# Insert formulas into the existing Calculations sheet.
ws_calc.cell(cv_row, 2, "=B2/B6*100")
ws_calc.cell(cv_row, 3, "=C2/C6*100")

ws_calc.cell(cv_row, 2).number_format = '0.00"%"'
ws_calc.cell(cv_row, 3).number_format = '0.00"%"'

# Add a CV summary table to Descriptive_Stats.
title = "PHASE 5 - COEFFICIENT OF VARIATION"

existing = [
    row for row in range(1, ws_desc.max_row + 1)
    if ws_desc.cell(row, 1).value == title
]

assert not existing, "CV table already exists."

start_row = ws_desc.max_row + 3

ws_desc.cell(start_row, 1, title)

headers = [
    "Measure",
    "Quantity",
    "Revenue",
    "Statistical Interpretation"
]

for col, heading in enumerate(headers, start=1):
    cell = ws_desc.cell(start_row + 1, col, heading)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E78")
    cell.alignment = Alignment(horizontal="center", wrap_text=True)

table = [
    (
        "Coefficient of Variation",
        f"=Calculations!B{cv_row}",
        f"=Calculations!C{cv_row}",
        "Standard deviation divided by mean, expressed as a percentage."
    )
]

for row_num, values in enumerate(table, start=start_row + 2):
    for col_num, value in enumerate(values, start=1):
        cell = ws_desc.cell(row_num, col_num, value)
        cell.alignment = Alignment(vertical="center", wrap_text=True)

    ws_desc.cell(row_num, 2).number_format = '0.00"%"'
    ws_desc.cell(row_num, 3).number_format = '0.00"%"'

interpretation_row = start_row + 5

lower_variable = min(
    results,
    key=lambda variable: results[variable]["cv"]
)

higher_variable = max(
    results,
    key=lambda variable: results[variable]["cv"]
)

ws_desc.cell(
    interpretation_row, 1, "INTERPRETATION"
)

ws_desc.cell(
    interpretation_row + 1, 1,
    (
        f"{lower_variable} has the lower CV "
        f"({results[lower_variable]['cv']:.2f}%), "
        f"while {higher_variable} has the higher CV "
        f"({results[higher_variable]['cv']:.2f}%). "
        f"Therefore, {lower_variable.lower()} is more consistent "
        "relative to its mean, whereas "
        f"{higher_variable.lower()} is relatively more variable."
    )
)

ws_desc.cell(interpretation_row, 1).font = Font(
    bold=True, color="FFFFFF"
)
ws_desc.cell(interpretation_row, 1).fill = PatternFill(
    "solid", fgColor="1F4E78"
)

ws_desc.merge_cells(
    start_row=interpretation_row + 1,
    start_column=1,
    end_row=interpretation_row + 1,
    end_column=4
)

ws_desc.cell(interpretation_row + 1, 1).alignment = Alignment(
    wrap_text=True, vertical="center"
)
ws_desc.row_dimensions[interpretation_row + 1].height = 45

widths = {1: 32, 2: 18, 3: 18, 4: 65}

for col, width in widths.items():
    letter = get_column_letter(col)
    current = ws_desc.column_dimensions[letter].width or 0
    ws_desc.column_dimensions[letter].width = max(current, width)

for row in ws_desc.iter_rows(
    min_row=start_row,
    max_row=interpretation_row + 1,
    min_col=1,
    max_col=4
):
    for cell in row:
        cell.border = Border(
            bottom=Side(style="thin", color="D9E2F3")
        )

wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(WORKBOOK)

print("\n" + "=" * 70)
print("CV FORMULAS AND SUMMARY TABLE CREATED")
print("Calculations worksheet CV row:", cv_row)
print("Descriptive_Stats table row:", start_row)
print("Workbook saved:", WORKBOOK)
print("STATUS: SUCCESS")
print("=" * 70)
