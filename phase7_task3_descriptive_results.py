import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

REPORT = "report/CIE3_Statistical_Analysis_Report.docx"

CHARTS = [
    (
        "charts/product_category_bar_chart.png",
        "Figure 1. Frequency distribution of chocolate product categories",
        "Praline was the most frequently recorded category, with 266 "
        "transactions, followed by White (237) and Dark (209). Truffle "
        "(138) and Milk (142) had fewer transactions. The distribution "
        "shows that transactions were not equally distributed across "
        "product categories."
    ),
    (
        "charts/customer_segment_pie_chart.png",
        "Figure 2. Distribution of transactions by customer gender",
        "Male customers accounted for 516 transactions (52.02%), while "
        "female customers accounted for 476 transactions (47.98%). "
        "The distribution is relatively balanced. These percentages "
        "represent transactions classified by gender, not unique customers."
    ),
    (
        "charts/revenue_histogram.png",
        "Figure 3. Frequency distribution of transaction revenue",
        "The revenue histogram shows a concentration of transactions "
        "in the lower revenue intervals. The $10–$20 interval contains "
        "306 transactions, the largest frequency. Frequencies generally "
        "decline across higher intervals, producing a longer right tail "
        "consistent with positive skewness."
    ),
    (
        "charts/revenue_boxplot.png",
        "Figure 4. Box-and-whisker plot of transaction revenue",
        "The median revenue is $20.47, and the middle 50% of transactions "
        "fall between approximately $11.94 and $35.17. The IQR is $23.23. "
        "The 1.5 × IQR rule identifies eight potential high-value outliers "
        "above the upper fence of approximately $70.02. These observations "
        "should be investigated rather than automatically removed because "
        "they may represent genuine high-revenue transactions."
    )
]

assert os.path.exists(REPORT), "Report not found."
for path, _, _ in CHARTS:
    assert os.path.exists(path), f"Missing chart: {path}"

doc = Document(REPORT)

existing_text = "\n".join(p.text for p in doc.paragraphs)
if "Figure 1. Frequency distribution of chocolate product categories" in existing_text:
    raise RuntimeError("Task 3 already appears to be inserted.")

heading = next(
    (p for p in doc.paragraphs
     if p.text.strip() == "Descriptive Statistical Analysis"),
    None
)
assert heading is not None, "Descriptive Statistical Analysis heading missing."

body = doc._element.body

def set_font(run, bold=False, size=12):
    run.font.name = "Times New Roman"
    run.font.size = Pt(size)
    run.bold = bold
    run._element.get_or_add_rPr().rFonts.set(
        qn("w:eastAsia"), "Times New Roman"
    )

def add_paragraph_after(cursor, text="", bold=False,
                        style=None, alignment=None):
    p_element = OxmlElement("w:p")
    cursor.addnext(p_element)

    paragraph = Paragraph(p_element, doc)
    if style:
        paragraph.style = doc.styles[style]

    if text:
        run = paragraph.add_run(text)
        set_font(run, bold=bold)

    paragraph.paragraph_format.line_spacing = 1.15
    paragraph.paragraph_format.space_after = Pt(6)

    if alignment is not None:
        paragraph.alignment = alignment

    return p_element

def add_image_after(cursor, path):
    p_element = OxmlElement("w:p")
    cursor.addnext(p_element)

    paragraph = Paragraph(p_element, doc)
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_after = Pt(3)

    run = paragraph.add_run()
    run.add_picture(path, width=Inches(5.7))

    return p_element

def add_caption(cursor, text):
    return add_paragraph_after(
        cursor,
        text,
        bold=True,
        alignment=WD_ALIGN_PARAGRAPH.CENTER
    )

def add_table_after(cursor, headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    def format_cell(cell, value, bold=False):
        cell.text = ""
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(str(value))
        set_font(run, bold=bold)

    for i, header_text in enumerate(headers):
        cell = table.rows[0].cells[i]
        format_cell(cell, header_text, True)
        shading = OxmlElement("w:shd")
        shading.set(qn("w:fill"), "D9EAF7")
        cell._tc.get_or_add_tcPr().append(shading)

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            format_cell(cells[i], value)

    cursor.addnext(table._tbl)
    return table._tbl

cursor = heading._p

cursor = add_paragraph_after(
    cursor,
    "This section presents the descriptive statistical findings for "
    "the 992 cleaned chocolate sales transactions. It examines product "
    "category and gender distributions, transaction revenue, and the "
    "central tendency and dispersion of quantity sold and revenue."
)

cursor = add_paragraph_after(
    cursor, "Categorical Distributions",
    bold=True, style="Heading 2"
)

cursor = add_paragraph_after(
    cursor,
    "The following figures summarise the categorical composition "
    "of the cleaned transaction dataset."
)

for path, caption, interpretation in CHARTS[:2]:
    cursor = add_image_after(cursor, path)
    cursor = add_caption(cursor, caption)
    cursor = add_paragraph_after(cursor, interpretation)

cursor = add_paragraph_after(
    cursor, "Revenue Distribution",
    bold=True, style="Heading 2"
)

for path, caption, interpretation in CHARTS[2:]:
    cursor = add_image_after(cursor, path)
    cursor = add_caption(cursor, caption)
    cursor = add_paragraph_after(cursor, interpretation)

cursor = add_paragraph_after(
    cursor, "Descriptive Statistics",
    bold=True, style="Heading 2"
)

cursor = add_paragraph_after(
    cursor,
    "Table 1 summarises the central tendency and dispersion of "
    "quantity sold and transaction revenue. The standard deviations "
    "are sample standard deviations."
)

statistics_rows = [
    ("Mean", "2.8901", "$24.3781"),
    ("Median", "3.0000", "$20.4700"),
    ("Mode", "1.0000", "$29.2000"),
    ("Standard deviation", "1.3923", "$15.6019"),
    ("Range", "4.0000", "$70.8100")
]

cursor = add_table_after(
    cursor,
    ["Statistic", "Quantity (units)", "Revenue"],
    statistics_rows
)

cursor = add_caption(
    cursor,
    "Table 1. Descriptive statistics for quantity and revenue"
)

cursor = add_paragraph_after(
    cursor,
    "For quantity sold, the mean is approximately 2.89 units and the "
    "median is 3 units. These values are close, indicating that the "
    "centre of the quantity distribution is relatively balanced. "
    "The mode is 1 unit, showing that one-unit transactions are the "
    "most frequently occurring individual quantity. The standard "
    "deviation is approximately 1.39 units, while the range is 4 units."
)

cursor = add_paragraph_after(
    cursor,
    "For revenue, the mean is approximately $24.38, which is higher "
    "than the median of $20.47. A mean greater than the median is "
    "consistent with positive (right) skewness, where relatively "
    "high-revenue transactions pull the mean upward. The mode is "
    "$29.20. Revenue also has a considerably larger standard "
    "deviation ($15.60) and range ($70.81), indicating substantial "
    "variation in transaction revenue."
)

cursor = add_paragraph_after(
    cursor,
    "The revenue box plot identifies eight potential upper outliers "
    "using the 1.5 × IQR rule. The lower quartile is approximately "
    "$11.94, the upper quartile is approximately $35.17, and the "
    "interquartile range is approximately $23.23. The upper outlier "
    "fence is approximately $70.02. No quantity observations were "
    "identified as outliers using the same rule. The potential revenue "
    "outliers were retained because statistical outlier status alone "
    "is not sufficient justification for deleting valid transactions."
)

doc.save(REPORT)

print("=" * 70)
print("PHASE 7 - TASK 3: DESCRIPTIVE RESULTS INSERTED")
print("=" * 70)
print(f"Report: {REPORT}")
print("Figure 1: Product category bar chart inserted.")
print("Figure 2: Customer gender pie chart inserted.")
print("Figure 3: Revenue histogram inserted.")
print("Figure 4: Revenue box plot inserted.")
print("Table 1: Descriptive statistics inserted.")
print("Mean, median, mode, standard deviation and range interpreted.")
print("Revenue skewness and potential outliers discussed.")
print("Document saved successfully.")
