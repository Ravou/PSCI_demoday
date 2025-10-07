import sys
import os

# Ajouter le dossier courant au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from app.models import db, User, ConsentLog, Audit
from config import Config

def init_database():
    """Initialise la base de données avec les tables"""
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        print("Suppression des tables existantes...")
        db.drop_all()
        print("Création des nouvelles tables...")
        db.create_all()
        print("✓ Base de données initialisée avec succès!")
        
        # Afficher les tables créées
        print("\nTables créées:")
        print("- users")
        print("- consent_logs")
        print("- audits")

if __name__ == '__main__':
    init_database()
