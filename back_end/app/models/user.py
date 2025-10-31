from __future__ import annotations
from datetime import datetime
from typing import List, Dict
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base_model import BaseModel
import bcrypt
import uuid

# -----------------------------
# Définition de User
# -----------------------------
class User(BaseModel):
    __tablename__ = "users"

    # UUID natif PostgreSQL pour l'ID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    consent_ip: Mapped[str] = mapped_column(String(50), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    consent_given: Mapped[bool] = mapped_column(Boolean, default=True)
    consent_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    consent_summary: Mapped[str] = mapped_column(String(255))
    account_created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # -----------------------------
    # Relation avec Audit
    # -----------------------------
    audits: Mapped[List["Audit"]] = relationship(
        "Audit", back_populates="user", cascade="all, delete-orphan"
    )

    # -----------------------------
    # Initialisation
    # -----------------------------
    def __init__(self, name: str, email: str, password: str, consent_ip: str, is_admin: bool = False):
        super().__init__()
        self.name = name
        self.email = email
        self.password_hash = self._hash_password(password)
        self.consent_ip = consent_ip
        self.is_admin = is_admin
        self.account_created_at = datetime.utcnow()
        self.consent_date = datetime.utcnow()
        self.consent_summary = "Consent granted for site scraping and temporary data processing."

    # -----------------------------
    # Mot de passe
    # -----------------------------
    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash.encode("utf-8"))

    # -----------------------------
    # Consentement
    # -----------------------------
    def archive_consent(self) -> dict:
        return {
            "email": self.email,
            "consent_date": self.consent_date.isoformat(),
            "consent_ip": self.consent_ip,
            "archived_at": datetime.utcnow().isoformat(),
        }

    # -----------------------------
    # Sérialisation
    # -----------------------------
    def to_dict(self) -> Dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
            "account_created_at": self.account_created_at.isoformat(),
            "consent_given": self.consent_given,
            "consent_date": self.consent_date.isoformat(),
            "consent_ip": self.consent_ip,
            "consent_summary": self.consent_summary,
        }

    # -----------------------------
    # Représentation
    # -----------------------------
    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', admin={self.is_admin}, created='{self.account_created_at.isoformat()}')>"

# -----------------------------
# Import Audit après définition de User
# -----------------------------
from app.models.audit import Audit
