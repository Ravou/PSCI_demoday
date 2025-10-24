import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // 🔥 CHANGEMENT 1: Ajout de consent_given dans le body
      const response = await axios.post('http://localhost:5000/api/users/register', {
        name,
        email,
        password,
        consent_given: true  // ✅ Obligatoire pour ton API
      });

      console.log('Inscription réussie:', response.data);
      alert('Inscription réussie ! Vous pouvez maintenant vous connecter.');
      navigate('/login');
    } catch (err) {
      // 🔥 CHANGEMENT 2: Meilleure gestion des erreurs axios
      console.error('Erreur inscription:', err);
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Erreur lors de l\'inscription'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-card">
          <h1 className="login-title">
            Créer un compte <span className="text-gradient">PSCI</span>
          </h1>
          <p className="login-subtitle">
            Rejoignez-nous pour sécuriser vos données
          </p>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="name">Nom</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Votre nom"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Mot de passe</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength="6"
              />
            </div>

            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Inscription...' : 'S\'inscrire'}
            </button>
          </form>

          <p className="login-footer">
            Déjà un compte ?{' '}
            <a href="/login" className="login-link">Se connecter</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;

