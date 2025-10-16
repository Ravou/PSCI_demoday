from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade
import traceback

api = Namespace('users', description='User operations, authentication and management')

# Swagger Models
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email address of the user'),
    'password': fields.String(required=True, description='Password for the account'),
    'organization': fields.String(required=False, description='Organization name')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

@api.route('/register')
class Register(Resource):
    def options(self):
        return {}, 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user account"""
        try:

            user_data = api.payload

            existing_user = facade.get_user_by_email(user_data['email'])

            if existing_user:

                return {'error': 'Email already registered'}, 400

            org_value = user_data.get('organization') or user_data.get('organisation')

            new_user = facade.create_user(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                organisation=org_value
            )

            return {
                'message': 'User created successfully',
                'user': {
                    'userid': new_user.userid,
                    'name': new_user.name,
                    'email': new_user.email,
                    'organization': new_user.organization
                }
            }, 201

        except Exception as e:

            traceback.print_exc()
            return {'error': str(e), 'type': type(e).__name__}, 400

@api.route('/login')
class Login(Resource):
    def options(self):
        return {}, 200

    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and create session"""
        try:
            login_data = api.payload
            email = login_data.get('email')
            password = login_data.get('password')

            user = facade.get_user_by_email(email)
            if not user:
                return {'error': 'Invalid email or password'}, 401

            if not facade.verify_password(user.userid, password):
                return {'error': 'Invalid email or password'}, 401

            return {
                'message': 'Login successful',
                'user': {
                    'userid': user.userid,
                    'name': user.name,
                    'email': user.email,
                    'organization': user.organization
                }
            }, 200

        except Exception as e:
            traceback.print_exc()
            return {'error': str(e), 'type': type(e).__name__}, 400

@api.route('/')
class UserList(Resource):
    def options(self):
        return {}, 200

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of all registered users"""
        try:
            users = facade.list_users()
            return [{
                'userid': u.userid,
                'name': u.name,
                'email': u.email,
                'organization': u.organization
            } for u in users], 200
        except Exception as e:
      
            traceback.print_exc()
            return {'error': str(e)}, 400

    @api.route('/<string:user_id>')

    class UserResource(Resource):
        def options(self, user_id):
            return {}, 200

    @api.response(200, 'User retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by user ID"""
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return {
                'userid': user.userid,
                'name': user.name,
                'email': user.email,
                'organization': user.organization
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {'error': str(e)}, 400

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        try:
            updated_data = api.payload
            user = facade.update_user(user_id, updated_data)
            if not user:
                return {'error': 'User not found'}, 404
            return {
                'message': 'User updated successfully',
                'user': {
                    'userid': user.userid,
                    'name': user.name,
                    'email': user.email,
                    'organization': user.organization
                }
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {'error': str(e)}, 400

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user account permanently"""
        try:
            success = facade.delete_user(user_id)
            if not success:
                return {'error': 'User not found'}, 404
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            traceback.print_exc()
            return {'error': str(e)}, 400
