from flask import Flask, request, jsonify, abort
from app.models import db, User, Audit, ConsentLog
from config import Config

app = Flask(__name__)


@app.route('/apiregister', methods=['POST'])
def register_user():
    """Création d'un nouveau compte utilisateur."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['email', 'password']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    # Vérifier si l'email existe déjà
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        abort(409, description='Un utilisateur avec cet email existe déjà')
    
    # Créer le nouvel utilisateur
    user = User(
        email=data['email'],
        password=data['password'],
        name=data.get('name', ''),
        organization=data.get('organization', '')
    )
    user.save()
    
    return jsonify({
        'message': 'Utilisateur créé avec succès',
        'user': user.to_dict()
    }), 201

@app.route('/apilogin', methods=['POST'])
def login_user():
    """Authentification utilisateur."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['email', 'password']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    # Rechercher l'utilisateur
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        abort(401, description='Email ou mot de passe incorrect')
    
    # Mettre à jour la dernière connexion
    from datetime import datetime
    user.last_login = datetime.utcnow()
    user.save()
    
    return jsonify({
        'message': f'Bienvenue, {user.name or user.email}',
        'userprofile': user.to_dict()
    }), 200

@app.route('/apiuserprofile', methods=['GET'])
def get_user_profile():
    """Récupération du profil utilisateur via query parameter."""
    userid = request.args.get('userid')
    
    if not userid:
        abort(400, description='Paramètre userid manquant')
    
    user = User.query.filter_by(userid=userid).first()
    
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    return jsonify(user.to_dict()), 200

@app.route('/apiuserprofile/<userid>', methods=['PUT'])
def update_user_profile(userid):
    """Mise à jour du profil utilisateur."""
    user = User.query.filter_by(userid=userid).first()
    
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    data = request.json
    
    # Mise à jour des champs fournis
    if 'name' in data:
        user.name = data['name']
    if 'organization' in data:
        user.organization = data['organization']
    if 'email' in data:
        # Vérifier que le nouvel email n'est pas déjà utilisé
        existing = User.query.filter_by(email=data['email']).first()
        if existing and existing.userid != userid:
            abort(409, description='Cet email est déjà utilisé')
        user.email = data['email']
    
    user.save()
    
    return jsonify({
        'message': 'Profil mis à jour avec succès',
        'user': user.to_dict()
    }), 200

@app.route('/apiuser/<userid>', methods=['DELETE'])
def delete_user(userid):
    """Suppression complète d'un utilisateur (droit à l'oubli RGPD)."""
    user = User.query.filter_by(userid=userid).first()
    
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    # Les audits et consentements seront supprimés automatiquement (cascade)
    user.delete()
    
    return jsonify({
        'message': 'Utilisateur et toutes ses données supprimés (droit à l\'oubli RGPD)'
    }), 200

@app.route('/apiuser/<userid>/audits', methods=['GET'])
def get_user_audits(userid):
    """Récupération de tous les audits d'un utilisateur."""
    user = User.query.filter_by(userid=userid).first()
    
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    audits = Audit.query.filter_by(userid=userid).all()
    
    return jsonify({
        'userid': userid,
        'total_audits': len(audits),
        'audits': [audit.to_dict() for audit in audits]
    }), 200

@app.route('/apiuser/<userid>/consents', methods=['GET'])
def get_user_consents(userid):
    """Récupération de tous les consentements d'un utilisateur."""
    user = User.query.filter_by(userid=userid).first()
    
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    consents = ConsentLog.query.filter_by(userid=userid).all()
    
    return jsonify({
        'userid': userid,
        'total_consents': len(consents),
        'consents': [consent.to_dict() for consent in consents]
    }), 200
