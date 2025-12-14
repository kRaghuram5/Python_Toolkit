'''This is to Extract Text or Images
using Library: PyPDF2, PyMuPDF (also called Fitz), or pdfminer.six
For image extraction: Use PyMuPDF or pdf2image.'''
#--REQUIRMENTS **The pdf file that to be extract 
import PyPDF2

# Open PDF file
pdf_file = open(r'example.pdf', 'rb')# --Enter the file name or path
pdf_reader = PyPDF2.PdfReader(pdf_file)
#writing in text file
output=open('output.txt','w')# Enter the file name to be create to text

# Extract text from each page
for page in pdf_reader.pages:
    print(page.extract_text())
    output.write(page.extract_text())
output.close()
pdf_file.close()
