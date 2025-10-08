"""
Modèles de données
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import des modèles
from .user import User
from .consent_log import ConsentLog
from .audit import Audit

