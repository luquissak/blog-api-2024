from spire.doc import *
from spire.doc.common import *

# Create word document
document = Document()

# Load a doc or docx file
document.LoadFromFile("test/sample.docx")

#Save the document to PDF
document.SaveToFile("test/ToPDF.pdf", FileFormat.PDF)
document.Close()