from flask_restx import Namespace, Resource, fields
from app.services.facade import facade  # façade qui gère la logique métier

api = Namespace('users', description='User operations, consent, scraping and audits')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'consent_given': fields.Boolean(required=True, description='Consent to scrape the website and process data'),
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered or consent missing')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Vérifie si l'utilisateur existe déjà
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Vérifie que le consentement a été donné
        if not user_data.get('consent_given', False):
            return {'error': 'User must give consent to proceed'}, 400

        # Crée le nouvel utilisateur
        new_user = facade.create_user(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            consent_given=user_data['consent_given'],
            consent_ip=user_data.get('consent_ip')
        )

        return {
            'id': new_user.id,
            'name': new_user.name,
            'email': new_user.email,
            'consent_given': new_user.consent_given
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.list_users()
        return [
            {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'consent_given': u.consent_given
            }
            for u in users
        ], 200

@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'name': user.name, 'email': user.email}, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        updated_data = api.payload
        user = facade.update_user(user_id, updated_data)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'name': user.name, 'email': user.email}, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user account"""
        success = facade.delete_user(user_id)
        if not success:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200

@api.route('/<string:user_id>/scrape')
class UserScrape(Resource):
    @api.response(200, 'Scraping completed successfully')
    @api.response(403, 'Consent required')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Launch the web scraper for a user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        if not user.consent_given:
            return {'error': 'Consent required to scrape'}, 403

        # Ici, tu peux lancer ton WebCrawler et stocker le résultat
        scraped_data = facade.scrape_user_data(user)
        return {'message': 'Scraping completed', 'scraped_data': scraped_data}, 200
    
@api.route('/user/<string:user_id>')
class UserAudits(Resource):
    @api.response(200, 'Audits retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """List all audits for a given user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        audits = facade.list_audits_for_user(user_id)
        return [audit.to_dict() for audit in audits], 200

    @api.expect(audit_model, validate=True)
    @api.response(201, 'Audit created successfully')
    @api.response(404, 'User not found')
    def post(self, user_id):
        """Create a new audit for the user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Exemple : lancer ton WebCrawler + PerplexityAuditor
        scraped_data = facade.run_scraper(user_id)
        audit_report = facade.run_perplexity_audit(scraped_data)

        new_audit = facade.create_audit(
            user_id=user_id,
            scraped_data=scraped_data,
            audit_report=audit_report
        )

        return new_audit.to_dict(), 201

