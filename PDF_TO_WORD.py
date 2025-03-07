from pdf2docx import Converter

pdf_file = "example.1.pdf"
docx_file = "output.docx"

converter = Converter(pdf_file)
converter.convert(docx_file, start=0, end=None)  # Converts the entire PDF
converter.close()

print("PDF converted to Word successfully!")