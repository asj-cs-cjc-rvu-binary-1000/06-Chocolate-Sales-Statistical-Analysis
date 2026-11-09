import os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side

BASE = "/workspaces/06-Chocolate-Sales-Statistical-Analysis"
FILE = os.path.join(
    BASE, "excel/chocolate_sales_analysis.xlsx"
)

wb = load_workbook(FILE)
clean = wb["Clean_Data"]
freq = wb["Freq_Tables"]

headers = {
    clean.cell(1, col).value: col
    for col in range(1, clean.max_column + 1)
}

if "revenue" not in headers:
    raise ValueError("Revenue column not found.")

revenue_col = headers["revenue"]
revenue_letter = clean.cell(1, revenue_col).column_letter
last_row = clean.max_row

# Put the quantitative table in columns I and J.
start_col = 9

# Clear only the area used by this table.
for row in range(1, 20):
    for col in range(start_col, start_col + 2):
        freq.cell(row, col).value = None

# Class boundaries.
bins = [
    (0, 10),
    (10, 20),
    (20, 30),
    (30, 40),
    (40, 50),
    (50, 60),
    (60, 70),
    (70, 80),
]

title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
white_font = Font(bold=True, color="FFFFFF")
bold_font = Font(bold=True)
thin_border = Border(
    bottom=Side(style="thin", color="B7C9D6")
)

# Title.
freq.cell(1, start_col, "Revenue Frequency Distribution")
freq.cell(1, start_col).font = white_font
freq.cell(1, start_col).fill = title_fill

# Headings.
freq.cell(2, start_col, "Revenue Interval")
freq.cell(2, start_col + 1, "Frequency")

for col in (start_col, start_col + 1):
    cell = freq.cell(2, col)
    cell.font = bold_font
    cell.fill = header_fill
    cell.border = thin_border

print("=" * 65)
print("PHASE 3 - TASK 4: QUANTITATIVE FREQUENCY DISTRIBUTION")
print("=" * 65)

# Create formulas for each interval.
for index, (lower, upper) in enumerate(bins, start=3):
    label = f"{lower}–{upper}"
    freq.cell(index, start_col, label)

    formula = (
        f'=COUNTIFS(Clean_Data!${revenue_letter}$2:'
        f'${revenue_letter}${last_row},">={lower}",'
        f'Clean_Data!${revenue_letter}$2:'
        f'${revenue_letter}${last_row},"<{upper}")'
    )

    freq.cell(index, start_col + 1, formula)

    print(f"{label}: {formula}")

# Total.
total_row = 3 + len(bins)
freq.cell(total_row, start_col, "Total")
freq.cell(
    total_row,
    start_col + 1,
    f"=SUM(J3:J{total_row - 1})"
)

freq.cell(total_row, start_col).font = bold_font
freq.cell(total_row, start_col + 1).font = bold_font

freq.column_dimensions["I"].width = 24
freq.column_dimensions["J"].width = 16

wb.save(FILE)

print("\nRevenue frequency table created.")
print("Source records:", last_row - 1)
print("Intervals:", len(bins))
print("Total formula:", freq.cell(total_row, start_col + 1).value)
print("\nQUANTITATIVE FREQUENCY TABLE CREATION COMPLETED")