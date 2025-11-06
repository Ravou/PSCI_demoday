import React, { useState } from 'react';

import { useNavigate } from 'react-router-dom';
import { authAPI } from '../services/api';
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
      const loginData = await authAPI.login(email, password);
      console.log('Réponse API:', loginData);

      const userId = loginData.user_id || loginData.id || loginData.userId;
      const userName = loginData.name || loginData.user_name || 'User';
      const userEmail = loginData.email;

      if (!userId) {
        setError('Erreur : ID utilisateur manquant');
        setLoading(false);
        return;
      }

      const userData = {
        id: String(userId),
        email: userEmail,
        name: userName,
        token: loginData.token || null,
      };

      
      localStorage.setItem('user_id', userData.id);
      localStorage.setItem('user_name', userData.name);
      localStorage.setItem('user_email', userData.email);
      if (userData.token) {
        localStorage.setItem('auth_token', userData.token);
      }


      if (onLoginSuccess) {
        onLoginSuccess(userData);
      }

      navigate('/dashboard');
    } catch (err) {
      console.error('Erreur login:', err);
      setError(err.message || 'Email ou mot de passe incorrect');
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
            Access your dashboard and manage your audits easily.
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
            Don't have an account yet?{' '}
            <a href="/register" className="login-link">Register</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

