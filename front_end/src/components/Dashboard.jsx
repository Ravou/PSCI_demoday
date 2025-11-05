import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

// ✅ Import des images (place-les dans front_end/src/assets/)
import auditIcon from '../assets/images/audit.jpg';
import auditProgressIcon from '../assets/images/auditprogress.jpg';
import scoreIcon from '../assets/images/score.jpg';

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
      console.error('Error loading audits:', err);
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
      setError('User not logged in');
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

      console.log('Audit created:', response.data);
      alert('Audit was created successfully!');
      setUrl('');
      loadAudits(user.id);
    } catch (err) {
      console.error('Error creating audit:', err);
      setError(
        err.response?.data?.error || 
        err.response?.data?.message || 
        'Error creating audit'
      );
    } finally {
      setLoading(false);
    }
  };


  
  const stats = {
    auditsCompleted: audits.filter(a => a.status === 'completed').length || audits.length,
    auditsInProgress: audits.filter(a => a.status === 'in_progress').length || 0,
    averageScore: audits.length > 0 
      ? Math.round(audits.reduce((acc, a) => acc + (a.score || 0), 0) / audits.length) 
      : 0
  };

  if (!user) {
    return <div className="loading-state">Loading...</div>;
  }

  return (
    <div className="dashboard">
      {/* ✅ Header SANS boutons Settings et Logout */}
      <div className="dashboard-header">
        <div className="header-content">
          <h1 className="dashboard-title">Dashboard</h1>
          <p className="dashboard-subtitle">
            Welcome, <span className="user-name">{user.name}</span> • {user.email}
          </p>
          </div>
        </div>


      {/* ✅ Stats Grid AVEC images */}
      <div className="stats-grid">
        <div className="stat-card card">
          <img src={auditIcon} alt="Audit Completed" className="stat-image" />
          <div className="stat-content">
            <div className="stat-value stat-value-primary">{stats.auditsCompleted}</div>
            <div className="stat-label">Audits Completed</div>
          </div>
        </div>

        <div className="stat-card card">
          <img src={auditProgressIcon} alt="Audit In Progress" className="stat-image" />
          <div className="stat-content">
            <div className="stat-value">{stats.auditsInProgress}</div>
            <div className="stat-label">Audits In Progress</div>
          </div>
        </div>

        <div className="stat-card card">
          <img src={scoreIcon} alt="Average Score" className="stat-image" />
          <div className="stat-content">
            <div className="stat-value">{stats.averageScore}/100</div>
            <div className="stat-label">Average Score</div>
          </div>
        </div>
      </div>

      {/* ✅ NOUVELLE SECTION : Bannière 24/7 Protection */}
      <div className="protection-banner card">
        <div className="banner-tag">24/7 PROTECTION WITH LIVE RECORDING</div>
        <h2 className="banner-title">
          Your safety is our mission. Your trust is our commitment.
        </h2>
        <p className="banner-subtitle">
          Click below to schedule your free risk assessment and learn how we can help protect your world.
        </p>
        <button 
          className="btn btn-primary btn-large"
          onClick={() => navigate('/contact')}
        >
          START PROTECTING YOUR PRESENCE
        </button>
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
        <h3 className="section-title"> Audit History</h3>

        {loadingAudits ? (
          <div className="empty-state">Loading audits...</div>
        ) : audits.length === 0 ? (
          <div className="empty-state">
            Enter your website URL to run a compliance audit!
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
                    <span className="meta-icon"></span>
                    <span>{new Date(audit.timestamp || audit.date).toLocaleString('en-US')}</span>
                  </div>
                </div>

                <div className="history-result">
                  <div className={`result-score ${(audit.score || 0) < 50 ? 'score-fail' : 'score-pass'}`}>
                    {audit.score || 0}/100
                  </div>
                  <div className={`result-status ${(audit.score || 0) < 50 ? 'status-fail' : 'status-pass'}`}>
                    {(audit.score || 0) < 50 ? '✗ Non-Compliant' : '✓ Compliant'}
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

