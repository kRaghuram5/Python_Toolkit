# This is to convert PDF file to Word format 
# --REQUIRMENTS **The PDF file that to be converted to word document.

from pdf2docx import Converter

pdf_file = "example.1.pdf" #--Enter the file name or path here!!
docx_file = "output.docx"  #--Enter the document file name to be created

converter = Converter(pdf_file)
converter.convert(docx_file, start=0, end=None) # converts the entire document, You can also change the constraints!!
converter.close()

print("PDF converted to Word successfully!")
