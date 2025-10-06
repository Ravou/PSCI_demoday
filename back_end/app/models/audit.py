from .base import db, BaseModel
from datetime import datetime


class Audit(BaseModel):
    """
    Modèle représentant un audit de conformité RGPD.
    Stocke les résultats d'analyse et génère les rapports.
    """
    __tablename__ = 'audits'
    
    # Attributs spécifiques
    userid = db.Column(db.String(36), db.ForeignKey('users.userid', ondelete='CASCADE'), nullable=False, index=True)
    target = db.Column(db.String(500), nullable=False)  # URL du site audité
    consenttype = db.Column(db.String(50), nullable=False)
    ipaddress = db.Column(db.String(50), nullable=False)
    
    # Résultats de l'audit
    status = db.Column(db.String(20), default='pending')  # pending, running, completed, failed
    compliance_score = db.Column(db.Float, nullable=True)  # Score de 0 à 100
    summary = db.Column(db.Text, nullable=True)
    detailed_report = db.Column(db.JSON, nullable=True)  # Rapport complet en JSON
    violations = db.Column(db.JSON, nullable=True)  # Liste des violations détectées
    recommendations = db.Column(db.JSON, nullable=True)  # Recommandations de mise en conformité
    
    # Métadonnées d'exécution
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Index pour recherches
    __table_args__ = (
        db.Index('idx_userid_status', 'userid', 'status'),
        db.Index('idx_target', 'target'),
    )
    
    def __init__(self, target, userid, consenttype, ipaddress):
        """Initialise un nouvel audit"""
        self.target = target
        self.userid = userid
        self.consenttype = consenttype
        self.ipaddress = ipaddress
        self.status = 'pending'
    
    def run_audit(self):
        """
        Lance l'analyse RGPD du site cible.
        Cette méthode devra appeler les services de scraping, NLP et IA.
        """
        try:
            self.status = 'running'
            self.started_at = datetime.utcnow()
            db.session.commit()
            
            # TODO: Implémenter l'appel aux services
            # - Service de scraping pour extraire le contenu
            # - Service NLP pour analyser le texte
            # - Service IA pour détecter les violations RGPD
            
            # Exemple de structure de résultat
            self.compliance_score = 75.5
            self.violations = [
                {
                    'article': 'Article 13 RGPD',
                    'description': 'Information sur le traitement des données manquante',
                    'severity': 'high'
                },
                {
                    'article': 'Article 7 RGPD',
                    'description': 'Consentement non explicite pour les cookies',
                    'severity': 'medium'
                }
            ]
            self.recommendations = [
                {
                    'violation': 'Article 13 RGPD',
                    'recommendation': 'Ajouter une page de politique de confidentialité',
                    'resource': 'https://www.cnil.fr/fr/reglement-europeen-protection-donnees'
                }
            ]
            
            self.status = 'completed'
            self.completed_at = datetime.utcnow()
            
        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            self.completed_at = datetime.utcnow()
        
        finally:
            db.session.commit()
    
    def get_summary(self):
        """Retourne un résumé textuel de l'audit"""
        if self.status != 'completed':
            return f"Audit en statut: {self.status}"
        
        summary = f"Score de conformité: {self.compliance_score}%\n"
        summary += f"Nombre de violations: {len(self.violations) if self.violations else 0}\n"
        
        if self.violations:
            summary += "\nViolations détectées:\n"
            for v in self.violations:
                summary += f"- {v['article']}: {v['description']}\n"
        
        return summary
    
    def to_dict(self):
        """Retourne une représentation dictionnaire de l'audit"""
        return {
            'id': self.id,
            'userid': self.userid,
            'target': self.target,
            'consenttype': self.consenttype,
            'ipaddress': self.ipaddress,
            'status': self.status,
            'compliance_score': self.compliance_score,
            'summary': self.summary,
            'violations': self.violations,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message
        }
    
    def __repr__(self):
        return f'<Audit {self.id} - {self.target} - {self.status}>'