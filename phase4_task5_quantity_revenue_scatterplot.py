
import csv
import os
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

from openpyxl.chart import ScatterChart, Reference, Series
from openpyxl.chart.trendline import Trendline

print("=" * 65)
print("PHASE 4 - TASK 5: QUANTITY VS REVENUE SCATTERPLOT")
print("=" * 65)

csv_path = "data/processed/chocolate_sales_clean.csv"
workbook_path = "excel/chocolate_sales_analysis.xlsx"
png_path = "charts/quantity_vs_revenue_scatterplot.png"

os.makedirs("charts", exist_ok=True)

# ---------------------------------------------------------
# 1. Read source data.
# ---------------------------------------------------------

quantities = []
revenues = []

with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    required = {"quantity", "revenue"}

    if not required.issubset(reader.fieldnames):
        raise ValueError("Quantity or revenue column missing.")

    for row in reader:
        quantities.append(float(row["quantity"]))
        revenues.append(float(row["revenue"]))

x = np.array(quantities)
y = np.array(revenues)

if len(x) != 992 or len(y) != 992:
    raise ValueError("Expected 992 observations.")

if len(x) != len(y):
    raise ValueError("Quantity and revenue lengths differ.")

# ---------------------------------------------------------
# 2. Calculate linear regression and R-squared.
# ---------------------------------------------------------

slope, intercept = np.polyfit(x, y, 1)

predicted = slope * x + intercept

ss_res = np.sum((y - predicted) ** 2)
ss_tot = np.sum((y - np.mean(y)) ** 2)

r_squared = 1 - (ss_res / ss_tot)

correlation = np.corrcoef(x, y)[0, 1]

print("\nREGRESSION RESULTS")
print("-" * 65)
print(f"Observations: {len(x)}")
print(f"Correlation coefficient: {correlation:.4f}")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"Regression equation: Revenue = {slope:.4f} × Quantity + {intercept:.4f}")
print(f"R-squared: {r_squared:.4f}")
print(f"Explained variation: {r_squared * 100:.2f}%")

# ---------------------------------------------------------
# 3. Load Excel workbook and locate columns dynamically.
# ---------------------------------------------------------

wb = openpyxl.load_workbook(workbook_path)

data_ws = wb["Clean_Data"]
charts_ws = wb["Charts"]

headers = {
    str(data_ws.cell(1, col).value).strip().lower(): col
    for col in range(1, data_ws.max_column + 1)
}

if "quantity" not in headers or "revenue" not in headers:
    raise ValueError("Quantity/revenue columns not found in Clean_Data.")

quantity_col = headers["quantity"]
revenue_col = headers["revenue"]

last_row = data_ws.max_row

# Verify the source data count.
assert last_row - 1 == 992

print("\nEXCEL SOURCE DATA")
print("-" * 65)
print("Quantity column:", openpyxl.utils.get_column_letter(quantity_col))
print("Revenue column:", openpyxl.utils.get_column_letter(revenue_col))
print("Data rows:", last_row - 1)

# ---------------------------------------------------------
# 4. Create editable Excel scatterplot.
# ---------------------------------------------------------

# Remove an existing chart at A38 when rerunning.
charts_ws._charts = [
    chart for chart in charts_ws._charts
    if not (
        chart.anchor._from.col == 0
        and chart.anchor._from.row == 37
    )
]

scatter = ScatterChart()

scatter.title = "Quantity vs Revenue"
scatter.style = 13
scatter.x_axis.title = "Quantity Sold"
scatter.y_axis.title = "Revenue ($)"
scatter.height = 12
scatter.width = 20

scatter.scatterStyle = "marker"
scatter.legend = None

xvalues = Reference(
    data_ws,
    min_col=quantity_col,
    min_row=2,
    max_row=last_row
)

yvalues = Reference(
    data_ws,
    min_col=revenue_col,
    min_row=2,
    max_row=last_row
)

series = Series(yvalues, xvalues, title="Revenue vs Quantity")

series.graphicalProperties.line.noFill = True

series.marker.symbol = "circle"
series.marker.size = 5

# Add linear regression trendline and R-squared.
series.trendline = Trendline(
    dispEq=True,
    dispRSqr=True
)

scatter.series.append(series)

charts_ws.add_chart(scatter, "A38")

# Enable automatic recalculation.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(workbook_path)

print("\nEditable Excel scatterplot created.")
print("Chart destination: Charts!A38")
print("Trendline equation enabled.")
print("R-squared display enabled.")

# ---------------------------------------------------------
# 5. Export PNG scatterplot with regression line.
# ---------------------------------------------------------

plt.figure(figsize=(11, 7))

plt.scatter(
    x,
    y,
    alpha=0.55,
    label="Transactions"
)

regression_x = np.linspace(x.min(), x.max(), 100)
regression_y = slope * regression_x + intercept

plt.plot(
    regression_x,
    regression_y,
    linewidth=2,
    label="Linear regression"
)

equation = (
    f"Revenue = {slope:.4f} × Quantity "
    f"+ {intercept:.4f}\n"
    f"R² = {r_squared:.4f}"
)

plt.text(
    0.05,
    0.95,
    equation,
    transform=plt.gca().transAxes,
    verticalalignment="top",
    bbox=dict(
        boxstyle="round",
        facecolor="white",
        alpha=0.8
    )
)

plt.title("Relationship Between Quantity and Revenue")
plt.xlabel("Quantity Sold")
plt.ylabel("Revenue ($)")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\n" + "=" * 65)
print("PHASE 4 - TASK 5 RESULTS")
print("=" * 65)
print("Observations:", len(x))
print(f"Correlation: {correlation:.4f}")
print(f"R-squared: {r_squared:.4f}")
print("Excel workbook:", workbook_path)
print("PNG image:", png_path)
print("\nSTATUS: SUCCESS")
print("=" * 65)