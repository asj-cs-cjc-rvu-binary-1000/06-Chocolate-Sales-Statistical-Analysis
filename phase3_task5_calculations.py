import os
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

BASE = "/workspaces/06-Chocolate-Sales-Statistical-Analysis"
FILE = os.path.join(
    BASE, "excel/chocolate_sales_analysis.xlsx"
)

wb = load_workbook(FILE)
clean = wb["Clean_Data"]
calc = wb["Calculations"]

headers = {
    clean.cell(1, col).value: col
    for col in range(1, clean.max_column + 1)
}

variables = ["quantity", "revenue"]

for variable in variables:
    if variable not in headers:
        raise ValueError(f"Missing variable: {variable}")

# Clear the calculations worksheet.
if calc.max_row:
    calc.delete_rows(1, calc.max_row)

for table_name in list(calc.tables.keys()):
    del calc.tables[table_name]

# Styling.
title_fill = PatternFill("solid", fgColor="1F4E78")
header_fill = PatternFill("solid", fgColor="D9EAF7")
white_font = Font(bold=True, color="FFFFFF")
bold_font = Font(bold=True)
thin_border = Border(
    bottom=Side(style="thin", color="B7C9D6")
)

calc["A1"] = "DESCRIPTIVE STATISTICAL CALCULATIONS"
calc["A1"].font = white_font
calc["A1"].fill = title_fill
calc["A1"].alignment = Alignment(horizontal="center")

calc.merge_cells("A1:C1")

calc["A2"] = "Statistic"
calc["B2"] = "Quantity"
calc["C2"] = "Revenue"

for cell in calc[2]:
    cell.font = bold_font
    cell.fill = header_fill
    cell.border = thin_border

statistics = [
    "Mean",
    "Median",
    "Mode",
    "Range",
    "Standard Deviation",
    "Q1 (First Quartile)",
    "Q2 (Second Quartile)",
    "Q3 (Third Quartile)",
    "Coefficient of Variation",
]

for row, statistic in enumerate(statistics, start=3):
    calc.cell(row, 1, statistic)

last_row = clean.max_row

# Excel formulas linked to the Clean_Data worksheet.
formula_functions = {
    "Mean": "AVERAGE",
    "Median": "MEDIAN",
    "Mode": "MODE.SNGL",
    "Range": None,
    "Standard Deviation": "STDEV.S",
    "Q1 (First Quartile)": "QUARTILE.INC",
    "Q2 (Second Quartile)": "QUARTILE.INC",
    "Q3 (Third Quartile)": "QUARTILE.INC",
    "Coefficient of Variation": None,
}

for output_col, variable in enumerate(variables, start=2):
    source_col = headers[variable]
    source_letter = clean.cell(1, source_col).column_letter
    source_range = (
        f"Clean_Data!${source_letter}$2:"
        f"${source_letter}${last_row}"
    )

    for row, statistic in enumerate(statistics, start=3):

        if statistic == "Range":
            formula = (
                f"=MAX({source_range})-MIN({source_range})"
            )

        elif statistic == "Coefficient of Variation":
            mean_cell = calc.cell(3, output_col).coordinate
            sd_cell = calc.cell(7, output_col).coordinate
            formula = f"={sd_cell}/{mean_cell}"

        elif statistic.startswith("Q"):
            quartile = {
                "Q1 (First Quartile)": 1,
                "Q2 (Second Quartile)": 2,
                "Q3 (Third Quartile)": 3,
            }[statistic]

            formula = (
                f"=QUARTILE.INC({source_range},{quartile})"
            )

        else:
            function = formula_functions[statistic]
            formula = f"={function}({source_range})"

        calc.cell(row, output_col, formula)

    # Format coefficient of variation as percentage.
    calc.cell(11, output_col).number_format = "0.00%"

    # Format other statistics to two decimal places.
    for row in range(3, 12):
        if row != 11:
            calc.cell(row, output_col).number_format = "0.00"

calc.column_dimensions["A"].width = 32
calc.column_dimensions["B"].width = 18
calc.column_dimensions["C"].width = 18

calc.freeze_panes = "B3"
calc.sheet_view.showGridLines = True

wb.save(FILE)

print("=" * 65)
print("PHASE 3 - TASK 5: DESCRIPTIVE CALCULATIONS")
print("=" * 65)

for variable, output_col in zip(variables, [2, 3]):
    source_col = headers[variable]
    source_letter = clean.cell(1, source_col).column_letter

    print(f"\n{variable.upper()}")
    print("Source range:",
          f"Clean_Data!${source_letter}$2:${source_letter}${last_row}")

    for row in range(3, 12):
        print(
            calc.cell(row, 1).value,
            "->",
            calc.cell(row, output_col).value
        )

print("\nWorkbook updated:", FILE)
print("Statistics created:", len(statistics))
print("\nCALCULATIONS WORKSHEET CREATED")