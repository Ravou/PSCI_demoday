import sys
import os

# Ajouter le dossier courant au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify
from app.models import db
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Import des routes depuis chaque module
# Note: Importer les fonctions, pas les apps Flask
import app.api.users as users_api
import app.api.consent_log as consent_api
import app.api.audits as audits_api

# Enregistrer les routes manuellement
app.add_url_rule('/apiregister', 'register_user', users_api.register_user, methods=['POST'])
app.add_url_rule('/apilogin', 'login_user', users_api.login_user, methods=['POST'])
app.add_url_rule('/apiuserprofile', 'get_user_profile', users_api.get_user_profile, methods=['GET'])
app.add_url_rule('/apiuserprofile/<userid>', 'update_user_profile', users_api.update_user_profile, methods=['PUT'])
app.add_url_rule('/apiuser/<userid>', 'delete_user', users_api.delete_user, methods=['DELETE'])
app.add_url_rule('/apiuser/<userid>/audits', 'get_user_audits', users_api.get_user_audits, methods=['GET'])
app.add_url_rule('/apiuser/<userid>/consents', 'get_user_consents_from_users', users_api.get_user_consents, methods=['GET'])

app.add_url_rule('/apiconsent', 'record_consent', consent_api.record_consent, methods=['POST'])
app.add_url_rule('/apiconsent-revoke', 'revoke_consent', consent_api.revoke_consent, methods=['POST'])
app.add_url_rule('/apiconsent/<userid>', 'get_consents', consent_api.get_user_consents, methods=['GET'])
app.add_url_rule('/apiconsent/verify', 'verify_consent', consent_api.verify_consent, methods=['POST'])

app.add_url_rule('/audits', 'create_audit', audits_api.create_audit, methods=['POST'])
app.add_url_rule('/audits', 'get_all_audits', audits_api.get_all_audits, methods=['GET'])
app.add_url_rule('/audits/<int:audit_id>', 'get_audit', audits_api.get_audit, methods=['GET'])
app.add_url_rule('/audits/<int:audit_id>/run', 'run_audit', audits_api.run_audit, methods=['POST'])
app.add_url_rule('/audits/<int:audit_id>/summary', 'get_audit_summary', audits_api.get_audit_summary, methods=['GET'])
app.add_url_rule('/audits/<int:audit_id>', 'delete_audit', audits_api.delete_audit, methods=['DELETE'])

# Route d'accueil
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