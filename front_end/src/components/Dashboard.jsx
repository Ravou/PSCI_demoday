import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

// ✅ Import des images
import auditIcon from '../assets/images/audit.jpg';
import auditProgressIcon from '../assets/images/auditprogress.jpg';
import scoreIcon from '../assets/images/score.jpg';

const Dashboard = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [user, setUser] = useState(null);
  const [audits, setAudits] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const userName = localStorage.getItem('user_name');
    const userEmail = localStorage.getItem('user_email');

    if (!userId) {
      navigate('/login');
      return;
    }

    setUser({ id: userId, name: userName, email: userEmail });
    loadAudits();
  }, [navigate]);

  const loadAudits = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await axios.get(
        `http://localhost:5000/api/audit/audits`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setAudits(response.data);
    } catch (err) {
      console.error('Error loading audits:', err);
      setAudits([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const token = localStorage.getItem('auth_token');
      await axios.post(
        `http://localhost:5000/api/audit/audits`,
        { target: url },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setUrl('');
      loadAudits(); // recharge les audits après création
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

  if (!user) return <div className="loading-state">Loading...</div>;

  // Calcul des stats
  const stats = {
    auditsCompleted: audits.filter(a => a.status === 'completed').length || audits.length,
    auditsInProgress: audits.filter(a => a.status === 'in_progress').length || 0,
    averageScore: audits.length > 0
      ? Math.round(audits.reduce((acc, a) => acc + (a.score || 0), 0) / audits.length)
      : 0
  };

  const lastAudit = audits[audits.length - 1];

  return (
    <div className="dashboard">
      {/* Stats */}
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

      {/* Audit Form */}
      <div className="audit-form-container no-card">
        <p className="audit-instruction">Check your website’s GDPR compliance</p>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} className="audit-form">
          <input
            type="url"
            className="form-input large-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
          />
          <button 
            type="submit" 
            className="btn btn-primary large-button"
            disabled={loading}
          >
            {loading ? 'Launching...' : '+ New Audit'}
          </button>
        </form>
      </div>

      {/* Latest Audit Result */}
      {lastAudit && lastAudit.content?.perplexity_report && (
        <div className="audit-result">
          <h3 className="section-title">Latest Audit Result</h3>
          <div className="audit-details">
            {lastAudit.content.perplexity_report.map((item, i) => (
              <div key={i} className="audit-item card">
                <h4>{item.point}</h4>
                <p><strong>Status:</strong> {item.status}</p>
                <p><strong>Evidence:</strong> {item.evidence}</p>
                <p><strong>Recommendation:</strong> {item.recommendation}</p>
                <p><strong>Articles:</strong> {item.articles}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
