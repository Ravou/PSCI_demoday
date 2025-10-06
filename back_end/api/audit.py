from flask_restx import Namespace, Resource, fields
from app.services.facade import facade  # façade qui gère la logique métier

api = Namespace('audit', description='Audit operations, consent, scraping and audits')

audit_model = api.model('Audit', {
    'target': fields.String(required=True, description='Target of the audit'),
    'findings': fields.List(fields.String, description='List of audit findings')
})

@api.route('/<string:user_id>/audits')
class UserAudits(Resource):
    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all audits for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        audits = facade.list_audits(user_id)
        return [{'target': a.target, 'findings': a.findings, 'timestamp': a.timestamp} for a in audits], 200
