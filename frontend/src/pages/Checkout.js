import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import './Checkout.css';

const Checkout = () => {
  const { isAuthenticated, user } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [cartItems, setCartItems] = useState([]);
  const [addresses, setAddresses] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedAddress, setSelectedAddress] = useState('');
  const [selectedPrescription, setSelectedPrescription] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('cash');
  const [deliveryOption, setDeliveryOption] = useState('standard');
  const [processingOrder, setProcessingOrder] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });
  const [prescriptionNeeded, setPrescriptionNeeded] = useState(false);
  const [estimatedDeliveryTime, setEstimatedDeliveryTime] = useState(null);
  
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/checkout' } });
      return;
    }
    
    fetchData();
  }, [isAuthenticated, navigate]);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      // Fetch cart items
      const cartResponse = await axios.get('http://localhost:8000/api/cart', { headers });
      setCartItems(cartResponse.data.items);
      
      // Check if prescription is needed
      const needsPrescription = cartResponse.data.items.some(item => item.requires_prescription);
      setPrescriptionNeeded(needsPrescription);
      
      // Fetch user addresses
      const addressesResponse = await axios.get('http://localhost:8000/api/users/addresses', { headers });
      setAddresses(addressesResponse.data);
      
      // Set default address if available
      if (addressesResponse.data.length > 0) {
        setSelectedAddress(addressesResponse.data[0].id.toString());
      }
      
      // Fetch prescriptions if needed
      if (needsPrescription) {
        const prescriptionsResponse = await axios.get('http://localhost:8000/api/prescriptions', { headers });
        setPrescriptions(prescriptionsResponse.data);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load checkout data');
      setLoading(false);
    }
  };

  const calculateSubtotal = () => {
    return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
  };

  const calculateDeliveryFee = () => {
    if (deliveryOption === 'express') return 5.99;
    if (deliveryOption === 'emergency') return 9.99;
    return 2.99; // standard
  };

  const calculateTotal = () => {
    return calculateSubtotal() + calculateDeliveryFee();
  };

  const getEstimatedDelivery = async () => {
    if (!selectedAddress) return;
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/api/delivery/estimate', {
        params: {
          address_id: selectedAddress,
          is_emergency: deliveryOption === 'emergency'
        },
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setEstimatedDeliveryTime(response.data.estimated_minutes);
    } catch (err) {
      console.error('Failed to get delivery estimate', err);
    }
  };

  useEffect(() => {
    if (selectedAddress) {
      getEstimatedDelivery();
    }
  }, [selectedAddress, deliveryOption]);

  const handlePlaceOrder = async () => {
    // Validate required fields
    if (!selectedAddress) {
      setMessage({ text: 'Please select a delivery address', type: 'error' });
      return;
    }
    
    if (prescriptionNeeded && !selectedPrescription) {
      setMessage({ text: 'Please select a prescription for prescription medicines', type: 'error' });
      return;
    }
    
    setProcessingOrder(true);
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/orders',
        {
          address_id: parseInt(selectedAddress),
          prescription_id: prescriptionNeeded ? parseInt(selectedPrescription) : null,
          payment_method: paymentMethod,
          delivery_option: deliveryOption
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      // Redirect to order confirmation page
      navigate(`/orders/${response.data.id}`, { state: { newOrder: true } });
    } catch (err) {
      let errorMsg = 'Failed to place order';
      
      if (err.response && err.response.data && err.response.data.detail) {
        errorMsg = err.response.data.detail;
      }
      
      setMessage({ text: errorMsg, type: 'error' });
      setProcessingOrder(false);
    }
  };

  if (loading) return <div className="loading">Loading checkout...</div>;
  if (error) return <div className="error">{error}</div>;
  if (cartItems.length === 0) return <div className="empty-checkout">Your cart is empty</div>;

  return (
    <div className="checkout-container">
      <h1>Checkout</h1>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      <div className="checkout-grid">
        <div className="checkout-details">
          <section className="checkout-section">
            <h2>Delivery Address</h2>
            {addresses.length === 0 ? (
              <div className="no-addresses">
                <p>You don't have any saved addresses.</p>
                <button 
                  className="add-address-button"
                  onClick={() => navigate('/profile?tab=addresses')}
                >
                  Add New Address
                </button>
              </div>
            ) : (
              <div className="address-selection">
                {addresses.map(address => (
                  <div className="address-option" key={address.id}>
                    <input 
                      type="radio"
                      id={`address-${address.id}`}
                      name="address"
                      value={address.id}
                      checked={selectedAddress === address.id.toString()}
                      onChange={(e) => setSelectedAddress(e.target.value)}
                    />
                    <label htmlFor={`address-${address.id}`}>
                      <div className="address-details">
                        <p>{address.street}, {address.city}</p>
                        <p>{address.state}, {address.postal_code}</p>
                        <p>{address.country}</p>
                      </div>
                    </label>
                  </div>
                ))}
                <button 
                  className="add-address-button"
                  onClick={() => navigate('/profile?tab=addresses')}
                >
                  Add New Address
                </button>
              </div>
            )}
          </section>
          
          {prescriptionNeeded && (
            <section className="checkout-section">
              <h2>Prescription</h2>
              {prescriptions.length === 0 ? (
                <div className="no-prescriptions">
                  <p>You don't have any saved prescriptions.</p>
                  <button 
                    className="add-prescription-button"
                    onClick={() => navigate('/prescriptions')}
                  >
                    Upload Prescription
                  </button>
                </div>
              ) : (
                <div className="prescription-selection">
                  {prescriptions.map(prescription => (
                    <div className="prescription-option" key={prescription.id}>
                      <input 
                        type="radio"
                        id={`prescription-${prescription.id}`}
                        name="prescription"
                        value={prescription.id}
                        checked={selectedPrescription === prescription.id.toString()}
                        onChange={(e) => setSelectedPrescription(e.target.value)}
                      />
                      <label htmlFor={`prescription-${prescription.id}`}>
                        <div className="prescription-details">
                          <p>Uploaded on: {new Date(prescription.created_at).toLocaleDateString()}</p>
                          <p>Status: {prescription.status}</p>
                          <p className="prescription-filename">{prescription.filename}</p>
                        </div>
                      </label>
                    </div>
                  ))}
                  <button 
                    className="add-prescription-button"
                    onClick={() => navigate('/prescriptions')}
                  >
                    Upload New Prescription
                  </button>
                </div>
              )}
            </section>
          )}
          
          <section className="checkout-section">
            <h2>Delivery Options</h2>
            <div className="delivery-options">
              <div className="delivery-option">
                <input 
                  type="radio"
                  id="standard-delivery"
                  name="delivery"
                  value="standard"
                  checked={deliveryOption === 'standard'}
                  onChange={() => setDeliveryOption('standard')}
                />
                <label htmlFor="standard-delivery">
                  <div className="delivery-option-details">
                    <span className="delivery-name">Standard Delivery</span>
                    <span className="delivery-time">20-30 minutes</span>
                    <span className="delivery-fee">$2.99</span>
                  </div>
                </label>
              </div>
              
              <div className="delivery-option">
                <input 
                  type="radio"
                  id="express-delivery"
                  name="delivery"
                  value="express"
                  checked={deliveryOption === 'express'}
                  onChange={() => setDeliveryOption('express')}
                />
                <label htmlFor="express-delivery">
                  <div className="delivery-option-details">
                    <span className="delivery-name">Express Delivery</span>
                    <span className="delivery-time">15-20 minutes</span>
                    <span className="delivery-fee">$5.99</span>
                  </div>
                </label>
              </div>
              
              <div className="delivery-option">
                <input 
                  type="radio"
                  id="emergency-delivery"
                  name="delivery"
                  value="emergency"
                  checked={deliveryOption === 'emergency'}
                  onChange={() => setDeliveryOption('emergency')}
                />
                <label htmlFor="emergency-delivery">
                  <div className="delivery-option-details">
                    <span className="delivery-name">Emergency Delivery</span>
                    <span className="delivery-time">10-15 minutes</span>
                    <span className="delivery-fee">$9.99</span>
                  </div>
                </label>
              </div>
            </div>
            
            {estimatedDeliveryTime && (
              <div className="estimated-delivery">
                Estimated delivery time: <span>{estimatedDeliveryTime} minutes</span>
              </div>
            )}
          </section>
          
          <section className="checkout-section">
            <h2>Payment Method</h2>
            <div className="payment-methods">
              <div className="payment-method">
                <input 
                  type="radio"
                  id="cash-payment"
                  name="payment"
                  value="cash"
                  checked={paymentMethod === 'cash'}
                  onChange={() => setPaymentMethod('cash')}
                />
                <label htmlFor="cash-payment">Cash on Delivery</label>
              </div>
              
              <div className="payment-method">
                <input 
                  type="radio"
                  id="card-payment"
                  name="payment"
                  value="card"
                  checked={paymentMethod === 'card'}
                  onChange={() => setPaymentMethod('card')}
                />
                <label htmlFor="card-payment">Credit/Debit Card</label>
              </div>
              
              <div className="payment-method">
                <input 
                  type="radio"
                  id="upi-payment"
                  name="payment"
                  value="upi"
                  checked={paymentMethod === 'upi'}
                  onChange={() => setPaymentMethod('upi')}
                />
                <label htmlFor="upi-payment">UPI</label>
              </div>
            </div>
          </section>
        </div>
        
        <div className="order-summary">
          <h2>Order Summary</h2>
          
          <div className="order-items">
            {cartItems.map(item => (
              <div className="order-item" key={item.id}>
                <div className="item-name-qty">
                  <span className="item-name">{item.name}</span>
                  <span className="item-qty">x{item.quantity}</span>
                </div>
                <span className="item-price">${(item.price * item.quantity).toFixed(2)}</span>
              </div>
            ))}
          </div>
          
          <div className="order-totals">
            <div className="subtotal">
              <span>Subtotal</span>
              <span>${calculateSubtotal().toFixed(2)}</span>
            </div>
            
            <div className="delivery-fee">
              <span>Delivery Fee</span>
              <span>${calculateDeliveryFee().toFixed(2)}</span>
            </div>
            
            <div className="total">
              <span>Total</span>
              <span>${calculateTotal().toFixed(2)}</span>
            </div>
          </div>
          
          <button 
            className="place-order-button"
            onClick={handlePlaceOrder}
            disabled={processingOrder}
          >
            {processingOrder ? 'Processing...' : 'Place Order'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Checkout; 