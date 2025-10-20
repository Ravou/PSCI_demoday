from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('consentlog', description='Consentlog operations, consent, scraping and audits')

consent_model = api.model('Consent', {
    'consent_type': fields.String(required=True, description='Type of consent'),
    'site_url': fields.String(required=True, description='URL of the site to crawl')
})

@api.route('/<string:user_id>/consent')
class UserConsent(Resource):
    @api.expect(consent_model, validate=True)
    @api.response(201, 'Consent recorded successfully')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Record consent for a user to crawl/scrape a site"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        consent_data = api.payload
        consent = facade.record_consent(user_id, consent_data['consent_type'], consent_data['site_url'])
        return {'user_id': user_id, 'consent_type': consent.consent_type, 'site_url': consent.site_url}, 201

    @api.response(200, 'User consents retrieved successfully')
    def get(self, user_id):
        """Get all consents for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        consents = facade.list_consents(user_id)
        return [{'consent_type': c.consent_type, 'site_url': c.site_url, 'timestamp': c.timestamp} for c in consents], 200
