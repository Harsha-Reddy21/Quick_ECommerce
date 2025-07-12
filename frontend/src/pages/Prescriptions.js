import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import './Prescriptions.css';

const Prescriptions = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploadingFile, setUploadingFile] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/prescriptions' } });
      return;
    }
    
    fetchPrescriptions();
  }, [isAuthenticated, navigate]);

  const fetchPrescriptions = async () => {
    try {
      const response = await api.get('/prescriptions');
      setPrescriptions(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch prescriptions');
      setLoading(false);
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadPrescription = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      setMessage({ text: 'Please select a file to upload', type: 'error' });
      return;
    }
    
    setUploadingFile(true);
    
    try {
      const formData = new FormData();
      formData.append('prescription_file', selectedFile);
      
      await api.post('/prescriptions/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      // Refresh prescriptions list
      fetchPrescriptions();
      setSelectedFile(null);
      
      // Reset file input
      document.getElementById('prescription-file').value = '';
      
      setMessage({ text: 'Prescription uploaded successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      let errorMsg = 'Failed to upload prescription';
      
      if (err.response && err.response.data && err.response.data.detail) {
        errorMsg = err.response.data.detail;
      }
      
      setMessage({ text: errorMsg, type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } finally {
      setUploadingFile(false);
    }
  };

  const deletePrescription = async (prescriptionId) => {
    try {
      await api.delete(`/prescriptions/${prescriptionId}`);
      
      // Update local state
      setPrescriptions(prev => prev.filter(p => p.id !== prescriptionId));
      
      setMessage({ text: 'Prescription deleted successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ text: 'Failed to delete prescription', type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'pending':
        return 'status-pending';
      case 'approved':
        return 'status-approved';
      case 'rejected':
        return 'status-rejected';
      default:
        return '';
    }
  };

  if (loading) return <div className="loading">Loading prescriptions...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="prescriptions-container">
      <h1>My Prescriptions</h1>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      <div className="upload-section">
        <h2>Upload New Prescription</h2>
        <form onSubmit={uploadPrescription} className="upload-form">
          <div className="form-group">
            <label htmlFor="prescription-file">Select Prescription File</label>
            <input
              type="file"
              id="prescription-file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={handleFileChange}
              required
            />
            <p className="file-formats">
              Accepted formats: PDF, JPG, JPEG, PNG
            </p>
          </div>
          
          <button 
            type="submit" 
            className="upload-button"
            disabled={uploadingFile || !selectedFile}
          >
            {uploadingFile ? 'Uploading...' : 'Upload Prescription'}
          </button>
        </form>
      </div>
      
      <div className="prescriptions-section">
        <h2>Your Prescriptions</h2>
        
        {prescriptions.length === 0 ? (
          <div className="no-prescriptions">
            <p>You haven't uploaded any prescriptions yet.</p>
          </div>
        ) : (
          <div className="prescriptions-list">
            {prescriptions.map(prescription => (
              <div className="prescription-card" key={prescription.id}>
                <div className="prescription-header">
                  <div className="prescription-filename">
                    {prescription.filename}
                  </div>
                  <div className={`prescription-status ${getStatusClass(prescription.status)}`}>
                    {prescription.status.charAt(0).toUpperCase() + prescription.status.slice(1)}
                  </div>
                </div>
                
                <div className="prescription-details">
                  <div className="prescription-date">
                    <span>Uploaded on:</span> {formatDate(prescription.created_at)}
                  </div>
                  
                  {prescription.verified_at && (
                    <div className="prescription-verified">
                      <span>Verified on:</span> {formatDate(prescription.verified_at)}
                    </div>
                  )}
                  
                  {prescription.status === 'rejected' && prescription.rejection_reason && (
                    <div className="rejection-reason">
                      <span>Rejection Reason:</span> {prescription.rejection_reason}
                    </div>
                  )}
                </div>
                
                <div className="prescription-actions">
                  <a 
                    href={prescription.file_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="view-button"
                  >
                    View
                  </a>
                  
                  {prescription.status !== 'approved' && (
                    <button 
                      className="delete-button"
                      onClick={() => deletePrescription(prescription.id)}
                    >
                      Delete
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      
      <div className="prescription-guidelines">
        <h3>Prescription Guidelines</h3>
        <ul>
          <li>Upload a clear, legible image or PDF of your prescription</li>
          <li>Ensure the doctor's signature and details are visible</li>
          <li>Prescriptions are typically verified within 30 minutes</li>
          <li>Approved prescriptions are valid for purchases requiring prescriptions</li>
          <li>If your prescription is rejected, please upload a clearer image or contact support</li>
        </ul>
      </div>
    </div>
  );
};

export default Prescriptions; 