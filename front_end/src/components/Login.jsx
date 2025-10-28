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
      console.error('Connection error:', err);
      
      // 🔥 CHANGEMENT: Gestion d'erreur adaptée à ton API
      // Ton backend retourne { error: 'Invalid credentials' }
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Incorrect email or password'
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
            Connect to <span className="text-gradient">PSCI</span>
          </h1>
          <p className="login-subtitle">
            Acces to your dashboard and manage your audits easily.
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
                placeholder="your@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
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
              {loading ? 'Connecting...' : 'Sign In'}
            </button>
          </form>

          <p className="login-footer">
              Don't have an account yet ?{' '}
            <a href="/register" className="login-link">Register</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

