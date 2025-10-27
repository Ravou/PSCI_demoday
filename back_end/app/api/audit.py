from flask_restx import Namespace, Resource, fields
from app.service.facade import facade

api = Namespace('audit', description='Audit operations for GDPR compliance')

# Modèle Swagger / validation
audit_model = api.model('Audit', {
    'target': fields.String(
        required=True,
        description='Target website or domain to audit'
    ),
    'run_perplexity': fields.Boolean(
        required=False,
        description='Run Perplexity AI on this audit',
        default=True  # <-- par défaut True
    )
})

# -------------------------------
# Liste des audits pour un utilisateur
# -------------------------------
@api.route('/<string:user_id>/audits')
class UserAudits(Resource):
    @api.expect(audit_model, validate=True)
    @api.response(201, 'Audit created successfully')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Create a full audit for a user (scraping + NLP + Semantic Matching + optional Perplexity)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        payload = api.payload
        target = payload['target']
        run_perplexity = payload.get('run_perplexity', True)  # <-- par défaut True

        audit = facade.create_audit(user_id, target, run_perplexity=run_perplexity)
        if not audit:
            return {'error': 'Audit creation failed'}, 500

        return audit.to_dict(), 201

    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """List all audits for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        audits = facade.list_audits(user_id)
        return [audit.to_dict() for audit in audits], 200


# -------------------------------
# Audit spécifique pour un site
# -------------------------------
@api.route('/<string:user_id>/audits/<string:site>')
class SingleAudit(Resource):
    @api.response(200, 'Audit retrieved successfully')
    @api.response(404, 'Audit not found')
    def get(self, user_id, site):
        """Get a specific audit by site"""
        audit = facade.get_audit(user_id, site)
        if not audit:
            return {'error': 'Audit not found'}, 404
        return audit.to_dict(), 200

    @api.expect(audit_model, validate=True)
    @api.response(200, 'Audit updated successfully')
    @api.response(404, 'Audit not found')
    def put(self, user_id, site):
        """Update audit target and rerun full pipeline"""
        audit = facade.get_audit(user_id, site)
        if not audit:
            return {'error': 'Audit not found'}, 404

        payload = api.payload
        new_target = payload['target']
        run_perplexity = payload.get('run_perplexity', True)  # <-- par défaut True

        updated_audit = facade.create_audit(user_id, new_target, run_perplexity=run_perplexity)
        return updated_audit.to_dict(), 200

    @api.response(200, 'Audit deleted successfully')
    @api.response(404, 'Audit not found')
    def delete(self, user_id, site):
        """Delete an audit for a specific site"""
        audits = facade.list_audits(user_id)
        for audit in audits:
            if audit.site == site:
                audits.remove(audit)
                return {'message': 'Audit deleted successfully'}, 200
        return {'error': 'Audit not found'}, 404


