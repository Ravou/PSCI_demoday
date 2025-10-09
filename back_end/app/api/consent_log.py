from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('consents', description='Consent management operations')

# Modèle Swagger pour les consentements
consent_model = api.model('Consent', {
    'user_id': fields.String(required=True, description='User ID'),
    'consenttype': fields.String(required=True, description='Type of consent (audit, data_collection, analysis, marketing)'),
    'ipaddress': fields.String(required=True, description='IP address of the user'),
    'consent_text': fields.String(description='Text of the consent')
})

consent_revoke_model = api.model('ConsentRevoke', {
    'user_id': fields.String(required=True, description='User ID'),
    'consenttype': fields.String(required=True, description='Type of consent to revoke')
})

consent_verify_model = api.model('ConsentVerify', {
    'user_id': fields.String(required=True, description='User ID'),
    'consenttype': fields.String(required=True, description='Type of consent to verify')
})


@api.route('/')
class ConsentList(Resource):
    @api.expect(consent_model, validate=True)
    @api.response(201, 'Consent recorded successfully')
    @api.response(400, 'Invalid consent type or missing fields')
    @api.response(404, 'User not found')
    def post(self):
        """Record a new consent"""
        consent_data = api.payload
        
        # Vérifier que l'utilisateur existe
        user = facade.get_user(consent_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404
        
        # Valider le type de consentement
        valid_types = ['audit', 'data_collection', 'analysis', 'marketing']
        if consent_data['consenttype'] not in valid_types:
            return {'error': f'Invalid consent type. Valid types: {valid_types}'}, 400
        
        # Créer le consentement
        consent = facade.create_consent(
            user_id=consent_data['user_id'],
            consenttype=consent_data['consenttype'],
            ipaddress=consent_data['ipaddress'],
            consent_text=consent_data.get('consent_text', f'Consent for {consent_data["consenttype"]}')
        )
        
        return {
            'message': 'Consent recorded successfully',
            'consent': {
                'id': consent.id,
                'user_id': consent.userid,
                'consenttype': consent.consenttype,
                'is_active': consent.is_active,
                'created_at': consent.created_at.isoformat()
            }
        }, 201


@api.route('/revoke')
class ConsentRevoke(Resource):
    @api.expect(consent_revoke_model, validate=True)
    @api.response(200, 'Consent revoked successfully')
    @api.response(404, 'User not found or no active consent')
    def post(self):
        """Revoke an active consent"""
        revoke_data = api.payload
        
        user = facade.get_user(revoke_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 404
        
        # Révoquer le consentement
        success = facade.revoke_consent(
            user_id=revoke_data['user_id'],
            consenttype=revoke_data['consenttype']
        )
        
        if not success:
            return {'error': 'No active consent found for this type'}, 404
        
        return {'message': 'Consent revoked successfully'}, 200


@api.route('/verify')
class ConsentVerify(Resource):
    @api.expect(consent_verify_model, validate=True)
    @api.response(200, 'Consent verification result')
    def post(self):
        """Verify if a consent is active"""
        verify_data = api.payload
        
        has_consent = facade.verify_consent(
            user_id=verify_data['user_id'],
            consenttype=verify_data['consenttype']
        )
        
        return {
            'user_id': verify_data['user_id'],
            'consenttype': verify_data['consenttype'],
            'has_active_consent': has_consent
        }, 200


@api.route('/<string:user_id>')
class UserConsents(Resource):
    @api.response(200, 'Consents retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get all consents for a specific user"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        consents = facade.list_consents(user_id)
        
        active_consents = [c for c in consents if c.is_active]
        revoked_consents = [c for c in consents if not c.is_active]
        
        return {
            'user_id': user_id,
            'total_consents': len(consents),
            'active_consents': len(active_consents),
            'revoked_consents': len(revoked_consents),
            'consents': [
                {
                    'id': c.id,
                    'consenttype': c.consenttype,
                    'is_active': c.is_active,
                    'created_at': c.created_at.isoformat(),
                    'revoked_at': c.revoked_at.isoformat() if c.revoked_at else None
                }
                for c in consents
            ]
        }, 200
