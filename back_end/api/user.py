from flask_restx import Namespace, Resource, fields
from app.services.facade import facade  # façade qui gère la logique métier

api = Namespace('users', description='User operations, consent, scraping and audits')

# === Modèles Swagger / validation ===
user_model = api.model('User', {
    'name': fields.String(required=True, description='Name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        new_user = facade.create_user(user_data['name'], user_data['email'], user_data['password'])
        return {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}, 201

    @api.response(200, 'Users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.list_users()
        return [{'id': u.id, 'name': u.name, 'email': u.email} for u in users], 200


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