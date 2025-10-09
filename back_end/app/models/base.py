from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

# Initialisation de SQLAlchemy
db = SQLAlchemy()

class BaseModel(db.Model):
    """Classe de base pour tous les modèles avec timestamps et UUID"""
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def save(self):
        """Sauvegarde l'instance en base de données"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """Supprime l'instance de la base de données"""
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        """Convertit l'instance en dictionnaire (à surcharger dans les sous-classes)"""
        raise NotImplementedError("La méthode to_dict() doit être implémentée")
