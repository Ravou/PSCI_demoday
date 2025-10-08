import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.models import db
from config import Config

# Créer l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Activer CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialiser la base de données
db.init_app(app)

# Créer l'API Flask-RESTX avec documentation Swagger
api = Api(
    app,
    version='1.0',
    title='API RGPD - Projet PSCI',
    description='API REST pour la gestion des audits RGPD avec documentation Swagger',
    doc='/docs'  # Documentation Swagger accessible sur /docs
)

# Importer et enregistrer les namespaces
from app.api.users import api as users_ns
from app.api.consent_log import api as consents_ns
from app.api.audits import api as audits_ns

api.add_namespace(users_ns, path='/users')
api.add_namespace(consents_ns, path='/consents')
api.add_namespace(audits_ns, path='/audits')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("=" * 60)
    print("API RGPD - Serveur démarré avec Flask-RESTX")
    print("URL: http://localhost:5000")
    print("Documentation Swagger: http://localhost:5000/docs")
    print("CORS activé pour: localhost:3000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
