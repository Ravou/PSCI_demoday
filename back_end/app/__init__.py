from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

def create_app():
    """
    Factory pattern pour créer l'application Flask SANS DATABASE
    """
    app = Flask(__name__)
    
    # Configuration basique (pas de database)
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Enable CORS pour permettre les requêtes depuis le frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Configuration Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
    
    swagger_template = {
        "info": {
            "title": "PSCI Backend API",
            "description": "API pour la gestion des audits RGPD et des utilisateurs",
            "version": "1.0.0",
            "contact": {
                "name": "PSCI Team",
                "email": "contact@psci.com"
            }
        },
        "schemes": ["http", "https"],
        "tags": [
            {"name": "Users", "description": "Gestion des utilisateurs"},
            {"name": "Audits", "description": "Gestion des audits RGPD"}
        ]
    }
    
    # Initialiser Swagger
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Importer et enregistrer les blueprints API
    try:
        from app.api.users import bp as users_bp
        from app.api.audits import bp as audits_bp
        
        app.register_blueprint(users_bp)
        app.register_blueprint(audits_bp)
        
        print("✅ Blueprints enregistrés avec succès")
    except ImportError as e:
        print(f"⚠️  Erreur lors de l'import des blueprints: {e}")
        print("📝 Créez les fichiers app/api/users.py et app/api/audits.py")
    
    # Route de test
    @app.route('/')
    def index():
        return {
            "message": "PSCI Backend API",
            "status": "running",
            "version": "1.0.0",
            "swagger_docs": "/docs"
        }
    
    @app.route('/health')
    def health():
        """
        Health check endpoint
        ---
        tags:
          - Health
        responses:
          200:
            description: API est en bonne santé
        """
        return {"status": "healthy"}, 200
    
    return app
