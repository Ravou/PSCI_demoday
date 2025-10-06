from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from models import Audit, ConsentLog,User  # À adapter selon ton arborescence réelle

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/rgpd'
db = SQLAlchemy(app)

@app.route('/audits', methods=['POST'])
def create_audit():
    data = request.json
    # Validation des paramètres
    for field in ['target', 'userid', 'consenttype', 'ipaddress']:
        if field not in data:
            abort(400, description=f'Missing field {field}')
    # Vérifier le consentement utilisateur
    consent = ConsentLog.query.filter_by(userid=data['userid'], consenttype=data['consenttype']).first()
    if not consent:
        abort(403, description="Consentement requis pour lancer l'audit")
    # Créer et enregistrer l'audit
    audit = Audit(
        target=data['target'],
        userid=data['userid'],
        consenttype=data['consenttype'],
        ipaddress=data['ipaddress']
    )
    db.session.add(audit)
    db.session.commit()
    return jsonify(audit.to_dict()), 201

@app.route('/audits', methods=['GET'])
def get_all_audits():
    audits = Audit.query.all()
    return jsonify([audit.to_dict() for audit in audits]), 200

@app.route('/audits/<int:audit_id>/run', methods=['POST'])
def run_audit(audit_id):
    audit = Audit.query.get(audit_id)
    if not audit:
        abort(404)
    audit.run_audit()  # Cette méthode doit mettre à jour les champs pertinents et sauvegarder en base
    db.session.commit()
    return jsonify(audit.to_dict())

@app.route('/audits/<int:audit_id>/summary', methods=['GET'])
def audit_summary(audit_id):
    audit = Audit.query.get(audit_id)
    if not audit:
        abort(404)
    return jsonify({"summary": audit.get_summary()})

# Endpoint RGPD : suppression d'un audit (droit à l’oubli)
@app.route('/audits/<int:audit_id>', methods=['DELETE'])
def delete_audit(audit_id):
    audit = Audit.query.get(audit_id)
    if not audit:
        abort(404)
    db.session.delete(audit)
    db.session.commit()
    return jsonify({'message': 'Audit supprimé'}), 200

if __name__ == '__main__':
    app.run(debug=True)