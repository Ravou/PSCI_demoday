import React, { useState } from 'react';

const Dashboard = ({ userid }) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Données fictives pour l'exemple
  const stats = {
    auditsCompleted: 2,
    auditsInProgress: 1,
    averageScore: 8
  };

  const auditHistory = [
    {
      url: 'https://www.carrefour.fr',
      date: '13 oct. 2025, 09:57',
      score: 0,
      status: 'Non conforme'
    }
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/api/audit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url, userid }),
      });

      const data = await response.json();

      if (response.ok) {
        alert('Audit lancé avec succès !');
        setUrl('');
      } else {
        setError(data.error || 'Audit failed');
      }
    } catch (err) {
      setError('Connection error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  
  return (
    <div style={{
      maxWidth: '1400px',
      margin: '0 auto',
      padding: '60px 40px'
    }}>
      {/* Header */}
      <div style={{marginBottom: '50px'}}>
        <h1 style={{
          fontSize: 'clamp(32px, 4vw, 48px)',
          fontWeight: '900',
          color: 'var(--texte-blanc)',
          marginBottom: '10px'
        }}>
          Dashboard
        </h1>
        <p style={{
          fontSize: '16px',
          color: 'var(--texte-gris)'
        }}>
          Monitor your GDPR compliance audits
        </p>
      </div>

      {/* Stats Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
        gap: '30px',
        marginBottom: '50px'
      }}>
        <div style={{
          background: 'rgba(26, 31, 46, 0.6)',
          border: '1px solid rgba(0, 255, 136, 0.2)',
          borderRadius: '16px',
          padding: '30px',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--vert-neon)',
            marginBottom: '10px'
          }}>
            {stats.auditsCompleted}
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            Audits Completed
          </div>
        </div>

        <div style={{
          background: 'rgba(26, 31, 46, 0.6)',
          border: '1px solid rgba(0, 255, 136, 0.2)',
          borderRadius: '16px',
          padding: '30px',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--texte-blanc)',
            marginBottom: '10px'
          }}>
            {stats.auditsInProgress}
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            Audits In Progress
          </div>
        </div>

        <div style={{
          background: 'rgba(26, 31, 46, 0.6)',
          border: '1px solid rgba(0, 255, 136, 0.2)',
          borderRadius: '16px',
          padding: '30px',
          backdropFilter: 'blur(10px)'
        }}>
          <div style={{
            fontSize: '48px',
            fontWeight: '900',
            color: 'var(--texte-blanc)',
            marginBottom: '10px'
          }}>
            {stats.averageScore}/100
          </div>
          <div style={{
            fontSize: '14px',
            color: 'var(--texte-gris)',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}>
            Average Score
          </div>
        </div>
      </div>

      {/* New Audit Section */}
      <div style={{
        background: 'rgba(26, 31, 46, 0.6)',
        border: '1px solid rgba(0, 255, 136, 0.2)',
        borderRadius: '16px',
        padding: '40px',
        backdropFilter: 'blur(10px)',
        marginBottom: '50px'
      }}>
        <h3 style={{
          fontSize: '24px',
          fontWeight: '700',
          color: 'var(--texte-blanc)',
          marginBottom: '20px'
        }}>
          Launch New Audit
        </h3>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit} style={{
          display: 'flex',
          gap: '15px',
          flexWrap: 'wrap'
        }}>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            required
            style={{
              flex: '1 1 300px',
              padding: '14px 18px',
              background: 'var(--gris-fonce)',
              border: '1px solid rgba(0, 255, 136, 0.2)',
              borderRadius: '8px',
              color: 'var(--texte-blanc)',
              fontSize: '15px'
            }}
          />
          <button 
            type="submit" 
            disabled={loading}
            className="btn btn-primary"
            style={{
              padding: '14px 40px'
            }}
          >
            {loading ? 'Launching...' : '+ New Audit'}
          </button>
        </form>
      </div>

      {/* Audit History */}
      <div>
        <h3 style={{
          fontSize: '24px',
          fontWeight: '700',
          color: 'var(--texte-blanc)',
          marginBottom: '25px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          📋 Audit History
        </h3>

        <div style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '15px'
        }}>
          {auditHistory.map((audit, index) => (
            <div key={index} style={{
              background: 'rgba(26, 31, 46, 0.6)',
              border: '1px solid rgba(0, 255, 136, 0.2)',
              borderRadius: '12px',
              padding: '25px 30px',
              backdropFilter: 'blur(10px)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '20px'
            }}>
              <div style={{flex: '1 1 300px'}}>
                <a href={audit.url} target="_blank" rel="noopener noreferrer" style={{
                  color: 'var(--vert-neon)',
                  textDecoration: 'none',
                  fontSize: '16px',
                  fontWeight: '600',
                  display: 'block',
                  marginBottom: '8px',
                  transition: 'all 0.3s'
                }}>
                  {audit.url}
                </a>
                <div style={{
                  color: 'var(--texte-gris)',
                  fontSize: '13px'
                }}>
                  🕐 {audit.date}
                </div>
              </div>

              <div style={{
                textAlign: 'right'
              }}>
                <div style={{
                  fontSize: '32px',
                  fontWeight: '900',
                  color: audit.score === 0 ? '#ff6b6b' : 'var(--vert-neon)',
                  marginBottom: '5px'
                }}>
                  {audit.score}/100
                </div>
                <div style={{
                  color: audit.score === 0 ? '#ff6b6b' : 'var(--texte-gris)',
                  fontSize: '13px',
                  textTransform: 'uppercase',
                  fontWeight: '600'
                }}>
                  ✗ {audit.status}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;


