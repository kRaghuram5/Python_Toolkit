# --This is to Reverse Page Numbers
# REQUIRMENTS **The pdf file that need to be reversed**
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("example.1.pdf") #--Enter the name of pdf name or path here
writer = PdfWriter()

# Reverse order
for page in reversed(reader.pages):
    writer.add_page(page)

with open("reversed.pdf", "wb") as f: #--Enter the name of file name or path
    writer.write(f)
