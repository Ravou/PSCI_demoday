import React, { useState, useEffect } from 'react';
import { auditService } from '../services/apiService';
import AuditForm from './AuditForm';

const Dashboard = ({ userid }) => {
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadAudits();
  }, [userid]);

  const loadAudits = async () => {
    try {
      setLoading(true);
      const response = await auditService.list(userid);
      setAudits(response.audits || []);
    } catch (error) {
      console.error('Erreur chargement audits:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAuditCompleted = () => {
    setShowForm(false);
    loadAudits(); // Recharger la liste
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getScoreColor = (score) => {
    if (score >= 70) return 'var(--vert-principal)';
    if (score >= 40) return 'var(--orange-warning)';
    return 'var(--rouge-erreur)';
  };

  const getScoreLabel = (score) => {
    if (score >= 70) return '✓ Conforme';
    if (score >= 40) return '⚠️ Partiellement conforme';
    return '✗ Non conforme';
  };

  return (
    <div className="container" style={{maxWidth: '1200px', padding: '20px'}}>
      {/* Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '30px'
      }}>
        <h1 style={{color: 'var(--vert-principal)', margin: 0}}>
          📊 Tableau de bord
        </h1>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
          style={{
            padding: '12px 24px',
            background: 'var(--vert-principal)',
            color: 'var(--noir-fonce)',
            border: 'none',
            borderRadius: '8px',
            fontSize: '16px',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}
        >
          {showForm ? '❌ Annuler' : '➕ Nouvel audit'}
        </button>
      </div>

      {/* Formulaire d'audit (si affiché) */}
      {showForm && (
        <div style={{marginBottom: '40px'}}>
          <AuditForm userid={userid} onAuditCompleted={handleAuditCompleted} />
        </div>
      )}

      {/* Statistiques */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
        gap: '20px',
        marginBottom: '40px'
      }}>
        <div className="card" style={{textAlign: 'center', padding: '30px'}}>
          <div style={{fontSize: '48px', fontWeight: 'bold', color: 'var(--vert-principal)'}}>
            {audits.length}
          </div>
          <div style={{color: 'var(--gris-clair)', marginTop: '10px'}}>
            Audits réalisés
          </div>
        </div>

        <div className="card" style={{textAlign: 'center', padding: '30px'}}>
          <div style={{fontSize: '48px', fontWeight: 'bold', color: 'var(--vert-secondaire)'}}>
            {audits.filter(a => a.status === 'completed').length}
          </div>
          <div style={{color: 'var(--gris-clair)', marginTop: '10px'}}>
            Audits terminés
          </div>
        </div>

        <div className="card" style={{textAlign: 'center', padding: '30px'}}>
          <div style={{fontSize: '48px', fontWeight: 'bold', color: getScoreColor(
            audits.length > 0 
              ? Math.round(audits.reduce((sum, a) => sum + (a.score || 0), 0) / audits.length)
              : 0
          )}}>
            {audits.length > 0 
              ? Math.round(audits.reduce((sum, a) => sum + (a.score || 0), 0) / audits.length)
              : 0}/100
          </div>
          <div style={{color: 'var(--gris-clair)', marginTop: '10px'}}>
            Score moyen
          </div>
        </div>
      </div>

      {/* Historique des audits */}
      <div>
        <h2 style={{color: 'var(--vert-secondaire)', marginBottom: '20px'}}>
          📋 Historique des audits
        </h2>

        {loading ? (
          <div className="card" style={{textAlign: 'center', padding: '40px'}}>
            <p style={{color: 'var(--gris-clair)'}}>⏳ Chargement...</p>
          </div>
        ) : audits.length === 0 ? (
          <div className="card" style={{textAlign: 'center', padding: '40px'}}>
            <p style={{color: 'var(--gris-clair)', marginBottom: '20px'}}>
              Aucun audit réalisé pour le moment
            </p>
            <button 
              onClick={() => setShowForm(true)}
              className="btn btn-primary"
            >
              🚀 Lancer votre premier audit
            </button>
          </div>
        ) : (
          <div style={{display: 'flex', flexDirection: 'column', gap: '15px'}}>
            {audits.map((audit) => (
              <div 
                key={audit.audit_id} 
                className="card"
                style={{
                  padding: '20px',
                  display: 'grid',
                  gridTemplateColumns: '1fr auto auto',
                  gap: '20px',
                  alignItems: 'center',
                  transition: 'transform 0.2s',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => e.currentTarget.style.transform = 'translateX(5px)'}
                onMouseLeave={(e) => e.currentTarget.style.transform = 'translateX(0)'}
              >
                {/* Info audit */}
                <div>
                  <h3 style={{
                    color: 'var(--vert-principal)',
                    margin: '0 0 8px 0',
                    fontSize: '18px'
                  }}>
                    {audit.target}
                  </h3>
                  <p style={{
                    color: 'var(--gris-clair)',
                    margin: 0,
                    fontSize: '14px'
                  }}>
                    🕒 {formatDate(audit.timestamp)}
                  </p>
                </div>

                {/* Score */}
                <div style={{textAlign: 'center'}}>
                  <div style={{
                    fontSize: '32px',
                    fontWeight: 'bold',
                    color: getScoreColor(audit.score || 0)
                  }}>
                    {audit.score || 0}/100
                  </div>
                  <div style={{
                    fontSize: '12px',
                    color: 'var(--gris-clair)',
                    marginTop: '5px'
                  }}>
                    {getScoreLabel(audit.score || 0)}
                  </div>
                </div>

                {/* Statut */}
                <div>
                  <span style={{
                    padding: '8px 16px',
                    borderRadius: '20px',
                    fontSize: '14px',
                    fontWeight: 'bold',
                    background: audit.status === 'completed' 
                      ? 'var(--vert-principal)' 
                      : audit.status === 'pending'
                      ? 'var(--orange-warning)'
                      : 'var(--rouge-erreur)',
                    color: 'var(--noir-fonce)'
                  }}>
                    {audit.status === 'completed' ? '✓ Terminé' :
                     audit.status === 'pending' ? '⏳ En cours' :
                     '✗ Échoué'}
                  </span>
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

