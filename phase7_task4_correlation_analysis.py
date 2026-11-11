import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

REPORT = "report/CIE3_Statistical_Analysis_Report.docx"
CHART = "charts/quantity_vs_revenue_scatterplot.png"

assert os.path.exists(REPORT), "Report document not found."
assert os.path.exists(CHART), "Correlation scatterplot not found."

doc = Document(REPORT)

existing_text = "\n".join(p.text for p in doc.paragraphs)

if "Figure 5. Relationship between quantity sold and total revenue" in existing_text:
    raise RuntimeError("Task 4 content already appears to be inserted.")

heading = next(
    (p for p in doc.paragraphs
     if p.text.strip() == "Correlation Analysis"),
    None
)
assert heading is not None, "Correlation Analysis heading missing."

# Use the Document object as the paragraph parent.
def set_font(run, bold=False, size=12):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    run._element.get_or_add_rPr().rFonts.set(
        qn("w:eastAsia"), "Times New Roman"
    )

def add_paragraph_after(cursor, text="", bold=False, alignment=None):
    element = OxmlElement("w:p")
    cursor.addnext(element)

    paragraph = Paragraph(element, doc)

    if text:
        run = paragraph.add_run(text)
        set_font(run, bold=bold)

    paragraph.paragraph_format.line_spacing = 1.15
    paragraph.paragraph_format.space_after = Pt(6)

    if alignment is not None:
        paragraph.alignment = alignment

    return element

def add_image_after(cursor, image_path):
    element = OxmlElement("w:p")
    cursor.addnext(element)

    paragraph = Paragraph(element, doc)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(3)

    run = paragraph.add_run()
    run.add_picture(image_path, width=Inches(5.9))

    return element

def shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), fill)
    tc_pr.append(shading)

def add_metrics_table(cursor):
    table = doc.add_table(rows=1, cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    headers = ["Correlation Measure", "Result"]
    for cell, value in zip(table.rows[0].cells, headers):
        cell.text = value
        shade_cell(cell, "D9EAF7")

    metrics = [
        ("Sample size (n)", "992"),
        ("Pearson correlation (r)", "0.7425"),
        ("Direction and strength", "Strong positive"),
        ("Regression slope", "8.3202"),
        ("Regression intercept", "0.3316"),
        ("Regression equation", "Revenue = 8.3202 × Quantity + 0.3316"),
        ("Coefficient of determination (R²)", "0.5513"),
        ("Explained variation", "55.13%"),
        ("Unexplained variation", "44.87%"),
    ]

    for label, value in metrics:
        cells = table.add_row().cells
        cells[0].text = label
        cells[1].text = value

    for row in table.rows:
        for cell in row.cells:
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            for paragraph in cell.paragraphs:
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    set_font(run, size=10)

    cursor.addnext(table._tbl)
    return table._tbl

cursor = heading._p

cursor = add_paragraph_after(
    cursor,
    "This section examines whether the quantity of chocolate sold is "
    "associated with total transaction revenue. Pearson's product-moment "
    "correlation coefficient and simple linear regression were used to "
    "describe the direction, strength and explanatory value of the "
    "relationship across the 992 cleaned transactions."
)

cursor = add_paragraph_after(
    cursor,
    "Correlation and Regression Results",
    bold=True
)

cursor = add_paragraph_after(
    cursor,
    "The Pearson correlation coefficient was calculated as r = 0.7425. "
    "This indicates a strong positive linear association between quantity "
    "sold and total revenue. Transactions involving larger quantities "
    "generally tend to have higher revenue."
)

cursor = add_paragraph_after(
    cursor,
    "The fitted simple linear regression equation is Revenue = "
    "8.3202 × Quantity + 0.3316. The slope indicates that an additional "
    "unit of quantity is associated with an estimated increase of "
    "approximately $8.32 in transaction revenue within this sample. "
    "The intercept is the model's estimated revenue when quantity is zero; "
    "since observed quantities range from 1 to 5, this intercept should "
    "not be interpreted as an observed transaction."
)

cursor = add_paragraph_after(
    cursor,
    "Table 2. Summary of correlation and regression results",
    bold=True
)

cursor = add_metrics_table(cursor)

cursor = add_paragraph_after(
    cursor,
    "Coefficient of Determination",
    bold=True
)

cursor = add_paragraph_after(
    cursor,
    "The coefficient of determination is R² = 0.5513, or 55.13%. "
    "This means that approximately 55.13% of the variation in transaction "
    "revenue is explained by the fitted linear relationship with quantity "
    "sold in this sample. The remaining 44.87% is not explained by this "
    "one-predictor model and may be associated with other factors, "
    "including unit price, product category, brand and discounts."
)

cursor = add_paragraph_after(
    cursor,
    "Scatterplot and Interpretation",
    bold=True
)

cursor = add_paragraph_after(
    cursor,
    "Figure 5 presents the scatterplot of quantity sold against total "
    "revenue, together with the fitted linear regression line. The "
    "upward pattern of the observations is consistent with the positive "
    "Pearson correlation coefficient. The points do not all lie directly "
    "on the regression line, indicating that quantity alone does not "
    "fully account for differences in transaction revenue."
)

cursor = add_image_after(cursor, CHART)

cursor = add_paragraph_after(
    cursor,
    "Figure 5. Relationship between quantity sold and total revenue",
    bold=True,
    alignment=WD_ALIGN_PARAGRAPH.CENTER
)

cursor = add_paragraph_after(
    cursor,
    "Limitations and Statistical Caution",
    bold=True
)

cursor = add_paragraph_after(
    cursor,
    "The results demonstrate association, not causation. The analysis "
    "uses observational transaction data, so it cannot establish that "
    "increasing quantity by itself causes revenue to increase. Unit price "
    "and discounts can influence revenue, while product category and brand "
    "may also affect the amount paid. These variables may help explain "
    "the variation not captured by the simple regression model. The "
    "relationship should therefore be interpreted within the context of "
    "the sampled transactions and the variables included in the analysis."
)

doc.save(REPORT)

print("=" * 70)
print("PHASE 7 - TASK 4: CORRELATION ANALYSIS INSERTED")
print("=" * 70)
print(f"Report: {REPORT}")
print("Pearson correlation: 0.7425")
print("Regression equation: Revenue = 8.3202 × Quantity + 0.3316")
print("R-squared: 0.5513 (55.13%)")
print("Explained variation: 55.13%")
print("Unexplained variation: 44.87%")
print("Figure 5: Correlation scatterplot inserted.")
print("Table 2: Correlation and regression summary inserted.")
print("Limitations and non-causal interpretation included.")
print("Document saved successfully.")
