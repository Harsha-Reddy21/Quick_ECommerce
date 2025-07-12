import React, { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../context/AuthContext';
import api from '../services/api';
import './Orders.css';

const Orders = () => {
  const { isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/orders' } });
      return;
    }
    
    fetchOrders();
  }, [isAuthenticated, navigate]);

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders');
      setOrders(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch orders');
      setLoading(false);
    }
  };

  const getOrderStatusClass = (status) => {
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

  const formatOrderStatus = (status) => {
    return status.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  const filteredOrders = activeTab === 'all' 
    ? orders 
    : orders.filter(order => order.status === activeTab);

  if (loading) return <div className="loading">Loading orders...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="orders-container">
      <h1>My Orders</h1>
      
      <div className="order-tabs">
        <button 
          className={activeTab === 'all' ? 'active' : ''}
          onClick={() => setActiveTab('all')}
        >
          All Orders
        </button>
        <button 
          className={activeTab === 'pending' ? 'active' : ''}
          onClick={() => setActiveTab('pending')}
        >
          Pending
        </button>
        <button 
          className={activeTab === 'processing' ? 'active' : ''}
          onClick={() => setActiveTab('processing')}
        >
          Processing
        </button>
        <button 
          className={activeTab === 'out_for_delivery' ? 'active' : ''}
          onClick={() => setActiveTab('out_for_delivery')}
        >
          Out for Delivery
        </button>
        <button 
          className={activeTab === 'delivered' ? 'active' : ''}
          onClick={() => setActiveTab('delivered')}
        >
          Delivered
        </button>
      </div>
      
      {filteredOrders.length === 0 ? (
        <div className="no-orders">
          <p>No orders found</p>
          <Link to="/medicines" className="shop-now-button">
            Shop Now
          </Link>
        </div>
      ) : (
        <div className="orders-list">
          {filteredOrders.map(order => (
            <Link to={`/orders/${order.id}`} className="order-card" key={order.id}>
              <div className="order-header">
                <div className="order-id">Order #{order.id}</div>
                <div className={`order-status ${getOrderStatusClass(order.status)}`}>
                  {formatOrderStatus(order.status)}
                </div>
              </div>
              
              <div className="order-details">
                <div className="order-date">
                  <span>Ordered on:</span> {formatDate(order.created_at)}
                </div>
                
                <div className="order-items-count">
                  <span>Items:</span> {order.items_count || 'N/A'}
                </div>
                
                <div className="order-total">
                  <span>Total:</span> ${order.total_amount.toFixed(2)}
                </div>
              </div>
              
              {order.estimated_delivery_time && (
                <div className="delivery-estimate">
                  <span>Estimated Delivery:</span> {formatDate(order.estimated_delivery_time)}
                </div>
              )}
              
              <div className="order-address">
                <span>Delivery to:</span> {order.delivery_address || 'N/A'}
              </div>
              
              <div className="view-details">
                View Details
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default Orders; 