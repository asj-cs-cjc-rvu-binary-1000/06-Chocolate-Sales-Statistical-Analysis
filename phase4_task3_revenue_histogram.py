
import csv
import os
from collections import Counter

import matplotlib.pyplot as plt
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties

print("=" * 65)
print("PHASE 4 - TASK 3: REVENUE HISTOGRAM")
print("=" * 65)

csv_path = "data/processed/chocolate_sales_clean.csv"
workbook_path = "excel/chocolate_sales_analysis.xlsx"
png_path = "charts/revenue_histogram.png"

os.makedirs("charts", exist_ok=True)

# ---------------------------------------------------------
# 1. Read revenue values from the cleaned dataset.
# ---------------------------------------------------------

revenues = []

with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    if "revenue" not in reader.fieldnames:
        raise ValueError("Revenue column not found in cleaned dataset.")

    for row in reader:
        value = row["revenue"]

        if value is not None and value.strip() != "":
            revenues.append(float(value))

if len(revenues) != 992:
    raise ValueError(
        f"Expected 992 revenue values, found {len(revenues)}."
    )

if min(revenues) < 0:
    raise ValueError("Negative revenue values detected.")

print("\nREVENUE DATA")
print("-" * 65)
print("Number of transactions:", len(revenues))
print(f"Minimum revenue: ${min(revenues):.2f}")
print(f"Maximum revenue: ${max(revenues):.2f}")
print(f"Mean revenue: ${sum(revenues) / len(revenues):.2f}")

# ---------------------------------------------------------
# 2. Create grouped frequency distribution.
#    Class intervals: 0-10, 10-20, ..., 70-80.
# ---------------------------------------------------------

bins = list(range(0, 81, 10))
labels = [
    f"${bins[i]}-${bins[i + 1]}"
    for i in range(len(bins) - 1)
]

frequencies = [0] * (len(bins) - 1)

for revenue in revenues:
    for i in range(len(bins) - 1):
        if bins[i] <= revenue < bins[i + 1]:
            frequencies[i] += 1
            break
    else:
        if revenue == bins[-1]:
            frequencies[-1] += 1

if sum(frequencies) != len(revenues):
    raise ValueError(
        "Grouped frequencies do not add up to 992."
    )

print("\nGROUPED REVENUE FREQUENCY")
print("-" * 65)

for label, frequency in zip(labels, frequencies):
    print(f"{label:15s} {frequency:5d}")

print("-" * 65)
print(f"{'Total':15s} {sum(frequencies):5d}")

# ---------------------------------------------------------
# 3. Verify the existing workbook and frequency table.
# ---------------------------------------------------------

wb = openpyxl.load_workbook(workbook_path)
freq = wb["Freq_Tables"]
charts = wb["Charts"]

expected_intervals = [
    "0-10",
    "10-20",
    "20-30",
    "30-40",
    "40-50",
    "50-60",
    "60-70",
    "70-80"
]

for index, expected_label in enumerate(expected_intervals, start=3):

    actual_label = str(
        freq.cell(index, 9).value
    )

    # Normalize spaces, currency symbols and dash characters.
    actual_normalized = (
        actual_label
        .replace(" ", "")
        .replace("$", "")
        .replace("–", "-")
        .replace("—", "-")
    )

    expected_normalized = expected_label.replace(" ", "")

    if actual_normalized != expected_normalized:
        raise ValueError(
            f"Unexpected revenue interval at I{index}: "
            f"{actual_label}"
        )

# Check formulas are present.
for row in range(3, 11):
    formula = freq.cell(row, 10).value

    if not isinstance(formula, str) or not formula.startswith("="):
        raise ValueError(
            f"Missing frequency formula at J{row}."
        )

print("\nExisting revenue frequency table verified.")

# ---------------------------------------------------------
# 4. Add an editable Excel histogram-style column chart.
# ---------------------------------------------------------

# Remove an earlier chart at A20 if the script is rerun.
charts._charts = [
    chart for chart in charts._charts
    if not (
        chart.anchor._from.col == 0
        and chart.anchor._from.row == 19
    )
]

chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Distribution of Transaction Revenue"
chart.x_axis.title = "Revenue Class Interval ($)"
chart.y_axis.title = "Frequency"
chart.height = 10
chart.width = 20
chart.gapWidth = 0

data = Reference(
    freq,
    min_col=10,
    min_row=2,
    max_row=10
)

categories = Reference(
    freq,
    min_col=9,
    min_row=3,
    max_row=10
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

chart.legend = None
chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True

charts.add_chart(chart, "A20")

# Request automatic formula recalculation in Excel.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(workbook_path)

print("Editable Excel histogram-style chart created.")
print("Chart data source: Freq_Tables!I2:J10")
print("Chart destination: Charts!A20")

# ---------------------------------------------------------
# 5. Export a true histogram as a PNG image.
# ---------------------------------------------------------

plt.figure(figsize=(11, 6))

plt.hist(
    revenues,
    bins=bins,
    edgecolor="black",
    alpha=0.85
)

plt.title("Distribution of Transaction Revenue")
plt.xlabel("Revenue ($)")
plt.ylabel("Frequency")
plt.xticks(bins)
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.close()

print("\n" + "=" * 65)
print("PHASE 4 - TASK 3 RESULTS")
print("=" * 65)
print("Total transactions:", len(revenues))
print("Revenue histogram created.")
print("Excel workbook:", workbook_path)
print("PNG image:", png_path)
print("\nSTATUS: SUCCESS")
print("=" * 65)