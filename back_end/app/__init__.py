from flask import Flask, redirect
from flask_restx import Api
from flask_bcrypt import Bcrypt

from app.api.user import api as user_ns
from app.api.audit import api as audit_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    api = Api(app, version='1.0', title='User Consent and Audit API',
              description='PSCI application API', doc='/api/')

    api.add_namespace(user_ns, path='/api/users')
    api.add_namespace(audit_ns, path='/api/audit')

    # Route d'accueil qui redirige vers Swagger
    @app.route('/')
    def index():
        return redirect('/api/')

    return app
