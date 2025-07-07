import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-container">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Quick Medicine Delivery</h1>
          <p>Get medicines delivered to your doorstep in 10-30 minutes</p>
          <Link to="/medicines" className="shop-now-button">
            Shop Now
          </Link>
        </div>
      </section>
      
      <section className="features-section">
        <h2>Why Choose Us</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Quick Delivery</h3>
            <p>Medicines delivered in as fast as 10 minutes</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔍</div>
            <h3>Wide Selection</h3>
            <p>Thousands of medicines and healthcare products</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">✅</div>
            <h3>Verified Products</h3>
            <p>All medicines are sourced from authorized distributors</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon">🔒</div>
            <h3>Secure Prescriptions</h3>
            <p>Upload and manage your prescriptions securely</p>
          </div>
        </div>
      </section>
      
      <section className="how-it-works-section">
        <h2>How It Works</h2>
        <div className="steps-container">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Upload Prescription</h3>
            <p>Upload your prescription or choose from non-prescription medicines</p>
          </div>
          
          <div className="step">
            <div className="step-number">2</div>
            <h3>Add to Cart</h3>
            <p>Select medicines and add them to your cart</p>
          </div>
          
          <div className="step">
            <div className="step-number">3</div>
            <h3>Checkout</h3>
            <p>Choose delivery address and payment method</p>
          </div>
          
          <div className="step">
            <div className="step-number">4</div>
            <h3>Quick Delivery</h3>
            <p>Get medicines delivered to your doorstep in minutes</p>
          </div>
        </div>
      </section>
      
      <section className="categories-section">
        <h2>Popular Categories</h2>
        <div className="categories-grid">
          <Link to="/medicines?category=fever" className="category-card">
            <h3>Fever & Pain Relief</h3>
          </Link>
          
          <Link to="/medicines?category=cold" className="category-card">
            <h3>Cold & Cough</h3>
          </Link>
          
          <Link to="/medicines?category=diabetes" className="category-card">
            <h3>Diabetes Care</h3>
          </Link>
          
          <Link to="/medicines?category=cardiac" className="category-card">
            <h3>Cardiac Care</h3>
          </Link>
          
          <Link to="/medicines?category=vitamins" className="category-card">
            <h3>Vitamins & Supplements</h3>
          </Link>
          
          <Link to="/medicines?category=skincare" className="category-card">
            <h3>Skin Care</h3>
          </Link>
        </div>
      </section>
      
      <section className="emergency-section">
        <div className="emergency-content">
          <h2>Emergency Medicine Delivery</h2>
          <p>Need medicines urgently? Get emergency delivery in just 10-15 minutes.</p>
          <Link to="/medicines" className="emergency-button">
            Order Emergency Medicines
          </Link>
        </div>
      </section>
      
      <section className="testimonials-section">
        <h2>What Our Customers Say</h2>
        <div className="testimonials-grid">
          <div className="testimonial-card">
            <p>"Received my medicines in just 12 minutes! Excellent service when I needed it most."</p>
            <div className="testimonial-author">- Rahul S.</div>
          </div>
          
          <div className="testimonial-card">
            <p>"The prescription verification process was quick and seamless. Very professional service."</p>
            <div className="testimonial-author">- Priya M.</div>
          </div>
          
          <div className="testimonial-card">
            <p>"Great selection of medicines and the app is very easy to use. My go-to for all medical needs."</p>
            <div className="testimonial-author">- Amit K.</div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home; 