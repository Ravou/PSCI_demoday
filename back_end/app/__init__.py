from flask import Flask, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.api.user import api as user_ns
from app.api.audit import api as audit_ns

# Initialisation des extensions
bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ✅ Initialise SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Configuration CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialise l'API REST
    api = Api(app, version='1.0', title='User Consent and Audit API',
              description='PSCI application API', doc='/api/')

    api.add_namespace(user_ns, path='/api/users')
    api.add_namespace(audit_ns, path='/api/audit')

    # Route d'accueil
    @app.route('/')
    def index():
        return redirect('/api/')

    # Headers CORS
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # ✅ Crée les tables si elles n'existent pas
    with app.app_context():
        db.create_all()

    return app

