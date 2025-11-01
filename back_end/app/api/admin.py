from flask_restx import Namespace, Resource, fields
from flask import request
from app.service.facade import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('admin', description='Admin operations')

# -------------------------------
# Models for Swagger / Validation
# -------------------------------
admin_user_model = api.model('AdminUser', {
    'name': fields.String(required=True, description='Full name of the user'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

admin_user_update_model = api.model('AdminUserUpdate', {
    'name': fields.String(required=False, description='Full name of the user'),
    'email': fields.String(required=False, description='Email address'),
    'password': fields.String(required=False, description='Password')
})

admin_audit_model = api.model('AdminAudit', {
    'user_id': fields.String(required=True, description='ID of the user'),
    'site': fields.String(required=True, description='Target website or domain'),
    'run_perplexity': fields.Boolean(required=False, description='Run Perplexity AI', default=True)
})

# -------------------------------
# Users (Admin only)
# -------------------------------
@api.route('/users/')
class AdminUserCreate(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(admin_user_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')

        if not email or not password or not name:
            return {'error': 'name, email and password are required'}, 400

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        user = facade.create_user(name=name, email=email, password=password, consent_ip='admin_panel')
        return {'id': user.id, 'email': user.email, 'name': user.name}, 201


@api.route('/users/<string:user_id>')
class AdminUserModify(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(admin_user_update_model, validate=True)
    @jwt_required()
    def put(self, user_id):
        """Update an existing user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.json
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400
            user.email = email

        if name:
            user.name = name
        if password:
            user._password_hash = user._hash_password(password)

        return {'message': 'User updated successfully', 'user': user.to_dict()}, 200


# -------------------------------
# Audits (Admin only)
# -------------------------------
@api.route('/audits/')
class AdminAuditCreate(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(admin_audit_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new audit for a user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        user_id = data.get('user_id')
        site = data.get('site')
        run_perplexity = data.get('run_perplexity', True)

        if not user_id or not site:
            return {'error': 'user_id and site are required'}, 400

        audit = facade.create_audit(user_id, site, run_perplexity=run_perplexity)
        if not audit:
            return {'error': 'Audit creation failed'}, 404

        return {'message': 'Audit created successfully', 'audit': audit.to_dict()}, 201


@api.route('/audits/<string:user_id>/<string:site>')
class AdminAuditModify(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(admin_audit_model, validate=True)
    @jwt_required()
    def put(self, user_id, site):
        """Update an existing audit for a user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        audit = facade.get_audit(user_id, site)
        if not audit:
            return {'error': 'Audit not found'}, 404

        data = request.json
        new_site = data.get('site', site)
        run_perplexity = data.get('run_perplexity', True)

        updated_audit = facade.create_audit(user_id, new_site, run_perplexity=run_perplexity)
        return {'message': 'Audit updated successfully', 'audit': updated_audit.to_dict()}, 200

    @api.doc(security='Bearer Auth')
    @jwt_required()
    def delete(self, user_id, site):
        """Delete an audit for a user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        result = facade.delete_audit(user_id, site)
        if result:
            return {'message': 'Audit deleted successfully'}, 200
        return {'error': 'Audit not found'}, 404