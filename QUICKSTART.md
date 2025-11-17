# 🚀 Quick Start Guide - PDF Toolkit

Get up and running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher
- ✅ pip (Python package manager)
- ✅ Git (optional, for cloning)

Check your Python version:
```bash
python --version
```

## Installation (Choose One Method)

### 🎯 Method 1: Automatic Setup (Easiest - Recommended)

```bash
# 1. Download/Clone the repository
git clone https://github.com/kRaghuram5/Python_Toolkit.git
cd Python_Toolkit

# 2. Run setup script
python setup.py

# 3. Start the application
python app.py

# 4. Open browser
# Navigate to: http://localhost:5000
```

That's it! 🎉

---

### 🛠️ Method 2: Manual Setup

```bash
# 1. Clone repository
git clone https://github.com/kRaghuram5/Python_Toolkit.git
cd Python_Toolkit

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# On Windows (CMD):
venv\Scripts\activate.bat
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Copy environment file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# 6. Run application
python app.py

# 7. Open browser
# Navigate to: http://localhost:5000
```

---

## 🎮 Using the Application

### Step 1: Choose Operation
- Click on any operation card (e.g., "PDF to Word")

### Step 2: Upload Files
- Drag and drop your file(s) into the upload area, OR
- Click "Browse Files" to select files

### Step 3: Convert
- Click the "Convert Now" button
- Wait for processing to complete

### Step 4: Download
- Click "Download File" to save your converted file
- Click "Convert Another File" to start over

---

## 📋 Available Operations

| Operation | Input | Output | Multiple Files? |
|-----------|-------|--------|-----------------|
| PDF to Word | PDF | DOCX | No |
| PDF to Text | PDF | TXT | No |
| PDF to Images | PDF | ZIP (Images) | No |
| Word to PDF | DOCX | PDF | No |
| Text to PDF | TXT | PDF | No |
| Images to PDF | Images | PDF | Yes |
| Extract Images | PDF | ZIP (Images) | No |
| Reverse PDF | PDF | PDF | No |
| Merge PDFs | PDF | PDF | Yes |

---

## ⚙️ Configuration

### Change Port
Edit `.env` file:
```env
PORT=8000  # Change from 5000 to 8000
```

### Change Upload Size Limit
Edit `.env` file:
```env
MAX_CONTENT_LENGTH=104857600  # 100MB in bytes
```

### Enable/Disable Debug Mode
Edit `.env` file:
```env
DEBUG=False  # Set to False for production
```

---

## 🔧 Troubleshooting

### Problem: Port 5000 already in use
**Solution:**
```bash
# Change port in .env file to 8000 or any other port
# OR find and kill process using port 5000
```

### Problem: Module not found errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Problem: Permission denied for uploads/outputs
**Solution:**
```bash
# On Windows (PowerShell as Admin)
icacls uploads /grant Users:F
icacls outputs /grant Users:F

# On macOS/Linux
chmod 755 uploads outputs
```

### Problem: Word to PDF not working
**Solution:**
The application will try to use `docx2pdf` (cross-platform). If that doesn't work:
- On Windows: Install Microsoft Word
- On macOS/Linux: Install LibreOffice

---

## 📱 Accessing from Other Devices

To access the application from other devices on your network:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   
   # macOS/Linux
   ifconfig
   ```

2. On other devices, navigate to:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```

Example: `http://192.168.1.100:5000`

---

## 🛑 Stopping the Application

Press `Ctrl + C` in the terminal where the app is running.

---

## 🚀 Next Steps

- **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contribute**: See [CONTRIBUTING.md](CONTRIBUTING.md)
- **Report Issues**: [GitHub Issues](https://github.com/kRaghuram5/Python_Toolkit/issues)

---

## 💡 Tips

1. **Files are automatically deleted after 1 hour** for security
2. **Maximum file size is 50MB** by default
3. **Use modern browsers** (Chrome, Firefox, Edge) for best experience
4. **Keep the terminal window open** while using the application

---

## 📞 Need Help?

- 📖 Read the full [README.md](README.md)
- 🐛 Report bugs on [GitHub Issues](https://github.com/kRaghuram5/Python_Toolkit/issues)
- 💬 Check existing issues for solutions

---

**Happy Converting! 🎉**
