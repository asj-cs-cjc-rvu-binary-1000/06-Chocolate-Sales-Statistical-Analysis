import os
import statistics
import openpyxl

from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)
ws_data = wb["Clean_Data"]
ws_desc = wb["Descriptive_Stats"]

quantity = [
    float(ws_data.cell(row, 6).value)
    for row in range(2, 994)
]

revenue = [
    float(ws_data.cell(row, 9).value)
    for row in range(2, 994)
]

assert len(quantity) == 992
assert len(revenue) == 992

data = {
    "Quantity": quantity,
    "Revenue": revenue
}

results = {}

for variable, values in data.items():
    sorted_values = sorted(values)

    q1 = statistics.quantiles(
        sorted_values, n=4, method="inclusive"
    )[0]

    q2 = statistics.median(sorted_values)

    q3 = statistics.quantiles(
        sorted_values, n=4, method="inclusive"
    )[2]

    results[variable] = {
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "iqr": q3 - q1
    }

print("=" * 70)
print("PHASE 5 - TASK 3: QUARTILES AND IQR")
print("=" * 70)

for variable, result in results.items():
    print(f"\n{variable}")
    print(f"Q1 (25th percentile): {result['q1']:.4f}")
    print(f"Q2 (50th percentile): {result['q2']:.4f}")
    print(f"Q3 (75th percentile): {result['q3']:.4f}")
    print(f"IQR: {result['iqr']:.4f}")

    assert result["q1"] < result["q2"] < result["q3"]
    assert result["iqr"] > 0

# Prevent duplicate insertion.
title = "PHASE 5 - MEASURES OF POSITION"

existing = [
    row for row in range(1, ws_desc.max_row + 1)
    if ws_desc.cell(row, 1).value == title
]

assert not existing, (
    "Quartile table already exists. Inspect before rerunning."
)

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

q_range = "Clean_Data!$F$2:$F$993"
r_range = "Clean_Data!$I$2:$I$993"

table = [
    (
        "Q1 (25th Percentile)",
        f"=QUARTILE.INC({q_range},1)",
        f"=QUARTILE.INC({r_range},1)",
        "Approximately 25% of observations are at or below Q1."
    ),
    (
        "Q2 (50th Percentile)",
        f"=QUARTILE.INC({q_range},2)",
        f"=QUARTILE.INC({r_range},2)",
        "Approximately 50% of observations are at or below Q2."
    ),
    (
        "Q3 (75th Percentile)",
        f"=QUARTILE.INC({q_range},3)",
        f"=QUARTILE.INC({r_range},3)",
        "Approximately 75% of observations are at or below Q3."
    ),
    (
        "Interquartile Range (IQR)",
        f"=B{start_row + 4}-B{start_row + 2}",
        f"=C{start_row + 4}-C{start_row + 2}",
        "Difference between Q3 and Q1; spread of the middle 50%."
    )
]

for row_num, values in enumerate(table, start=start_row + 2):
    for col_num, value in enumerate(values, start=1):
        cell = ws_desc.cell(row_num, col_num, value)
        cell.alignment = Alignment(vertical="center", wrap_text=True)

    ws_desc.cell(row_num, 2).number_format = "0.00"
    ws_desc.cell(row_num, 3).number_format = "0.00"

# Add variable-specific interpretation.
interpretation_row = start_row + 7

ws_desc.cell(interpretation_row, 1, "INTERPRETATION - QUANTITY")
ws_desc.cell(
    interpretation_row + 1, 1,
    (
        f"The middle 50% of quantity observations lie between "
        f"{results['Quantity']['q1']:.2f} and "
        f"{results['Quantity']['q3']:.2f}, giving an IQR of "
        f"{results['Quantity']['iqr']:.2f}."
    )
)

ws_desc.cell(interpretation_row + 3, 1, "INTERPRETATION - REVENUE")
ws_desc.cell(
    interpretation_row + 4, 1,
    (
        f"The middle 50% of revenue observations lie between "
        f"${results['Revenue']['q1']:.2f} and "
        f"${results['Revenue']['q3']:.2f}, giving an IQR of "
        f"${results['Revenue']['iqr']:.2f}."
    )
)

for row in (interpretation_row, interpretation_row + 3):
    cell = ws_desc.cell(row, 1)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E78")

for row in (interpretation_row + 1, interpretation_row + 4):
    ws_desc.merge_cells(
        start_row=row,
        start_column=1,
        end_row=row,
        end_column=4
    )
    ws_desc.cell(row, 1).alignment = Alignment(
        wrap_text=True, vertical="center"
    )
    ws_desc.row_dimensions[row].height = 35

widths = {1: 30, 2: 18, 3: 18, 4: 65}

for col, width in widths.items():
    letter = get_column_letter(col)
    current = ws_desc.column_dimensions[letter].width or 0
    ws_desc.column_dimensions[letter].width = max(current, width)

for row in ws_desc.iter_rows(
    min_row=start_row,
    max_row=interpretation_row + 4,
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
print("QUARTILE AND IQR TABLE CREATED")
print("Worksheet: Descriptive_Stats")
print("Table title row:", start_row)
print("Excel QUARTILE.INC formulas inserted.")
print("Workbook saved:", WORKBOOK)
print("STATUS: SUCCESS")
print("=" * 70)
