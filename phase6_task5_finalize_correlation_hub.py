import os
import openpyxl

from openpyxl.chart import ScatterChart, Series, Reference
from openpyxl.chart.trendline import Trendline
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

wb = openpyxl.load_workbook(WORKBOOK)

clean = wb["Clean_Data"]
corr = wb["Correlation"]
charts = wb["Charts"]

last_row = clean.max_row

# --------------------------------------------------
# 1. Verify original Phase 4 scatterplot.
# --------------------------------------------------

original_scatterplots = [
    chart for chart in charts._charts
    if isinstance(chart, ScatterChart)
]

assert len(original_scatterplots) == 1, (
    "Expected exactly one original scatterplot."
)

original = original_scatterplots[0]

# --------------------------------------------------
# 2. Create final scatterplot for Correlation Hub.
# --------------------------------------------------

# Remove only previously created charts from this
# worksheet to make the script safe to rerun.
corr._charts.clear()

x_values = Reference(
    clean,
    min_col=6,
    min_row=2,
    max_row=last_row
)

y_values = Reference(
    clean,
    min_col=9,
    min_row=2,
    max_row=last_row
)

chart = ScatterChart()

chart.title = "Quantity vs Revenue"
chart.style = 13
chart.x_axis.title = "Quantity Sold (Units)"
chart.y_axis.title = "Total Revenue ($)"

chart.height = 10
chart.width = 19

chart.scatterStyle = "marker"
chart.legend = None

series = Series(
    y_values,
    x_values,
    title="Observed Transactions"
)

series.graphicalProperties.line.noFill = True
series.graphicalProperties.solidFill = "4472C4"
series.graphicalProperties.line.solidFill = "4472C4"

series.trendline = Trendline(
    trendlineType="linear",
    dispEq=True,
    dispRSqr=True
)

chart.series.append(series)

corr.add_chart(chart, "A29")

# --------------------------------------------------
# 3. Add final report reference values.
# --------------------------------------------------

corr["A3"] = "Pearson's Correlation Coefficient"
corr["A5"] = "Pearson's r"
corr["B5"] = (
    f"=CORREL(Clean_Data!$F$2:$F${last_row},"
    f"Clean_Data!$I$2:$I${last_row})"
)

corr["A7"] = "Direction and Strength Interpretation"
corr["A8"] = "Pearson's r"
corr["B8"] = 0.7425
corr["A9"] = "Direction"
corr["B9"] = "Positive"
corr["A10"] = "Strength"
corr["B10"] = "Strong"

corr["A12"] = "Statistical Interpretation"

corr["A17"] = "Coefficient of Determination (R²)"
corr["A19"] = "Squared Pearson Correlation (r²)"
corr["B19"] = "=B5^2"

corr["A20"] = "Excel RSQ Function"
corr["B20"] = (
    f"=RSQ(Clean_Data!$I$2:$I${last_row},"
    f"Clean_Data!$F$2:$F${last_row})"
)

corr["A21"] = "R² as Percentage"
corr["B21"] = "=B19*100"

corr["A22"] = "Unexplained Variation (%)"
corr["B22"] = "=100-B21"

corr["A24"] = "Interpretation"

# --------------------------------------------------
# 4. Add final summary section.
# --------------------------------------------------

corr["A28"] = "FINAL CORRELATION HUB - REPORT REFERENCE"

summary = [
    ("Research Question",
     "Is there an association between quantity sold and total revenue?"),
    ("Independent Variable", "Quantity sold"),
    ("Dependent Variable", "Total revenue"),
    ("Sample Size", last_row - 1),
    ("Pearson's r", 0.7425),
    ("Direction", "Positive"),
    ("Strength", "Strong"),
    ("Trendline Equation",
     "Revenue = 8.3202 × Quantity + 0.3316"),
    ("R²", 0.5513),
    ("Explained Variation", "55.13%"),
    ("Unexplained Variation", "44.87%"),
]

for row_number, (label, value) in enumerate(summary, start=47):
    corr.cell(row_number, 1, label)
    corr.cell(row_number, 2, value)

# --------------------------------------------------
# 5. Formatting.
# --------------------------------------------------

title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")

thin = Side(style="thin", color="B7C9D6")
border = Border(
    left=thin,
    right=thin,
    top=thin,
    bottom=thin
)

for cell in ("A28",):
    corr[cell].font = Font(
        bold=True,
        color="FFFFFF",
        size=13
    )
    corr[cell].fill = title_fill

for row in range(47, 58):
    for col in range(1, 3):
        cell = corr.cell(row, col)
        cell.border = border
        cell.alignment = Alignment(
            vertical="center",
            wrap_text=True
        )

    corr.cell(row, 1).font = Font(bold=True)
    corr.cell(row, 1).fill = header_fill

corr["B5"].number_format = "0.0000"
corr["B8"].number_format = "0.0000"
corr["B19"].number_format = "0.0000"
corr["B20"].number_format = "0.0000"
corr["B21"].number_format = '0.00"%"'
corr["B22"].number_format = '0.00"%"'

corr.column_dimensions["A"].width = 43
corr.column_dimensions["B"].width = 75

corr.freeze_panes = "A3"
corr.sheet_view.showGridLines = False

# Request recalculation when opened in Excel.
try:
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
except AttributeError:
    pass

wb.save(WORKBOOK)
wb.close()

print("=" * 70)
print("PHASE 6 - TASK 5: CORRELATION HUB CREATED")
print("=" * 70)
print("Original Charts worksheet preserved.")
print("New scatterplot added to Correlation worksheet.")
print("X-axis: Quantity")
print("Y-axis: Revenue")
print("Linear trendline: Enabled")
print("Trendline equation: Enabled")
print("Trendline R-squared: Enabled")
print("Pearson's r: 0.7425")
print("R-squared: 0.5513")
print("Report reference summary: Rows 47-57")
print("\nWorkbook saved successfully.")
