import os
import csv
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

REPORT = "report/CIE3_Statistical_Analysis_Report.docx"
DATA_DICTIONARY = "docs/data_dictionary.md"
CLEANING_DECISIONS = "docs/cleaning_decisions.md"
SAMPLED_DATA = "data/processed/chocolate_sales_analysis_dataset.csv"
CLEAN_DATA = "data/processed/chocolate_sales_clean.csv"

for path in [
    REPORT, DATA_DICTIONARY, CLEANING_DECISIONS,
    SAMPLED_DATA, CLEAN_DATA
]:
    assert os.path.exists(path), f"Required file not found: {path}"

with open(DATA_DICTIONARY, encoding="utf-8") as f:
    dictionary_text = f.read()

with open(CLEANING_DECISIONS, encoding="utf-8") as f:
    cleaning_text = f.read()

def csv_dimensions(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = sum(1 for _ in reader)
    return rows, len(header)

sample_rows, sample_columns = csv_dimensions(SAMPLED_DATA)
clean_rows, clean_columns = csv_dimensions(CLEAN_DATA)

assert sample_rows == 1000, f"Expected 1000 sampled rows, got {sample_rows}"
assert clean_rows == 992, f"Expected 992 clean rows, got {clean_rows}"
assert sample_columns == 24 and clean_columns == 24

# Confirm documentation contains the key cleaning evidence.
assert "P0000" in cleaning_text and "P0201" in cleaning_text
assert "quantity" in dictionary_text.lower()
assert "revenue" in dictionary_text.lower()

doc = Document(REPORT)

# Prevent accidental duplicate insertion.
all_text = "\n".join(p.text for p in doc.paragraphs)
if "The present study investigates whether there is an association" in all_text:
    raise RuntimeError("Task 2 content already exists. No changes made.")

def set_run_font(run, bold=False):
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.bold = bold
    run._element.get_or_add_rPr().rFonts.set(
        qn("w:eastAsia"), "Times New Roman"
    )

def insert_paragraph_after(paragraph, text="", style=None):
    new_p = OxmlElement("w:p")
    paragraph._p.addnext(new_p)
    from docx.text.paragraph import Paragraph
    result = Paragraph(new_p, paragraph._parent)
    if style:
        result.style = style
    if text:
        run = result.add_run(text)
        set_run_font(run)
    result.paragraph_format.line_spacing = 1.15
    result.paragraph_format.space_after = Pt(6)
    return result

def shade_cell(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def format_cell(cell, text, bold=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(str(text))
    set_run_font(run, bold)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def insert_table_after(paragraph, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, header in enumerate(headers):
        format_cell(table.rows[0].cells[i], header, True)
        shade_cell(table.rows[0].cells[i], "D9EAF7")

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            format_cell(cells[i], value)

    paragraph._p.addnext(table._tbl)
    return table

# Locate the existing headings.
paragraphs = list(doc.paragraphs)
heading_map = {
    p.text.strip(): p for p in paragraphs
    if p.text.strip() in ["Introduction", "Methodology"]
}
assert "Introduction" in heading_map
assert "Methodology" in heading_map

# ---------------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------------
intro = heading_map["Introduction"]

p = insert_paragraph_after(
    intro,
    "The present study investigates whether there is an association "
    "between the quantity of chocolate sold and the total revenue "
    "generated from sales transactions. The research question guiding "
    "the analysis is: “Is there an association between quantity sold "
    "and revenue?” The study examines whether transactions involving "
    "larger quantities of chocolate tend to generate higher revenue."
)

p = insert_paragraph_after(
    p,
    "The analysis uses the chocolate sales dataset supplied for this "
    "project. The project data are organised into transaction records "
    "and related product, customer, store, and calendar information. "
    "The transaction data provide the quantities sold and revenue "
    "values, while the supporting datasets provide descriptive "
    "information about products, customers, and stores. The analysis "
    "uses the project’s reproducible sampled dataset rather than "
    "attempting to process the full sales file directly in Excel."
)

p = insert_paragraph_after(
    p,
    "Quantity is treated as the independent variable, while total "
    "revenue is treated as the dependent variable. Descriptive "
    "statistics and visualisations are used to summarise the data. "
    "Pearson’s correlation coefficient and the coefficient of "
    "determination are then used to assess the direction, strength, "
    "and explanatory power of the linear association. The results "
    "are interpreted as evidence of association rather than proof "
    "of a cause-and-effect relationship."
)

# ---------------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------------
method = heading_map["Methodology"]

p = insert_paragraph_after(
    method,
    "The study began with the supplied raw sales data and related "
    "reference datasets. Because the complete sales file was too large "
    "for convenient direct analysis in Excel, a Simple Random Sample "
    "of 1,000 transactions was selected without replacement. A fixed "
    "random seed of 42 was used so that the sampling process could be "
    "reproduced. Product, customer, and store information was joined "
    "to the sampled transaction records using the relevant identifiers."
)

p = insert_paragraph_after(
    p,
    "The variables used in the analysis and their measurement scales "
    "are summarised below. Nominal variables identify categories "
    "without a numerical order. Interval variables have meaningful "
    "differences but no absolute zero, while ratio variables have "
    "meaningful differences and a true zero."
)

variable_rows = [
    ("Quantity", "Quantitative – discrete", "Ratio", "Independent variable; number of units sold."),
    ("Revenue", "Quantitative – continuous", "Ratio", "Dependent variable; total transaction revenue."),
    ("Unit price", "Quantitative – continuous", "Ratio", "Supporting variable; price per unit."),
    ("Discount", "Quantitative", "Ratio", "Supporting variable; transaction discount."),
    ("Profit", "Quantitative – continuous", "Ratio", "Supporting variable; transaction profit."),
    ("Age", "Quantitative – discrete", "Ratio", "Customer age."),
    ("Order date", "Temporal", "Interval", "Date of the transaction."),
    ("Product category", "Qualitative", "Nominal", "Chocolate category."),
    ("Brand", "Qualitative", "Nominal", "Product brand."),
    ("Gender", "Qualitative", "Nominal", "Customer gender category."),
    ("Loyalty member", "Qualitative", "Nominal", "Loyalty membership status."),
    ("Country", "Qualitative", "Nominal", "Transaction/customer country."),
]

table = insert_table_after(
    p,
    ["Variable", "Type", "Measurement scale", "Role / description"],
    variable_rows
)

p = insert_paragraph_after(
    p,
    "The initial sample contained 1,000 transactions and 24 variables. "
    "During data validation, eight records were identified with "
    "unmatched product identifiers, including P0000 and P0201. "
    "These records lacked corresponding product information such as "
    "product name, brand, category, cocoa percentage, and product "
    "weight. Since these missing attributes could not be reliably "
    "recovered from the supplied product reference data, the affected "
    "transactions were excluded from the analytical dataset."
)

p = insert_paragraph_after(
    p,
    "No numerical values were imputed, and no unsupported category "
    "labels were introduced. The original 1,000-record sampled dataset "
    "was retained separately for traceability. After excluding the "
    "eight unmatched records, the final cleaned dataset contained "
    "992 transactions and 24 variables, with no missing or empty "
    "cells. This cleaned dataset was used for the subsequent frequency "
    "tables, descriptive statistics, visualisations, and correlation "
    "analysis."
)

p = insert_paragraph_after(
    p,
    "The resulting workflow therefore consisted of reproducible "
    "sampling, joining the relevant reference information, validating "
    "the joined records, removing eight unmatched transactions, and "
    "using the remaining 992 complete transactions for statistical "
    "analysis. The cleaning decisions and variable definitions are "
    "documented separately in the project documentation."
)

# Add source note below the variable table.
note = doc.add_paragraph(
    "Source: Project data dictionary and Phase 1 variable classification."
)
note.paragraph_format.line_spacing = 1.15
for run in note.runs:
    set_run_font(run)

doc.save(REPORT)

print("=" * 70)
print("PHASE 7 - TASK 2: INTRODUCTION AND METHODOLOGY WRITTEN")
print("=" * 70)
print(f"Report: {REPORT}")
print(f"Original sample: {sample_rows} records, {sample_columns} variables")
print(f"Clean dataset: {clean_rows} records, {clean_columns} variables")
print(f"Records removed: {sample_rows - clean_rows}")
print(f"Variable scale table: {len(variable_rows)} variables")
print("Introduction: Added")
print("Methodology: Added")
print("Sampling method and seed: Documented")
print("Cleaning decisions: Documented")
print("Report saved successfully.")
