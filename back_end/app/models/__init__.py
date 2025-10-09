"""
Modèles de données
Ordre d'import: BaseModel -> User -> ConsentLog -> Audit
"""
from .base import db, BaseModel

# Import dans l'ordre des dépendances
from .user import User
from .consent_log import ConsentLog
from .audit import Audit

# Export explicite
__all__ = ['db', 'BaseModel', 'User', 'ConsentLog', 'Audit']
