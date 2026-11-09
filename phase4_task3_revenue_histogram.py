import csv
import os
import math
import openpyxl
import matplotlib.pyplot as plt

WORKBOOK_PATH = "excel/chocolate_sales_analysis.xlsx"
DATA_PATH = "data/processed/chocolate_sales_clean.csv"
PNG_PATH = "charts/revenue_histogram.png"

BIN_EDGES = list(range(0, 81, 10))
EXPECTED_COUNTS = [179, 306, 194, 138, 99, 46, 22, 8]

print("=" * 65)
print("PHASE 4 - TASK 3: REVENUE HISTOGRAM")
print("=" * 65)

# ------------------------------------------------------------
# 1. Read revenue values from the cleaned CSV.
# ------------------------------------------------------------

with open(DATA_PATH, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    revenue_column = next(
        (
            name for name in reader.fieldnames
            if name.strip().lower() in ("revenue", "total_revenue")
        ),
        None
    )

    if revenue_column is None:
        raise ValueError(
            f"Could not identify the revenue column. "
            f"Available columns: {reader.fieldnames}"
        )

    revenues = []

    for row in reader:
        value = row[revenue_column].strip()
        if value:
            revenues.append(float(value))

assert len(revenues) == 992, (
    f"Expected 992 revenue values, found {len(revenues)}"
)

assert all(value >= 0 for value in revenues), (
    "Revenue contains negative values."
)

print(f"\nRevenue column: {revenue_column}")
print(f"Valid revenue observations: {len(revenues)}")
print(f"Minimum revenue: ${min(revenues):.2f}")
print(f"Maximum revenue: ${max(revenues):.2f}")

# ------------------------------------------------------------
# 2. Calculate grouped frequencies and verify existing table.
# Bins: 0-10, 10-20, ..., 70-80.
# ------------------------------------------------------------

frequencies = []

for index in range(len(BIN_EDGES) - 1):
    lower = BIN_EDGES[index]
    upper = BIN_EDGES[index + 1]

    if index == len(BIN_EDGES) - 2:
        count = sum(
            lower <= value <= upper
            for value in revenues
        )
    else:
        count = sum(
            lower <= value < upper
            for value in revenues
        )

    frequencies.append(count)

print("\nREVENUE GROUPED FREQUENCY DISTRIBUTION")
print("-" * 65)

for index, count in enumerate(frequencies):
    print(
        f"${BIN_EDGES[index]:.0f}-${BIN_EDGES[index + 1]:.0f}"
        f"{'':<12}{count:>5}"
    )

print("-" * 65)
print(f"{'Total':<20}{sum(frequencies):>5}")

assert frequencies == EXPECTED_COUNTS, (
    f"Frequency mismatch. Expected {EXPECTED_COUNTS}, "
    f"calculated {frequencies}"
)

assert sum(frequencies) == 992

# ------------------------------------------------------------
# 3. Load workbook and verify the existing frequency table.
# ------------------------------------------------------------

wb = openpyxl.load_workbook(
    WORKBOOK_PATH,
    data_only=False
)

assert "Clean_Data" in wb.sheetnames
assert "Freq_Tables" in wb.sheetnames
assert "Charts" in wb.sheetnames

freq_ws = wb["Freq_Tables"]
charts_ws = wb["Charts"]

for index, expected_count in enumerate(EXPECTED_COUNTS, start=3):
    label = freq_ws.cell(index, 9).value
    formula = freq_ws.cell(index, 10).value

    assert label is not None, (
        f"Missing revenue interval in Freq_Tables!I{index}"
    )

    assert isinstance(formula, str) and formula.startswith("="), (
        f"Missing frequency formula in Freq_Tables!J{index}"
    )

print("\nVerified existing revenue frequency table.")

# ------------------------------------------------------------
# 4. Create editable Excel column chart with zero gap.
# This represents a histogram using the grouped frequencies.
# ------------------------------------------------------------

from openpyxl.chart import BarChart, Reference

# Remove an earlier version of this chart if the script is rerun.
charts_ws._charts = [
    chart for chart in charts_ws._charts
    if not (
        chart.anchor._from.col == 0
        and chart.anchor._from.row == 19
    )
]

chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Distribution of Transaction Revenue"
chart.y_axis.title = "Frequency"
chart.x_axis.title = "Revenue ($)"
chart.height = 10
chart.width = 18
chart.gapWidth = 0

data = Reference(
    freq_ws,
    min_col=10,
    min_row=2,
    max_row=10
)

categories = Reference(
    freq_ws,
    min_col=9,
    min_row=3,
    max_row=10
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

charts_ws.add_chart(chart, "A20")

# Ensure Excel recalculates formulas when the workbook is opened.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(WORKBOOK_PATH)

print("\nEditable Excel histogram chart created.")
print("Chart data source: Freq_Tables!I2:J10")
print("Chart destination: Charts!A20")
print("Bar gap width: 0")

# ------------------------------------------------------------
# 5. Export a high-resolution PNG histogram.
# ------------------------------------------------------------

os.makedirs("charts", exist_ok=True)

plt.figure(figsize=(10, 6))

plt.hist(
    revenues,
    bins=BIN_EDGES,
    edgecolor="black",
    linewidth=1.2
)

plt.title("Distribution of Transaction Revenue")
plt.xlabel("Revenue ($)")
plt.ylabel("Frequency")
plt.xticks(BIN_EDGES)
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()
plt.savefig(
    PNG_PATH,
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("\nPNG histogram exported successfully.")
print(f"PNG image: {PNG_PATH}")

print("\n" + "=" * 65)
print("PHASE 4 - TASK 3 RESULTS")
print("=" * 65)
print(f"Total transactions: {len(revenues)}")
print(f"Revenue range: ${min(revenues):.2f} to ${max(revenues):.2f}")
print(f"Frequency total: {sum(frequencies)}")
print(f"Excel workbook: {WORKBOOK_PATH}")
print(f"PNG image: {PNG_PATH}")
print("\nSTATUS: SUCCESS")
print("=" * 65)
