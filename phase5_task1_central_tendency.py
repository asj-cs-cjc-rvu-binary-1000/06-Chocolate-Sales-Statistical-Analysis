import os
import statistics
from collections import Counter

import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils import get_column_letter

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)

# Correct worksheet name confirmed from workbook inspection.
ws_data = wb["Clean_Data"]
ws_calc = wb["Calculations"]
ws_desc = wb["Descriptive_Stats"]

# Read cleaned observations.
quantity = []
revenue = []

for row in ws_data.iter_rows(min_row=2, values_only=True):
    if row[5] is not None and row[8] is not None:
        quantity.append(float(row[5]))
        revenue.append(float(row[8]))

assert len(quantity) == 992, f"Quantity count: {len(quantity)}"
assert len(revenue) == 992, f"Revenue count: {len(revenue)}"

def calculate_stats(values):
    counts = Counter(values)
    highest_frequency = max(counts.values())
    modes = sorted(
        value for value, count in counts.items()
        if count == highest_frequency
    )

    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "mode": modes[0],
        "mode_frequency": highest_frequency,
        "number_of_modes": len(modes)
    }

results = {
    "Quantity": calculate_stats(quantity),
    "Revenue": calculate_stats(revenue)
}

print("=" * 70)
print("PHASE 5 - TASK 1: CENTRAL TENDENCY")
print("=" * 70)

for variable, result in results.items():
    print(f"\n{variable}")
    print(f"Mean: {result['mean']:.4f}")
    print(f"Median: {result['median']:.4f}")
    print(f"Mode: {result['mode']:.4f}")
    print(f"Mode frequency: {result['mode_frequency']}")
    print(f"Number of modes: {result['number_of_modes']}")

# Display existing Calculations sheet entries for comparison.
print("\n" + "-" * 70)
print("EXISTING CALCULATIONS SHEET")
print("-" * 70)

for row in range(1, ws_calc.max_row + 1):
    label = ws_calc.cell(row, 1).value
    if isinstance(label, str) and label.strip().lower() in (
        "mean", "median", "mode"
    ):
        print(
            label,
            "| Quantity:", ws_calc.cell(row, 2).value,
            "| Revenue:", ws_calc.cell(row, 3).value
        )

# Append a new central tendency table.
start_row = ws_desc.max_row + 3

ws_desc.cell(
    start_row, 1, "PHASE 5 - MEASURES OF CENTRAL TENDENCY"
)

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

table_rows = [
    ("Mean", "mean", "Arithmetic average of the observations."),
    ("Median", "median", "Middle value after arranging observations in order."),
    ("Mode", "mode", "Most frequently occurring value.")
]

for row_num, (label, key, explanation) in enumerate(
    table_rows, start=start_row + 2
):
    ws_desc.cell(row_num, 1, label)
    ws_desc.cell(row_num, 2, results["Quantity"][key])
    ws_desc.cell(row_num, 3, results["Revenue"][key])
    ws_desc.cell(row_num, 4, explanation)

    ws_desc.cell(row_num, 2).number_format = "0.00"
    ws_desc.cell(row_num, 3).number_format = "0.00"

# Add interpretations based on the calculated results.
interpretation_row = start_row + 6

ws_desc.cell(interpretation_row, 1, "INTERPRETATION - QUANTITY")
ws_desc.cell(
    interpretation_row + 1, 1,
    (
        f"Quantity has a mean of {results['Quantity']['mean']:.2f} "
        f"and a median of {results['Quantity']['median']:.2f}. "
        "These values are close, suggesting no substantial skewness "
        "based on the mean-median comparison alone."
    )
)

ws_desc.cell(interpretation_row + 3, 1, "INTERPRETATION - REVENUE")
ws_desc.cell(
    interpretation_row + 4, 1,
    (
        f"Revenue has a mean of {results['Revenue']['mean']:.2f} "
        f"and a median of {results['Revenue']['median']:.2f}. "
        "The mean is higher than the median, suggesting a right-skewed "
        "distribution in which relatively high revenue transactions "
        "pull the average upward."
    )
)

for row in (interpretation_row, interpretation_row + 3):
    cell = ws_desc.cell(row, 1)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor="1F4E78")

for row in (interpretation_row + 1, interpretation_row + 4):
    ws_desc.merge_cells(
        start_row=row, start_column=1,
        end_row=row, end_column=4
    )
    ws_desc.cell(row, 1).alignment = Alignment(
        wrap_text=True, vertical="center"
    )
    ws_desc.row_dimensions[row].height = 38

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

ws_desc.freeze_panes = "A2"

wb.save(WORKBOOK)

print("\n" + "=" * 70)
print("CENTRAL TENDENCY TABLE CREATED")
print("Worksheet: Descriptive_Stats")
print("Observations:", len(quantity))
print("Table title row:", start_row)
print("Workbook saved:", WORKBOOK)
print("STATUS: SUCCESS")
print("=" * 70)
