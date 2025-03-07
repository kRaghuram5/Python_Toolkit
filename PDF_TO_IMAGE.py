# This is For Converting PDF to Images
# --REQUIRMENTS **A PDF file that u need to convert to images 
import fitz  # PyMuPDF

doc = fitz.open("example.pdf") #--Enter your name of pdf file or path of file here
for page_num, page in enumerate(doc, start=1):
    pix = page.get_pixmap()
    pix.save(f"page_{page_num}.png")

print("PDF pages converted to images successfully!")
