from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from app.service.facade import facade

api = Namespace(
    'protected',
    description='Zone protégée',
    authorizations={
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    security='Bearer Auth'
)

@api.route('')
class ProtectedResource(Resource):
    @jwt_required()
    @api.doc(security='Bearer Auth')
    def get(self):
        """A protected endpoint that requires a valid JWT token"""
        current_user = get_jwt_identity()

        return {'message': f'Hello, user {current_user}'}, 200
