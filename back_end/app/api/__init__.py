from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialisation de la base de données
db = SQLAlchemy()

def create_app():
    """Factory pattern pour créer l'application Flask"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/rgpd'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialiser la DB avec l'app
    db.init_app(app)
    
    # Importer et enregistrer les blueprints
    from .audits import app as audits_bp
    from .consent_log import app as consent_bp
    from .users import app as users_bp
    
    return app
