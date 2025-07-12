import React, { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import './Cart.css';

const Cart = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [updating, setUpdating] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [prescriptionNeeded, setPrescriptionNeeded] = useState(false);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/cart' } });
      return;
    }
    
    fetchCartItems();
  }, [isAuthenticated, navigate]);

  const fetchCartItems = async () => {
    try {
      const response = await api.get('/cart');
      setCartItems(response.data.items);
      setPrescriptionNeeded(response.data.items.some(item => item.requires_prescription));
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch cart items');
      setLoading(false);
    }
  };

  const updateQuantity = async (itemId, newQuantity) => {
    if (newQuantity < 1) return;
    
    setUpdating(true);
    
    try {
      await api.put('/cart/update', {
        cart_item_id: itemId,
        quantity: newQuantity
      });
      
      // Update local state
      setCartItems(prevItems => 
        prevItems.map(item => 
          item.id === itemId ? { ...item, quantity: newQuantity } : item
        )
      );
    } catch (err) {
      setMessage({ 
        text: 'Failed to update quantity', 
        type: 'error' 
      });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } finally {
      setUpdating(false);
    }
  };

  const removeItem = async (itemId) => {
    setUpdating(true);
    
    try {
      await api.delete(`/cart/remove/${itemId}`);
      
      // Update local state
      setCartItems(prevItems => prevItems.filter(item => item.id !== itemId));
      
      // Check if any remaining items require prescription
      const stillNeedsPrescription = cartItems
        .filter(item => item.id !== itemId)
        .some(item => item.requires_prescription);
      
      setPrescriptionNeeded(stillNeedsPrescription);
      
      setMessage({ 
        text: 'Item removed from cart', 
        type: 'success' 
      });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ 
        text: 'Failed to remove item', 
        type: 'error' 
      });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } finally {
      setUpdating(false);
    }
  };

  const calculateTotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const proceedToCheckout = () => {
    navigate('/checkout');
  };

  if (loading) return <div className="loading">Loading cart...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="cart-container">
      <h1>Your Cart</h1>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      {cartItems.length === 0 ? (
        <div className="empty-cart">
          <p>Your cart is empty</p>
          <Link to="/medicines" className="continue-shopping">
            Continue Shopping
          </Link>
        </div>
      ) : (
        <>
          <div className="cart-items">
            {cartItems.map(item => (
              <div className="cart-item" key={item.id}>
                <div className="cart-item-image">
                  <img 
                    src={item.image_url || '/images/medicine-placeholder.jpg'} 
                    alt={item.name} 
                  />
                </div>
                
                <div className="cart-item-details">
                  <h3>{item.name}</h3>
                  <p className="item-price">${item.price.toFixed(2)}</p>
                  
                  {item.requires_prescription && (
                    <div className="prescription-required-tag">
                      Prescription Required
                    </div>
                  )}
                </div>
                
                <div className="cart-item-actions">
                  <div className="quantity-controls">
                    <button 
                      onClick={() => updateQuantity(item.id, item.quantity - 1)}
                      disabled={updating || item.quantity <= 1}
                    >
                      -
                    </button>
                    <span>{item.quantity}</span>
                    <button 
                      onClick={() => updateQuantity(item.id, item.quantity + 1)}
                      disabled={updating || item.quantity >= item.stock}
                    >
                      +
                    </button>
                  </div>
                  
                  <div className="item-subtotal">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                  
                  <button 
                    className="remove-item"
                    onClick={() => removeItem(item.id)}
                    disabled={updating}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
          
          <div className="cart-summary">
            <div className="cart-total">
              <span>Total:</span>
              <span>${calculateTotal().toFixed(2)}</span>
            </div>
            
            {prescriptionNeeded && (
              <div className="prescription-notice">
                <p>
                  Some items in your cart require a valid prescription. 
                  Please upload your prescription during checkout.
                </p>
                <Link to="/prescriptions" className="upload-prescription-link">
                  Manage Prescriptions
                </Link>
              </div>
            )}
            
            <button 
              className="checkout-button"
              onClick={proceedToCheckout}
              disabled={updating}
            >
              Proceed to Checkout
            </button>
            
            <Link to="/medicines" className="continue-shopping">
              Continue Shopping
            </Link>
          </div>
        </>
      )}
    </div>
  );
};

export default Cart; 