# Quick Start Guide

## Project Overview

This is a **Full-Stack PDF Toolkit** with:
- **Backend:** Python Flask REST API with PDF/document conversion operations
- **Frontend:** Modern React UI with real-time feedback and drag-drop file upload

## Directory Structure

```
Python_Toolkit/
├── backend/                    # Python Flask API (Port 5000)
│   ├── app.py                 # Main Flask application
│   ├── utils/pdf_converter.py # All conversion logic
│   ├── uploads/               # Temp uploads
│   ├── outputs/               # Converted files
│   └── [conversion scripts]
│
├── client/                     # React Frontend (Port 3000)
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── api.js             # Backend API client
│   │   └── App.js
│   ├── package.json
│   └── .env (API_URL config)
│
└── [Config files]
```

## Installation & Running (Windows PowerShell)

### 1. Backend Setup

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on: `http://localhost:5000`

### 2. Frontend Setup (New PowerShell Terminal)

```powershell
cd client
npm install
npm start
```

Frontend opens at: `http://localhost:3000`

## Available Operations

| Operation | Input | Output | Notes |
|-----------|-------|--------|-------|
| PDF to Word | PDF | DOCX | Converts PDF to editable Word document |
| PDF to Text | PDF | TXT | Extracts text content from PDF |
| PDF to Images | PDF | ZIP | Converts pages to images (PNG) |
| Word to PDF | DOCX | PDF | Converts Word to PDF |
| Text to PDF | TXT | PDF | Converts text file to PDF |
| Images to PDF | PNG/JPG | PDF | Combines multiple images into PDF |
| Extract Images | PDF | ZIP | Extracts all images from PDF |
| Reverse PDF | PDF | PDF | Reverses page order |
| Merge PDFs | PDF(s) | PDF | Merges multiple PDFs |

## API Endpoints

```
GET  /                       # API info
GET  /api/operations         # List all operations
POST /api/convert            # Convert files
GET  /api/download/<file>    # Download converted file
```

## Environment Configuration

### Backend (.env or app.py)
```python
FLASK_ENV=development
MAX_CONTENT_LENGTH=50MB      # Max upload size
SECRET_KEY=your-secret-key
```

### Frontend (client/.env)
```
REACT_APP_API_URL=http://localhost:5000
```

For production:
```
REACT_APP_API_URL=https://your-api.com
```

## Deployment

### Backend
Deploy the `backend/` folder to:
- **Heroku** (free tier available)
- **Render.com** (free tier available)
- **Replit.com** (free tier available)
- **AWS Elastic Beanstalk**
- **DigitalOcean**
- **Railway.app**

### Frontend
Build and deploy to:
- **Vercel** (Recommended for Next.js/React)
- **Netlify** (GitHub integration)
- **AWS S3 + CloudFront**
- **Firebase Hosting**

### Steps

1. **Build frontend:**
   ```bash
   cd client
   npm run build
   ```

2. **Deploy backend** to server with environment variables

3. **Update frontend API URL** in `client/.env` to production backend

4. **Deploy frontend** build folder to static hosting

## Features

✅ **Drag & Drop Upload** - Intuitive file selection
✅ **Real-time Progress** - Visual feedback during conversion
✅ **Multiple File Support** - For merge and image operations
✅ **Error Handling** - Clear error messages
✅ **Auto Cleanup** - Old files removed every 1 hour
✅ **CORS Enabled** - Works with separate frontend
✅ **Responsive Design** - Works on mobile and desktop

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend Disconnected | Check Flask is running on port 5000 |
| CORS Error | Ensure Flask-CORS is installed |
| Large File Upload | Check MAX_CONTENT_LENGTH in app.py (default 50MB) |
| PDF to Word fails | PyMuPDF version conflict - use PDF to Text instead |
| Port Already in Use | Change port in app.py or close existing process |

## Development Workflow

1. **Terminal 1 - Backend:**
   ```bash
   cd backend && python app.py
   ```

2. **Terminal 2 - Frontend:**
   ```bash
   cd client && npm start
   ```

3. **Edit code** - Both hot-reload automatically (frontend requires page refresh sometimes)

4. **Test** - UI at localhost:3000, API at localhost:5000

## Performance Notes

- **Max upload:** 50MB (configurable)
- **Auto cleanup:** Files older than 1 hour deleted
- **Processing:** Depends on file size and operation
- **Memory:** Monitor for large batch operations

## Security Considerations

⚠️ **Development Mode**: Change SECRET_KEY in production
⚠️ **CORS**: Restrict to your domain in production
⚠️ **File Upload**: Validate file types on backend
⚠️ **No Authentication**: Add user auth for production use

## Next Steps

1. ✅ Run both servers
2. ✅ Test conversions in UI
3. ✅ Deploy backend to server
4. ✅ Build and deploy frontend
5. ✅ Update API URL for production
6. ✅ Add authentication (optional)
7. ✅ Add monitoring/logging (optional)

## Support & Updates

- Check browser console for errors
- Check Flask console for backend errors
- Review error messages displayed in UI
- See logs in uploads/outputs folders

---

**Happy Converting! 🎉**
