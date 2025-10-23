from flask_restx import Namespace, Resource, fields
from app.service.facade import facade

api = Namespace('audit', description='Audit operations for GDPR compliance')

audit_model = api.model('Audit', {
    'target': fields.String(required=True, description='Target website or domain to audit'),
    'run_perplexity': fields.Boolean(required=False, description='Run Perplexity AI on this audit', default=False)
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
        run_perplexity = payload.get('run_perplexity', False)

        api_key = None
        if run_perplexity:
            api_key = "YOUR_PERPLEXITY_API_KEY"  # ou récupérer depuis .env / config

        audit = facade.create_audit(user_id, target, api_key=api_key)
        if not audit:
            return {'error': 'Audit creation failed'}, 500

        return {
            'id': audit.id,
            'user_id': audit.user_id,
            'site': audit.site,
            'timestamp': audit.timestamp.isoformat(),
            'content': audit.content
        }, 201

    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """List all audits for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        audits = facade.list_audits(user_id)
        return [{
            'id': a.id,
            'user_id': a.user_id,
            'site': a.site,
            'timestamp': a.timestamp.isoformat(),
            'content': a.content
        } for a in audits], 200

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
        return {
            'id': audit.id,
            'user_id': audit.user_id,
            'site': audit.site,
            'timestamp': audit.timestamp.isoformat(),
            'content': audit.content
        }, 200

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
        run_perplexity = payload.get('run_perplexity', False)
        api_key = "YOUR_PERPLEXITY_API_KEY" if run_perplexity else None

        updated_audit = facade.create_audit(user_id, new_target, api_key=api_key)
        return {
            'id': updated_audit.id,
            'user_id': updated_audit.user_id,
            'site': updated_audit.site,
            'timestamp': updated_audit.timestamp.isoformat(),
            'content': updated_audit.content
        }, 200

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




