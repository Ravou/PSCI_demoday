from flask import Flask, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.api.user import api as user_ns
from app.api.audit import api as audit_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configuration CORS AVANT l'initialisation de l'API
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",  # En production, remplace par "http://localhost:3000"
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    bcrypt.init_app(app)

    api = Api(app, version='1.0', title='User Consent and Audit API',
              description='PSCI application API', doc='/api/')

    api.add_namespace(user_ns, path='/api/users')
    api.add_namespace(audit_ns, path='/api/audit')

    # Route d'accueil qui redirige vers Swagger
    @app.route('/')
    def index():
        return redirect('/api/')

    # Hook pour ajouter les headers CORS à toutes les réponses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app