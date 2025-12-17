import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './OperationPage.css';
import FileUploadDropzone from './FileUploadDropzone';
import OperationParamsForm from './OperationParamsForm';
import Toast from './Toast';
import { convertFiles, downloadFile } from '../api';

const OperationPage = ({ operation }) => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [toasts, setToasts] = useState([]);
  const [operationParams, setOperationParams] = useState({});

  const getIcon = (id) => {
    const icons = {
      pdf_to_word: '📄',
      pdf_to_text: '📝',
      pdf_to_images: '🖼️',
      word_to_pdf: '📑',
      text_to_pdf: '✍️',
      images_to_pdf: '📸',
      extract_images: '🎨',
      split_pdf: '✂️',
      merge_pdfs: '🔗',
      reverse_pdf: '↩️',
      compress_pdf: '🗜️',
      rotate_pdf: '🔄',
      add_watermark: '💧',
      remove_pages: '🗑️',
    };
    return icons[id] || '📋';
  };

  const addToast = (message, type = 'info') => {
    const id = Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  };

  const handleConvert = async () => {
    if (!selectedFiles.length) {
      addToast('Please select at least one file.', 'warning');
      return;
    }

    try {
      setLoading(true);
      addToast('Converting your file...', 'info');

      const result = await convertFiles(selectedFiles, operation.id, operationParams);

      if (result.success && result.download_url) {
        addToast('Conversion completed! Downloading...', 'success');
        
        const filename = result.download_url.split('/').pop();
        setTimeout(() => {
          downloadFile(filename);
        }, 500);

        setSelectedFiles([]);
        setOperationParams({});
      } else {
        addToast(result.error || 'Conversion failed.', 'error');
      }
    } catch (error) {
      addToast(`Error: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="operation-page">
      {/* Toast Container */}
      <div className="toast-container">
        {toasts.map(toast => (
          <Toast
            key={toast.id}
            message={toast.message}
            type={toast.type}
            onClose={() => setToasts(prev => prev.filter(t => t.id !== toast.id))}
            duration={3000}
          />
        ))}
      </div>

      {/* Header */}
      <div className="op-page-header">
        <Link to="/" className="back-btn">
          ← Back
        </Link>
        <div className="op-page-title">
          <div className="op-page-icon">{getIcon(operation.id)}</div>
          <div className="op-page-info">
            <h1>{operation.name}</h1>
            <p>{operation.description}</p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="op-page-container">
        <div className="op-page-content">
          {/* File Upload */}
          <div className="upload-section">
            <h2>Upload File</h2>
            <FileUploadDropzone
              onFilesSelected={setSelectedFiles}
              maxFiles={operation.multiple ? 10 : 1}
              accept={operation ? `.${operation.accepts.toLowerCase().replace(/\s+/g, ',.').toLowerCase()}` : '*'}
            />
          </div>

          {/* Parameters Form */}
          {operation.params && operation.params.length > 0 && (
            <OperationParamsForm
              operationId={operation.id}
              params={operation.params}
              onParamsChange={setOperationParams}
            />
          )}

          {/* Selected Files Info */}
          {selectedFiles.length > 0 && (
            <div className="files-info">
              <p className="files-count">
                ✓ {selectedFiles.length} file{selectedFiles.length !== 1 ? 's' : ''} selected
              </p>
            </div>
          )}

          {/* Convert Button */}
          <button
            className={`convert-btn ${loading ? 'loading' : ''}`}
            onClick={handleConvert}
            disabled={loading || !selectedFiles.length}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Converting...
              </>
            ) : (
              '🚀 Convert'
            )}
          </button>

          {/* Info Box */}
          <div className="info-box">
            <h3>📋 About this tool</h3>
            <p><strong>Input:</strong> {operation.accepts}</p>
            <p><strong>Output:</strong> {operation.produces}</p>
            {operation.multiple && (
              <p><strong>Supports:</strong> Multiple files</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OperationPage;
