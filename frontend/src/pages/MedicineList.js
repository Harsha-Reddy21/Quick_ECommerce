import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import './MedicineList.css';

const MedicineList = () => {
  const [medicines, setMedicines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    const fetchMedicines = async () => {
      try {
        const response = await api.get('/medicines');
        setMedicines(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch medicines');
        setLoading(false);
      }
    };

    const fetchCategories = async () => {
      try {
        const response = await api.get('/categories');
        setCategories(response.data);
      } catch (err) {
        console.error('Failed to fetch categories', err);
      }
    };

    fetchMedicines();
    fetchCategories();
  }, []);

  const filteredMedicines = medicines.filter(medicine => {
    const matchesSearch = medicine.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = categoryFilter === '' || medicine.category_id === parseInt(categoryFilter);
    return matchesSearch && matchesCategory;
  });

  if (loading) return <div className="loading">Loading medicines...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="medicine-list-container">
      <h1>Medicines</h1>
      
      <div className="filters">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Search medicines..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="category-filter">
          <select 
            value={categoryFilter} 
            onChange={(e) => setCategoryFilter(e.target.value)}
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {filteredMedicines.length === 0 ? (
        <div className="no-results">No medicines found</div>
      ) : (
        <div className="medicines-grid">
          {filteredMedicines.map(medicine => (
            <Link 
              to={`/medicines/${medicine.id}`} 
              className="medicine-card" 
              key={medicine.id}
            >
              <div className="medicine-image">
                <img 
                  src={medicine.image_url || '/images/medicine-placeholder.jpg'} 
                  alt={medicine.name} 
                />
              </div>
              <div className="medicine-info">
                <h3>{medicine.name}</h3>
                <p className="medicine-description">{medicine.description.substring(0, 100)}...</p>
                <div className="medicine-price-stock">
                  <span className="price">${medicine.price.toFixed(2)}</span>
                  <span className={`stock ${medicine.stock > 10 ? 'in-stock' : 'low-stock'}`}>
                    {medicine.stock > 0 ? `${medicine.stock} in stock` : 'Out of stock'}
                  </span>
                </div>
                <div className="medicine-prescription">
                  {medicine.requires_prescription ? 
                    <span className="prescription-required">Prescription Required</span> : 
                    <span className="no-prescription">No Prescription</span>
                  }
                </div>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};

export default MedicineList; 