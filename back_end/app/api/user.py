from flask import request
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

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
})


@api.route('/')
class UserList(Resource):
    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """List all users"""
        users = facade.list_users()
        return [{
            'id': u.id,
            'name': u.name,
            'email': u.email
        } for u in users], 200

    def options(self):
        """Handle preflight CORS requests"""
        return {}, 200

@api.route('/register')
class UserRegister(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User registered successfully')
    @api.response(400, 'Email already registered or consent missing')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check consent
        if not user_data.get('consent_given', False):
            return {'error': 'User must give consent to proceed'}, 400

        # Check if user already exists
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        # Create user via facade
        user = facade.create_user(
            name=user_data['name'],
            email=user_data['email'],
            password=user_data['password'],
            consent_ip=request.remote_addr or "127.0.0.1"
        )

        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'message': 'User registered successfully'
        }, 201

    def options(self):
        return {}, 200

@api.route('/login')
class UserLogin(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Login a user"""
        login_data = api.payload
        email = login_data.get('email')
        password = login_data.get('password')

        user = facade.authenticate_user(email, password)
        if not user:
            return {'error': 'Invalid credentials'}, 401

        return {
            'message': 'Login successful',
            'user_id': user.id,
            'name': user.name,
            'email': user.email
        }, 200

    def options(self):
        return {}, 200

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
        if 'password' in data:
            user._password_hash = user._hash_password(data['password'])
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'message': 'User updated successfully'
        }, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        deleted = facade.delete_user(user_id)
        if not deleted:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200

    def options(self, user_id):
        return {}, 200

