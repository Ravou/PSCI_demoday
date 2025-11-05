from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.service.facade import facade

api = Namespace('users', description='User operations and consent management')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'consent_given': fields.Boolean(required=True, description='Consent to process and audit data'),
})


# -----------------------------
# List of users (admin only)
# -----------------------------
@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """List all users (admin only)"""
        claims = get_jwt()
        if not claims.get("is_admin"):
            return {'error': 'Admin access required'}, 403

        users = facade.list_users()
        return [{
            'id': u['id'],
            'name': u['name'],
            'email': u['email']
        } for u in users], 200

    def options(self):
        """Handle preflight CORS requests"""
        return {}, 200


# -----------------------------
# Registration of user (public)
# -----------------------------
@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User registered successfully')
    @api.response(400, 'Email already registered or consent missing')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        if not user_data.get('consent_given', False):
            return {'error': 'User must give consent to proceed'}, 400

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            consent_ip=request.remote_addr or "127.0.0.1"
        )

        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'message': 'User registered successfully'
        }, 201

    def options(self):
        return {}, 200


# -----------------------------
# Management of a specific user (JWT)
# -----------------------------
@api.route('/<string:user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details (self or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if current_user_id != user_id and not claims.get("is_admin"):
            return {'error': 'Unauthorized access'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email']
        }, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user info (self or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if current_user_id != user_id and not claims.get("is_admin"):
            return {'error': 'Unauthorized access'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload
        user['name'] = data.get('name', user['name'])
        if 'password' in data:
            user['password_hash'] = facade.user_repo._hash_password(data['password'])

        return {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'message': 'User updated successfully'
        }, 200

    @jwt_required()
    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete user (self or admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if current_user_id != user_id and not claims.get("is_admin"):
            return {'error': 'Unauthorized access'}, 403

        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404

        return {'message': 'User deleted successfully'}, 200

    def options(self, user_id):
        return {}, 200

