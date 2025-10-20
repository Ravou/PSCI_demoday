from flask import Flask
from flask_restx import Api
from flask_cors import Bcrypt

from back_end.api.user import api as user_ns
from back_end.api.consentlog import api as consentlog_ns
from back_end.api.audit import api as audit_ns

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)

    api = Api(app, version='1.0', title='User Consent and Audit API',
              description='PSCI application API', doc='/api/')

    api.add_namespace(user_ns, path='/api/users')
    api.add_namespace(consentlog_ns, path='/api/consentlog')
    api.add_namespace(audit_ns, path='/api/audit')

    return app