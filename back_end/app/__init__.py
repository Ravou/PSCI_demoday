from flask import Flask
from flask_cors import CORS
from flask_restx import Api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS globally
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize Flask-RESTX API with /api prefix
    api = Api(
        app,
        version='1.0',
        title='PSCI GDPR Compliance API',
        description='API for GDPR compliance management system',
        doc='/docs',
        prefix='/api'  # This makes all routes start with /api
    )
    
    # Import and register namespaces
    from app.api.users import api as users_ns
    from app.api.audits import api as audits_ns
    from app.api.consent_log import api as consent_ns
    
    # Register namespaces (they will be under /api/)
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(audits_ns, path='/audits')
    api.add_namespace(consent_ns, path='/consents')
    
    return app
