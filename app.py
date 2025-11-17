"""
PDF Toolkit Web Application
A Flask-based web application for various PDF operations
"""

from flask import Flask, render_template, request, send_file, jsonify, flash
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
    extract_images_from_pdf, reverse_pdf, merge_pdfs
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
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

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


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


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
        
        elif operation == 'pdf_to_text':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_text(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'pdf_to_images':
            if not allowed_file(saved_files[0], 'pdf'):
                return jsonify({'error': 'Invalid file type. Please upload a PDF file.'}), 400
            output_file = pdf_to_images(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'word_to_pdf':
            if not allowed_file(saved_files[0], 'word'):
                return jsonify({'error': 'Invalid file type. Please upload a Word document.'}), 400
            output_file = word_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
        elif operation == 'text_to_pdf':
            if not allowed_file(saved_files[0], 'text'):
                return jsonify({'error': 'Invalid file type. Please upload a text file.'}), 400
            output_file = text_to_pdf(saved_files[0], app.config['OUTPUT_FOLDER'], unique_id)
        
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
        
        elif operation == 'merge_pdfs':
            for file in saved_files:
                if not allowed_file(file, 'pdf'):
                    return jsonify({'error': 'Invalid file type. Please upload PDF files only.'}), 400
            output_file = merge_pdfs(saved_files, app.config['OUTPUT_FOLDER'], unique_id)
        
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
