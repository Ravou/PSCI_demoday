import React, { useState } from 'react';
import { userService } from '../services/apiService';
import { useNavigate } from 'react-router-dom';

const Register = ({ onRegisterSuccess }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    organization: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
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
    setSuccess('');
    setLoading(true);

    try {
      const response = await userService.register(formData);
      console.log('✓ Inscription réussie:', response);
      
      setSuccess('Compte créé avec succès ! Redirection...');
      
      setTimeout(() => {
        if (onRegisterSuccess) {
          onRegisterSuccess(response.user);
        }
        navigate('/login');
      }, 1500);
      
    } catch (err) {
      console.error('✗ Erreur inscription:', err);
      setError(err.description || err.message || 'Erreur lors de l\'inscription');
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Inscription</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nom complet *</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            disabled={loading}
            placeholder="John Doe"
          />
        </div>

        <div className="form-group">
          <label>Email *</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            disabled={loading}
            placeholder="votre@email.com"
          />
        </div>
        
        <div className="form-group">
          <label>Mot de passe *</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            disabled={loading}
            placeholder="••••••••"
            minLength="6"
          />
        </div>

        <div className="form-group">
          <label>Organisation</label>
          <input
            type="text"
            name="organization"
            value={formData.organization}
            onChange={handleChange}
            disabled={loading}
            placeholder="Nom de votre entreprise"
          />
        </div>



        <button type="submit" disabled={loading}>
          {loading ? 'Inscription...' : 'S\'inscrire'}
        </button>
      </form>
      
      <div className="link">
        Déjà inscrit ? <a href="/login">Se connecter</a>
      </div>
    </div>
  );
};

export default Register;

