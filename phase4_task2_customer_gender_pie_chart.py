import os
from collections import Counter

import openpyxl
import matplotlib.pyplot as plt

from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Font


# ============================================================
# PHASE 4 - TASK 2
# CUSTOMER GENDER PIE CHART
# ============================================================

WORKBOOK_PATH = "excel/chocolate_sales_analysis.xlsx"

PNG_PATH = "charts/customer_segment_pie_chart.png"

EXPECTED_GENDERS = ["Female", "Male"]

EXPECTED_TOTAL = 992

print("=" * 65)
print("PHASE 4 - TASK 2: CUSTOMER GENDER PIE CHART")
print("=" * 65)


# ------------------------------------------------------------
# 1. CHECK FILES
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
# 3. READ GENDER DATA FROM CLEAN_DATA
# ------------------------------------------------------------

gender_column = 18  # Column R

gender_values = []

for row in range(2, clean_ws.max_row + 1):

    value = clean_ws.cell(
        row=row,
        column=gender_column
    ).value

    if value is not None:
        gender_values.append(str(value).strip())


if len(gender_values) != EXPECTED_TOTAL:
    raise ValueError(
        f"Expected {EXPECTED_TOTAL} records, "
        f"found {len(gender_values)}."
    )


# ------------------------------------------------------------
# 4. CALCULATE GENDER FREQUENCIES
# ------------------------------------------------------------

gender_counts = Counter(gender_values)

if set(gender_counts.keys()) != set(EXPECTED_GENDERS):
    raise ValueError(
        f"Unexpected gender values: {gender_counts}"
    )

genders = EXPECTED_GENDERS

frequencies = [
    gender_counts[gender]
    for gender in genders
]

total_frequency = sum(frequencies)

percentages = [
    (frequency / total_frequency) * 100
    for frequency in frequencies
]


# ------------------------------------------------------------
# 5. VERIFY FREQUENCY DISTRIBUTION
# ------------------------------------------------------------

print("\nCUSTOMER GENDER FREQUENCY DISTRIBUTION")
print("-" * 65)

for gender, frequency, percentage in zip(
    genders,
    frequencies,
    percentages
):

    print(
        f"{gender:<15} {frequency:>8} "
        f"({percentage:.2f}%)"
    )

print("-" * 65)
print(f"{'Total':<15} {total_frequency:>8} (100.00%)")


if total_frequency != EXPECTED_TOTAL:
    raise ValueError("Total frequency is incorrect.")


# ------------------------------------------------------------
# 6. VERIFY EXISTING FREQUENCY TABLE
# ------------------------------------------------------------

for row, gender in enumerate(genders, start=3):

    existing_gender = freq_ws.cell(row, 5).value
    existing_formula = freq_ws.cell(row, 6).value

    if existing_gender != gender:
        raise ValueError(
            f"Unexpected gender in E{row}: "
            f"{existing_gender}"
        )

    if not (
        isinstance(existing_formula, str)
        and existing_formula.startswith("=")
    ):
        raise ValueError(
            f"F{row} does not contain a frequency formula."
        )

    print(
        f"Verified Freq_Tables!E{row}:F{row}"
    )


# ------------------------------------------------------------
# 7. CREATE EDITABLE EXCEL PIE CHART
# ------------------------------------------------------------

chart = PieChart()

chart.title = "Customer Distribution by Gender"

chart.height = 10
chart.width = 14

chart.style = 10

# Link directly to the existing frequency table.

data = Reference(
    freq_ws,
    min_col=6,
    min_row=2,
    max_row=4
)

labels = Reference(
    freq_ws,
    min_col=5,
    min_row=3,
    max_row=4
)

chart.add_data(
    data,
    titles_from_data=True
)

chart.set_categories(labels)

# Display category names and percentages.

chart.dataLabels = DataLabelList()

chart.dataLabels.showPercent = True
chart.dataLabels.showCatName = True


# ------------------------------------------------------------
# 8. REMOVE PREVIOUS COPY OF THIS CHART
# ------------------------------------------------------------

chart_ws._charts = [
    existing_chart
    for existing_chart in chart_ws._charts
    if not (
        getattr(existing_chart.anchor, "_from", None)
        and existing_chart.anchor._from.col == 9
        and existing_chart.anchor._from.row == 0
    )
]


# ------------------------------------------------------------
# 9. INSERT PIE CHART INTO CHARTS WORKSHEET
# ------------------------------------------------------------

# Place beside the existing category chart.

chart_ws.add_chart(chart, "J1")

chart_ws["J20"] = "CUSTOMER GENDER DISTRIBUTION"

chart_ws["J20"].font = Font(
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
# 11. SAVE WORKBOOK
# ------------------------------------------------------------

wb.save(WORKBOOK_PATH)

print("\nEditable Excel pie chart created successfully.")

print("Chart data source: Freq_Tables!E2:F4")

print("Chart destination: Charts!J1")


# ------------------------------------------------------------
# 12. CREATE PNG PIE CHART
# ------------------------------------------------------------

plt.figure(figsize=(9, 7))

plt.pie(
    frequencies,
    labels=genders,
    autopct="%1.2f%%",
    startangle=90,
    counterclock=False,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    textprops={"fontsize": 11}
)

plt.title(
    "Customer Distribution by Gender",
    fontsize=15,
    fontweight="bold"
)

plt.axis("equal")

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
print("PHASE 4 - TASK 2 RESULTS")
print("=" * 65)

print("Total transactions:", total_frequency)

for gender, frequency, percentage in zip(
    genders,
    frequencies,
    percentages
):

    print(
        f"{gender:<15}: {frequency} "
        f"({percentage:.2f}%)"
    )

print("\nTotal percentage:", f"{sum(percentages):.2f}%")

print("\nExcel workbook:", WORKBOOK_PATH)

print("PNG image:", PNG_PATH)

print("\nSTATUS: SUCCESS")

print("=" * 65)

