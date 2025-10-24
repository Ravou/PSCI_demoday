import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [audits, setAudits] = useState([]);
  const [loadingAudits, setLoadingAudits] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const userName = localStorage.getItem('user_name');
    const userEmail = localStorage.getItem('user_email');

    if (!userId) {
      navigate('/login');
      return;
    }

    setUser({
      id: userId,
      name: userName,
      email: userEmail
    });

    loadAudits(userId);
  }, [navigate]);

  const loadAudits = async (userId) => {
    try {
      setLoadingAudits(true);
      const response = await axios.get(
        `http://localhost:5000/api/audit/${userId}/audits`
      );
      setAudits(response.data);
    } catch (err) {
      console.error('Erreur chargement audits:', err);
      setAudits([]);
    } finally {
      setLoadingAudits(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    if (!user) {
      setError('Utilisateur non connecté');
      setLoading(false);
      return;
    }

    try {
      const response = await axios.post(
        `http://localhost:5000/api/audit/${user.id}/audits`,
        {
          site_url: url,
          consent_text: '',
          run_nlp: true,
          run_semantic_matching: true,
          use_perplexity: false
        }
      );

      console.log('Audit créé:', response.data);
      alert('Audit lancé avec succès !');
      setUrl('');
      loadAudits(user.id);
    } catch (err) {
      console.error('Erreur création audit:', err);
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Erreur lors de la création de l\'audit'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const stats = {
    auditsCompleted: audits.filter(a => a.status === 'completed').length || audits.length,
    auditsInProgress: audits.filter(a => a.status === 'in_progress').length || 0,
    averageScore: audits.length > 0 
      ? Math.round(audits.reduce((acc, a) => acc + (a.score || 0), 0) / audits.length) 
      : 0
  };

  if (!user) {
    return <div className="loading-state">Chargement...</div>;
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">
            Bienvenue, <span className="user-name">{user.name}</span> • {user.email}
          </p>
        </div>
        <button className="btn-logout" onClick={handleLogout}>
          🚪 Déconnexion
        </button>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card card">
          <div className="stat-icon">✓</div>
          <div className="stat-content">
            <div className="stat-value stat-value-primary">{stats.auditsCompleted}</div>
            <div className="stat-label">Audits Completed</div>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon">⏳</div>
          <div className="stat-content">
            <div className="stat-value">{stats.auditsInProgress}</div>
            <div className="stat-label">Audits In Progress</div>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon">��</div>
          <div className="stat-content">
            <div className="stat-value">{stats.averageScore}/100</div>
            <div className="stat-label">Average Score</div>
          </div>
        </div>
      </div>

      {/* New Audit Form */}
      <div className="card audit-form-container">
        <h3 className="section-title">Launch New Audit</h3>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="audit-form">
          <input
            type="url"
            className="form-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
          />
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Launching...' : '+ New Audit'}
          </button>
        </form>
      </div>

      {/* Audit History */}
      <div className="audit-history">
        <h3 className="section-title">📋 Audit History</h3>

        {loadingAudits ? (
          <div className="empty-state">Chargement des audits...</div>
        ) : audits.length === 0 ? (
          <div className="empty-state">
            Aucun audit pour le moment. Créez-en un ci-dessus !
          </div>
        ) : (
          <div className="history-list">
            {audits.map((audit, index) => (
              <div key={audit.id || index} className="history-item card">
                <div className="history-info">
                  <a 
                    href={audit.site || audit.url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="history-url"
                  >
                    {audit.site || audit.url}
                  </a>
                  <div className="history-meta">
                    <span className="meta-icon">🕐</span>
                    <span>{new Date(audit.timestamp || audit.date).toLocaleString('fr-FR')}</span>
                  </div>
                </div>

                <div className="history-result">
                  <div className={`result-score ${(audit.score || 0) < 50 ? 'score-fail' : 'score-pass'}`}>
                    {audit.score || 0}/100
                  </div>
                  <div className={`result-status ${(audit.score || 0) < 50 ? 'status-fail' : 'status-pass'}`}>
                    {(audit.score || 0) < 50 ? '✗ Non conforme' : '✓ Conforme'}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

