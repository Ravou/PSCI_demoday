import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const AuditForm = ({ userid }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/api/audits/create', {
        userid,
        target_url: url,
      });

      setResult(response.data);
      alert('Audit créé avec succès !');
    } catch (err) {
      setError(err.response?.data?.message || 'Erreur lors de l\'audit');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-container" style={{ maxWidth: '800px' }}>
        <div className="login-card">
          <h1 className="login-title">
            Audit <span className="text-gradient">RGPD</span>
          </h1>
          <p className="login-subtitle">
            Enter your website URL to run a compliance audit
          </p>

          {error && <div className="error-message">{error}</div>}

          {result && (
            <div style={{
              background: 'rgba(57, 255, 20, 0.1)',
              border: '1px solid rgba(57, 255, 20, 0.3)',
              color: 'var(--accent-primary)',
              padding: 'var(--spacing-md)',
              borderRadius: 'var(--radius-md)',
              marginBottom: 'var(--spacing-xl)',
              textAlign: 'center'
            }}>
              <p><strong>Audit ID:</strong> {result.auditid}</p>
              <p><strong>URL:</strong> {result.target_url}</p>
              <p><strong>Statut:</strong> {result.status}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="login-form">
            <div className="form-group">
              <label htmlFor="url">URL of the website</label>
              <input
                type="url"
                id="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://example.com"
                required
              />
            </div>

            <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
              {loading ? 'Analyse en cours...' : 'Lancer l\'audit'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AuditForm;
