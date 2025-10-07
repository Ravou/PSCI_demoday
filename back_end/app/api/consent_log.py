from flask import Flask, request, jsonify, abort
from app.models import db, ConsentLog, User
from config import Config
from datetime import datetime

app = Flask(__name__)


@app.route('/apiconsent', methods=['POST'])
def record_consent():
    """Enregistrement d'un consentement utilisateur."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['userid', 'consenttype', 'ipaddress']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    # Vérifier que l'utilisateur existe
    user = User.query.filter_by(userid=data['userid']).first()
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    # Validation du type de consentement
    valid_consent_types = ['audit', 'data_collection', 'analysis', 'marketing']
    if data['consenttype'] not in valid_consent_types:
        abort(400, description=f'Type de consentement invalide. Types valides: {valid_consent_types}')
    
    # Créer et enregistrer le consentement
    consent = ConsentLog(
        userid=data['userid'],
        consenttype=data['consenttype'],
        ipaddress=data['ipaddress'],
        consent_text=data.get('consent_text', f'Consentement pour {data["consenttype"]}')
    )
    consent.save()
    
    return jsonify({
        'message': 'Consentement enregistré avec succès',
        'consent': consent.to_dict()
    }), 201

@app.route('/apiconsent-revoke', methods=['POST'])
def revoke_consent():
    """Révocation d'un consentement utilisateur."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['userid', 'consenttype']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    # Vérifier que l'utilisateur existe
    user = User.query.filter_by(userid=data['userid']).first()
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    # Rechercher le consentement actif
    consent = ConsentLog.query.filter_by(
        userid=data['userid'],
        consenttype=data['consenttype'],
        is_active=True
    ).first()
    
    if not consent:
        abort(404, description='Aucun consentement actif trouvé pour ce type')
    
    # Révoquer le consentement
    consent.revoke()
    consent.save()
    
    return jsonify({
        'message': 'Consentement révoqué avec succès',
        'consent': consent.to_dict()
    }), 200

@app.route('/apiconsent/<userid>', methods=['GET'])
def get_user_consents(userid):
    """Récupération de tous les consentements d'un utilisateur."""
    # Vérifier que l'utilisateur existe
    user = User.query.filter_by(userid=userid).first()
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    consents = ConsentLog.query.filter_by(userid=userid).all()
    
    # Séparer les consentements actifs et révoqués
    active_consents = [c for c in consents if c.is_active]
    revoked_consents = [c for c in consents if not c.is_active]
    
    return jsonify({
        'userid': userid,
        'total_consents': len(consents),
        'active_consents': len(active_consents),
        'revoked_consents': len(revoked_consents),
        'consents': [consent.to_dict() for consent in consents]
    }), 200

@app.route('/apiconsent/verify', methods=['POST'])
def verify_consent():
    """Vérification qu'un consentement actif existe."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['userid', 'consenttype']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    has_consent = ConsentLog.has_active_consent(data['userid'], data['consenttype'])
    
    return jsonify({
        'userid': data['userid'],
        'consenttype': data['consenttype'],
        'has_active_consent': has_consent
    }), 200
