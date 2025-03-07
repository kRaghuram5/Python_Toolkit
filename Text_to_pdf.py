from reportlab.pdfgen import canvas

text_file = "output.txt"
pdf_file = "output1.pdf"

c = canvas.Canvas(pdf_file)
with open(text_file, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, start=1):
        c.drawString(100, 800 - (line_num * 15), line.strip())  # Adjust y-coordinates
c.save()

print("Text converted to PDF successfully!")