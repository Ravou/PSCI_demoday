from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade
import traceback

api = Namespace('users', description='User operations, consent, scraping and audits')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'organization': fields.String(required=False, description='Organisation of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        try:
            print("\n=== DEBUG REGISTER ===")
            print(f"Payload received: {api.payload}")
            print(f"Request headers: {dict(request.headers)}")
            print(f"Content-Type: {request.content_type}")
            
            user_data = api.payload
            
            print(f"Extracted user_data: {user_data}")
            print(f"Email: {user_data.get('email')}")
            print(f"Name: {user_data.get('name')}")
            print(f"Password: {'***' if user_data.get('password') else 'MISSING'}")
            print(f"Organization: {user_data.get('organization')}")
            
            # Vérifier si l'email existe déjà
            print("Checking if email exists...")
            existing_user = facade.get_user_by_email(user_data['email'])
            
            if existing_user:
                print(f"Email already registered: {user_data['email']}")
                print("=====================\n")
                return {'error': 'Email already registered'}, 400
            
            print("Email not found, creating new user...")
            
            # Accepter 'organization' OU 'organisation'
            org_value = user_data.get('organization') or user_data.get('organisation')
            
            print(f"Creating user with org: {org_value}")
            
            # Créer l'utilisateur
            new_user = facade.create_user(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                organisation=org_value
            )
            
            print(f"User created successfully: {new_user.userid}")
            print("=====================\n")
            
            return {
                'message': 'User created successfully',
                'userprofile': {
                    'userid': new_user.userid,
                    'name': new_user.name,
                    'email': new_user.email,
                    'organization': new_user.organization
                }
            }, 201
            
        except Exception as e:
            print("\n=== ERROR IN REGISTER ===")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print(f"Full traceback:")
            traceback.print_exc()
            print("=========================\n")
            
            # Retourner l'erreur avec détails
            return {
                'error': str(e),
                'type': type(e).__name__,
                'details': 'Check server logs for full traceback'
            }, 400

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of all users"""
        try:
            users = facade.list_users()
            return [{
                'userid': u.userid,
                'name': u.name,
                'email': u.email,
                'organization': u.organization
            } for u in users], 200
        except Exception as e:
            print(f"Error listing users: {e}")
            traceback.print_exc()
            return {'error': str(e)}, 400


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
            'userid': user.userid,
            'name': user.name,
            'email': user.email,
            'organization': user.organization
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user information"""
        updated_data = api.payload
        user = facade.update_user(user_id, updated_data)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'userid': user.userid,
            'name': user.name,
            'email': user.email,
            'organization': user.organization
        }, 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user account"""
        success = facade.delete_user(user_id)
        if not success:
            return {'error': 'User not found'}, 404
        return {'message': 'User deleted successfully'}, 200
