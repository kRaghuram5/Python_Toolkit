import React, { useState, useEffect, useCallback } from 'react';
import './PDFConverter.css';
import HomePage from './HomePage';
import OperationPage from './OperationPage';
import Toast from './Toast';
import { getOperations, getApiStatus } from '../api';

const PDFConverter = () => {
  const [operations, setOperations] = useState([]);
  const [currentPage, setCurrentPage] = useState('home'); // 'home' or operation id
  const [apiStatus, setApiStatus] = useState(false);
  const [toasts, setToasts] = useState([]);

  const fetchOperations = useCallback(async () => {
    try {
      const ops = await getOperations();
      setOperations(ops);
    } catch (error) {
      addToast('Failed to load operations. Make sure backend is running.', 'error');
      console.error('Error:', error);
    }
  }, []);

  useEffect(() => {
    fetchOperations();
    checkApiStatus();
  }, [fetchOperations]);

  const checkApiStatus = async () => {
    const status = await getApiStatus();
    setApiStatus(status ? true : false);
  };

  const addToast = (message, type = 'info') => {
    const id = Math.random();
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== id));
    }, 3000);
  };

  const handleOperationSelect = (operationId) => {
    setCurrentPage(operationId);
  };

  const handleBack = () => {
    setCurrentPage('home');
  };

  const currentOperation = operations.find(op => op.id === currentPage);

  return (
    <div className="pdf-converter">
      {/* Header - Hidden when on home page, shown for operation pages */}
      {currentPage !== 'home' && (
        <header className="app-header">
          <div className="header-content">
            <div className="logo" onClick={() => setCurrentPage('home')}>
              <span className="logo-text">ProPDF</span>
            </div>
            <div className="header-status">
              {!apiStatus && (
                <div className={`api-status disconnected`}>
                  <span className="status-dot"></span>
                  Backend Disconnected
                </div>
              )}
            </div>
          </div>
        </header>
      )}

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

      {/* Main Content */}
      {currentPage === 'home' ? (
        <HomePage operations={operations} onOperationSelect={handleOperationSelect} />
      ) : currentOperation ? (
        <OperationPage operation={currentOperation} onBack={handleBack} />
      ) : (
        <div className="loading-page">Loading...</div>
      )}
    </div>
  );
};

export default PDFConverter;
