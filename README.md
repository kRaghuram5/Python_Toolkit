# 🚀 PDF Toolkit - Universal File Converter

A powerful, modern web application for PDF operations built with Flask and Python. Convert, merge, extract, and modify PDF files with an intuitive drag-and-drop interface.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### 📄 PDF Conversions
- **PDF to Word** - Convert PDF files to editable Word documents (.docx)
- **PDF to Text** - Extract text content from PDF files
- **PDF to Images** - Convert each PDF page into high-quality images (PNG)

### 📝 Document to PDF
- **Word to PDF** - Convert Word documents to PDF format
- **Text to PDF** - Transform plain text files into formatted PDFs
- **Images to PDF** - Combine multiple images into a single PDF document

### 🔧 PDF Operations
- **Extract Images** - Extract all embedded images from PDF files
- **Reverse PDF** - Reverse the page order of any PDF document
- **Merge PDFs** - Combine multiple PDF files into one document

## 🎨 User Interface

- **Modern & Intuitive** - Beautiful gradient design with smooth animations
- **Drag & Drop** - Simply drag files to upload them
- **Real-time Progress** - Track your conversion progress
- **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **No Installation Required** - Just run and access via browser

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PDF Processing**: PyPDF2, PyMuPDF (Fitz), pdf2docx
- **Image Processing**: Pillow (PIL)
- **Document Generation**: ReportLab

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- For Word to PDF conversion (Windows): Microsoft Word installed OR docx2pdf package

## 🚀 Quick Start

### Method 1: Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/kRaghuram5/Python_Toolkit.git
   cd Python_Toolkit
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Start the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   ```
   Navigate to: http://localhost:5000
   ```

### Method 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kRaghuram5/Python_Toolkit.git
   cd Python_Toolkit
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   # Copy the example environment file
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   ```
   Open http://localhost:5000 in your browser
   ```

## 📁 Project Structure

```
Python_Toolkit/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup script
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── utils/                 # Utility modules
│   ├── __init__.py
│   └── pdf_converter.py   # PDF conversion functions
│
├── static/                # Static files (CSS, JS, images)
│   ├── style.css          # Application styles
│   └── script.js          # Frontend JavaScript
│
├── templates/             # HTML templates
│   └── index.html         # Main page template
│
├── uploads/               # Temporary uploaded files (auto-created)
└── outputs/               # Converted files (auto-created)
```

## 🔧 Configuration

### Environment Variables

Edit the `.env` file to configure the application:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Server Configuration
HOST=0.0.0.0
PORT=5000

# File Upload Configuration
MAX_CONTENT_LENGTH=52428800  # 50MB
UPLOAD_FOLDER=uploads
OUTPUT_FOLDER=outputs

# File Cleanup
FILE_RETENTION_TIME=3600  # 1 hour in seconds
```

## 🌐 API Endpoints

### Get Available Operations
```
GET /api/operations
```
Returns a list of all available conversion operations.

### Convert Files
```
POST /api/convert
```
**Form Data:**
- `files`: File(s) to convert
- `operation`: Operation ID (e.g., 'pdf_to_word')

### Download File
```
GET /api/download/<filename>
```
Download the converted file.

## 🐳 Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads outputs

EXPOSE 5000

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t pdf-toolkit .
docker run -p 5000:5000 pdf-toolkit
```

## ☁️ Deployment Options

### 1. Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create your-app-name

# Add buildpack
heroku buildpacks:add --index 1 heroku/python

# Deploy
git push heroku main
```

### 2. AWS EC2

1. Launch an EC2 instance (Ubuntu recommended)
2. SSH into the instance
3. Install Python and dependencies
4. Clone the repository
5. Run the application with gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### 3. DigitalOcean App Platform

1. Connect your GitHub repository
2. Select Python as the environment
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `python app.py`
5. Deploy!

### 4. Render

1. Create a new Web Service
2. Connect your GitHub repository
3. Set environment to Python 3
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app:app`

### 5. PythonAnywhere

1. Create a free account
2. Upload your code
3. Create a new web app
4. Configure WSGI file
5. Install requirements in console

## 🔒 Security Considerations

- Files are automatically deleted after 1 hour
- Maximum file size is limited to 50MB
- CORS is enabled (configure as needed for production)
- Change the SECRET_KEY in production
- Use HTTPS in production
- Consider implementing user authentication
- Add rate limiting for API endpoints

## 🎯 Usage Examples

### Convert PDF to Word
1. Select "PDF to Word" operation
2. Upload your PDF file
3. Click "Convert Now"
4. Download the generated Word document

### Merge Multiple PDFs
1. Select "Merge PDFs" operation
2. Upload multiple PDF files
3. Click "Convert Now"
4. Download the merged PDF

### Extract Images from PDF
1. Select "Extract Images" operation
2. Upload your PDF file
3. Click "Convert Now"
4. Download the ZIP file containing all images

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do / Future Enhancements

- [ ] Add user authentication
- [ ] Implement file compression options
- [ ] Add PDF encryption/decryption
- [ ] Support for more file formats (Excel, PowerPoint)
- [ ] Batch processing with progress tracking
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] PDF editing features (rotate, crop, add watermark)
- [ ] API key system for developers
- [ ] Mobile app version

## 🐛 Known Issues

- Word to PDF conversion requires Microsoft Word on Windows (or use docx2pdf as fallback)
- Large PDF files may take longer to process
- Some complex PDF formatting might not be preserved perfectly in conversions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**kRaghuram5**
- GitHub: [@kRaghuram5](https://github.com/kRaghuram5)

## 🙏 Acknowledgments

- PyPDF2 for PDF manipulation
- PyMuPDF (Fitz) for PDF rendering
- pdf2docx for PDF to Word conversion
- Flask community for excellent documentation
- All contributors and users of this project

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/kRaghuram5/Python_Toolkit/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your problem

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

**Made with ❤️ by kRaghuram5** 
