from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='User operations and consent management')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'consent_given': fields.Boolean(required=True, description='Consent to process and audit data'),
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

        # Vérifie le consentement
        if not user_data.get('consent_given', False):
            return {'error': 'User must give consent to proceed'}, 400

        # Crée le nouvel utilisateur
        new_user = facade.create_user(
            email=user_data['email'],
            password=user_data['password'],
            consent_given=user_data['consent_given'],
        )

        return new_user.to_dict(), 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [u.to_dict() for u in users], 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        user = facade.update_user(user_id, api.payload)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        success = facade.delete_user(user_id)
        if not success:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
