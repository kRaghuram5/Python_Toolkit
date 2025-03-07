import fitz  # PyMuPDF
import os
doc = fitz.open("example.1.pdf")
for page_number, page in enumerate(doc, start=1):
    images = page.get_images(full=True)
    for img_index, img in enumerate(images, start=1):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        with open(f"page_{page_number}_image_{img_index}.{image_ext}", "wb") as img_file:
            img_file.write(image_bytes)
            print(f"Image saved: page_{page_number}_image_{img_index}.{image_ext}")