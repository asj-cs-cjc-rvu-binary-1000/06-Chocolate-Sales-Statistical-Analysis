
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

from openpyxl.chart import BarChart, Reference

print("=" * 65)
print("PHASE 4 - TASK 4: REVENUE BOX-AND-WHISKER PLOT")
print("=" * 65)

csv_path = "data/processed/chocolate_sales_clean.csv"
workbook_path = "excel/chocolate_sales_analysis.xlsx"
png_path = "charts/revenue_boxplot.png"

os.makedirs("charts", exist_ok=True)

# ---------------------------------------------------------
# 1. Read revenue values.
# ---------------------------------------------------------

revenues = []

with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    if "revenue" not in reader.fieldnames:
        raise ValueError("Revenue column not found.")

    for row in reader:
        value = row["revenue"]

        if value and value.strip():
            revenues.append(float(value))

revenues = np.array(revenues)

if len(revenues) != 992:
    raise ValueError(
        f"Expected 992 observations, found {len(revenues)}."
    )

# ---------------------------------------------------------
# 2. Calculate five-number summary and IQR.
#    NumPy's linear percentile method matches QUARTILE.INC.
# ---------------------------------------------------------

minimum = float(np.min(revenues))
q1 = float(np.percentile(revenues, 25, method="linear"))
median = float(np.percentile(revenues, 50, method="linear"))
q3 = float(np.percentile(revenues, 75, method="linear"))
maximum = float(np.max(revenues))

iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

outliers = revenues[
    (revenues < lower_fence) |
    (revenues > upper_fence)
]

print("\nREVENUE FIVE-NUMBER SUMMARY")
print("-" * 65)
print(f"Minimum:             ${minimum:.2f}")
print(f"First quartile (Q1): ${q1:.2f}")
print(f"Median (Q2):         ${median:.2f}")
print(f"Third quartile (Q3): ${q3:.2f}")
print(f"Maximum:             ${maximum:.2f}")
print(f"Interquartile range: ${iqr:.2f}")
print(f"Lower outlier fence: ${lower_fence:.2f}")
print(f"Upper outlier fence: ${upper_fence:.2f}")
print(f"Number of outliers:  {len(outliers)}")

# ---------------------------------------------------------
# 3. Create an actual box-and-whisker plot using Matplotlib.
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

plt.boxplot(
    revenues,
    vert=True,
    patch_artist=True,
    showmeans=True,
    showfliers=True
)

plt.title("Box-and-Whisker Plot of Transaction Revenue")
plt.ylabel("Revenue ($)")
plt.xticks([1], ["Transaction Revenue"])
plt.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig(png_path, dpi=300, bbox_inches="tight")
plt.close()

print("\nBox-and-whisker plot exported successfully.")

# ---------------------------------------------------------
# 4. Save the five-number summary in the Excel workbook.
# ---------------------------------------------------------

wb = openpyxl.load_workbook(workbook_path)

if "Boxplot_Summary" in wb.sheetnames:
    del wb["Boxplot_Summary"]

summary_ws = wb.create_sheet("Boxplot_Summary")

summary_ws["A1"] = "Revenue Boxplot Statistical Summary"
summary_ws["A2"] = "Statistic"
summary_ws["B2"] = "Value"

summary_data = [
    ("Minimum", minimum),
    ("Q1", q1),
    ("Median", median),
    ("Q3", q3),
    ("Maximum", maximum),
    ("IQR", iqr),
    ("Lower Fence", lower_fence),
    ("Upper Fence", upper_fence),
    ("Outlier Count", int(len(outliers)))
]

for row, (label, value) in enumerate(summary_data, start=3):
    summary_ws.cell(row=row, column=1, value=label)
    summary_ws.cell(row=row, column=2, value=value)

    if label != "Outlier Count":
        summary_ws.cell(row=row, column=2).number_format = '$#,##0.00'

summary_ws.column_dimensions["A"].width = 25
summary_ws.column_dimensions["B"].width = 18

# ---------------------------------------------------------
# 5. Add an editable Excel five-number summary chart.
#    This is a supporting summary chart, not a native
#    Excel Box & Whisker chart.
# ---------------------------------------------------------

charts_ws = wb["Charts"]

# Remove an earlier summary chart at J20 if rerun.
charts_ws._charts = [
    chart for chart in charts_ws._charts
    if not (
        chart.anchor._from.col == 9
        and chart.anchor._from.row == 19
    )
]

chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "Revenue Five-Number Summary"
chart.x_axis.title = "Statistical Measure"
chart.y_axis.title = "Revenue ($)"
chart.height = 9
chart.width = 16
chart.legend = None

data = Reference(
    summary_ws,
    min_col=2,
    min_row=2,
    max_row=7
)

categories = Reference(
    summary_ws,
    min_col=1,
    min_row=3,
    max_row=7
)

chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)

charts_ws.add_chart(chart, "J20")

# Enable Excel recalculation.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(workbook_path)

print("\nExcel five-number summary saved.")
print("Summary sheet: Boxplot_Summary")
print("Supporting editable chart: Charts!J20")

print("\n" + "=" * 65)
print("PHASE 4 - TASK 4 RESULTS")
print("=" * 65)
print("Total revenue observations:", len(revenues))
print("IQR:", round(iqr, 2))
print("Number of potential outliers:", len(outliers))
print("Excel workbook:", workbook_path)
print("PNG image:", png_path)
print("\nSTATUS: SUCCESS")
print("=" * 65)