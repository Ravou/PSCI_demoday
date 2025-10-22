from flask import Flask
from flask_restx import Api
from app.api.user import api as users_ns
from app.api.audit import api as audit_ns
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)

    # Crée l'API RESTx avec Swagger
    api = Api(
        app,
        version='1.0',
        title='RGPD Audit API',
        description='API pour gérer les utilisateurs et audits RGPD',
        doc='/docs'  # Swagger disponible sur /docs
    )

    # Ajoute les namespaces
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(audit_ns, path='/audit')

    return app