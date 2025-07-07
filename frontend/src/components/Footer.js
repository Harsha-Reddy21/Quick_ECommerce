import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-section">
          <h3>QuickMed</h3>
          <p>Your trusted medicine delivery service with quick delivery in 10-30 minutes.</p>
        </div>
        
        <div className="footer-section">
          <h3>Quick Links</h3>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/medicines">Medicines</a></li>
            <li><a href="/prescriptions">Prescriptions</a></li>
            <li><a href="/profile">My Account</a></li>
          </ul>
        </div>
        
        <div className="footer-section">
          <h3>Contact Us</h3>
          <p>Email: support@quickmed.com</p>
          <p>Phone: +1 (555) 123-4567</p>
          <p>Address: 123 Health Street, Medical City</p>
        </div>
      </div>
      
      <div className="footer-bottom">
        <p>&copy; {new Date().getFullYear()} QuickMed. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer; 