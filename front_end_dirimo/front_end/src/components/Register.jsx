import React, { useState } from 'react';
<<<<<<< HEAD
import { Link, useNavigate } from 'react-router-dom';
import { userService } from '../services/apiService';


const Register = ({ onRegisterSuccess }) => {
 
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
 
    organization: ''
  });
 
  const [error, setError] = useState('');
 
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
=======
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
>>>>>>> c1a3fa18 (adding some corrections of my front_end)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

<<<<<<< HEAD
  const validate = () => {
    if (!formData.name.trim()) return 'Name is required';
    if (!formData.email.trim()) return 'Email is required';
    if (formData.password.length < 6) return 'Password must be at least 6 characters';
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);

    try {
      // 1) Inscription
      const reg = await userService.register({
        name: formData.name.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password,
        organization: formData.organization.trim()
      });

      if (onRegisterSuccess && reg?.user) {
        onRegisterSuccess(reg.user);
      }

      // 2) Auto-login immédiat avec les mêmes identifiants
      const login = await userService.login({
        email: formData.email.trim().toLowerCase(),
        password: formData.password
      });

      // 3) Redirection vers le dashboard
      navigate('/dashboard');
    } catch (err) {
      // Affiche le message backend si fourni
      const msg = err?.error || err?.description || 'Registration failed. Please try again.';
      setError(msg);
=======
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
        maxWidth: '480px',
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
            Get Started
          </h2>
          <p style={{
            color: 'var(--texte-gris)',
            fontSize: '15px'
          }}>
            Create your account to start auditing
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
            <label>Full Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
              placeholder="John Doe"
              autoComplete="name"
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
              placeholder="your@email.com"
              autoComplete="email"
            />
          </div>

          <div className="form-group">
            <label>Password *</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="••••••••"
              autoComplete="new-password"
              minLength={6}
            />
          </div>

          <div className="form-group">
            <label>Organization</label>
            <input
              type="text"
              name="organization"
              value={formData.organization}
              onChange={handleChange}
              placeholder="Your company name"
              autoComplete="organization"
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '10px' }}
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div style={{
          textAlign: 'center',
          marginTop: '30px',
          paddingTop: '30px',
          borderTop: '1px solid rgba(0, 255, 136, 0.1)'
        }}>
          <p style={{ color: 'var(--texte-gris)', fontSize: '15px' }}>
            Already have an account?{' '}
            <Link to="/login" style={{
              color: 'var(--vert-neon)',
              textDecoration: 'none',
              fontWeight: '700',
              transition: 'all 0.3s'
            }}>
              Sign In
            </Link>
          </p>
        </div>
      </div>
=======
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
>>>>>>> c1a3fa18 (adding some corrections of my front_end)
    </div>
  );
};

export default Register;

<<<<<<< HEAD

=======
>>>>>>> c1a3fa18 (adding some corrections of my front_end)
