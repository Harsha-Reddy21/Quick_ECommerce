import React, { useState, useEffect, useContext } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import './Profile.css';

const Profile = () => {
  const { isAuthenticated, user, updateUser } = useContext(AuthContext);
  const navigate = useNavigate();
  const location = useLocation();
  
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [addresses, setAddresses] = useState([]);
  const [message, setMessage] = useState({ text: '', type: '' });
  
  // Form states
  const [profileForm, setProfileForm] = useState({
    name: '',
    email: '',
    phone: ''
  });
  
  const [passwordForm, setPasswordForm] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });
  
  const [addressForm, setAddressForm] = useState({
    street: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
    is_default: false
  });
  
  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login', { state: { from: '/profile' } });
      return;
    }
    
    // Check if a specific tab is requested via query params
    const params = new URLSearchParams(location.search);
    const tab = params.get('tab');
    if (tab) {
      setActiveTab(tab);
    }
    
    fetchUserData();
  }, [isAuthenticated, navigate, location]);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };
      
      // Fetch user profile
      const userResponse = await axios.get('http://localhost:8000/api/users/me', { headers });
      setProfileForm({
        name: userResponse.data.name || '',
        email: userResponse.data.email || '',
        phone: userResponse.data.phone || ''
      });
      
      // Fetch user addresses
      const addressesResponse = await axios.get('http://localhost:8000/api/users/addresses', { headers });
      setAddresses(addressesResponse.data);
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load user data');
      setLoading(false);
    }
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileForm(prev => ({ ...prev, [name]: value }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordForm(prev => ({ ...prev, [name]: value }));
  };

  const handleAddressChange = (e) => {
    const { name, value, type, checked } = e.target;
    setAddressForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const updateProfile = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(
        'http://localhost:8000/api/users/me',
        profileForm,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      updateUser(response.data);
      setMessage({ text: 'Profile updated successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ text: 'Failed to update profile', type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  const updatePassword = async (e) => {
    e.preventDefault();
    
    if (passwordForm.new_password !== passwordForm.confirm_password) {
      setMessage({ text: 'Passwords do not match', type: 'error' });
      return;
    }
    
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        'http://localhost:8000/api/users/password',
        {
          current_password: passwordForm.current_password,
          new_password: passwordForm.new_password
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      setPasswordForm({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      
      setMessage({ text: 'Password updated successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      let errorMsg = 'Failed to update password';
      
      if (err.response && err.response.data && err.response.data.detail) {
        errorMsg = err.response.data.detail;
      }
      
      setMessage({ text: errorMsg, type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  const addAddress = async (e) => {
    e.preventDefault();
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/users/addresses',
        addressForm,
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      setAddresses(prev => [...prev, response.data]);
      setAddressForm({
        street: '',
        city: '',
        state: '',
        postal_code: '',
        country: '',
        is_default: false
      });
      
      setMessage({ text: 'Address added successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ text: 'Failed to add address', type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  const deleteAddress = async (addressId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`http://localhost:8000/api/users/addresses/${addressId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setAddresses(prev => prev.filter(address => address.id !== addressId));
      setMessage({ text: 'Address deleted successfully', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ text: 'Failed to delete address', type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  const setDefaultAddress = async (addressId) => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        `http://localhost:8000/api/users/addresses/${addressId}/default`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      
      // Update local state to reflect the change
      setAddresses(prev => 
        prev.map(address => ({
          ...address,
          is_default: address.id === addressId
        }))
      );
      
      setMessage({ text: 'Default address updated', type: 'success' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    } catch (err) {
      setMessage({ text: 'Failed to update default address', type: 'error' });
      setTimeout(() => setMessage({ text: '', type: '' }), 3000);
    }
  };

  if (loading) return <div className="loading">Loading profile...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="profile-container">
      <h1>My Profile</h1>
      
      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
      
      <div className="profile-tabs">
        <button 
          className={activeTab === 'profile' ? 'active' : ''}
          onClick={() => setActiveTab('profile')}
        >
          Profile
        </button>
        <button 
          className={activeTab === 'password' ? 'active' : ''}
          onClick={() => setActiveTab('password')}
        >
          Password
        </button>
        <button 
          className={activeTab === 'addresses' ? 'active' : ''}
          onClick={() => setActiveTab('addresses')}
        >
          Addresses
        </button>
      </div>
      
      <div className="profile-content">
        {activeTab === 'profile' && (
          <div className="profile-section">
            <h2>Personal Information</h2>
            <form onSubmit={updateProfile}>
              <div className="form-group">
                <label htmlFor="name">Full Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={profileForm.name}
                  onChange={handleProfileChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={profileForm.email}
                  onChange={handleProfileChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                  type="tel"
                  id="phone"
                  name="phone"
                  value={profileForm.phone}
                  onChange={handleProfileChange}
                />
              </div>
              
              <button type="submit" className="update-button">
                Update Profile
              </button>
            </form>
          </div>
        )}
        
        {activeTab === 'password' && (
          <div className="profile-section">
            <h2>Change Password</h2>
            <form onSubmit={updatePassword}>
              <div className="form-group">
                <label htmlFor="current_password">Current Password</label>
                <input
                  type="password"
                  id="current_password"
                  name="current_password"
                  value={passwordForm.current_password}
                  onChange={handlePasswordChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="new_password">New Password</label>
                <input
                  type="password"
                  id="new_password"
                  name="new_password"
                  value={passwordForm.new_password}
                  onChange={handlePasswordChange}
                  required
                />
              </div>
              
              <div className="form-group">
                <label htmlFor="confirm_password">Confirm New Password</label>
                <input
                  type="password"
                  id="confirm_password"
                  name="confirm_password"
                  value={passwordForm.confirm_password}
                  onChange={handlePasswordChange}
                  required
                />
              </div>
              
              <button type="submit" className="update-button">
                Update Password
              </button>
            </form>
          </div>
        )}
        
        {activeTab === 'addresses' && (
          <div className="profile-section">
            <h2>Delivery Addresses</h2>
            
            <div className="addresses-list">
              {addresses.length === 0 ? (
                <p>No addresses saved yet.</p>
              ) : (
                addresses.map(address => (
                  <div className="address-card" key={address.id}>
                    <div className="address-details">
                      <p>{address.street}</p>
                      <p>{address.city}, {address.state} {address.postal_code}</p>
                      <p>{address.country}</p>
                      
                      {address.is_default && (
                        <div className="default-badge">Default</div>
                      )}
                    </div>
                    
                    <div className="address-actions">
                      {!address.is_default && (
                        <button 
                          className="set-default-button"
                          onClick={() => setDefaultAddress(address.id)}
                        >
                          Set as Default
                        </button>
                      )}
                      
                      <button 
                        className="delete-button"
                        onClick={() => deleteAddress(address.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
            
            <div className="add-address-section">
              <h3>Add New Address</h3>
              <form onSubmit={addAddress}>
                <div className="form-group">
                  <label htmlFor="street">Street Address</label>
                  <input
                    type="text"
                    id="street"
                    name="street"
                    value={addressForm.street}
                    onChange={handleAddressChange}
                    required
                  />
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="city">City</label>
                    <input
                      type="text"
                      id="city"
                      name="city"
                      value={addressForm.city}
                      onChange={handleAddressChange}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="state">State/Province</label>
                    <input
                      type="text"
                      id="state"
                      name="state"
                      value={addressForm.state}
                      onChange={handleAddressChange}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="postal_code">Postal Code</label>
                    <input
                      type="text"
                      id="postal_code"
                      name="postal_code"
                      value={addressForm.postal_code}
                      onChange={handleAddressChange}
                      required
                    />
                  </div>
                  
                  <div className="form-group">
                    <label htmlFor="country">Country</label>
                    <input
                      type="text"
                      id="country"
                      name="country"
                      value={addressForm.country}
                      onChange={handleAddressChange}
                      required
                    />
                  </div>
                </div>
                
                <div className="form-group checkbox">
                  <input
                    type="checkbox"
                    id="is_default"
                    name="is_default"
                    checked={addressForm.is_default}
                    onChange={handleAddressChange}
                  />
                  <label htmlFor="is_default">Set as default address</label>
                </div>
                
                <button type="submit" className="add-button">
                  Add Address
                </button>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile; 