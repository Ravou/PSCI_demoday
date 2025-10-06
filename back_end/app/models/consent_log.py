from .base import db, BaseModel
from datetime import datetime

class ConsentLog(BaseModel):
    """
    Modèle pour tracer tous les consentements utilisateurs.
    Exigence RGPD : preuve de consentement explicite et révocable.
    """
    __tablename__ = 'consent_logs'
    
    # Attributs spécifiques
    userid = db.Column(db.String(36), db.ForeignKey('users.userid', ondelete='CASCADE'), nullable=False, index=True)
    consenttype = db.Column(db.String(50), nullable=False)
    ipaddress = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    consent_text = db.Column(db.Text, nullable=True)  # Texte du consentement donné
    
    # Index composite pour recherches rapides
    __table_args__ = (
        db.Index('idx_userid_consenttype', 'userid', 'consenttype'),
    )
    
    def __init__(self, userid, consenttype, ipaddress, consent_text=None):
        """Initialise un nouveau consentement"""
        self.userid = userid
        self.consenttype = consenttype
        self.ipaddress = ipaddress
        self.consent_text = consent_text
        self.is_active = True
    
    def revoke(self):
        """Révoque le consentement"""
        self.is_active = False
        self.revoked_at = datetime.utcnow()
    
    @classmethod
    def has_active_consent(cls, userid, consenttype):
        """Vérifie si un consentement actif existe pour un utilisateur et un type"""
        return cls.query.filter_by(
            userid=userid,
            consenttype=consenttype,
            is_active=True
        ).first() is not None
    
    def to_dict(self):
        """Retourne une représentation dictionnaire du consentement"""
        return {
            'id': self.id,
            'userid': self.userid,
            'consenttype': self.consenttype,
            'ipaddress': self.ipaddress,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'revoked_at': self.revoked_at.isoformat() if self.revoked_at else None,
            'consent_text': self.consent_text
        }
    
    def __repr__(self):
        status = 'Active' if self.is_active else 'Révoqué'
        return f'<ConsentLog {self.userid} - {self.consenttype} - {status}>'
