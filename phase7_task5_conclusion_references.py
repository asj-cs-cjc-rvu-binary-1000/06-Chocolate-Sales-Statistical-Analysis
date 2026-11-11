import os
from docx import Document
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

REPORT = "report/CIE3_Statistical_Analysis_Report.docx"
REFERENCES = "docs/references.md"

assert os.path.exists(REPORT), "Report not found."
assert os.path.exists(REFERENCES), "References documentation not found."

doc = Document(REPORT)

existing_text = "\n".join(p.text for p in doc.paragraphs)
assert "The findings indicate a strong positive association" not in existing_text, \
    "Conclusion already appears to be inserted."

def find_heading(title):
    heading = next(
        (p for p in doc.paragraphs if p.text.strip() == title),
        None
    )
    assert heading is not None, f"Missing heading: {title}"
    return heading

def add_paragraph_after(cursor, text, bold_prefix=None):
    element = OxmlElement("w:p")
    cursor.addnext(element)
    paragraph = Paragraph(element, doc)

    if bold_prefix and text.startswith(bold_prefix):
        first = paragraph.add_run(bold_prefix)
        first.bold = True
        first.font.name = "Times New Roman"
        first.font.size = Pt(12)

        remainder = paragraph.add_run(text[len(bold_prefix):])
        remainder.font.name = "Times New Roman"
        remainder.font.size = Pt(12)

        for run in (first, remainder):
            run._element.get_or_add_rPr().rFonts.set(
                qn("w:eastAsia"), "Times New Roman"
            )
    else:
        run = paragraph.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run._element.get_or_add_rPr().rFonts.set(
            qn("w:eastAsia"), "Times New Roman"
        )

    paragraph.paragraph_format.line_spacing = 1.15
    paragraph.paragraph_format.space_after = Pt(6)
    return element

# ---------------------------------------------------------
# CONCLUSION
# ---------------------------------------------------------

conclusion_heading = find_heading("Conclusion")
cursor = conclusion_heading._p

conclusion_paragraphs = [
    (
        "The findings indicate a strong positive association between "
        "the quantity of chocolate sold and total transaction revenue "
        "in the analysed sample. Therefore, the research question is "
        "answered affirmatively: transactions with higher quantities "
        "generally tend to generate higher revenue. Pearson's correlation "
        "coefficient of 0.7425 supports this conclusion."
    ),
    (
        "The descriptive analysis was conducted using 992 cleaned "
        "transactions. The average quantity sold was 2.8901 units, "
        "while the median was 3 units. Average transaction revenue "
        "was $24.3781, compared with a median of $20.47. The higher "
        "revenue mean relative to its median, together with the revenue "
        "histogram and boxplot, indicates a positively skewed revenue "
        "distribution. Eight potential upper outliers were identified "
        "using the 1.5 times IQR rule. These observations were retained "
        "because potential outliers should be investigated rather than "
        "automatically removed."
    ),
    (
        "The simple linear regression model produced the equation "
        "Revenue = 8.3202 × Quantity + 0.3316. Its coefficient of "
        "determination was 0.5513, indicating that approximately "
        "55.13% of the observed variation in transaction revenue "
        "is explained by its linear relationship with quantity in "
        "this sample. The remaining 44.87% is not explained by this "
        "single-predictor model."
    ),
    (
        "The findings suggest that transaction quantity is a useful "
        "indicator associated with revenue. However, revenue is also "
        "influenced by unit prices, product categories, brands, discounts, "
        "promotional activities, seasonal demand, and customer or store "
        "characteristics. These factors may contribute to the variation "
        "not explained by quantity alone."
    ),
    (
        "An important limitation is that this study uses observational "
        "transaction data rather than a controlled experiment. The "
        "correlation and regression results therefore describe an "
        "association and do not establish that increasing quantity "
        "causes revenue to increase. The findings are also limited to "
        "the cleaned sample of 992 transactions selected for this "
        "project."
    ),
    (
        "Further research could use multiple linear regression to "
        "examine quantity alongside unit price, discount, product "
        "category, and other relevant variables. Additional analysis "
        "could also investigate differences across customer segments, "
        "stores, and time periods. Such work may provide a more "
        "comprehensive understanding of the factors associated with "
        "chocolate sales revenue."
    ),
    (
        "Overall, the project demonstrates a strong positive linear "
        "association between quantity sold and total revenue. The "
        "statistical results answer the research question while "
        "highlighting the importance of considering other variables "
        "and avoiding unsupported causal conclusions."
    ),
]

for paragraph_text in conclusion_paragraphs:
    cursor = add_paragraph_after(cursor, paragraph_text)

# ---------------------------------------------------------
# REFERENCES
# ---------------------------------------------------------

references_heading = find_heading("References")
cursor = references_heading._p

references = [
    (
        "[1] Project-provided chocolate sales dataset files: "
        "data/raw/sales.csv, data/raw/products.csv, "
        "data/raw/customers.csv, data/raw/stores.csv, and "
        "data/raw/calendar.csv. Original publisher and licensing "
        "information have not been independently verified."
    ),
    (
        "[2] Statistical Analysis of Chocolate Sales Data. "
        "Internal project document: docs/analysis_plan.md."
    ),
    (
        "[3] Statistical Analysis of Chocolate Sales Data. "
        "Internal project document: docs/data_dictionary.md."
    ),
    (
        "[4] Statistical Analysis of Chocolate Sales Data. "
        "Internal project document: docs/cleaning_decisions.md."
    ),
    (
        "[5] Statistical Analysis of Chocolate Sales Data. "
        "Internal project document: docs/correlation_discussion.md."
    ),
    (
        "[6] Microsoft Excel. Spreadsheet software used for "
        "statistical calculations, frequency tables, and charts."
    ),
    (
        "[7] Python Software Foundation. Python programming language. "
        "https://www.python.org/"
    ),
    (
        "[8] Openpyxl documentation. "
        "https://openpyxl.readthedocs.io/"
    ),
    (
        "[9] python-docx documentation. "
        "https://python-docx.readthedocs.io/"
    ),
    (
        "Source transparency note: The original external provenance "
        "and licensing details of the dataset remain unverified. "
        "No unverified publisher or dataset URL has been attributed."
    ),
]

for reference in references:
    cursor = add_paragraph_after(cursor, reference)

doc.save(REPORT)

print("=" * 70)
print("PHASE 7 - TASK 5: CONCLUSION AND REFERENCES INSERTED")
print("=" * 70)
print(f"Report: {REPORT}")
print(f"References documentation: {REFERENCES}")
print(f"Conclusion paragraphs inserted: {len(conclusion_paragraphs)}")
print(f"Reference entries inserted: {len(references)}")
print("Research question answered.")
print("Statistical findings and limitations discussed.")
print("Recommendations for further research included.")
print("Document saved successfully.")
