import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Register = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [consentGiven, setConsentGiven] = useState(false); // ✅ État pour le consentement
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // ✅ Validation du consentement AVANT l'envoi
    if (!consentGiven) {
      setError('You must accept the terms and conditions to create an account');
      return;
    }

    setLoading(true);

    try {
 // CHANGEMENT 1: Envoi du consentement au backend
      const response = await axios.post('http://localhost:5000/api/users/register', {
        name,
        email,
        password,
        consent_given: true
      });
// CHANGEMENT 2: Meuilleure gestion des errreurs axios
      console.log('Registration successful:', response.data);
      alert('Registration successful! You can now log in.');
      navigate('/login');
    } catch (err) {
      console.error('Erreur inscription:', err); // Obligatoire pour ton API 
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Error during registration'
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
            Create an account <span className="text-gradient">PSCI</span>
          </h1>
          <p className="login-subtitle">
            Join PSCI to manage your audits efficiently.
          </p>

          {error && <div className="error-message">{error}</div>}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="name">Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your Name"
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
                minLength="6"
              />
            </div>

            {/* ✅ SECTION CONSENTEMENT GDPR */}
            <div className="form-group consent-group">
              <label className="consent-label">
                <input
                  type="checkbox"
                  checked={consentGiven}
                  onChange={(e) => setConsentGiven(e.target.checked)}
                  className="consent-checkbox"
                />
                <span className="consent-text">
                  I agree that my personal data will be collected and processed in accordance with the{' '}
                  <a href="/privacy-policy" target="_blank" className="consent-link">
                    privacy policy
                  </a>
                  {' '}and{' '}
                  <a href="/gdpr-terms" target="_blank" className="consent-link">
                    GDPR
                  </a>
                  . I consent to the scraping and temporary processing of my data.
                </span>
              </label>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary btn-full" 
              disabled={loading || !consentGiven}
            >
              {loading ? 'Loading...' : 'Sign Up'}
            </button>
          </form>

          <p className="login-footer">
            Already have an account?{' '}
            <a href="/login" className="login-link">Log in</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;

