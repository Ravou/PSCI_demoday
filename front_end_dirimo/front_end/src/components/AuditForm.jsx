import React, { useState, useEffect } from 'react';
import { auditService, consentService } from '../services/apiService';

const AuditForm = ({ userid }) => {
  const [target, setTarget] = useState('');
  const [hasConsent, setHasConsent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Vérifier le consentement au chargement
  useEffect(() => {
    checkConsent();
  }, [userid]);

  const checkConsent = async () => {
    try {
      const response = await consentService.verify(userid, 'audit');
      setHasConsent(response.has_active_consent);
    } catch (err) {
      console.error('Erreur vérification consentement:', err);
    }
  };

  const requestConsent = async () => {
    try {
      await consentService.record({
        userid,
        consenttype: 'audit',
        ipaddress: '127.0.0.1', // À remplacer par l'IP réelle
        consent_text: 'J\'accepte l\'analyse RGPD de mon site web'
      });
      setHasConsent(true);
      setSuccess('Consentement enregistré avec succès');
    } catch (err) {
      setError(err.description || 'Erreur d\'enregistrement du consentement');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    if (!hasConsent) {
      setError('Vous devez donner votre consentement avant de créer un audit');
      setLoading(false);
      return;
    }

    try {
      // Créer l'audit
      const auditResponse = await auditService.create({
        target,
        userid,
        consenttype: 'audit',
        ipaddress: '127.0.0.1'
      });

      console.log('Audit créé:', auditResponse);
      const auditId = auditResponse.audit.id;

      // Exécuter l'audit automatiquement
      const runResponse = await auditService.run(auditId);
      console.log('Audit exécuté:', runResponse);

      setSuccess(`Audit créé et exécuté avec succès! ID: ${auditId}`);
      setTarget('');
    } catch (err) {
      setError(err.description || 'Erreur lors de la création de l\'audit');
      console.error('Erreur audit:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="audit-form-container">
      <h2>Créer un audit RGPD</h2>
      
      {!hasConsent && (
        <div className="consent-warning">
          <p>⚠️ Vous devez donner votre consentement pour effectuer des audits</p>
          <button onClick={requestConsent}>Donner mon consentement</button>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>URL du site à auditer:*</label>
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
          {loading ? 'Analyse en cours...' : 'Lancer l\'audit'}
        </button>
      </form>
    </div>
  );
};

export default AuditForm;

