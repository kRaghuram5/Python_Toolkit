import React from 'react';
import './OperationParamsForm.css';

const OperationParamsForm = ({ operation, params, onChange }) => {
  if (!operation.params) return null;

  const handleChange = (paramName, value) => {
    onChange({
      ...params,
      [paramName]: value,
    });
  };

  return (
    <div className="section">
      <h2>⚙️ Step 3: Configure Options</h2>
      <div className="params-form">
        {operation.id === 'split_pdf' && (
          <>
            <div className="form-group">
              <label htmlFor="start_page">Start Page:</label>
              <input
                id="start_page"
                type="number"
                min="1"
                value={params.start_page || 1}
                onChange={(e) => handleChange('start_page', e.target.value)}
                placeholder="1"
              />
            </div>
            <div className="form-group">
              <label htmlFor="end_page">End Page:</label>
              <input
                id="end_page"
                type="number"
                min="1"
                value={params.end_page || 1}
                onChange={(e) => handleChange('end_page', e.target.value)}
                placeholder="1"
              />
            </div>
          </>
        )}

        {operation.id === 'rotate_pdf' && (
          <div className="form-group">
            <label htmlFor="rotation">Rotation Angle:</label>
            <select
              id="rotation"
              value={params.rotation || 90}
              onChange={(e) => handleChange('rotation', e.target.value)}
            >
              <option value="90">90° (Clockwise)</option>
              <option value="180">180° (Flip)</option>
              <option value="270">270° (Counter-clockwise)</option>
            </select>
          </div>
        )}

        {operation.id === 'add_watermark' && (
          <div className="form-group">
            <label htmlFor="watermark">Watermark Text:</label>
            <input
              id="watermark"
              type="text"
              maxLength="100"
              value={params.watermark || 'Watermark'}
              onChange={(e) => handleChange('watermark', e.target.value)}
              placeholder="Enter watermark text"
            />
            <small>Leave empty for default watermark</small>
          </div>
        )}

        {operation.id === 'remove_pages' && (
          <div className="form-group">
            <label htmlFor="pages">Pages to Remove (comma-separated):</label>
            <input
              id="pages"
              type="text"
              value={params.pages || ''}
              onChange={(e) => handleChange('pages', e.target.value)}
              placeholder="e.g., 1,3,5"
            />
            <small>Example: Enter "2,5,8" to remove pages 2, 5, and 8</small>
          </div>
        )}
      </div>
    </div>
  );
};

export default OperationParamsForm;
