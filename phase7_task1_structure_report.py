import os
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

OUTPUT = "report/CIE3_Statistical_Analysis_Report.docx"

os.makedirs("report", exist_ok=True)

# Preserve an existing report rather than silently overwriting it.
if os.path.exists(OUTPUT):
    backup = OUTPUT.replace(".docx", "_backup_before_phase7.docx")
    if not os.path.exists(backup):
        import shutil
        shutil.copy2(OUTPUT, backup)
        print(f"Existing report backed up to: {backup}")

doc = Document()

# ---------------------------------------------------------
# GLOBAL PAGE AND FONT FORMATTING
# ---------------------------------------------------------
section = doc.sections[0]
section.top_margin = Inches(0.8)
section.bottom_margin = Inches(0.8)
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)

styles = doc.styles

for style_name in ["Normal", "Title", "Subtitle",
                   "Heading 1", "Heading 2", "Heading 3"]:
    style = styles[style_name]
    style.font.name = "Times New Roman"
    style.font.size = Pt(12)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    style.paragraph_format.line_spacing = 1.15

styles["Normal"].paragraph_format.space_after = Pt(6)

# Heading formatting: retain 12 pt Times New Roman.
for style_name in ["Heading 1", "Heading 2", "Heading 3"]:
    styles[style_name].font.bold = True
    styles[style_name].paragraph_format.space_before = Pt(12)
    styles[style_name].paragraph_format.space_after = Pt(6)
    styles[style_name].paragraph_format.keep_with_next = True

# ---------------------------------------------------------
# TITLE PAGE
# ---------------------------------------------------------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(100)

run = p.add_run("STATISTICAL ANALYSIS OF CHOCOLATE SALES")
run.bold = True
run.font.name = "Times New Roman"
run.font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(18)
run = p.add_run("Applied Statistics – CIE 3")
run.font.name = "Times New Roman"
run.font.size = Pt(12)

for _ in range(3):
    doc.add_paragraph()

details = [
    ("Student Name", "Aryan S Jain"),
    ("Student USN", "1RUA25CSE0087"),
    ("Course Code", "SE2041"),
    ("Course Name", "Applied Statistics"),
    ("Professor", "Prof. Varadurga Bhat"),
    ("Date", "11 November 2026"),
]

for label, value in details:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(f"{label}: {value}")
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

# ---------------------------------------------------------
# TABLE OF CONTENTS PAGE
# ---------------------------------------------------------
doc.add_page_break()

doc.add_heading("Table of Contents", level=1)

p = doc.add_paragraph()
run = p.add_run()

# Insert a Word TOC field. It can be updated in Word/LibreOffice.
fld_char_begin = OxmlElement("w:fldChar")
fld_char_begin.set(qn("w:fldCharType"), "begin")

instr_text = OxmlElement("w:instrText")
instr_text.set(qn("xml:space"), "preserve")
instr_text.text = ' TOC \\o "1-2" \\h \\z \\u '

fld_char_separate = OxmlElement("w:fldChar")
fld_char_separate.set(qn("w:fldCharType"), "separate")

placeholder = OxmlElement("w:t")
placeholder.text = "Update this Table of Contents when the report is complete."

fld_char_end = OxmlElement("w:fldChar")
fld_char_end.set(qn("w:fldCharType"), "end")

run._r.append(fld_char_begin)
run._r.append(instr_text)
run._r.append(fld_char_separate)
run._r.append(placeholder)
run._r.append(fld_char_end)

# ---------------------------------------------------------
# REPORT SECTION HEADINGS
# ---------------------------------------------------------
doc.add_page_break()

sections = [
    "Introduction",
    "Methodology",
    "Descriptive Statistical Analysis",
    "Correlation Analysis",
    "Conclusion",
    "References",
]

for heading in sections:
    doc.add_heading(heading, level=1)
    # Empty paragraph provides a clear insertion point for later tasks.
    doc.add_paragraph()

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
for sec in doc.sections:
    footer = sec.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    run = p.add_run("Applied Statistics – CIE 3 | ")
    run.font.name = "Times New Roman"
    run.font.size = Pt(10)

    # Automatic page number field.
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")

    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)

# Ask Word-compatible applications to refresh fields when opened.
settings = doc.settings.element
update_fields = OxmlElement("w:updateFields")
update_fields.set(qn("w:val"), "true")
settings.append(update_fields)

doc.save(OUTPUT)

print("=" * 70)
print("PHASE 7 - TASK 1: REPORT STRUCTURE CREATED")
print("=" * 70)
print(f"Output: {OUTPUT}")
print("Title page: Created")
print("Table of Contents field: Inserted")
print("Required section headings: Created")
print("Font: Times New Roman, 12 pt")
print("Line spacing: 1.15")
print("Footer: Automatic page numbering")
print("Document saved successfully.")
