from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.service.facade import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Authenticate via Facade (returns dict if correct, None otherwise)
        user = facade.authenticate_user(credentials['email'], credentials['password'])
        
        if not user:
            return {'error': 'Invalid credentials'}, 401

        # Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user['id']),       # use dict key
            additional_claims={"is_admin": user.get('is_admin', False)}
        )
        
        return {'access_token': access_token}, 200