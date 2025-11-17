# Legacy Scripts

These are the original standalone Python scripts that have been refactored into the web application.

## Purpose

These scripts are kept for reference and for users who prefer command-line tools over the web interface.

## Scripts Overview

- `Extract_PDF_Image.py` - Extract images from PDF files
- `Image_to_pdf.py` - Convert images to PDF
- `PDF_TO_IMAGE.py` - Convert PDF pages to images
- `PDF_to_Text.py` - Extract text from PDF
- `PDF_TO_WORD.py` - Convert PDF to Word document
- `Reverse_PDF.py` - Reverse PDF page order
- `Text_to_pdf.py` - Convert text to PDF
- `word_to_pdf.py` - Convert Word to PDF

## Usage

These scripts can still be used independently by running them directly:

```bash
python legacy_scripts/PDF_TO_WORD.py
```

**Note:** You'll need to edit the file paths directly in each script.

## Recommendation

For better user experience, please use the web application instead:
```bash
python app.py
```

Then access the application at `http://localhost:5000`
