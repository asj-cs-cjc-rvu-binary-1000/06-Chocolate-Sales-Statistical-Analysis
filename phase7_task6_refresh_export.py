import os
import uno
from com.sun.star.beans import PropertyValue

DOCX = os.path.abspath(
    "report/CIE3_Statistical_Analysis_Report.docx"
)
PDF = os.path.abspath(
    "report/CIE3_Statistical_Analysis_Report.pdf"
)

def prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p

local_ctx = uno.getComponentContext()
resolver = local_ctx.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", local_ctx
)

ctx = resolver.resolve(
    "uno:socket,host=localhost,port=2002;"
    "urp;StarOffice.ComponentContext"
)

smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext(
    "com.sun.star.frame.Desktop", ctx
)

doc = desktop.loadComponentFromURL(
    uno.systemPathToFileUrl(DOCX),
    "_blank",
    0,
    (
        prop("Hidden", True),
        prop("ReadOnly", False),
        prop("UpdateDocMode", 3),
    )
)

if not doc:
    raise RuntimeError("Could not open the Word report.")

indexes = doc.getDocumentIndexes()
print("Document indexes found:", indexes.getCount())

for i in range(indexes.getCount()):
    indexes.getByIndex(i).update()
    print(f"PASS: Updated document index {i + 1}")

doc.getTextFields().refresh()
doc.store()

doc.storeToURL(
    uno.systemPathToFileUrl(PDF),
    (
        prop("FilterName", "writer_pdf_Export"),
        prop("Overwrite", True),
    )
)

doc.close(True)

assert os.path.exists(DOCX)
assert os.path.exists(PDF)
assert os.path.getsize(PDF) > 0

print("DOCX saved:", DOCX)
print("PDF exported:", PDF)
print("PDF size:", os.path.getsize(PDF), "bytes")
print("EXPORT COMPLETED.")
