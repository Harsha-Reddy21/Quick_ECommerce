import React, { useState, useEffect, useContext } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import './OrderDetail.css';

const OrderDetail = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const { isAuthenticated } = useContext(AuthContext);
  
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isNewOrder] = useState(location.state?.newOrder || false);
  
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: `/orders/${id}` } });
      return;
    }
    
    fetchOrderDetails();
  }, [isAuthenticated, id, navigate]);

  const fetchOrderDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:8000/api/orders/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setOrder(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch order details');
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const formatOrderStatus = (status) => {
    if (!status) return 'N/A';
    return status.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const getStatusClass = (status) => {
    if (!status) return '';
    
    switch (status) {
      case 'pending':
        return 'status-pending';
      case 'processing':
        return 'status-processing';
      case 'out_for_delivery':
        return 'status-out-for-delivery';
      case 'delivered':
        return 'status-delivered';
      case 'cancelled':
        return 'status-cancelled';
      default:
        return '';
    }
  };

  const handleCancelOrder = async () => {
    if (!order || order.status === 'delivered' || order.status === 'cancelled') {
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `http://localhost:8000/api/orders/${id}/cancel`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      // Refresh order details
      fetchOrderDetails();
    } catch (err) {
      setError('Failed to cancel order');
    }
  };

  if (loading) return <div className="loading">Loading order details...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!order) return <div className="error">Order not found</div>;

  return (
    <div className="order-detail-container">
      {isNewOrder && (
        <div className="order-success-message">
          <h2>Order Placed Successfully!</h2>
          <p>Your order has been received and is being processed.</p>
        </div>
      )}
      
      <div className="order-detail-header">
        <div className="order-detail-id">
          <h1>Order #{order.id}</h1>
          <div className={`order-detail-status ${getStatusClass(order.status)}`}>
            {formatOrderStatus(order.status)}
          </div>
        </div>
        
        <div className="order-detail-date">
          Placed on {formatDate(order.created_at)}
        </div>
      </div>
      
      <div className="order-detail-grid">
        <div className="order-detail-main">
          <section className="order-detail-section">
            <h2>Order Items</h2>
            <div className="order-items-list">
              {order.items && order.items.map(item => (
                <div className="order-detail-item" key={item.id}>
                  <div className="item-image">
                    <img 
                      src={item.image_url || '/images/medicine-placeholder.jpg'} 
                      alt={item.name} 
                    />
                  </div>
                  
                  <div className="item-details">
                    <h3>{item.name}</h3>
                    <p className="item-price">${item.price.toFixed(2)} x {item.quantity}</p>
                    
                    {item.requires_prescription && (
                      <div className="prescription-required-tag">
                        Prescription Required
                      </div>
                    )}
                  </div>
                  
                  <div className="item-subtotal">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </section>
          
          {order.status === 'out_for_delivery' && order.delivery_partner && (
            <section className="order-detail-section delivery-tracking">
              <h2>Delivery Tracking</h2>
              <div className="delivery-partner-info">
                <div className="partner-name">
                  <span>Delivery Partner:</span> {order.delivery_partner.name}
                </div>
                <div className="partner-contact">
                  <span>Contact:</span> {order.delivery_partner.phone || 'N/A'}
                </div>
              </div>
              
              <div className="estimated-delivery">
                <span>Estimated Delivery:</span> {formatDate(order.estimated_delivery_time)}
              </div>
              
              <div className="tracking-map">
                <p>Live tracking map will be displayed here</p>
              </div>
            </section>
          )}
        </div>
        
        <div className="order-detail-sidebar">
          <section className="order-detail-section">
            <h2>Order Summary</h2>
            <div className="order-summary-details">
              <div className="summary-row">
                <span>Subtotal</span>
                <span>${order.subtotal?.toFixed(2) || 'N/A'}</span>
              </div>
              
              <div className="summary-row">
                <span>Delivery Fee</span>
                <span>${order.delivery_fee?.toFixed(2) || 'N/A'}</span>
              </div>
              
              <div className="summary-row total">
                <span>Total</span>
                <span>${order.total_amount?.toFixed(2) || 'N/A'}</span>
              </div>
              
              <div className="summary-row">
                <span>Payment Method</span>
                <span>{order.payment_method || 'N/A'}</span>
              </div>
            </div>
          </section>
          
          <section className="order-detail-section">
            <h2>Delivery Address</h2>
            <div className="delivery-address">
              {order.address ? (
                <>
                  <p>{order.address.street}</p>
                  <p>{order.address.city}, {order.address.state} {order.address.postal_code}</p>
                  <p>{order.address.country}</p>
                </>
              ) : (
                <p>Address information not available</p>
              )}
            </div>
          </section>
          
          {(order.status === 'pending' || order.status === 'processing') && (
            <button 
              className="cancel-order-button"
              onClick={handleCancelOrder}
            >
              Cancel Order
            </button>
          )}
          
          <button 
            className="back-to-orders-button"
            onClick={() => navigate('/orders')}
          >
            Back to Orders
          </button>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail; 