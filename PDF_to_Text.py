'''1. Extract Text or Images
Library: PyPDF2, PyMuPDF (also called Fitz), or pdfminer.six
For image extraction: Use PyMuPDF or pdf2image.
Example:'''
import PyPDF2

# Open PDF file
pdf_file = open(r'E:\Resume.pdf', 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)
#writing in text file
output=open('output.txt','w')

# Extract text from each page
for page in pdf_reader.pages:
    print(page.extract_text())
    output.write(page.extract_text())
output.close()
pdf_file.close()