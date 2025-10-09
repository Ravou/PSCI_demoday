import React, { useState, useEffect } from 'react';
import { auditService, consentService } from '../services/apiService';

const AuditForm = ({ userid }) => {
  const [target, setTarget] = useState('');
  const [hasConsent, setHasConsent] = useState(false);
  const [consentId, setConsentId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [auditResult, setAuditResult] = useState(null);
  const [currentAuditId, setCurrentAuditId] = useState(null);
  useEffect(() => {
    checkConsent();
  }, [userid]);

  const checkConsent = async () => {
    try {
      const response = await consentService.list(userid);
      
      const activeConsent = response.consents?.find(
        c => c.consenttype === 'audit' && c.is_active
      );
      
      if (activeConsent) {
        setHasConsent(true);
        setConsentId(activeConsent.id);
        console.log('Consent trouvé:', activeConsent.id);
      } else {
        setHasConsent(false);
        setConsentId(null);
      }
    } catch (err) {
      console.error('Erreur vérification consentement:', err);
      setHasConsent(false);
      setConsentId(null);
    }
  };

  const requestConsent = async () => {
    try {
      const response = await consentService.record({
        user_id: userid,
        consenttype: 'audit',
        ipaddress: '127.0.0.1',
        consent_text: 'J\'accepte l\'analyse RGPD de mon site web'
      });
      
      setConsentId(response.consent?.id);
      setHasConsent(true);
      setSuccess('✓ Consentement enregistré');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.description || 'Erreur consentement');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setAuditResult(null);
    setLoading(true);

    if (!hasConsent || !consentId) {
      setError('⚠️ Consentement requis');
      setLoading(false);
      return;
    }

    try {
      // 1. Créer l'audit
      const createResponse = await auditService.create({
        target,
        userid,
        consent_id: consentId
      });

      console.log('Audit créé:', createResponse);
      const auditId = createResponse.audit?.audit_id;
      
      if (!auditId) {
        throw new Error('ID audit manquant');
      }

      setCurrentAuditId(auditId);
      setSuccess('⏳ Analyse en cours...');

      // 2. Lancer l'audit
      const runResponse = await auditService.run(auditId);
      console.log('Audit exécuté:', runResponse);

      // 3. Récupérer le résumé
      const summaryResponse = await auditService.getSummary(auditId);
      console.log('Résumé brut:', summaryResponse);

      // ✅ Parser les violations et recommendations (ce sont des chaînes JSON)
      const parsedResult = {
        ...summaryResponse,
        violations: (() => {
          try {
            return typeof summaryResponse.violations === 'string' && summaryResponse.violations.trim() !== ''
              ? JSON.parse(summaryResponse.violations)
              : (Array.isArray(summaryResponse.violations) ? summaryResponse.violations : []);
          } catch (e) {
            console.error('Erreur parsing violations:', e);
            return [];
          }
        })(),
        recommendations: (() => {
          try {
            return typeof summaryResponse.recommendations === 'string' && summaryResponse.recommendations.trim() !== ''
              ? JSON.parse(summaryResponse.recommendations)
              : (Array.isArray(summaryResponse.recommendations) ? summaryResponse.recommendations : []);
          } catch (e) {
            console.error('Erreur parsing recommendations:', e);
            return [];
          }
        })()
      };

      console.log('Résumé parsé:', parsedResult);
      setAuditResult(parsedResult);
      setSuccess('✓ Audit terminé !');
      setTarget('');
      
    } catch (err) {
   
      console.error('Erreur audit:', err);
      setError(err.description || err.message || 'Erreur lors de l\'audit');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{maxWidth: '900px'}}>
      <h2>🔍 Créer un audit RGPD</h2>
      
      {!hasConsent && (
        <div className="info" style={{marginBottom: '20px'}}>
          <p>⚠️ Consentement requis pour effectuer des audits</p>
          <button onClick={requestConsent} className="btn btn-primary" style={{marginTop: '10px'}}>
            Donner mon consentement
          </button>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>URL du site à auditer *</label>
          <input
            type="url"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="https://example.com"
            required
            disabled={loading || !hasConsent}
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <button type="submit" disabled={loading || !hasConsent}>
          {loading ? '⏳ Analyse en cours...' : '🚀 Lancer l\'audit'}
        </button>
      </form>

      {/* Affichage des résultats */}
      {auditResult && (
        <div className="audit-results" style={{marginTop: '40px'}}>
          {/* Score */}
          <div className="card" style={{marginBottom: '20px', background: 'var(--gris-moyen)'}}>
            <h3 style={{color: 'var(--vert-principal)', marginBottom: '20px'}}>
              📊 Score de conformité
            </h3>
            <div style={{textAlign: 'center'}}>
              <div style={{
                fontSize: '72px',
                fontWeight: '900',
                color: auditResult.score >= 70 ? 'var(--vert-principal)' : 
                       auditResult.score >= 40 ? 'var(--orange-warning)' : 
                       'var(--rouge-erreur)',
                textShadow: '0 0 30px var(--ombre-verte)',
                marginBottom: '10px'
              }}>
                {auditResult.score || 0}/100
              </div>
              <p style={{color: 'var(--gris-clair)', fontSize: '16px'}}>
                {auditResult.score >= 70 ? '✓ Conforme' : 
                 auditResult.score >= 40 ? '⚠️ Partiellement conforme' : 
                 '✗ Non conforme'}
              </p>
            </div>
          </div>

          {/* Violations */}
          {auditResult.violations && auditResult.violations.length > 0 && (
            <div className="card" style={{marginBottom: '20px'}}>
              <h3 style={{color: 'var(--rouge-erreur)', marginBottom: '20px'}}>
                ⚠️ Violations RGPD ({auditResult.violations.length})
              </h3>
              {auditResult.violations.map((violation, index) => (
                <div key={index} style={{
                  background: 'var(--gris-moyen)',
                  padding: '15px',
                  borderRadius: '8px',
                  marginBottom: '15px',
                  borderLeft: `4px solid ${
                    violation.severity === 'critical' ? 'var(--rouge-erreur)' :
                    violation.severity === 'high' ? '#ff9933' :
                    'var(--orange-warning)'
                  }`
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                    <strong style={{color: 'var(--vert-secondaire)'}}>{violation.article}</strong>
                    <span style={{
                      padding: '4px 12px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      background: violation.severity === 'critical' ? 'var(--rouge-erreur)' :
                                 violation.severity === 'high' ? '#ff9933' : 'var(--orange-warning)',
                      color: 'var(--noir-fonce)'
                    }}>
                      {violation.severity}
                    </span>
                  </div>
                  <p style={{color: 'var(--texte-blanc)', margin: 0}}>
                    {violation.description}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* Recommendations */}
          {auditResult.recommendations && auditResult.recommendations.length > 0 && (
            <div className="card">
              <h3 style={{color: 'var(--vert-principal)', marginBottom: '20px'}}>
                💡 Recommandations ({auditResult.recommendations.length})
              </h3>
              {auditResult.recommendations.map((rec, index) => (
                <div key={index} style={{
                  background: 'var(--gris-moyen)',
                  padding: '15px',
                  borderRadius: '8px',
                  marginBottom: '15px',
                  borderLeft: '4px solid var(--vert-principal)'
                }}>
                  <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                    <strong style={{color: 'var(--vert-secondaire)', display: 'block'}}>
                      {rec.title}
                    </strong>
                    <span style={{
                      padding: '4px 12px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      fontWeight: 'bold',
                      background: rec.priority === 'critical' ? 'var(--rouge-erreur)' :
                                 rec.priority === 'high' ? '#ff9933' : 'var(--orange-warning)',
                      color: 'var(--noir-fonce)'
                    }}>
                      {rec.priority}
                    </span>
                  </div>
                  <p style={{color: 'var(--texte-blanc)', margin: 0}}>
                    {rec.description}
                  </p>
                </div>
              ))}
            </div>
          )}

          {/* Summary text */}
          {auditResult.summary_text && typeof auditResult.summary_text === 'string' && (
            <div className="card" style={{marginTop: '20px'}}>
              <h3 style={{color: 'var(--vert-secondaire)', marginBottom: '15px'}}>
                📋 Résumé de l'audit
              </h3>
              <p style={{color: 'var(--texte-blanc)', whiteSpace: 'pre-wrap', lineHeight: '1.6'}}>
                {auditResult.summary_text}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default AuditForm;

