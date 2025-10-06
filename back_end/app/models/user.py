from __future__ import annotations
from typing import Optional
from datetime import datetime
import uuid

from app.models.base_model import BaseModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    """
    SQLAlchemy model representing a user with GDPR-friendly relations and utilities.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    organization = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    # Relations with cascade delete for GDPR-compliant removals
    audits = db.relationship('Audit', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    consents = db.relationship('ConsentLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, email: str, password: str, name: Optional[str] = None, organization: Optional[str] = None):
        """Initialize a new user with a hashed password."""
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.organization = organization

    def check_password(self, password: str) -> bool:
        """Verify the provided password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def set_password(self, password: str):
        """Update the user's password (hashed)."""
        self.password_hash = generate_password_hash(password)

    def to_dict(self) -> dict:
        """Return a dict representation without sensitive password data."""
        return {
            "userid": self.userid,
            "name": self.name,
            "email": self.email,
            "id": str(self.id),
            "organization": self.organization,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active
        }

    def __repr__(self):
        return f'<User {self.email}>'
