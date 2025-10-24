import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = ({ onLoginSuccess }) => {
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
      const response = await axios.post('http://localhost:5000/api/users/login', {
        email,
        password,
      });

      console.log('Réponse API:', response.data); // Debug

      // 🔥 CHANGEMENT: Adaptation aux champs exacts de ton API
      // Ton backend retourne: { message, user_id, name, email }
      const userData = {
        id: response.data.user_id,      // ✅ Ton API retourne "user_id" pas "userid"
        email: response.data.email,
        name: response.data.name,
        token: response.data.token || null, // Optionnel si tu n'as pas de JWT pour l'instant
      };

      // Stocke dans localStorage pour persistance
      localStorage.setItem('user_id', userData.id);
      localStorage.setItem('user_name', userData.name);
      localStorage.setItem('user_email', userData.email);
      if (userData.token) {
        localStorage.setItem('auth_token', userData.token);
      }

      // Appelle la fonction callback si fournie
      if (onLoginSuccess) {
        onLoginSuccess(userData);
      }

      navigate('/dashboard');
    } catch (err) {
      console.error('Erreur connexion:', err);
      
      // 🔥 CHANGEMENT: Gestion d'erreur adaptée à ton API
      // Ton backend retourne { error: 'Invalid credentials' }
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Identifiants incorrects'
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
            Connexion à <span className="text-gradient">PSCI</span>
          </h1>
          <p className="login-subtitle">
            Accédez à votre tableau de bord sécurisé
          </p>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
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
              />
            </div>

            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Connexion...' : 'Se connecter'}
            </button>
          </form>

          <p className="login-footer">
            Pas encore de compte ?{' '}
            <a href="/register" className="login-link">S'inscrire</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

