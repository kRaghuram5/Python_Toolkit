#This is to convert text to pdf 
# --REQUIRMENTS ** TEXT FILE  to be converted to pdf **
from reportlab.pdfgen import canvas

text_file = "example.txt" #Enter your Text file to be converted
pdf_file = "example.pdf" # Enter the pdf name to be created

c = canvas.Canvas(pdf_file)
with open(text_file, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, start=1):
        c.drawString(100, 800 - (line_num * 15), line.strip())  # Adjust y-coordinates
c.save()

print("Text converted to PDF successfully!")
