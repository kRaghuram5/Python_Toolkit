#This is for Converting image To PDF
# --REQUIRMNETS **Enter the One or More Image with Name or Respective path in the form of list**
from PIL import Image

images = ["page_1.png", "page_2.png"]  # Enter the List of image name or file paths here
pdf_path = "output.pdf"

image_objects = [Image.open(img).convert("RGB") for img in images]
image_objects[0].save(pdf_path, save_all=True, append_images=image_objects[1:])

print("Images converted to PDF successfully!")
