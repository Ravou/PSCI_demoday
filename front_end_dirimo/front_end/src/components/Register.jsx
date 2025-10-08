import React, { useState } from 'react';
import { userService } from '../services/apiService';

const Register = ({ onRegisterSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    organization: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await userService.register(formData);
      console.log('Inscription réussie:', response);
      
      if (onRegisterSuccess) {
        onRegisterSuccess(response.user);
      }
    } catch (err) {
      setError(err.description || 'Erreur d\'inscription');
      console.error('Erreur inscription:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <h2>Inscription</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:*</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label>Mot de passe:*</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Nom:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label>Organisation:</label>
          <input
            type="text"
            name="organization"
            value={formData.organization}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Inscription...' : 'S\'inscrire'}
        </button>
      </form>
    </div>
  );
};

export default Register;

