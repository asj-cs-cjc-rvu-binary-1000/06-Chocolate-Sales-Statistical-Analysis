from docx import Document
from docx.text.paragraph import Paragraph
from docx.oxml import OxmlElement
from docx.shared import Inches, Pt
from docx.enum.text import WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.style import WD_STYLE_TYPE

REPORT = "report/CIE3_Statistical_Analysis_Report.docx"

doc = Document(REPORT)

# Locate the TOC heading and Introduction heading.
toc_heading = [
    p for p in doc.paragraphs
    if p.text.strip() == "Table of Contents"
]

intro_heading = [
    p for p in doc.paragraphs
    if p.text.strip() == "Introduction"
]

assert len(toc_heading) == 1, "TOC heading not unique."
assert len(intro_heading) == 1, "Introduction heading not unique."

toc = toc_heading[0]
intro = intro_heading[0]

# Remove only empty paragraphs between TOC and Introduction.
between = []
collect = False

for p in doc.paragraphs:
    if p._p is toc._p:
        collect = True
        continue

    if p._p is intro._p:
        break

    if collect:
        between.append(p)

for p in between:
    if not p.text.strip():
        p._element.getparent().remove(p._element)
    else:
        raise RuntimeError(
            "Unexpected content between TOC and Introduction: "
            + p.text
        )

entries = [
    ("Introduction", 3),
    ("Methodology", 3),
    ("Descriptive Statistical Analysis", 4),
    ("Correlation Analysis", 8),
    ("Conclusion", 10),
    ("References", 10),
]

for title, page in entries:
    p = intro.insert_paragraph_before()
    p.style = doc.styles["Normal"]

    p.paragraph_format.left_indent = Inches(0.15)
    p.paragraph_format.right_indent = Inches(0.1)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15

    p.paragraph_format.tab_stops.add_tab_stop(
        Inches(6.1),
        WD_TAB_ALIGNMENT.RIGHT,
        WD_TAB_LEADER.DOTS
    )

    run = p.add_run(title)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    page_run = p.add_run(f"\t{page}")
    page_run.font.name = "Times New Roman"
    page_run.font.size = Pt(12)

doc.save(REPORT)

print("PASS: Table of Contents inserted.")
print("Entries inserted:", len(entries))
print("DOCX saved:", REPORT)
