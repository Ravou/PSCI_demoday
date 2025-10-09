import React, { useState } from 'react';
import { userService } from '../services/apiService';
import { useNavigate } from 'react-router-dom';

const Login = ({ onLoginSuccess }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await userService.login({ email, password });
      console.log('✓ Connexion réussie:', response);
      
      if (response.userprofile || response.user) {
        const userData = response.userprofile || response.user;
        onLoginSuccess(userData);
        navigate('/dashboard');
      } else {
        setError('Réponse serveur invalide');
      }
    } catch (err) {
      console.error('✗ Erreur login:', err);
      setError(err.description || err.message || 'Email ou mot de passe incorrect');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Connexion</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
            placeholder="votre@email.com"
          />
        </div>
        
        <div className="form-group">
          <label>Mot de passe</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
            placeholder="••••••••"
          />
        </div>



        <button type="submit" disabled={loading}>
          {loading ? 'Connexion...' : 'Se connecter'}
        </button>
      </form>
      <div className="link">
        Pas de compte ? <a href="/register">S'inscrire</a>
      </div>
    </div>
  );
};

export default Login;


