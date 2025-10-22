from flask_restx import Namespace, Resource, fields
from app.services.facade import facade  

api = Namespace('audit', description='Audit operations for GDPR compliance')


audit_model = api.model('Audit', {
    'target': fields.String(required=True, description='Target website or domain to audit'),
})

@api.route('/<string:user_id>/audits')
class UserAudits(Resource):
    @api.expect(audit_model, validate=True)
    @api.response(201, 'Audit created successfully')
    @api.response(403, 'Consent required before running an audit')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Create and run an audit for a given user"""
        # 🔹 Récupère le user
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # 🔹 Vérifie le consentement RGPD
        if not user.consent_given:
            return {'error': 'Consent required before launching an audit'}, 403

        # 🔹 Récupère les infos envoyées
        audit_data = api.payload
        target = audit_data['target']

        # --- Étape 1 : Scraping du site cible ---
        scraped_data = facade.run_scraper(user_id, target)

        # --- Étape 2 : Audit IA via PerplexityAuditor ---
        audit_report = facade.run_perplexity_audit(scraped_data)

        # --- Étape 3 : Création et stockage de l’audit ---
        audit = facade.create_audit(
            user_id=user_id,
            target=target,
            findings=audit_report
        )

        # --- Étape 4 : Retour JSON ---
        return {
            'audit_id': audit.id,
            'user_id': user_id,
            'target': target,
            'findings': audit_report,
            'timestamp': audit.timestamp
        }, 201

    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """List all audits for a given user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        audits = facade.list_audits_for_user(user_id)
        return [
            {
                'audit_id': a.id,
                'target': a.target,
                'findings': a.findings,
                'timestamp': a.timestamp
            }
            for a in audits
        ], 200

