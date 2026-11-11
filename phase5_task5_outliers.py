import os
import statistics
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)
data = wb["Clean_Data"]
desc = wb["Descriptive_Stats"]

# ---------------------------------------------------------
# 1. Calculate outlier statistics independently
# ---------------------------------------------------------

variables = {
    "Quantity": {"column": 6, "excel_column": "F"},
    "Revenue": {"column": 9, "excel_column": "I"}
}

results = {}

for name, info in variables.items():
    values = [
        float(data.cell(row, info["column"]).value)
        for row in range(2, data.max_row + 1)
    ]

    q1, _, q3 = statistics.quantiles(
        values, n=4, method="inclusive"
    )

    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    lower_count = sum(value < lower for value in values)
    upper_count = sum(value > upper for value in values)

    results[name] = {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower": lower,
        "upper": upper,
        "lower_count": lower_count,
        "upper_count": upper_count,
        "total": lower_count + upper_count
    }

# ---------------------------------------------------------
# 2. Locate actual quartile rows
# ---------------------------------------------------------

quartile_rows = {}

for row in range(1, desc.max_row + 1):
    label = desc.cell(row, 1).value

    if not isinstance(label, str):
        continue

    label = label.strip()

    if label.startswith("Q1 "):
        quartile_rows["Q1"] = row
    elif label.startswith("Q3 "):
        quartile_rows["Q3"] = row
    elif "Interquartile Range (IQR)" in label:
        quartile_rows["IQR"] = row

assert set(quartile_rows) == {"Q1", "Q3", "IQR"}, (
    f"Quartile rows not found: {quartile_rows}"
)

print("Located quartile rows:", quartile_rows)

# ---------------------------------------------------------
# 3. Create outlier summary table
# ---------------------------------------------------------

existing = [
    row for row in range(1, desc.max_row + 1)
    if desc.cell(row, 1).value ==
    "PHASE 5 - OUTLIER DETECTION USING 1.5 x IQR"
]

assert not existing, "Outlier table already exists. Inspect before rerunning."

title_row = desc.max_row + 3
header_row = title_row + 1
first_data_row = header_row + 1

desc.cell(title_row, 1).value = (
    "PHASE 5 - OUTLIER DETECTION USING 1.5 x IQR"
)

headers = [
    "Variable", "Q1", "Q3", "IQR",
    "Lower Fence", "Upper Fence",
    "Lower Outliers", "Upper Outliers",
    "Total Outliers"
]

thin = Side(style="thin", color="808080")

for col, header in enumerate(headers, start=1):
    cell = desc.cell(header_row, col)
    cell.value = header
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="4472C4")
    cell.alignment = Alignment(
        horizontal="center", vertical="center",
        wrap_text=True
    )
    cell.border = Border(
        left=thin, right=thin, top=thin, bottom=thin
    )

# ---------------------------------------------------------
# 4. Add formulas and results
# ---------------------------------------------------------

for index, (name, info) in enumerate(variables.items()):
    row = first_data_row + index
    source_col = info["excel_column"]

    desc.cell(row, 1).value = name

    # Link to existing Task 3 quartile calculations.
    for col, quartile in [
        (2, "Q1"), (3, "Q3"), (4, "IQR")
    ]:
        source_row = quartile_rows[quartile]
        source_letter = "B" if name == "Quantity" else "C"
        desc.cell(row, col).value = (
            f"={source_letter}{source_row}"
        )

    # Calculate fences.
    desc.cell(row, 5).value = f"=B{row}-1.5*D{row}"
    desc.cell(row, 6).value = f"=C{row}+1.5*D{row}"

    # Count observations outside fences.
    last_row = data.max_row

    desc.cell(row, 7).value = (
        f'=COUNTIF(Clean_Data!${source_col}$2:'
        f'${source_col}${last_row},"<"&E{row})'
    )

    desc.cell(row, 8).value = (
        f'=COUNTIF(Clean_Data!${source_col}$2:'
        f'${source_col}${last_row},">"&F{row})'
    )

    desc.cell(row, 9).value = f"=G{row}+H{row}"

    for col in range(1, 10):
        cell = desc.cell(row, col)
        cell.border = Border(
            left=thin, right=thin, top=thin, bottom=thin
        )
        cell.alignment = Alignment(
            horizontal="center", vertical="center"
        )

    for col in range(2, 7):
        desc.cell(row, col).number_format = "0.00"

    for col in range(7, 10):
        desc.cell(row, col).number_format = "0"

# ---------------------------------------------------------
# 5. Add interpretation
# ---------------------------------------------------------

interpretation_row = first_data_row + 4

desc.cell(
    interpretation_row, 1
).value = "OUTLIER INTERPRETATION"

desc.cell(
    interpretation_row, 1
).font = Font(bold=True, color="FFFFFF")

desc.cell(
    interpretation_row, 1
).fill = PatternFill("solid", fgColor="4472C4")

quantity_count = results["Quantity"]["total"]
revenue_count = results["Revenue"]["total"]

desc.cell(
    interpretation_row + 1, 1
).value = (
    f"Quantity: {quantity_count} potential outlier(s) "
    "were identified using the 1.5 x IQR rule."
)

desc.cell(
    interpretation_row + 2, 1
).value = (
    f"Revenue: {revenue_count} potential outlier(s) "
    "were identified using the 1.5 x IQR rule."
)

desc.cell(
    interpretation_row + 3, 1
).value = (
    "Potential outliers are observations outside the "
    "1.5 x IQR fences. They should be investigated, "
    "not automatically deleted, because extreme values "
    "may represent genuine transactions."
)

for row in range(interpretation_row + 1, interpretation_row + 4):
    desc.merge_cells(
        start_row=row, start_column=1,
        end_row=row, end_column=9
    )
    desc.cell(row, 1).alignment = Alignment(
        wrap_text=True, vertical="top"
    )

widths = {
    "A": 25, "B": 12, "C": 12, "D": 12,
    "E": 15, "F": 15, "G": 17, "H": 17, "I": 16
}

for column, width in widths.items():
    desc.column_dimensions[column].width = max(
        desc.column_dimensions[column].width or 0,
        width
    )

desc.row_dimensions[header_row].height = 34

# Recalculate formulas when opened in Excel/LibreOffice.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(WORKBOOK)

# ---------------------------------------------------------
# 6. Print independent results
# ---------------------------------------------------------

print("=" * 70)
print("PHASE 5 - TASK 5: OUTLIER DETECTION")
print("=" * 70)

for name, result in results.items():
    print(f"\n{name}")
    print(f"Q1: {result['q1']:.4f}")
    print(f"Q3: {result['q3']:.4f}")
    print(f"IQR: {result['iqr']:.4f}")
    print(f"Lower fence: {result['lower']:.4f}")
    print(f"Upper fence: {result['upper']:.4f}")
    print(f"Lower outliers: {result['lower_count']}")
    print(f"Upper outliers: {result['upper_count']}")
    print(f"Total outliers: {result['total']}")

print("\nOutlier summary table created.")
print("Worksheet: Descriptive_Stats")
print(f"Table title row: {title_row}")
print("STATUS: SUCCESS")
print("=" * 70)
