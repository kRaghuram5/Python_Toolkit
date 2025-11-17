"""
Utility functions for PDF conversion operations
Refactored from individual scripts to support web application
"""

import os
import shutil
import zipfile
from datetime import datetime
import PyPDF2

# Optional imports - make each dependency optional
try:
    import fitz  # PyMuPDF
    HAVE_FITZ = True
except Exception:
    fitz = None
    HAVE_FITZ = False

try:
    from pdf2docx import Converter
    HAVE_PDF2DOCX = True
except Exception:
    Converter = None
    HAVE_PDF2DOCX = False

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    HAVE_REPORTLAB = True
except Exception:
    canvas = None
    letter = None
    HAVE_REPORTLAB = False

try:
    from PIL import Image
    HAVE_PIL = True
except Exception:
    Image = None
    HAVE_PIL = False

try:
    from docx2pdf import convert as docx2pdf_convert
    HAVE_DOCX2PDF = True
except Exception:
    docx2pdf_convert = None
    HAVE_DOCX2PDF = False


def pdf_to_word(pdf_path, output_folder, unique_id):
    """
    Convert PDF to Word document
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the generated Word file
    """
    if not HAVE_PDF2DOCX:
        raise Exception("pdf2docx is not installed. Install it with: python -m pip install pdf2docx")
    
    try:
        output_filename = f"{unique_id}_output.docx"
        output_path = os.path.join(output_folder, output_filename)
        
        converter = Converter(pdf_path)
        converter.convert(output_path, start=0, end=None)
        converter.close()
        
        return output_path
    except AttributeError as e:
        if "'Rect' object has no attribute 'get_area'" in str(e):
            raise Exception(f"PDF to Word conversion is currently unavailable due to a compatibility issue between pdf2docx (0.5.8) and PyMuPDF (1.26+). "
                          f"Alternative: Use 'PDF to Text' to extract content, then copy into Word manually. "
                          f"Technical note: pdf2docx needs an update to support newer PyMuPDF versions.")
        raise Exception(f"PDF to Word conversion failed: {str(e)}")
    except Exception as e:
        raise Exception(f"PDF to Word conversion failed: {str(e)}")


def pdf_to_text(pdf_path, output_folder, unique_id):
    """
    Extract text from PDF
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the generated text file
    """
    try:
        output_filename = f"{unique_id}_output.txt"
        output_path = os.path.join(output_folder, output_filename)
        
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            with open(output_path, 'w', encoding='utf-8') as output_file:
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    output_file.write(text)
                    output_file.write('\n' + '='*80 + '\n')
        
        return output_path
    except Exception as e:
        raise Exception(f"PDF to Text conversion failed: {str(e)}")


def pdf_to_images(pdf_path, output_folder, unique_id):
    """
    Convert PDF pages to images
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Directory to save output files
        unique_id: Unique identifier for the files
    
    Returns:
        Path to the ZIP file containing all images
    """
    if not HAVE_FITZ:
        raise Exception("PyMuPDF (fitz) is not installed. Install it with: python -m pip install PyMuPDF\nOr install full requirements to enable PDF->image features.")

    try:
        # Create temporary directory for images
        temp_dir = os.path.join(output_folder, f"{unique_id}_images")
        os.makedirs(temp_dir, exist_ok=True)
        
        doc = fitz.open(pdf_path)
        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better quality
            image_path = os.path.join(temp_dir, f"page_{page_num}.png")
            pix.save(image_path)
        
        doc.close()
        
        # Create ZIP file
        zip_filename = f"{unique_id}_images.zip"
        zip_path = os.path.join(output_folder, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        return zip_path
    except Exception as e:
        raise Exception(f"PDF to Images conversion failed: {str(e)}")


def word_to_pdf(word_path, output_folder, unique_id):
    """
    Convert Word document to PDF
    Note: This function uses comtypes which only works on Windows
    For cross-platform support, consider using LibreOffice or docx2pdf
    
    Args:
        word_path: Path to input Word file
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the generated PDF file
    """
    try:
        output_filename = f"{unique_id}_output.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        # Try using docx2pdf (cross-platform alternative)
        if HAVE_DOCX2PDF:
            try:
                docx2pdf_convert(word_path, output_path)
                return output_path
            except Exception:
                pass
        
        # Fallback to comtypes (Windows only)
        try:
            import comtypes.client
            
            # Convert to absolute paths
            word_path_abs = os.path.abspath(word_path)
            output_path_abs = os.path.abspath(output_path)
            
            word = comtypes.client.CreateObject("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(word_path_abs)
            doc.SaveAs(output_path_abs, FileFormat=17)
            doc.Close()
            word.Quit()
            
            return output_path
        except Exception as e:
            raise Exception(f"Word to PDF requires docx2pdf or Microsoft Word. Error: {str(e)}")
    
    except Exception as e:
        raise Exception(f"Word to PDF conversion failed: {str(e)}")


def text_to_pdf(text_path, output_folder, unique_id):
    """
    Convert text file to PDF
    
    Args:
        text_path: Path to input text file
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the generated PDF file
    """
    if not HAVE_REPORTLAB:
        raise Exception("reportlab is not installed. Install it with: python -m pip install reportlab")
    
    try:
        output_filename = f"{unique_id}_output.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        y_position = height - 50
        line_height = 15
        
        with open(text_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                
                # Create new page if needed
                if y_position < 50:
                    c.showPage()
                    y_position = height - 50
                
                # Handle long lines by wrapping
                if len(line) > 80:
                    words = line.split()
                    current_line = ""
                    for word in words:
                        test_line = current_line + " " + word if current_line else word
                        if len(test_line) <= 80:
                            current_line = test_line
                        else:
                            c.drawString(50, y_position, current_line)
                            y_position -= line_height
                            current_line = word
                            if y_position < 50:
                                c.showPage()
                                y_position = height - 50
                    if current_line:
                        c.drawString(50, y_position, current_line)
                        y_position -= line_height
                else:
                    c.drawString(50, y_position, line)
                    y_position -= line_height
        
        c.save()
        return output_path
    except Exception as e:
        raise Exception(f"Text to PDF conversion failed: {str(e)}")


def images_to_pdf(image_paths, output_folder, unique_id):
    """
    Convert multiple images to a single PDF
    
    Args:
        image_paths: List of paths to input image files
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the generated PDF file
    """
    if not HAVE_PIL:
        raise Exception("Pillow (PIL) is not installed. Install it with: python -m pip install Pillow")
    
    try:
        output_filename = f"{unique_id}_output.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        image_objects = []
        for img_path in image_paths:
            img = Image.open(img_path)
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            image_objects.append(img)
        
        if image_objects:
            image_objects[0].save(
                output_path,
                save_all=True,
                append_images=image_objects[1:] if len(image_objects) > 1 else []
            )
        
        return output_path
    except Exception as e:
        raise Exception(f"Images to PDF conversion failed: {str(e)}")


def extract_images_from_pdf(pdf_path, output_folder, unique_id):
    """
    Extract all images from a PDF file
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Directory to save output files
        unique_id: Unique identifier for the files
    
    Returns:
        Path to the ZIP file containing all extracted images
    """
    if not HAVE_FITZ:
        raise Exception("PyMuPDF (fitz) is not installed. Install it with: python -m pip install PyMuPDF\nOr install full requirements to enable image extraction features.")

    try:
        # Create temporary directory for images
        temp_dir = os.path.join(output_folder, f"{unique_id}_extracted_images")
        os.makedirs(temp_dir, exist_ok=True)
        
        doc = fitz.open(pdf_path)
        image_count = 0
        
        for page_number, page in enumerate(doc, start=1):
            images = page.get_images(full=True)
            
            for img_index, img in enumerate(images, start=1):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                image_filename = f"page_{page_number}_image_{img_index}.{image_ext}"
                image_path = os.path.join(temp_dir, image_filename)
                
                with open(image_path, "wb") as img_file:
                    img_file.write(image_bytes)
                
                image_count += 1
        
        doc.close()
        
        if image_count == 0:
            shutil.rmtree(temp_dir)
            raise Exception("No images found in the PDF file")
        
        # Create ZIP file
        zip_filename = f"{unique_id}_extracted_images.zip"
        zip_path = os.path.join(output_folder, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, arcname=file)
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        return zip_path
    except Exception as e:
        raise Exception(f"Image extraction failed: {str(e)}")


def reverse_pdf(pdf_path, output_folder, unique_id):
    """
    Reverse the page order of a PDF file
    
    Args:
        pdf_path: Path to input PDF file
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the reversed PDF file
    """
    try:
        output_filename = f"{unique_id}_reversed.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        reader = PyPDF2.PdfReader(pdf_path)
        writer = PyPDF2.PdfWriter()
        
        # Reverse order
        for page in reversed(reader.pages):
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    except Exception as e:
        raise Exception(f"PDF reversal failed: {str(e)}")


def merge_pdfs(pdf_paths, output_folder, unique_id):
    """
    Merge multiple PDF files into a single PDF
    
    Args:
        pdf_paths: List of paths to input PDF files
        output_folder: Directory to save output file
        unique_id: Unique identifier for the file
    
    Returns:
        Path to the merged PDF file
    """
    try:
        output_filename = f"{unique_id}_merged.pdf"
        output_path = os.path.join(output_folder, output_filename)
        
        writer = PyPDF2.PdfWriter()
        
        for pdf_path in pdf_paths:
            reader = PyPDF2.PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    except Exception as e:
        raise Exception(f"PDF merging failed: {str(e)}")
