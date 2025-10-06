from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import Audit, ConsentLog, User # À adapter selon ton arborescence
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/rgpd'
db = SQLAlchemy(app)

@app.route('/apiconsent', methods=['POST'])
def record_consent():
    """
    Enregistrement d'un consentement utilisateur.
    Paramètres attendus: userid, consenttype, ipaddress
    """
    data = request.json
    # Validation des paramètres requis
    for field in ['userid', 'consenttype', 'ipaddress']:
        if field not in data:
            abort(400, description=f'Missing required field: {field}')
    
    # Validation du type de consentement (exemple: 'audit', 'data_collection', etc.)
    valid_consent_types = ['audit', 'data_collection', 'analysis']
    if data['consenttype'] not in valid_consent_types:
        abort(400, description='Invalid consent type')
    
    # Créer et enregistrer le consentement
    consent = ConsentLog(
        userid=data['userid'],
        consenttype=data['consenttype'],
        ipaddress=data['ipaddress'],
        timestamp=datetime.utcnow(),
        is_active=True
    )
    db.session.add(consent)
    db.session.commit()
    
    return jsonify({
        'message': 'Consentement enregistré',
        'consent': consent.to_dict()
    }), 201

@app.route('/apiconsent-revoke', methods=['POST'])
def revoke_consent():
    """
    Révocation d'un consentement utilisateur.
    Paramètres attendus: userid, consenttype
    """
    data = request.json
    # Validation des paramètres requis
    for field in ['userid', 'consenttype']:
        if field not in data:
            abort(400, description=f'Missing required field: {field}')
    
    # Rechercher le consentement actif
    consent = ConsentLog.query.filter_by(
        userid=data['userid'],
        consenttype=data['consenttype'],
        is_active=True
    ).first()
    
    if not consent:
        abort(404, description='Aucun consentement actif trouvé')
    
    # Révoquer le consentement
    consent.is_active = False
    consent.revoked_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Consentement révoqué',
        'consent': consent.to_dict()
    }), 200

@app.route('/apiconsent/<userid>', methods=['GET'])
def get_user_consents(userid):
    """
    Récupération de tous les consentements d'un utilisateur (traçabilité RGPD).
    """
    consents = ConsentLog.query.filter_by(userid=userid).all()
    return jsonify([consent.to_dict() for consent in consents]), 200

if __name__ == '__main__':
    app.run(debug=True)
