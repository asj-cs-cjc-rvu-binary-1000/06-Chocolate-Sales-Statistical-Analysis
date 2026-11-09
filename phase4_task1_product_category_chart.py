import os
from collections import Counter

import openpyxl
import matplotlib.pyplot as plt

from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font


# ============================================================
# PHASE 4 - TASK 1
# PRODUCT CATEGORY BAR CHART
# CORRECTED VERSION
# ============================================================

BASE_DIR = os.getcwd()

WORKBOOK_PATH = (
    "excel/chocolate_sales_analysis.xlsx"
)

PNG_PATH = (
    "charts/product_category_bar_chart.png"
)

EXPECTED_CATEGORIES = [
    "Dark",
    "Milk",
    "Praline",
    "Truffle",
    "White"
]

EXPECTED_TOTAL = 992

print("=" * 65)
print("PHASE 4 - TASK 1: PRODUCT CATEGORY BAR CHART")
print("=" * 65)


# ------------------------------------------------------------
# 1. CHECK REQUIRED FILES
# ------------------------------------------------------------

if not os.path.exists(WORKBOOK_PATH):
    raise FileNotFoundError(WORKBOOK_PATH)

os.makedirs("charts", exist_ok=True)


# ------------------------------------------------------------
# 2. LOAD WORKBOOK
# ------------------------------------------------------------

wb = openpyxl.load_workbook(WORKBOOK_PATH)

clean_ws = wb["Clean_Data"]
freq_ws = wb["Freq_Tables"]
chart_ws = wb["Charts"]

print("\nWorkbook loaded successfully.")


# ------------------------------------------------------------
# 3. READ CATEGORY DATA FROM CLEAN_DATA
# ------------------------------------------------------------

category_column = 14  # Column N

category_values = []

for row in range(2, clean_ws.max_row + 1):

    value = clean_ws.cell(
        row=row,
        column=category_column
    ).value

    if value is not None:
        category_values.append(str(value).strip())


if len(category_values) != EXPECTED_TOTAL:
    raise ValueError(
        f"Expected {EXPECTED_TOTAL} records, "
        f"found {len(category_values)}."
    )


# ------------------------------------------------------------
# 4. CALCULATE CATEGORY FREQUENCIES
# ------------------------------------------------------------

frequency_counts = Counter(category_values)

if set(frequency_counts.keys()) != set(EXPECTED_CATEGORIES):
    raise ValueError(
        "Unexpected category values found: "
        f"{frequency_counts}"
    )

categories = EXPECTED_CATEGORIES

frequencies = [
    frequency_counts[category]
    for category in categories
]

total_frequency = sum(frequencies)


# ------------------------------------------------------------
# 5. VERIFY FREQUENCY TABLE AGAINST PYTHON COUNTS
# ------------------------------------------------------------

print("\nCATEGORY FREQUENCY DISTRIBUTION")
print("-" * 65)

for category, frequency in zip(categories, frequencies):

    print(f"{category:<15} {frequency:>10}")

print("-" * 65)
print(f"{'Total':<15} {total_frequency:>10}")

if total_frequency != EXPECTED_TOTAL:
    raise ValueError("Total frequency verification failed.")


# ------------------------------------------------------------
# 6. VERIFY EXISTING EXCEL FREQUENCY TABLE
# ------------------------------------------------------------

for index, category in enumerate(categories, start=3):

    existing_category = freq_ws.cell(
        row=index,
        column=1
    ).value

    existing_formula = freq_ws.cell(
        row=index,
        column=2
    ).value

    if existing_category != category:
        raise ValueError(
            f"Unexpected category in A{index}: "
            f"{existing_category}"
        )

    if not (
        isinstance(existing_formula, str)
        and existing_formula.startswith("=")
    ):
        raise ValueError(
            f"B{index} does not contain a frequency formula."
        )

    print(
        f"Verified Freq_Tables!A{index}:B{index}"
    )


# ------------------------------------------------------------
# 7. CREATE EDITABLE EXCEL COLUMN CHART
# ------------------------------------------------------------

chart = BarChart()

chart.type = "col"
chart.style = 10

chart.title = (
    "Chocolate Sales by Product Category"
)

chart.x_axis.title = "Product Category"
chart.y_axis.title = "Number of Transactions"

chart.height = 10
chart.width = 19

chart.y_axis.scaling.min = 0

chart.legend = None

# Link directly to the existing frequency table.
# The chart remains editable in Microsoft Excel.

data = Reference(
    freq_ws,
    min_col=2,
    min_row=2,
    max_row=7
)

labels = Reference(
    freq_ws,
    min_col=1,
    min_row=3,
    max_row=7
)

chart.add_data(
    data,
    titles_from_data=True
)

chart.set_categories(labels)

chart.dataLabels = DataLabelList()
chart.dataLabels.showVal = True


# ------------------------------------------------------------
# 8. REMOVE PREVIOUS COPY OF THIS CHART
# ------------------------------------------------------------

chart_ws._charts = [
    existing_chart
    for existing_chart in chart_ws._charts
    if not (
        getattr(existing_chart.anchor, "_from", None)
        and existing_chart.anchor._from.col == 0
        and existing_chart.anchor._from.row == 0
    )
]


# ------------------------------------------------------------
# 9. INSERT CHART INTO CHARTS WORKSHEET
# ------------------------------------------------------------

chart_ws.add_chart(chart, "A1")

chart_ws["A20"] = "PHASE 4 - DATA VISUALISATION"

chart_ws["A20"].font = Font(
    bold=True,
    size=14
)


# ------------------------------------------------------------
# 10. ENABLE EXCEL FORMULA RECALCULATION
# ------------------------------------------------------------

wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"


# ------------------------------------------------------------
# 11. SAVE EXCEL WORKBOOK
# ------------------------------------------------------------

wb.save(WORKBOOK_PATH)

print("\nEditable Excel chart created successfully.")
print("Chart data source: Freq_Tables!A2:B7")
print("Chart destination: Charts!A1")


# ------------------------------------------------------------
# 12. CREATE PNG CHART
# ------------------------------------------------------------

plt.figure(figsize=(10, 6))

bars = plt.bar(
    categories,
    frequencies
)

plt.title(
    "Chocolate Sales by Product Category",
    fontsize=15,
    fontweight="bold"
)

plt.xlabel(
    "Product Category",
    fontsize=12
)

plt.ylabel(
    "Number of Transactions",
    fontsize=12
)

plt.grid(
    axis="y",
    linestyle="--",
    alpha=0.4
)

for bar, frequency in zip(bars, frequencies):

    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        str(frequency),
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    PNG_PATH,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# 13. FINAL OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("PHASE 4 - TASK 1 RESULTS")
print("=" * 65)

print("Total transactions:", total_frequency)

for category, frequency in zip(categories, frequencies):
    print(f"{category:<15}: {frequency}")

print("\nExcel workbook:", WORKBOOK_PATH)
print("PNG image:", PNG_PATH)

print("\nSTATUS: SUCCESS")

print("=" * 65)

