import os
import shutil
import openpyxl

WORKBOOK = "excel/chocolate_sales_analysis.xlsx"
BACKUP = "excel/chocolate_sales_analysis_before_formula_fix.xlsx"

assert os.path.exists(WORKBOOK), "Workbook not found."

# Preserve the original workbook before making changes.
shutil.copy2(WORKBOOK, BACKUP)

wb = openpyxl.load_workbook(WORKBOOK, data_only=False)

replacements = {
    "MODE.SNGL(": "MODE(",
    "STDEV.S(": "STDEV(",
    "QUARTILE.INC(": "QUARTILE("
}

changed = []

for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            formula = cell.value
            if isinstance(formula, str) and formula.startswith("="):
                updated = formula
                for old, new in replacements.items():
                    updated = updated.replace(old, new)

                if updated != formula:
                    cell.value = updated
                    changed.append(f"{ws.title}!{cell.coordinate}")

# Ask Excel to recalculate formulas when the workbook is opened.
wb.calculation.fullCalcOnLoad = True
wb.calculation.forceFullCalc = True
wb.calculation.calcMode = "auto"

wb.save(WORKBOOK)

print("FORMULA COMPATIBILITY FIX")
print("=========================")
print("Updated cells:", len(changed))
for cell in changed:
    print("-", cell)

# Reopen and verify the saved formulas.
check = openpyxl.load_workbook(WORKBOOK, data_only=False)

expected = {
    "Calculations": {
        "B5": "=MODE(Clean_Data!$F$2:$F$993)",
        "C5": "=MODE(Clean_Data!$I$2:$I$993)",
        "B7": "=STDEV(Clean_Data!$F$2:$F$993)",
        "C7": "=STDEV(Clean_Data!$I$2:$I$993)",
        "B8": "=QUARTILE(Clean_Data!$F$2:$F$993,1)",
        "C10": "=QUARTILE(Clean_Data!$I$2:$I$993,3)"
    },
    "Descriptive_Stats": {
        "B20": "=STDEV(Clean_Data!$F$2:$F$993)",
        "C20": "=STDEV(Clean_Data!$I$2:$I$993)",
        "B32": "=QUARTILE(Clean_Data!$F$2:$F$993,1)",
        "C34": "=QUARTILE(Clean_Data!$I$2:$I$993,3)"
    }
}

for sheet, cells in expected.items():
    for address, formula in cells.items():
        actual = check[sheet][address].value
        assert actual == formula, (
            f"Formula mismatch: {sheet}!{address}: {actual}"
        )

print("\nAll selected compatibility formulas verified.")
print("Backup:", BACKUP)
print("Workbook saved:", WORKBOOK)
