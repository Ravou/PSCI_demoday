from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
from flask_restx import Api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Enable CORS globally with wildcard
    CORS(app)
    
    # Handle OPTIONS manually before anything else
    @app.before_request
    def handle_options():
        if request.method.lower() == 'options':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            }
            return jsonify(headers), 200
    
    # Add CORS headers to all responses
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    # Initialize Flask-RESTX API
    api = Api(
        app,
        version='1.0',
        title='PSCI GDPR Compliance API',
        description='API for GDPR compliance management system',
        doc='/docs',
        prefix='/api'
    )
    
    # Import and register namespaces
    from app.api.users import api as users_ns
    from app.api.audits import api as audits_ns
    from app.api.consent_log import api as consent_ns
    
    # Register namespaces
    api.add_namespace(users_ns, path='/users')
    api.add_namespace(audits_ns, path='/audits')
    api.add_namespace(consent_ns, path='/consents')
    
    print("\n" + "="*60)
    print("API GDPR - Server started with Flask-RESTX")
    print("URL: http://localhost:5000")
    print("Swagger Documentation: http://localhost:5000/docs")
    print("CORS enabled for: localhost:3000")
    print("="*60 + "\n")
    
    return app
