"""
PDF Toolkit Web Application
A Flask-based web application for various PDF operations
"""

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta
import threading
import time

# Import utility modules
from utils.pdf_converter import (
    pdf_to_word, pdf_to_text, pdf_to_images,
    word_to_pdf, text_to_pdf, images_to_pdf,
    extract_images_from_pdf, reverse_pdf, merge_pdfs,
    split_pdf, compress_pdf, rotate_pdf, add_watermark, remove_pages,
    pdf_to_powerpoint, powerpoint_to_pdf, excel_to_pdf, 
    add_page_numbers, repair_pdf
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'

# Enable CORS for API endpoints
CORS(app)

# Ensure required directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'pdf': ['pdf'],
    'word': ['doc', 'docx'],
    'text': ['txt'],
    'image': ['png', 'jpg', 'jpeg', 'bmp', 'gif']
}


def allowed_file(filename, file_type):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS.get(file_type, [])


def smart_rename_output(output_file, base_name):
    """Rename output file to use input filename with operation suffix"""
    if not output_file or not os.path.exists(output_file):
        return output_file
    
    try:
        # Get file extension
        _, ext = os.path.splitext(output_file)
        output_dir = os.path.dirname(output_file)
        
        # Create new filename with smart naming
        new_filename = f"{base_name}{ext}"
        new_filepath = os.path.join(output_dir, new_filename)
        
        # Handle filename conflicts by adding counter
        counter = 1
        while os.path.exists(new_filepath):
            name_parts = base_name.rsplit('_', 1)
            if len(name_parts) > 1 and name_parts[-1].isdigit():
                base_without_counter = name_parts[0]
            else:
                base_without_counter = base_name
            new_filename = f"{base_without_counter}_{counter}{ext}"
            new_filepath = os.path.join(output_dir, new_filename)
            counter += 1
        
        # Rename the file
        os.rename(output_file, new_filepath)
        return new_filepath
    except Exception as e:
        print(f"Error renaming file: {str(e)}")
        return output_file


def cleanup_old_files():
    """Remove files older than 1 hour from uploads and outputs folders"""
    while True:
        try:
            current_time = time.time()
            for folder in [app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        filepath = os.path.join(folder, filename)
                        if os.path.isfile(filepath):
                            file_age = current_time - os.path.getmtime(filepath)
                            if file_age > 3600:  # 1 hour
                                os.remove(filepath)
                                print(f"Deleted old file: {filepath}")
        except Exception as e:
            print(f"Error during cleanup: {str(e)}")
        
        time.sleep(1800)  # Run cleanup every 30 minutes


# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker and monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'PDF Toolkit API',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/')
def index():
    """API information endpoint"""
    return jsonify({
        'name': 'PDF Toolkit API',
        'version': '2.0',
        'description': 'RESTful API for PDF and document conversion operations',
        'endpoints': {
            'PDF Operations': {
                'POST /api/merge': 'Merge multiple PDFs',
                'POST /api/split': 'Split PDF (params: start_page, end_page)',
                'POST /api/compress': 'Compress PDF',
                'POST /api/rotate': 'Rotate PDF (param: rotation angle)',
                'POST /api/watermark': 'Add watermark (param: watermark text)',
                'POST /api/remove-pages': 'Remove pages (param: pages comma-separated)',
                'POST /api/add-page-numbers': 'Add page numbers',
                'POST /api/repair-pdf': 'Repair damaged PDF',
            },
            'Conversions': {
                'POST /api/pdf-to-word': 'Convert PDF to Word (.docx)',
                'POST /api/pdf-to-text': 'Convert PDF to Text (.txt)',
                'POST /api/pdf-to-powerpoint': 'Convert PDF to PowerPoint (.pptx)',
                'POST /api/word-to-pdf': 'Convert Word to PDF',
                'POST /api/text-to-pdf': 'Convert Text to PDF',
                'POST /api/powerpoint-to-pdf': 'Convert PowerPoint to PDF',
                'POST /api/excel-to-pdf': 'Convert Excel to PDF',
            },
            'Utilities': {
                'GET /api/download/<filename>': 'Download converted file',
                'GET /api/operations': 'Get list of available operations',
            }
        }
    })


@app.route('/api/convert', methods=['POST'])
def convert_file():
    """Handle file conversion requests"""
    try:
        # Check if files were uploaded
        if 'files' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        files = request.files.getlist('files')
        operation = request.form.get('operation')
        
        if not files or files[0].filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not operation:
            return jsonify({'error': 'No operation specified'}), 400
        
        # Generate unique identifier for this operation
        unique_id = str(uuid.uuid4())
        
        # Extract base filename from first file for smart naming
        base_filename = secure_filename(files[0].filename)
        base_name = os.path.splitext(base_filename)[0]  # Remove extension
        
        # Save uploaded files
        saved_files = []
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
            file.save(filepath)
            saved_files.append(filepath)
        
        # Perform the requested operation
        output_file = None
        
        if operation == 'pdf_to_word':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_word(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_word")
        
        elif operation == 'pdf_to_text':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_text(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_text")
        
        elif operation == 'pdf_to_images':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_images(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'word_to_pdf':
            if not allowed_file(saved_files[0], 'word'):
                return jsonify({'error': 'Invalid file type. Please upload a Word document.'}), 400
            output_file = word_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}")
        
        elif operation == 'text_to_pdf':
            if not allowed_file(saved_files[0], 'text'):
                return jsonify({'error': 'Invalid file type. Please upload a text file.'}), 400
            output_file = text_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}")
        
        elif operation == 'images_to_pdf':
            for file in saved_files:
                if not allowed_file(file, 'image'):
                    return jsonify({'error': 'Invalid file type. Please upload image files.'}), 400
            output_file = images_to_pdf(saved_files, app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'extract_images':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = extract_images_from_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'reverse_pdf':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = reverse_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_reversed")
        
        elif operation == 'merge_pdfs':
            for file in saved_files:
                if not allowed_file(file, 'pdf'):
                    return jsonify({'error': 'Invalid file type. Please upload PDF files only.'}), 400
            output_file = merge_pdfs(saved_files, app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_merged")
        
        elif operation == 'split_pdf':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            start_page = request.form.get('start_page', 1, type=int)
            end_page = request.form.get('end_page', 1, type=int)
            output_file = split_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id, start_page, end_page)
            output_file = smart_rename_output(output_file, f"{base_name}_split")
        
        elif operation == 'compress_pdf':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = compress_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_compressed")
        
        elif operation == 'rotate_pdf':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            rotation = request.form.get('rotation', 90, type=int)
            output_file = rotate_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id, rotation)
            output_file = smart_rename_output(output_file, f"{base_name}_rotated")
        
        elif operation == 'add_watermark':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            watermark_text = request.form.get('watermark', 'Watermark')
            output_file = add_watermark(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id, watermark_text)
            output_file = smart_rename_output(output_file, f"{base_name}_watermarked")
        
        elif operation == 'remove_pages':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            pages = request.form.get('pages', '1')
            pages_to_remove = [int(p.strip()) for p in pages.split(',') if p.strip()]
            output_file = remove_pages(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id, pages_to_remove)
            output_file = smart_rename_output(output_file, f"{base_name}_removed")
        
        elif operation == 'pdf_to_powerpoint':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_powerpoint(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_presentation")
        
        elif operation == 'powerpoint_to_pdf':
            if not allowed_file(saved_files[0], 'word'):
                return jsonify({'error': 'Invalid file type. Please upload a PowerPoint file.'}), 400
            output_file = powerpoint_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}")
        
        elif operation == 'excel_to_pdf':
            # Check for Excel files
            if '.' not in saved_files[0] or saved_files[0].rsplit('.', 1)[1].lower() not in ['xls', 'xlsx']:
                return jsonify({'error': 'Invalid file type. Please upload an Excel file.'}), 400
            output_file = excel_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}")
        
        elif operation == 'add_page_numbers':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = add_page_numbers(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_numbered")
        
        elif operation == 'repair_pdf':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = repair_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
            output_file = smart_rename_output(output_file, f"{base_name}_repaired")
        
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        if output_file and os.path.exists(output_file):
            return jsonify({
                'success': True,
                'message': 'Conversion completed successfully',
                'download_url': f'/api/download/{os.path.basename(output_file)}'
            })
        else:
            return jsonify({'error': 'Conversion failed'}), 500
    
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Handle file download requests"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500


# ===== SPECIFIC OPERATION ENDPOINTS =====

@app.route('/api/merge', methods=['POST'])
def merge():
    """Merge multiple PDF files"""
    try:
        if 'files' not in request.files or len(request.files.getlist('files')) < 2:
            return jsonify({'error': 'Please upload at least 2 PDF files'}), 400
        
        files = request.files.getlist('files')
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(files[0].filename))[0]
        
        saved_files = []
        for file in files:
            if allowed_file(file.filename, 'pdf'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
                file.save(filepath)
                saved_files.append(filepath)
        
        if not saved_files:
            return jsonify({'error': 'No valid PDF files uploaded'}), 400
        
        output_file = merge_pdfs(saved_files, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_merged")
        
        return jsonify({
            'success': True,
            'message': 'PDFs merged successfully',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error merging PDFs: {str(e)}")
        return jsonify({'error': f'Merge failed: {str(e)}'}), 500


@app.route('/api/split', methods=['POST'])
def split():
    """Split PDF pages"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        start_page = int(request.form.get('start_page', 1))
        end_page = int(request.form.get('end_page', 1))
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = split_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id, start_page, end_page)
        output_file = smart_rename_output(output_file, f"{base_name}_split")
        
        return jsonify({
            'success': True,
            'message': f'Pages {start_page}-{end_page} extracted',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error splitting PDF: {str(e)}")
        return jsonify({'error': f'Split failed: {str(e)}'}), 500


@app.route('/api/compress', methods=['POST'])
def compress():
    """Compress PDF file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = compress_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_compressed")
        
        return jsonify({
            'success': True,
            'message': 'PDF compressed successfully',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error compressing PDF: {str(e)}")
        return jsonify({'error': f'Compression failed: {str(e)}'}), 500


@app.route('/api/rotate', methods=['POST'])
def rotate():
    """Rotate PDF pages"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        rotation = int(request.form.get('rotation', 90))
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = rotate_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id, rotation)
        output_file = smart_rename_output(output_file, f"{base_name}_rotated")
        
        return jsonify({
            'success': True,
            'message': f'PDF rotated {rotation}°',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error rotating PDF: {str(e)}")
        return jsonify({'error': f'Rotation failed: {str(e)}'}), 500


@app.route('/api/watermark', methods=['POST'])
def watermark():
    """Add watermark to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        watermark_text = request.form.get('watermark', 'Watermark')
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = add_watermark(filepath, app.config['OUTPUT_FOLDER'], unique_id, watermark_text)
        output_file = smart_rename_output(output_file, f"{base_name}_watermarked")
        
        return jsonify({
            'success': True,
            'message': 'Watermark added',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error adding watermark: {str(e)}")
        return jsonify({'error': f'Watermark failed: {str(e)}'}), 500


@app.route('/api/remove-pages', methods=['POST'])
def remove():
    """Remove pages from PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        pages = request.form.get('pages', '1')
        pages_to_remove = [int(p.strip()) for p in pages.split(',') if p.strip()]
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = remove_pages(filepath, app.config['OUTPUT_FOLDER'], unique_id, pages_to_remove)
        output_file = smart_rename_output(output_file, f"{base_name}_removed")
        
        return jsonify({
            'success': True,
            'message': f'Pages {pages} removed',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error removing pages: {str(e)}")
        return jsonify({'error': f'Remove failed: {str(e)}'}), 500


@app.route('/api/pdf-to-word', methods=['POST'])
def pdf_to_word_endpoint():
    """Convert PDF to Word"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = pdf_to_word(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_word")
        
        return jsonify({
            'success': True,
            'message': 'PDF converted to Word',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to Word: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/pdf-to-text', methods=['POST'])
def pdf_to_text_endpoint():
    """Convert PDF to Text"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = pdf_to_text(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_text")
        
        return jsonify({
            'success': True,
            'message': 'PDF converted to Text',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to Text: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/word-to-pdf', methods=['POST'])
def word_to_pdf_endpoint():
    """Convert Word to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'word'):
            return jsonify({'error': 'Invalid file type. Upload .doc or .docx'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = word_to_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}")
        
        return jsonify({
            'success': True,
            'message': 'Word converted to PDF',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/text-to-pdf', methods=['POST'])
def text_to_pdf_endpoint():
    """Convert Text to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'text'):
            return jsonify({'error': 'Invalid file type. Upload .txt'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = text_to_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}")
        
        return jsonify({
            'success': True,
            'message': 'Text converted to PDF',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/pdf-to-powerpoint', methods=['POST'])
def pdf_to_powerpoint_endpoint():
    """Convert PDF to PowerPoint"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = pdf_to_powerpoint(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_presentation")
        
        return jsonify({
            'success': True,
            'message': 'PDF converted to PowerPoint',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to PowerPoint: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/powerpoint-to-pdf', methods=['POST'])
def powerpoint_to_pdf_endpoint():
    """Convert PowerPoint to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = powerpoint_to_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}")
        
        return jsonify({
            'success': True,
            'message': 'PowerPoint converted to PDF',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/excel-to-pdf', methods=['POST'])
def excel_to_pdf_endpoint():
    """Convert Excel to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = excel_to_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}")
        
        return jsonify({
            'success': True,
            'message': 'Excel converted to PDF',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error converting to PDF: {str(e)}")
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500


@app.route('/api/add-page-numbers', methods=['POST'])
def add_page_numbers_endpoint():
    """Add page numbers to PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = add_page_numbers(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_numbered")
        
        return jsonify({
            'success': True,
            'message': 'Page numbers added',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error adding page numbers: {str(e)}")
        return jsonify({'error': f'Failed: {str(e)}'}), 500


@app.route('/api/repair-pdf', methods=['POST'])
def repair_pdf_endpoint():
    """Repair damaged PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        unique_id = str(uuid.uuid4())
        base_name = os.path.splitext(secure_filename(file.filename))[0]
        
        if not allowed_file(file.filename, 'pdf'):
            return jsonify({'error': 'Invalid file type'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{file.filename}")
        file.save(filepath)
        
        output_file = repair_pdf(filepath, app.config['OUTPUT_FOLDER'], unique_id)
        output_file = smart_rename_output(output_file, f"{base_name}_repaired")
        
        return jsonify({
            'success': True,
            'message': 'PDF repaired',
            'download_url': f'/api/download/{os.path.basename(output_file)}'
        })
    except Exception as e:
        print(f"Error repairing PDF: {str(e)}")
        return jsonify({'error': f'Repair failed: {str(e)}'}), 500

@app.route('/api/operations')
def get_operations():
    """Return list of available operations"""
    operations = [
        {
            'id': 'pdf_to_word',
            'name': 'PDF to Word',
            'description': 'Convert PDF files to editable Word documents',
            'accepts': 'PDF',
            'produces': 'DOCX',
            'multiple': False
        },
        {
            'id': 'pdf_to_text',
            'name': 'PDF to Text',
            'description': 'Extract text content from PDF files',
            'accepts': 'PDF',
            'produces': 'TXT',
            'multiple': False
        },
        {
            'id': 'pdf_to_images',
            'name': 'PDF to Images',
            'description': 'Convert PDF pages to image files (ZIP)',
            'accepts': 'PDF',
            'produces': 'ZIP',
            'multiple': False
        },
        {
            'id': 'word_to_pdf',
            'name': 'Word to PDF',
            'description': 'Convert Word documents to PDF format',
            'accepts': 'DOCX',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'text_to_pdf',
            'name': 'Text to PDF',
            'description': 'Convert text files to PDF format',
            'accepts': 'TXT',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'images_to_pdf',
            'name': 'Images to PDF',
            'description': 'Combine multiple images into a single PDF',
            'accepts': 'Images',
            'produces': 'PDF',
            'multiple': True
        },
        {
            'id': 'extract_images',
            'name': 'Extract Images',
            'description': 'Extract all images from a PDF file (ZIP)',
            'accepts': 'PDF',
            'produces': 'ZIP',
            'multiple': False
        },
        {
            'id': 'reverse_pdf',
            'name': 'Reverse PDF',
            'description': 'Reverse the page order of a PDF file',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'merge_pdfs',
            'name': 'Merge PDFs',
            'description': 'Combine multiple PDF files into one',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': True
        },
        {
            'id': 'split_pdf',
            'name': 'Split PDF',
            'description': 'Extract a range of pages from a PDF',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False,
            'params': {'start_page': 'integer', 'end_page': 'integer'}
        },
        {
            'id': 'compress_pdf',
            'name': 'Compress PDF',
            'description': 'Reduce PDF file size while maintaining readability',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'rotate_pdf',
            'name': 'Rotate PDF',
            'description': 'Rotate all pages in a PDF (90°, 180°, 270°)',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False,
            'params': {'rotation': 'integer (90, 180, 270)'}
        },
        {
            'id': 'add_watermark',
            'name': 'Add Watermark',
            'description': 'Add text watermark to all PDF pages',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False,
            'params': {'watermark': 'string'}
        },
        {
            'id': 'remove_pages',
            'name': 'Remove Pages',
            'description': 'Remove specific pages from a PDF',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False,
            'params': {'pages': 'comma-separated page numbers (e.g., 1,3,5)'}
        },
        {
            'id': 'pdf_to_powerpoint',
            'name': 'PDF to PowerPoint',
            'description': 'Convert PDF pages to PowerPoint presentation',
            'accepts': 'PDF',
            'produces': 'PPTX',
            'multiple': False
        },
        {
            'id': 'powerpoint_to_pdf',
            'name': 'PowerPoint to PDF',
            'description': 'Convert PowerPoint presentation to PDF',
            'accepts': 'PPTX',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'excel_to_pdf',
            'name': 'Excel to PDF',
            'description': 'Convert Excel spreadsheet to PDF',
            'accepts': 'XLSX',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'add_page_numbers',
            'name': 'Add Page Numbers',
            'description': 'Add page numbers to PDF document',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False
        },
        {
            'id': 'repair_pdf',
            'name': 'Repair PDF',
            'description': 'Repair damaged or corrupt PDF files',
            'accepts': 'PDF',
            'produces': 'PDF',
            'multiple': False
        }
    ]
    return jsonify(operations)


if __name__ == '__main__':
    print("=" * 60)
    print("  PDF Toolkit Web Application")
    print("=" * 60)
    print("\n  🚀 Server starting...")
    print(f"  📂 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"  📁 Output folder: {app.config['OUTPUT_FOLDER']}")
    print(f"  🌐 Access the application at: http://localhost:5000")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
