from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config 

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name="development"):
    app = Flask(__name__)
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)

    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.api.user import api as user_ns
    from app.api.audit import api as audit_ns
    from app.api.auth import api as auth_ns
    from app.api.protected import api as protected_ns
    from app.api.admin import api as admin_ns

    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "Type 'Bearer <JWT token>' to authorize."
        }
    }

    api = Api(
        app,
        version='1.0',
        title='User Consent and Audit API',
        description='PSCI application API',
        doc='/api/',
        authorizations=authorizations,
        security='Bearer Auth'
    )

    api.add_namespace(user_ns, path='/api/users')
    api.add_namespace(audit_ns, path='/api/audit')
    api.add_namespace(auth_ns, path='/api/auth')
    api.add_namespace(protected_ns, path='/api/protected')
    api.add_namespace(admin_ns, path='/api/admin')

    @app.route('/')
    def index():
        return redirect('/api/')

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    return app