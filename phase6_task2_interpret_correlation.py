import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"
ANALYSIS_PLAN = "docs/analysis_plan.md"

assert os.path.exists(WORKBOOK), "Workbook not found."
assert os.path.exists(ANALYSIS_PLAN), "Analysis plan not found."

wb = openpyxl.load_workbook(WORKBOOK)
ws = wb["Correlation"]

# Pearson correlation result.
r = 0.7425

# Direction and strength classification.
direction = "Positive"
strength = "Strong"

interpretation = (
    "There is a strong positive linear association between quantity "
    "sold and total revenue (Pearson's r = 0.7425). This indicates "
    "that transactions involving higher quantities tend to have "
    "higher total revenue. The association is strong because the "
    "absolute correlation coefficient falls within the 0.60–0.79 "
    "classification interval. This finding describes association "
    "and does not establish causation."
)

# Add interpretation to the Correlation worksheet.
ws["A7"] = "Direction and Strength Interpretation"
ws["A8"] = "Pearson's r"
ws["B8"] = r
ws["A9"] = "Direction"
ws["B9"] = direction
ws["A10"] = "Strength"
ws["B10"] = strength
ws["A12"] = "Statistical Interpretation"
ws["A13"] = interpretation

title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
thin = Side(style="thin", color="B7C9D6")

for cell in ("A7", "A12"):
    ws[cell].font = Font(bold=True, color="FFFFFF")
    ws[cell].fill = title_fill

for row in (8, 9, 10):
    for col in (1, 2):
        cell = ws.cell(row, col)
        cell.border = Border(
            left=thin, right=thin, top=thin, bottom=thin
        )
        if col == 1:
            cell.font = Font(bold=True)
            cell.fill = header_fill

ws["B8"].number_format = "0.0000"
ws["A13"].alignment = Alignment(
    wrap_text=True,
    vertical="top"
)
ws.merge_cells("A13:F15")
ws["A13"].alignment = Alignment(
    wrap_text=True,
    vertical="top"
)
ws.row_dimensions[13].height = 42
ws.row_dimensions[14].height = 25
ws.row_dimensions[15].height = 25

wb.save(WORKBOOK)
wb.close()

# Append interpretation to analysis_plan.md without duplication.
with open(ANALYSIS_PLAN, "r", encoding="utf-8") as file:
    content = file.read()

heading = "## Phase 6 – Correlation Interpretation"

if heading not in content:
    with open(ANALYSIS_PLAN, "a", encoding="utf-8") as file:
        file.write(
            "\n\n" + heading + "\n\n"
            "**Pearson's correlation coefficient:** 0.7425\n\n"
            "**Direction:** Positive.\n\n"
            "**Strength:** Strong (0.60–0.79).\n\n"
            + interpretation + "\n"
        )

print("=" * 70)
print("PHASE 6 - TASK 2: INTERPRETATION CREATED")
print("=" * 70)
print(f"Pearson's r : {r:.4f}")
print(f"Direction   : {direction}")
print(f"Strength    : {strength}")
print("\nInterpretation:")
print(interpretation)
print("\nUpdated files:")
print(WORKBOOK)
print(ANALYSIS_PLAN)
