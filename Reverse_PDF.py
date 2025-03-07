'''Reverse Page Numbers
Library: PyPDF2'''
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("example.1.pdf")
writer = PdfWriter()

# Reverse order
for page in reversed(reader.pages):
    writer.add_page(page)

with open("reordered.pdf", "wb") as f:
    writer.write(f)