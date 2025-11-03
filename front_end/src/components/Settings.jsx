import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Settings.css';

const Settings = () => {
  const [activeTab, setActiveTab] = useState('profile'); // profile, password, audits
  const [user, setUser] = useState(null);
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  // Form states
  const [profileData, setProfileData] = useState({
    name: '',
    email: ''
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  // Load user data on mount
  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    const userName = localStorage.getItem('user_name');
    const userEmail = localStorage.getItem('user_email');

    if (!userId) {
      navigate('/login');
      return;
    }

    setUser({ id: userId, name: userName, email: userEmail });
    setProfileData({ name: userName, email: userEmail });
    loadAudits(userId);
  }, [navigate]);

  const loadAudits = async (userId) => {
    try {
      const response = await axios.get(
        `http://localhost:5000/api/audit/${userId}/audits`
      );
      setAudits(response.data);
    } catch (err) {
      console.error('Error loading audits:', err);
      setAudits([]);
    }
  };

  // Update profile
  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      const response = await axios.put(
        `http://localhost:5000/api/users/${user.id}`,
        {
          name: profileData.name,
          email: profileData.email,
          password: user.password, // Keep existing password
          consent_given: true
        }
      );

      // Update localStorage
      localStorage.setItem('user_name', profileData.name);
      localStorage.setItem('user_email', profileData.email);
      
      setSuccess('Profile updated successfully!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Error updating profile');
    } finally {
      setLoading(false);
    }
  };

  // Update password
  const handlePasswordUpdate = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate passwords
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setError('New passwords do not match');
      return;
    }

    if (passwordData.newPassword.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.put(
        `http://localhost:5000/api/users/${user.id}`,
        {
          name: user.name,
          email: user.email,
          password: passwordData.newPassword,
          consent_given: true
        }
      );

      setSuccess('Password updated successfully!');
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.response?.data?.error || 'Error updating password');
    } finally {
      setLoading(false);
    }
  };

  if (!user) return <div className="loading-state">Loading...</div>;

  return (
    <div className="settings-page">
      <div className="settings-container">
        <div className="settings-header">
          <h1 className="settings-title">Account Settings</h1>
          <p className="settings-subtitle">Manage your profile and preferences</p>
        </div>

        {/* Tabs Navigation */}
        <div className="settings-tabs">
          <button
            className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
             Profile
          </button>
          <button
            className={`tab-button ${activeTab === 'password' ? 'active' : ''}`}
            onClick={() => setActiveTab('password')}
          >
             Password
          </button>
          <button
            className={`tab-button ${activeTab === 'audits' ? 'active' : ''}`}
            onClick={() => setActiveTab('audits')}
          >
             Audit History
          </button>
        </div>

        {/* Messages */}
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        {/* Tab Content */}
        <div className="settings-content">
          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="tab-panel">
              <h2 className="panel-title">Personal Information</h2>
              <form onSubmit={handleProfileUpdate} className="settings-form">
                <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input
                    type="text"
                    id="name"
                    value={profileData.name}
                    onChange={(e) => setProfileData({ ...profileData, name: e.target.value })}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({ ...profileData, email: e.target.value })}
                    required
                  />
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Saving...' : 'Save Changes'}
                  </button>
                  <button 
                    type="button" 
                    className="btn btn-ghost"
                    onClick={() => navigate('/dashboard')}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Password Tab */}
          {activeTab === 'password' && (
            <div className="tab-panel">
              <h2 className="panel-title">Change Password</h2>
              <form onSubmit={handlePasswordUpdate} className="settings-form">
                <div className="form-group">
                  <label htmlFor="currentPassword">Current Password</label>
                  <input
                    type="password"
                    id="currentPassword"
                    value={passwordData.currentPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                    placeholder="••••••••"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="newPassword">New Password</label>
                  <input
                    type="password"
                    id="newPassword"
                    value={passwordData.newPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                    placeholder="••••••••"
                    minLength="6"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="confirmPassword">Confirm New Password</label>
                  <input
                    type="password"
                    id="confirmPassword"
                    value={passwordData.confirmPassword}
                    onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                    placeholder="••••••••"
                    minLength="6"
                    required
                  />
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn btn-primary" disabled={loading}>
                    {loading ? 'Updating...' : 'Update Password'}
                  </button>
                </div>
              </form>
            </div>
          )}

          {/* Audits History Tab */}
          {activeTab === 'audits' && (
            <div className="tab-panel">
              <h2 className="panel-title">Audit History</h2>
              {audits.length === 0 ? (
                <div className="empty-state">
                  No audits yet. Create your first audit from the dashboard!
                </div>
              ) : (
                <div className="audits-list">
                  {audits.map((audit, index) => (
                    <div key={audit.id || index} className="audit-item">
                      <div className="audit-info">
                        <h3 className="audit-url">{audit.site || audit.url}</h3>
                        <p className="audit-date">
                           {new Date(audit.timestamp || audit.date).toLocaleString('en-US')}
                        </p>
                      </div>
                      <div className="audit-score">
                        <span className={`score-value ${(audit.score || 0) < 50 ? 'fail' : 'pass'}`}>
                          {audit.score || 0}/100
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;

