import bcrypt
from app.models import db, User, ConsentLog, Audit

class Facade:
    """Business logic layer"""

    # ==================== USERS ====================
    def create_user(self, name, email, password, organisation=None):

        user = User(
            email=email,
            name=name,
            organization=organisation
        )
        user.set_password(password)
        user.save()
        return user

    def get_user(self, user_id):
        return User.query.filter_by(userid=user_id).first()

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def list_users(self):
        return User.query.all()

    def update_user(self, user_id, updated_data):
        user = self.get_user(user_id)
        if not user:
            return None
        if 'name' in updated_data:
            user.name = updated_data['name']
        if 'email' in updated_data:
            user.email = updated_data['email']
        if 'organization' in updated_data:
            user.organization = updated_data['organization']
        if 'password' in updated_data and updated_data['password']:
            user.set_password(updated_data['password'])
        user.save()
        return user

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        if not user:
            return False
        user.delete()
        return True

    def verify_password(self, user_id, raw_password):
        user = self.get_user(user_id)
        if not user:
            return False
        return user.check_password(raw_password)

    def verify_password_by_email(self, email, raw_password):
        user = self.get_user_by_email(email)
        if not user:
            return False
        return user.check_password(raw_password)

    # ==================== CONSENTS ====================
    def create_consent(self, user_id, consenttype, ipaddress, consent_text):
        consent = ConsentLog(
            userid=user_id,
            consenttype=consenttype,
            ipaddress=ipaddress,
            consent_text=consent_text
        )
        consent.save()
        return consent

    def get_consent(self, consent_id):
        return ConsentLog.query.get(consent_id)

    def list_consents(self, user_id):
        return ConsentLog.query.filter_by(userid=user_id).all()

    def verify_consent(self, user_id, consenttype):
        return ConsentLog.has_active_consent(user_id, consenttype)

    def revoke_consent(self, user_id, consenttype):
        consent = ConsentLog.query.filter_by(
            userid=user_id,
            consenttype=consenttype,
            is_active=True
        ).first()
        if not consent:
            return False
        consent.revoke()
        consent.save()
        return True

    # ==================== AUDITS ====================
    def create_audit(self, user_id, consent_id, target):
        
        audit = Audit(
            target=target,
            user_id=user_id,
            consent_id=consent_id
        )
        audit.save()
        return audit

    def get_audit(self, audit_id):
        return Audit.query.get(audit_id)

    def list_audits(self, user_id):
        return Audit.query.filter_by(user_id=user_id).all()

    def run_audit(self, audit_id):
        audit = self.get_audit(audit_id)
        if audit:
            audit.run_audit()
        return audit

    def get_audit_summary(self, audit_id):
        audit = self.get_audit(audit_id)
        if not audit:
            return None
        return {
            'summary_text': audit.get_summary(),
            'violations': audit.violations or [],
            'recommendations': audit.recommendations or []
        }


facade = Facade()
