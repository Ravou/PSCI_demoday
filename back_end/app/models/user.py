from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from app.models.audit import Audit
from app.models.base_model import BaseModel
import bcrypt


class User(BaseModel):
    """Represents a user with mandatory consent and integrated GDPR-friendly archival system."""

    # In-memory storage for active users and archived consents
    _users: List['User'] = []
    _archived_consents: List[dict] = []

    allowed_update_fields = ['name', 'email', 'password']

    def __init__(self, name: str, email: str, password: str, consent_ip: str):
        super().__init__()
        self.name = name
        self.email = email
        self._password_hash = self._hash_password(password)
        self.account_created_at = datetime.utcnow()

        # Consent (mandatory to create an account)
        self.consent_given = True
        self.consent_date = datetime.utcnow()
        self.consent_ip = consent_ip
        self.consent_summary = (
            "Consent granted for site scraping and temporary data processing."
        )

        # Relationships (to be linked later)
        self.audits: List['Audit'] = []
        self.scraped_data: List['dict'] = []

        User._users.append(self)

    # -----------------------
    # Password management
    # -----------------------
    def _hash_password(self, password: str) -> str:
        """Hashes the password before storing it."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str) -> bool:
        """Checks if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self._password_hash.encode('utf-8'))

    # -----------------------
    # Consent archival and account deletion
    # -----------------------
    def _archive_consent(self):
        """Archives minimal consent data for legal traceability (GDPR)."""
        record = {
            "email": self.email,
            "consent_date": self.consent_date,
            "consent_ip": self.consent_ip,
            "archived_at": datetime.utcnow(),
        }
        User._archived_consents.append(record)
        print(f"Consent archived for {self.email} at {record['archived_at']}")

    def delete_account(self, archive_consent: bool = True):
        """Deletes the user's account and all associated data, optionally archiving consent."""
        if archive_consent:
            self._archive_consent()

        # Delete linked audits and raw data
        for audit in getattr(self, 'audits', []):
            audit.delete()
        for data in getattr(self, 'scraped_data', []):
            data.delete()

        # Remove the user from active records
        User._users = [u for u in User._users if u.id != self.id]
        print(f"Account deleted and consent revoked for {self.email}.")

    # -----------------------
    # Class methods
    # -----------------------
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Finds a user by email."""
        return next((user for user in cls._users if user.email == email), None)

    @classmethod
    def get_by_id(cls, id: str) -> Optional['User']:
        """Finds a user by ID."""
        return next((user for user in cls._users if user.id == id), None)

    @classmethod
    def list_all(cls) -> List['User']:
        """Returns all active users."""
        return cls._users

    @classmethod
    def list_archived_consents(cls) -> List[dict]:
        """Returns all archived consents."""
        return cls._archived_consents

    # -----------------------
    # Representation
    # -----------------------
    def __repr__(self):
        return (
            f"User(id='{self.id}', email='{self.email}', "
            f"consent_given={self.consent_given}, created='{self.account_created_at}')"
        )

