from .base import db, BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(BaseModel):
    """
    Modèle représentant un utilisateur du système RGPD.
    Lié aux audits et consentements pour traçabilité complète.
    """
    __tablename__ = 'users'
    
    # Attributs spécifiques
    userid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relations avec cascade pour suppression RGPD
    audits = db.relationship('Audit', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    consents = db.relationship('ConsentLog', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, email, password, name=None, organization=None):
        """Initialise un nouvel utilisateur avec mot de passe hashé"""
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.organization = organization
    
    def check_password(self, password):
        """Vérifie si le mot de passe fourni est correct"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Met à jour le mot de passe de l'utilisateur"""
        self.password_hash = generate_password_hash(password)
    
    def to_dict(self):
        """Retourne une représentation dictionnaire sans le mot de passe"""
        return {
            'userid': self.userid,
            'email': self.email,
            'name': self.name,
            'organization': self.organization,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
