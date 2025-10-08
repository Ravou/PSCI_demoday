from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('audits', description='Audit operations for GDPR compliance')

# Modèle Swagger pour les audits
audit_model = api.model('Audit', {
    'target': fields.String(required=True, description='Target URL to audit'),
    'consent_id': fields.String(required=True, description='Consent ID for this audit')
})

audit_response = api.model('AuditResponse', {
    'audit_id': fields.String(description='Audit ID'),
    'user_id': fields.String(description='User ID'),
    'target': fields.String(description='Target URL'),
    'status': fields.String(description='Audit status'),
    'compliance_score': fields.Float(description='Compliance score percentage'),
    'timestamp': fields.DateTime(description='Audit creation timestamp')
})


@api.route('/<string:user_id>/audits')
class UserAudits(Resource):
    
    @api.expect(audit_model, validate=True)  # ✅ Corrigé : validate au lieu de valiate
    @api.response(201, 'Audit created successfully')
    @api.response(404, 'User or consent not found')
    @api.response(403, 'Consent does not belong to user')
    def post(self, user_id):
        """Create an audit for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        audit_data = api.payload
        consent_id = audit_data['consent_id']
        target = audit_data['target']

        # Vérifier que le consentement existe et appartient à l'utilisateur
        consent = facade.get_consent(consent_id)
        if not consent:
            return {'error': 'Consent not found'}, 404
        
        if consent.user_id != user_id:
            return {'error': 'Consent does not belong to user'}, 403

        # Créer l'audit
        audit = facade.create_audit(
            user_id=user_id,
            consent_id=consent_id,
            target=target
        )
        
        # ✅ Corrigé : retourner un seul objet, pas une liste
        return {
            'message': 'Audit created successfully',
            'audit': {
                'audit_id': audit.id,
                'user_id': user_id,
                'consent_id': consent_id,
                'target': target,
                'status': audit.status,
                'timestamp': audit.created_at.isoformat()
            }
        }, 201

    # ✅ Corrigé : Pas de @api.expect sur un GET
    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all audits for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        audits = facade.list_audits(user_id)
        
        return {
            'user_id': user_id,
            'total_audits': len(audits),
            'audits': [
                {
                    'audit_id': a.id,
                    'target': a.target,
                    'status': a.status,
                    'compliance_score': a.compliance_score,
                    'timestamp': a.created_at.isoformat()
                }
                for a in audits
            ]
        }, 200


@api.route('/<string:audit_id>/run')
class AuditRun(Resource):
    @api.response(200, 'Audit executed successfully')
    @api.response(404, 'Audit not found')
    @api.response(400, 'Audit already completed')
    def post(self, audit_id):
        """Execute an audit"""
        audit = facade.get_audit(audit_id)
        if not audit:
            return {'error': 'Audit not found'}, 404
        
        if audit.status not in ['pending', 'failed']:
            return {'error': f'Cannot execute audit with status: {audit.status}'}, 400
        
        # Exécuter l'audit
        facade.run_audit(audit_id)
        
        return {
            'message': 'Audit executed successfully',
            'audit': {
                'audit_id': audit.id,
                'status': audit.status,
                'compliance_score': audit.compliance_score
            }
        }, 200


@api.route('/<string:audit_id>/summary')
class AuditSummary(Resource):
    @api.response(200, 'Audit summary retrieved successfully')
    @api.response(404, 'Audit not found')
    def get(self, audit_id):
        """Get summary of an audit"""
        audit = facade.get_audit(audit_id)
        if not audit:
            return {'error': 'Audit not found'}, 404
        
        summary = facade.get_audit_summary(audit_id)
        
        return {
            'audit_id': audit_id,
            'target': audit.target,
            'status': audit.status,
            'compliance_score': audit.compliance_score,
            'violations': summary.get('violations', []),
            'recommendations': summary.get('recommendations', []),
            'summary_text': summary.get('summary_text', '')
        }, 200
