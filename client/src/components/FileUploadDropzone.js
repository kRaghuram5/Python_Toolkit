import React, { useState, useRef } from 'react';
import './FileUploadDropzone.css';

const FileUploadDropzone = ({ onFilesSelected, maxFiles = 10, accept = '*' }) => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files).slice(0, maxFiles);
    handleFilesChange(droppedFiles);
  };

  const handleFilesChange = (selectedFiles) => {
    setFiles(selectedFiles);
    onFilesSelected(selectedFiles);
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleInputChange = (e) => {
    const selectedFiles = Array.from(e.target.files).slice(0, maxFiles);
    handleFilesChange(selectedFiles);
  };

  const removeFile = (index) => {
    const newFiles = files.filter((_, i) => i !== index);
    handleFilesChange(newFiles);
  };

  return (
    <div className="file-upload-container">
      <div
        className={`dropzone ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <div className="dropzone-content">
          <svg className="dropzone-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="7 10 12 15 17 10"></polyline>
            <line x1="12" y1="15" x2="12" y2="3"></line>
          </svg>
          <p className="dropzone-text">Drag & drop your files here</p>
          <p className="dropzone-subtext">or click to browse</p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          onChange={handleInputChange}
          accept={accept}
          style={{ display: 'none' }}
        />
      </div>

      {files.length > 0 && (
        <div className="file-list">
          <h4>Selected Files ({files.length})</h4>
          <ul>
            {files.map((file, index) => (
              <li key={index} className="file-item">
                <span className="file-name">{file.name}</span>
                <span className="file-size">({(file.size / 1024).toFixed(2)} KB)</span>
                <button
                  className="remove-btn"
                  onClick={() => removeFile(index)}
                  title="Remove file"
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUploadDropzone;
