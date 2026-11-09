import os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE = "/workspaces/06-Chocolate-Sales-Statistical-Analysis"
FILE = os.path.join(
    BASE, "excel/chocolate_sales_analysis.xlsx"
)

wb = load_workbook(FILE)

clean = wb["Clean_Data"]
freq = wb["Freq_Tables"]

# Clear the frequency worksheet.
if freq.max_row:
    freq.delete_rows(1, freq.max_row)

for table_name in list(freq.tables.keys()):
    del freq.tables[table_name]

# Find the source column positions.
headers = {
    clean.cell(1, col).value: col
    for col in range(1, clean.max_column + 1)
}

required_variables = ["category", "gender"]

for variable in required_variables:
    if variable not in headers:
        raise ValueError(f"Missing source variable: {variable}")

last_data_row = clean.max_row

# Formatting styles.
title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
white_font = Font(bold=True, color="FFFFFF")
bold_font = Font(bold=True)
thin_border = Border(
    bottom=Side(style="thin", color="B7C9D6")
)

print("=" * 65)
print("PHASE 3 - TASK 3: QUALITATIVE FREQUENCY TABLES")
print("=" * 65)

# Each table is placed in its own two-column section.
table_positions = {
    "category": 1,
    "gender": 5
}

for variable, start_col in table_positions.items():

    source_col = headers[variable]
    source_letter = clean.cell(
        row=1, column=source_col
    ).column_letter

    # Obtain unique categories from the source data.
    values = sorted({
        clean.cell(row, source_col).value
        for row in range(2, last_data_row + 1)
        if clean.cell(row, source_col).value not in (None, "")
    })

    # Title.
    title = f"{variable.title()} Frequency Distribution"
    freq.cell(1, start_col, title)
    freq.cell(1, start_col).font = white_font
    freq.cell(1, start_col).fill = title_fill

    # Column headings.
    freq.cell(2, start_col, variable.title())
    freq.cell(2, start_col + 1, "Frequency")

    for col in (start_col, start_col + 1):
        cell = freq.cell(2, col)
        cell.font = bold_font
        cell.fill = header_fill
        cell.border = thin_border

    # Category labels and dynamic COUNTIF formulas.
    for index, value in enumerate(values, start=3):
        freq.cell(index, start_col, value)

        formula = (
            f'=COUNTIF(Clean_Data!${source_letter}$2:'
            f'${source_letter}${last_data_row},'
            f'{freq.cell(index, start_col).coordinate})'
        )
        freq.cell(index, start_col + 1, formula)

    # Total frequency.
    total_row = 3 + len(values)
    freq.cell(total_row, start_col, "Total")
    freq.cell(total_row, start_col + 1,
              f"=SUM({freq.cell(3, start_col + 1).coordinate}:"
              f"{freq.cell(total_row - 1, start_col + 1).coordinate})")

    freq.cell(total_row, start_col).font = bold_font
    freq.cell(total_row, start_col + 1).font = bold_font

    # Column widths.
    freq.column_dimensions[
        freq.cell(1, start_col).column_letter
    ].width = 24

    freq.column_dimensions[
        freq.cell(1, start_col + 1).column_letter
    ].width = 15

    print(f"\n{variable.upper()} FREQUENCY TABLE")
    for value in values:
        print("-", value)

    print("Categories:", len(values))
    print("Total formula:", freq.cell(total_row, start_col + 1).value)

freq.freeze_panes = "A3"
freq.sheet_view.showGridLines = True

wb.save(FILE)

print("\nWorkbook updated:", FILE)
print("Frequency tables created for:", ", ".join(required_variables))
print("\nFREQUENCY TABLE CREATION COMPLETED")