# PDF Toolkit - Full Stack Application

A complete PDF and document conversion toolkit with a Python Flask backend and React frontend.

## Project Structure

```
Python_Toolkit/
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── utils/              # PDF conversion utilities
│   │   ├── pdf_converter.py
│   │   └── __init__.py
│   ├── uploads/            # Temporary upload directory
│   ├── outputs/            # Converted files directory
│   ├── requirements.txt     # Python dependencies
│   └── [various conversion scripts]
│
├── client/                  # React frontend
│   ├── public/             # Static assets
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── api.js          # API client
│   │   ├── App.js
│   │   ├── index.js
│   │   └── [CSS files]
│   ├── package.json
│   └── .env
│
├── legacy_scripts/         # Legacy Python scripts
├── venv/                   # Python virtual environment
└── [Config files]
```

## Features

### Available Operations
- **PDF to Word** - Convert PDF files to editable Word documents
- **PDF to Text** - Extract text content from PDFs
- **PDF to Images** - Convert PDF pages to image files (ZIP)
- **Word to PDF** - Convert Word documents to PDF
- **Text to PDF** - Convert text files to PDF
- **Images to PDF** - Combine multiple images into a single PDF
- **Extract Images** - Extract all images from a PDF (ZIP)
- **Reverse PDF** - Reverse the page order of a PDF
- **Merge PDFs** - Combine multiple PDF files into one

## Setup & Installation

### Prerequisites
- Python 3.8+ (backend)
- Node.js 14+ (frontend)
- npm or yarn (frontend package manager)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**
   ```bash
   python app.py
   ```
   Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to client directory:**
   ```bash
   cd client
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   Frontend will open at `http://localhost:3000`

## API Endpoints

### 1. Get Operations List
```
GET /api/operations
```
Returns all available conversion operations.

### 2. Convert Files
```
POST /api/convert
Content-Type: multipart/form-data

Parameters:
- files: File(s) to convert
- operation: Operation ID (e.g., 'pdf_to_text')
```

### 3. Download File
```
GET /api/download/{filename}
```
Download a converted file.

## Environment Variables

### Backend (.env)
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-in-production
```

### Frontend (client/.env)
```
REACT_APP_API_URL=http://localhost:5000
```

For production:
```
REACT_APP_API_URL=https://your-backend-domain.com
```

## Deployment

### Backend Deployment (Python Flask)
1. **Heroku:**
   ```bash
   git push heroku main
   ```

2. **AWS/DigitalOcean/Render:**
   - Deploy the `backend` folder
   - Set environment variables
   - Run `pip install -r requirements.txt`
   - Run `python app.py` or use a WSGI server (Gunicorn)

### Frontend Deployment (React)
1. **Build the React app:**
   ```bash
   cd client
   npm run build
   ```

2. **Deploy to static hosting:**
   - **Vercel:** Push to GitHub, connect repository to Vercel
   - **Netlify:** Push to GitHub, connect repository to Netlify
   - **AWS S3:** Upload `build` folder to S3
   - **Firebase Hosting:** Use Firebase CLI

3. **Update API URL:**
   - Modify `REACT_APP_API_URL` in `.env` to point to production backend

## Important Notes

### Deployment Strategy
- **Backend and Frontend deploy separately**
- Backend: Server (Heroku, Render, AWS, DigitalOcean, etc.)
- Frontend: Static hosting (Vercel, Netlify, S3, Firebase, etc.)
- Frontend communicates with backend via CORS-enabled REST API

### CORS Configuration
The Flask backend is configured with CORS enabled for all origins during development. For production:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-frontend-domain.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

### File Upload Limits
- Default: 50MB max file size
- Configured in `backend/app.py`: `MAX_CONTENT_LENGTH`

### Cleanup
- Uploaded and output files older than 1 hour are automatically deleted
- Cleanup runs every 30 minutes in a background thread

## Troubleshooting

### "Backend Disconnected" in UI
- Ensure Flask server is running on `http://localhost:5000`
- Check CORS configuration
- Verify `REACT_APP_API_URL` in client/.env

### PDF Conversion Fails
- Check that all required Python packages are installed
- Some operations (PDF to Word) may have library compatibility issues
- See error messages in browser console for details

### File Upload Issues
- Ensure `backend/uploads` and `backend/outputs` directories exist
- Check file size is under 50MB limit
- Verify file format matches operation requirements

## Development Workflow

1. **Start backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **In a new terminal, start frontend:**
   ```bash
   cd client
   npm start
   ```

3. **Make changes:**
   - Frontend: Edit files in `client/src/`
   - Backend: Edit files in `backend/`, restart server

4. **Test:**
   - Frontend hot-reloads automatically
   - Backend requires manual restart

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please create an issue in the repository.
