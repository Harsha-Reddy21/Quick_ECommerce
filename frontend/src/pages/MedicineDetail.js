import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import './MedicineDetail.css';

const MedicineDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useContext(AuthContext);
  
  const [medicine, setMedicine] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [addingToCart, setAddingToCart] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    const fetchMedicine = async () => {
      try {
        const response = await api.get(`/medicines/${id}`);
        setMedicine(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch medicine details');
        setLoading(false);
      }
    };

    fetchMedicine();
  }, [id]);

  const handleQuantityChange = (e) => {
    const value = parseInt(e.target.value);
    if (value > 0 && value <= (medicine?.stock || 1)) {
      setQuantity(value);
    }
  };

  const addToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: `/medicines/${id}` } });
      return;
    }

    setAddingToCart(true);
    
    try {
      await api.post('/cart/add', {
        medicine_id: medicine.id,
        quantity: quantity
      });
      
      setMessage({ text: 'Added to cart successfully!', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      let errorMsg = 'Failed to add to cart';
      
      if (err.response && err.response.data && err.response.data.detail) {
        errorMsg = err.response.data.detail;
      }
      
      setMessage({ text: errorMsg, type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 5000);
    } finally {
      setAddingToCart(false);
    }
  };

  if (loading) return <div className="loading">Loading medicine details...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!medicine) return <div className="error">Medicine not found</div>;

  return (
    <div className="medicine-detail-container">
      <div className="medicine-detail-grid">
        <div className="medicine-image-container">
          <img 
            src={medicine.image_url || '/images/medicine-placeholder.jpg'} 
            alt={medicine.name} 
            className="medicine-detail-image"
          />
        </div>
        
        <div className="medicine-detail-info">
          <h1>{medicine.name}</h1>
          
          <div className="medicine-category">
            Category: <span>{medicine.category_name || 'General'}</span>
          </div>
          
          <div className="medicine-price-detail">
            ${medicine.price.toFixed(2)}
          </div>
          
          <div className={`medicine-stock-detail ${medicine.stock > 10 ? 'in-stock' : 'low-stock'}`}>
            {medicine.stock > 0 ? `${medicine.stock} in stock` : 'Out of stock'}
          </div>
          
          {medicine.requires_prescription && (
            <div className="prescription-warning">
              <i className="fas fa-prescription"></i>
              This medicine requires a valid prescription
            </div>
          )}
          
          <div className="medicine-description-detail">
            <h3>Description</h3>
            <p>{medicine.description}</p>
          </div>
          
          {medicine.dosage_instructions && (
            <div className="medicine-dosage">
              <h3>Dosage Instructions</h3>
              <p>{medicine.dosage_instructions}</p>
            </div>
          )}
          
          {medicine.side_effects && (
            <div className="medicine-side-effects">
              <h3>Possible Side Effects</h3>
              <p>{medicine.side_effects}</p>
            </div>
          )}
          
          <div className="add-to-cart-section">
            <div className="quantity-selector">
              <label htmlFor="quantity">Quantity:</label>
              <input
                type="number"
                id="quantity"
                min="1"
                max={medicine.stock}
                value={quantity}
                onChange={handleQuantityChange}
              />
            </div>
            
            <button 
              className="add-to-cart-button"
              onClick={addToCart}
              disabled={addingToCart || medicine.stock === 0}
            >
              {addingToCart ? 'Adding...' : 'Add to Cart'}
            </button>
          </div>
          
          {message.text && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicineDetail; 