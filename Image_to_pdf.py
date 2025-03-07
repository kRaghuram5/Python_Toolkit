from PIL import Image

images = ["page_1.png", "page_2.png"]  # List of image file paths
pdf_path = "output.pdf"

image_objects = [Image.open(img).convert("RGB") for img in images]
image_objects[0].save(pdf_path, save_all=True, append_images=image_objects[1:])

print("Images converted to PDF successfully!")