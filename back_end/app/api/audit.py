from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        default=True
    )
})


# -------------------------------
# Liste ou création d’audits (par l’utilisateur connecté)
# -------------------------------
@api.route('/audits')
class UserAudits(Resource):
    @jwt_required()
    @api.expect(audit_model, validate=True)
    @api.response(201, 'Audit created successfully')
    def post(self):
        """Create a full audit for the logged-in user"""
        current_user_id = get_jwt_identity()  # Récupère depuis le JWT

        payload = api.payload
        target = payload['target']
        run_perplexity = payload.get('run_perplexity', True)

        audit = facade.create_audit(current_user_id, target, run_perplexity=run_perplexity)
        if not audit:
            return {'error': 'Audit creation failed'}, 500

        return audit, 201

    @jwt_required()
    @api.response(200, 'Audits retrieved successfully')
    def get(self):
        """List all audits for the logged-in user"""
        current_user_id = get_jwt_identity()
        audits = facade.list_audits(current_user_id)
        return audits, 200

    def options(self):
        """Handle preflight CORS requests"""
        return {}, 200


# -------------------------------
# Audit spécifique (par site)
# -------------------------------
@api.route('/audits/<string:site>')
class SingleAudit(Resource):
    @jwt_required()
    @api.response(200, 'Audit retrieved successfully')
    @api.response(404, 'Audit not found')
    def get(self, site):
        """Get a specific audit by site for the logged-in user"""
        current_user_id = get_jwt_identity()
        audit = facade.get_audit(current_user_id, site)
        if not audit:
            return {'error': 'Audit not found'}, 404
        return audit, 200

    @jwt_required()
    @api.expect(audit_model, validate=True)
    @api.response(200, 'Audit updated successfully')
    @api.response(404, 'Audit not found')
    def put(self, site):
        """Update audit target and rerun full pipeline"""
        current_user_id = get_jwt_identity()
        payload = api.payload
        new_target = payload['target']
        run_perplexity = payload.get('run_perplexity', True)

        updated_audit = facade.create_audit(current_user_id, new_target, run_perplexity=run_perplexity)
        if not updated_audit:
            return {'error': 'Audit update failed'}, 500

        return updated_audit, 200

    @jwt_required()
    @api.response(200, 'Audit deleted successfully')
    @api.response(404, 'Audit not found')
    def delete(self, site):
        """Delete an audit for a specific site"""
        current_user_id = get_jwt_identity()
        audits = facade.list_audits(current_user_id)

        for audit in audits:
            if audit['site'] == site:
                audits.remove(audit)
                return {'message': 'Audit deleted successfully'}, 200

        return {'error': 'Audit not found'}, 404

    def options(self, site):
        """Handle preflight CORS requests"""
        return {}, 200


