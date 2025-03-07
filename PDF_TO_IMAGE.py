#4. PDF to Other Formats PDF to Image
import fitz  # PyMuPDF

doc = fitz.open("example.pdf")
with open("output.txt", "w", encoding="utf-8") as f:
    for page in doc:
        text = page.get_text()
        f.write(text + "\n")

print("PDF converted to Text successfully!")
import fitz  # PyMuPDF

doc = fitz.open("E:\\DSA OEE.pdf")
for page_num, page in enumerate(doc, start=1):
    pix = page.get_pixmap()
    pix.save(f"page_{page_num}.png")

print("PDF pages converted to images successfully!")