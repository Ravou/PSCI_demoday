from flask import Flask, jsonify
from app.models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Import des routes depuis chaque module
from app.api.users import *
from app.api.consent_log import *  
from app.api.audits import *

# Route d'accueil de l'API
@app.route('/')
def index():
    return jsonify({
        'message': 'API RGPD - Projet PSCI',
        'version': '1.0.0',
        'status': 'operational',
        'endpoints': {
            'users': {
                'register': 'POST /apiregister',
                'login': 'POST /apilogin', 
                'profile': 'GET /apiuserprofile?userid=<id>',
                'update': 'PUT /apiuserprofile/<userid>',
                'delete': 'DELETE /apiuser/<userid>',
                'audits': 'GET /apiuser/<userid>/audits',
                'consents': 'GET /apiuser/<userid>/consents'
            },
            'consents': {
                'record': 'POST /apiconsent',
                'revoke': 'POST /apiconsent-revoke',
                'list': 'GET /apiconsent/<userid>',
                'verify': 'POST /apiconsent/verify'
            },
            'audits': {
                'create': 'POST /audits',
                'list': 'GET /audits',
                'get': 'GET /audits/<id>',
                'run': 'POST /audits/<id>/run',
                'summary': 'GET /audits/<id>/summary',
                'delete': 'DELETE /audits/<id>'
            }
        }
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': 'connected',
        'models': ['User', 'ConsentLog', 'Audit']
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("=" * 60)
    print("API RGPD - Serveur démarré")
    print("URL: http://localhost:5000")
    print("Documentation: http://localhost:5000/")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
