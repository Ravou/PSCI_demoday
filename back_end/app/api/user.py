# app/api/users.py
from flask_restx import Namespace, Resource, fields
from app.service.facade import facade

api = Namespace('users', description='User operations and consent management')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
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

        # Vérifie le consentement
        if not user_data.get('consent_given', False):
            return {'error': 'User must give consent to proceed'}, 400

        # Vérifie si l'utilisateur existe déjà
        for u in facade.list_users():
            if u.email == user_data['email']:
                return {'error': 'Email already registered'}, 400

        # Crée le nouvel utilisateur via la façade
        user = facade.create_user(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            consent_ip="127.0.0.1"  # ou récupéré depuis request.remote_addr
        )

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'consent_given': user_data['consent_given']
        }, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [{
            'id': u.id,
            'name': u.name,
            'email': u.email
        } for u in users], 200


@api.route('/<string:user_id>')
class UserResource(Resource):
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        data = api.payload
        user.name = data.get('name', user.name)
        user.password = data.get('password', user.password)
        # Note : on ne met pas à jour email pour simplifier
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
