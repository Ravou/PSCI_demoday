import React, { useState } from 'react';
<<<<<<< HEAD
import { Link, useNavigate } from 'react-router-dom';
import { userService } from '../services/apiService';


const Login = ({ onLoginSuccess }) => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

=======
import { userService } from '../services/apiService';

const Login = ({ onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

>>>>>>> c1a3fa18 (adding some corrections of my front_end)
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
<<<<<<< HEAD
      // Appelle le vrai endpoint /api/users/login via apiService (Axios)
      const data = await userService.login({
        email: formData.email,
        password: formData.password
      });

      // Stockage déjà fait dans userService (authToken, userProfile)
      // Si tu veux un callback parent:
      if (onLoginSuccess && data?.user) {
        onLoginSuccess(data.user);
      }

      // Redirection vers le dashboard
      navigate('/dashboard');
    } catch (err) {
      // Unifier le message d'erreur
      const msg = err?.error || err?.description || 'Login failed. Please check your credentials.';
      setError(msg);
=======
      const response = await userService.login({ email, password });
      console.log('Connexion réussie:', response);
      
      // Appeler le callback de succès
      if (onLoginSuccess) {
        onLoginSuccess(response.userprofile);
      }
    } catch (err) {
      setError(err.description || 'Erreur de connexion');
      console.error('Erreur login:', err);
>>>>>>> c1a3fa18 (adding some corrections of my front_end)
    } finally {
      setLoading(false);
    }
  };

  return (
<<<<<<< HEAD
    <div style={{
      minHeight: '80vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px 20px'
    }}>
      <div style={{
        maxWidth: '450px',
        width: '100%',
        background: 'rgba(26, 31, 46, 0.6)',
        border: '1px solid rgba(0, 255, 136, 0.2)',
        borderRadius: '20px',
        padding: '50px 40px',
        backdropFilter: 'blur(10px)',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.4)'
      }}>
        <div style={{textAlign: 'center', marginBottom: '40px'}}>
          <h2 style={{
            fontSize: '36px',
            fontWeight: '900',
            color: 'var(--texte-blanc)',
            marginBottom: '10px'
          }}>
            Welcome Back
          </h2>
          <p style={{
            color: 'var(--texte-gris)',
            fontSize: '15px'
          }}>
            Sign in to access your dashboard
          </p>
        </div>

        {error && (
          <div className="error-message" style={{
            backgroundColor: 'rgba(255, 0, 0, 0.1)',
            border: '1px solid rgba(255, 0, 0, 0.3)',
            color: '#ff6b6b',
            padding: '12px',
            borderRadius: '8px',
            marginBottom: '20px',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              placeholder="your@email.com"
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              autoComplete="current-password"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div style={{
          textAlign: 'center',
          marginTop: '30px',
          paddingTop: '30px',
          borderTop: '1px solid rgba(0, 255, 136, 0.1)'
        }}>
          <p style={{ color: 'var(--texte-gris)', fontSize: '15px' }}>
            Don't have an account?{' '}
            <Link to="/register" style={{
              color: 'var(--vert-neon)',
              textDecoration: 'none',
              fontWeight: '700',
              transition: 'all 0.3s'
            }}>
              Sign Up
            </Link>
          </p>
        </div>
      </div>
=======
    <div className="login-container">
      <h2>Connexion</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        
        <div className="form-group">
          <label>Mot de passe:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        
        <button type="submit" disabled={loading}>
          {loading ? 'Connexion...' : 'Se connecter'}
        </button>
      </form>
>>>>>>> c1a3fa18 (adding some corrections of my front_end)
    </div>
  );
};

export default Login;

<<<<<<< HEAD

=======
>>>>>>> c1a3fa18 (adding some corrections of my front_end)
