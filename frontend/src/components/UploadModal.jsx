import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, X, File as FileIcon, CheckCircle, AlertCircle } from 'lucide-react';
import './UploadModal.css';

const UploadModal = ({ isOpen, onClose, onUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const inputRef = useRef(null);

  if (!isOpen) return null;

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateAndSetFile = (selectedFiles) => {
    setError(null);
    setSuccess(false);
    if (!selectedFiles || selectedFiles.length === 0) return;
    
    const validFiles = Array.from(selectedFiles).filter(f => f.name.endsWith('.pdf') || f.name.endsWith('.docx'));
    if (validFiles.length > 0) {
      setFiles(prev => [...prev, ...validFiles]);
    }
    if (validFiles.length !== selectedFiles.length) {
      setError('Some files were ignored. Only PDF and DOCX files are supported.');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files);
    }
  };

  const onButtonClick = () => {
    inputRef.current.click();
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    
    setUploading(true);
    setError(null);
    
    const formData = new FormData();
    files.forEach(f => formData.append('files', f));

    try {
      await axios.post('/api/resumes/upload_bulk', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setSuccess(true);
      setTimeout(() => {
        onUploadSuccess();
        handleClose();
      }, 2000);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Failed to upload resumes.');
    } finally {
      setUploading(false);
    }
  };

  const handleClose = () => {
    setFiles([]);
    setError(null);
    setSuccess(false);
    setDragActive(false);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content glass">
        <button className="close-button" onClick={handleClose}>
          <X size={24} />
        </button>
        
        <h2>Upload Candidate Resume</h2>
        <p className="modal-subtitle">AI will automatically parse skills and experience.</p>
        
        <div 
          className={`drop-zone ${dragActive ? 'drag-active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={onButtonClick}
        >
          <input
            ref={inputRef}
            type="file"
            multiple
            className="file-input-hidden"
            accept=".pdf,.docx"
            onChange={handleChange}
          />
          
          {files.length === 0 ? (
            <div className="drop-content">
              <Upload size={48} className="upload-icon" />
              <p>Drag and drop your files here</p>
              <span className="upload-btn">Browse Files</span>
              <p className="file-hint">Supports PDF and DOCX</p>
            </div>
          ) : (
            <div className="files-selected-list">
              {files.map((f, i) => (
                <div key={i} className="file-selected">
                  <FileIcon size={24} className="file-icon" />
                  <p className="file-name">{f.name}</p>
                  <button 
                    className="remove-file"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFiles(prev => prev.filter((_, idx) => idx !== i));
                    }}
                  >
                    <X size={16} />
                  </button>
                </div>
              ))}
              <div className="add-more-files" onClick={(e) => {
                  e.stopPropagation();
                  onButtonClick();
              }}>
                 + Add more files
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="alert error">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="alert success">
            <CheckCircle size={20} />
            <span>Successfully parsed and added candidate!</span>
          </div>
        )}

        <button 
          className={`submit-button ${files.length === 0 || uploading || success ? 'disabled' : ''}`}
          onClick={handleUpload}
          disabled={files.length === 0 || uploading || success}
        >
          {uploading ? (
            <span className="loading-text">
              <div className="spinner-small"></div>
              Analyzing {files.length} resume{files.length !== 1 ? 's' : ''} with AI...
            </span>
          ) : (
            `Process ${files.length} Resume${files.length !== 1 ? 's' : ''}`
          )}
        </button>
      </div>
    </div>
  );
};

export default UploadModal;
