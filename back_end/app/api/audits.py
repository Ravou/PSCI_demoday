from flask import Flask, request, jsonify, abort
from app.models import db, Audit, ConsentLog, User
from config import Config

app = Flask(__name__)


@app.route('/audits', methods=['POST'])
def create_audit():
    """Création d'un nouvel audit RGPD."""
    data = request.json
    
    # Validation des paramètres requis
    for field in ['target', 'userid', 'consenttype', 'ipaddress']:
        if field not in data:
            abort(400, description=f'Champ requis manquant: {field}')
    
    # Vérifier que l'utilisateur existe
    user = User.query.filter_by(userid=data['userid']).first()
    if not user:
        abort(404, description='Utilisateur non trouvé')
    
    # Vérifier le consentement utilisateur AVANT de créer l'audit
    if not ConsentLog.has_active_consent(data['userid'], data['consenttype']):
        abort(403, description='Consentement actif requis pour créer un audit')
    
    # Validation de l'URL cible
    import re
    url_pattern = re.compile(
        r'^https?://'  # http:// ou https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domaine
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # port optionnel
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    if not url_pattern.match(data['target']):
        abort(400, description='URL cible invalide')
    
    # Créer et enregistrer l'audit
    audit = Audit(
        target=data['target'],
        userid=data['userid'],
        consenttype=data['consenttype'],
        ipaddress=data['ipaddress']
    )
    audit.save()
    
    return jsonify({
        'message': 'Audit créé avec succès',
        'audit': audit.to_dict()
    }), 201

@app.route('/audits', methods=['GET'])
def get_all_audits():
    """Récupération de tous les audits avec filtres optionnels."""
    # Paramètres de requête optionnels
    userid = request.args.get('userid')
    status = request.args.get('status')
    limit = request.args.get('limit', type=int)
    
    # Construire la requête
    query = Audit.query
    
    if userid:
        # Vérifier que l'utilisateur existe
        user = User.query.filter_by(userid=userid).first()
        if not user:
            abort(404, description='Utilisateur non trouvé')
        query = query.filter_by(userid=userid)
    
    if status:
        valid_statuses = ['pending', 'running', 'completed', 'failed']
        if status not in valid_statuses:
            abort(400, description=f'Status invalide. Status valides: {valid_statuses}')
        query = query.filter_by(status=status)
    
    # Ordonner par date de création (plus récent en premier)
    query = query.order_by(Audit.created_at.desc())
    
    if limit:
        query = query.limit(limit)
    
    audits = query.all()
    
    return jsonify({
        'total_audits': len(audits),
        'filters': {
            'userid': userid,
            'status': status,
            'limit': limit
        },
        'audits': [audit.to_dict() for audit in audits]
    }), 200

@app.route('/audits/<int:audit_id>', methods=['GET'])
def get_audit(audit_id):
    """Récupération d'un audit spécifique."""
    audit = Audit.query.get(audit_id)
    
    if not audit:
        abort(404, description='Audit non trouvé')
    
    return jsonify(audit.to_dict()), 200

@app.route('/audits/<int:audit_id>/run', methods=['POST'])
def run_audit(audit_id):
    """Exécution d'un audit RGPD."""
    audit = Audit.query.get(audit_id)
    
    if not audit:
        abort(404, description='Audit non trouvé')
    
    if audit.status not in ['pending', 'failed']:
        abort(400, description=f'Impossible d\'exécuter un audit avec le statut: {audit.status}')
    
    # Vérifier que le consentement est toujours actif
    if not ConsentLog.has_active_consent(audit.userid, audit.consenttype):
        abort(403, description='Consentement expiré ou révoqué. Impossible d\'exécuter l\'audit')
    
    # Exécuter l'audit (appelle la méthode du modèle)
    audit.run_audit()
    
    return jsonify({
        'message': 'Audit exécuté avec succès',
        'audit': audit.to_dict()
    }), 200

@app.route('/audits/<int:audit_id>/summary', methods=['GET'])
def get_audit_summary(audit_id):
    """Récupération du résumé d'un audit."""
    audit = Audit.query.get(audit_id)
    
    if not audit:
        abort(404, description='Audit non trouvé')
    
    summary = audit.get_summary()
    
    return jsonify({
        'audit_id': audit_id,
        'status': audit.status,
        'target': audit.target,
        'summary': summary,
        'compliance_score': audit.compliance_score,
        'total_violations': len(audit.violations) if audit.violations else 0,
        'completed_at': audit.completed_at.isoformat() if audit.completed_at else None
    }), 200

@app.route('/audits/<int:audit_id>', methods=['DELETE'])
def delete_audit(audit_id):
    """Suppression d'un audit."""
    audit = Audit.query.get(audit_id)
    
    if not audit:
        abort(404, description='Audit non trouvé')
    
    audit.delete()
    
    return jsonify({
        'message': 'Audit supprimé avec succès'
    }), 200

