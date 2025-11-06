import React, { useState } from 'react';
import axios from 'axios';
import './Login.css';

const AuditForm = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(''); // <-- ajouté

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setSuccess('');
    setLoading(true);

    try {
      const token = localStorage.getItem('token');

      if (!token) {
        setError('Utilisateur non authentifié');
        return;
      }

      const response = await axios.post(
        'http://localhost:5000/api/audit/audits',
        { target: url },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      setResult(response.data);
      setSuccess('Audit créé avec succès !'); // maintenant ok
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error ||
        err.response?.data?.message ||
        'Erreur lors de l\'audit'
      );
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
          {success && <div className="success-message">{success}</div>}

          {result && (
            <div>
              <div style={{
                background: 'rgba(57, 255, 20, 0.1)',
                border: '1px solid rgba(57, 255, 20, 0.3)',
                color: 'var(--accent-primary)',
                padding: 'var(--spacing-md)',
                borderRadius: 'var(--radius-md)',
                marginBottom: 'var(--spacing-xl)',
                textAlign: 'center'
              }}>
                <p><strong>Audit ID:</strong> {result.id || 'N/A'}</p>
                <p><strong>Site audité:</strong> {result.site || 'N/A'}</p>
                <p><strong>Date:</strong> {result.timestamp ? new Date(result.timestamp).toLocaleString() : 'N/A'}</p>
              </div>

              {result.content && (
                <div>
                  <h2>Détails de l’audit</h2>
                  {result.content.map((item, index) => (
                    <div key={index} className="audit-item" style={{
                      border: '1px solid #ddd',
                      padding: '1rem',
                      borderRadius: '0.5rem',
                      marginBottom: '1rem'
                    }}>
                      <h3>{item.point}</h3>
                      <p><strong>Status:</strong> {item.status}</p>
                      <p><strong>Evidence:</strong> {item.evidence}</p>
                      <p><strong>Recommendation:</strong> {item.recommendation}</p>
                    </div>
                  ))}
                </div>
              )}
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
