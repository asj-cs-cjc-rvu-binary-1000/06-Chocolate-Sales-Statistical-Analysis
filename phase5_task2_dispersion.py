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

# Read the cleaned observations independently for verification.
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

# Independent Python calculations.
results = {}

for variable, values in data.items():
    data_range = max(values) - min(values)
    sample_sd = statistics.stdev(values)
    sample_variance = statistics.variance(values)

    results[variable] = {
        "minimum": min(values),
        "maximum": max(values),
        "range": data_range,
        "standard_deviation": sample_sd,
        "variance": sample_variance
    }

print("=" * 70)
print("PHASE 5 - TASK 2: MEASURES OF DISPERSION")
print("=" * 70)

for variable, result in results.items():
    print(f"\n{variable}")
    print(f"Minimum: {result['minimum']:.4f}")
    print(f"Maximum: {result['maximum']:.4f}")
    print(f"Range: {result['range']:.4f}")
    print(
        f"Sample standard deviation: "
        f"{result['standard_deviation']:.4f}"
    )
    print(f"Sample variance: {result['variance']:.4f}")

    assert result["range"] > 0
    assert result["standard_deviation"] > 0
    assert result["standard_deviation"] < result["range"]

# Avoid accidentally creating duplicate tables.
title = "PHASE 5 - MEASURES OF DISPERSION"

existing = [
    row for row in range(1, ws_desc.max_row + 1)
    if ws_desc.cell(row, 1).value == title
]

assert not existing, (
    "Dispersion table already exists. Inspect the worksheet "
    "before running this script again."
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

# Source ranges.
q_range = "Clean_Data!$F$2:$F$993"
r_range = "Clean_Data!$I$2:$I$993"

# Rows: Range, Sample Standard Deviation, Sample Variance.
table = [
    (
        "Range",
        f"=MAX({q_range})-MIN({q_range})",
        f"=MAX({r_range})-MIN({r_range})",
        "Maximum minus minimum; measures the total span."
    ),
    (
        "Sample Standard Deviation",
        f"=STDEV.S({q_range})",
        f"=STDEV.S({r_range})",
        "Typical spread of observations around the mean."
    ),
    (
        "Sample Variance",
        f"=B{start_row + 3}^2",
        f"=C{start_row + 3}^2",
        "Square of the sample standard deviation."
    )
]

for row_num, values in enumerate(table, start=start_row + 2):
    for col_num, value in enumerate(values, start=1):
        cell = ws_desc.cell(row_num, col_num, value)
        cell.alignment = Alignment(vertical="center", wrap_text=True)

    ws_desc.cell(row_num, 2).number_format = "0.00"
    ws_desc.cell(row_num, 3).number_format = "0.00"

# Add interpretations for each variable.
interpretation_row = start_row + 6

ws_desc.cell(interpretation_row, 1, "INTERPRETATION - QUANTITY")
ws_desc.cell(
    interpretation_row + 1, 1,
    (
        f"Quantity has a range of {results['Quantity']['range']:.2f} "
        f"and a sample standard deviation of "
        f"{results['Quantity']['standard_deviation']:.2f}. "
        "The standard deviation is smaller than the range, indicating "
        "that observations are spread around the mean within a "
        "four-unit overall span."
    )
)

ws_desc.cell(interpretation_row + 3, 1, "INTERPRETATION - REVENUE")
ws_desc.cell(
    interpretation_row + 4, 1,
    (
        f"Revenue has a range of ${results['Revenue']['range']:.2f} "
        f"and a sample standard deviation of "
        f"${results['Revenue']['standard_deviation']:.2f}. "
        "The standard deviation indicates considerable variation "
        "in transaction revenue."
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
    ws_desc.row_dimensions[row].height = 42

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

# Ask Excel to recalculate formulas when the workbook is opened.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(WORKBOOK)

print("\n" + "=" * 70)
print("DISPERSION TABLE CREATED")
print("Worksheet: Descriptive_Stats")
print("Table title row:", start_row)
print("Excel formulas inserted.")
print("Independent Python calculations completed.")
print("Workbook saved:", WORKBOOK)
print("STATUS: SUCCESS")
print("=" * 70)
