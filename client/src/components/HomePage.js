import React, { useState } from 'react';
import './HomePage.css';

const HomePage = ({ operations, onOperationSelect }) => {
  const [conversionDropdown, setConversionDropdown] = useState(false);
  const [allToolsDropdown, setAllToolsDropdown] = useState(false);

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
      pdf_to_powerpoint: '🎯',
      powerpoint_to_pdf: '📊',
      excel_to_pdf: '📈',
      add_page_numbers: '🔢',
      repair_pdf: '🔧',
    };
    return icons[id] || '📋';
  };

  // Organize operations
  const conversionOps = operations.filter(op => 
    ['pdf_to_word', 'pdf_to_text', 'pdf_to_images', 'word_to_pdf', 'text_to_pdf', 'images_to_pdf'].includes(op.id)
  );

  const handleNavClick = (opId) => {
    setConversionDropdown(false);
    setAllToolsDropdown(false);
    onOperationSelect(opId);
  };

  const OperationBox = ({ operation }) => (
    <div
      className="op-box"
      onClick={() => onOperationSelect(operation.id)}
      title={operation.description}
    >
      <div className="op-box-icon">{getIcon(operation.id)}</div>
      <div className="op-box-name">{operation.name}</div>
    </div>
  );

  const DropdownItem = ({ operation }) => (
    <div
      className="dropdown-item"
      onClick={() => handleNavClick(operation.id)}
    >
      <span className="dropdown-icon">{getIcon(operation.id)}</span>
      <span className="dropdown-name">{operation.name}</span>
    </div>
  );

  return (
    <div className="home-page">
      {/* Navigation Bar */}
      <nav className="nav-bar">
        <div className="nav-container">
          <div className="logo-nav">ProPDF</div>

          <button
            className="nav-link"
            onClick={() => handleNavClick('merge_pdfs')}
          >
            MERGE PDF
          </button>

          <button
            className="nav-link"
            onClick={() => handleNavClick('split_pdf')}
          >
            SPLIT PDF
          </button>

          <div className="nav-dropdown"
            onMouseEnter={() => setConversionDropdown(true)}
            onMouseLeave={() => setConversionDropdown(false)}
          >
            <button
              className="nav-link"
            >
              CONVERT PDF ▼
            </button>
            {conversionDropdown && (
              <div className="dropdown-menu">
                <div className="dropdown-section">
                  <div className="dropdown-section-title">CONVERT TO PDF</div>
                  {conversionOps
                    .filter(op => ['word_to_pdf', 'text_to_pdf', 'images_to_pdf'].includes(op.id))
                    .map(op => (
                      <DropdownItem key={op.id} operation={op} />
                    ))}
                </div>
                <div className="dropdown-section">
                  <div className="dropdown-section-title">CONVERT FROM PDF</div>
                  {conversionOps
                    .filter(op => ['pdf_to_word', 'pdf_to_text', 'pdf_to_images'].includes(op.id))
                    .map(op => (
                      <DropdownItem key={op.id} operation={op} />
                    ))}
                </div>
              </div>
            )}
          </div>

          <div className="nav-dropdown"
            onMouseEnter={() => setAllToolsDropdown(true)}
            onMouseLeave={() => setAllToolsDropdown(false)}
          >
            <button
              className="nav-link nav-all-tools"
            >
              ALL PDF TOOLS ▼
            </button>
            {allToolsDropdown && (
              <div className="dropdown-menu dropdown-menu-large">
                {operations
                  .filter(op => !['merge_pdfs', 'split_pdf', ...conversionOps.map(o => o.id)].includes(op.id))
                  .map(op => (
                    <DropdownItem key={op.id} operation={op} />
                  ))}
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <h1>Transform Your PDFs Instantly</h1>
          <p>Professional PDF tools with premium features. 100% free, no signup required. Get started in seconds!</p>
          <div className="hero-stats">
            <div className="stat">
              <span className="stat-number">14+</span>
              <span className="stat-label">Tools</span>
            </div>
            <div className="stat">
              <span className="stat-number">100%</span>
              <span className="stat-label">Free</span>
            </div>
            <div className="stat">
              <span className="stat-number">∞</span>
              <span className="stat-label">No Limits</span>
            </div>
          </div>

          {/* All Operations Grid */}
          <div className="op-boxes-grid">
            {operations.map(op => (
              <OperationBox key={op.id} operation={op} />
            ))}
          </div>
        </div>
        <div className="hero-background">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
          <div className="gradient-orb orb-3"></div>
        </div>
      </div>

      {/* Coming Soon */}
      <div className="coming-soon">
        <p>🚀 Coming soon: Edit PDF, OCR, Security tools, and premium features!</p>
      </div>
    </div>
  );
};

export default HomePage;
