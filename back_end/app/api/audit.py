from flask_restx import Namespace, Resource, fields
from app.services.facade import facade  # façade qui gère la logique métier

api = Namespace('audit', description='Audit operations, consent, scraping and audits')

audit_model = api.model('Audit', {
    'target': fields.String(required=True, description='Target of the audit'),
    'findings': fields.List(fields.String, description='List of audit findings')
})

@api.route('/<string:user_id>/audits')
class UserAudits(Resource):

    @api.expect(audit_model, valiate=True)
    @api.response(201, 'Audit created successfully')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Create an audit for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        audit_data = api.payload
        consent_id = audit_data['consent_id']
        target = audit_data['target']
        findings = audit_data['findings']

        consent = facade.get_consent(consent_id)
        if not consent or consent.user_id != user_id:
            return {'error': 'Consent not found or does not belong to user'}, 404

        audit = facade.create_audit(user_id, consent_id, target, findings)
        return [{'audit_id': audit.id, 'user_id': user_id, 'consent_id': consent_id, 'target': target, 'findings': findings, 'timestamp': audit.timestamp} for audit in audit], 201

    @api.expect(audit_model, validate=True)
    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all audits for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        audits = facade.list_audits(user_id)
        return [{'target': a.target, 'findings': a.findings, 'timestamp': a.timestamp} for a in audits], 200
