from typing import List, Dict, Optional
from app.models.base_model import BaseModel
from datetime import datetime


class Audit(BaseModel):
    def __init__(
        self,
        user_id: str,
        site: str,
        content: dict,
        timestamp: Optional[datetime] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.site = site
        self.content = content
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update(
            {
                "user_id": self.user_id,
                "site": self.site,
                "content": self.content,
                "timestamp": self.timestamp.isoformat(),
            }
        )
        return base

    # Méthodes modifiées pour recevoir et retourner des dicts/lists en mémoire
    
    @staticmethod
    def load_all_from_memory(audits_data: List[dict]) -> List["Audit"]:
        """Transforme une liste de dicts en objets Audit (mémoire uniquement)."""
        audits = []
        for a in audits_data:
            audits.append(
                Audit(
                    user_id=a["user_id"],
                    site=a["site"],
                    content=a["content"],
                    timestamp=datetime.fromisoformat(a["timestamp"]),
                )
            )
        return audits

    @staticmethod
    def save_all_to_memory(audits: List["Audit"]) -> List[dict]:
        """Transforme une liste d’Audit en liste de dicts (mémoire uniquement)."""
        return [audit.to_dict() for audit in audits]

    def save_in_memory(self, audits: List["Audit"]) -> List["Audit"]:
        """
        Ajoute ou met à jour self dans la liste d’audits en mémoire.
        Retourne la liste mise à jour.
        """
        updated = False
        for i, audit in enumerate(audits):
            if audit.user_id == self.user_id and audit.site == self.site:
                audits[i] = self
                updated = True
                break
        if not updated:
            audits.append(self)
        return audits

    @staticmethod
    def delete_from_memory(audits: List["Audit"], user_id: str, site: str) -> List["Audit"]:
        """Supprime l’audit pour user+site dans la liste en mémoire."""
        return [a for a in audits if not (a.user_id == user_id and a.site == site)]

    @staticmethod
    def get_by_user_in_memory(audits: List["Audit"], user_id: str) -> List["Audit"]:
        return [a for a in audits if a.user_id == user_id]

    @staticmethod
    def get_by_user_and_site_in_memory(audits: List["Audit"], user_id: str, site: str) -> Optional["Audit"]:
        for a in audits:
            if a.user_id == user_id and a.site == site:
                return a
        return None

    @staticmethod
    def list_sites_for_user_in_memory(audits: List["Audit"], user_id: str) -> List[str]:
        return list({a.site for a in audits if a.user_id == user_id})

    @staticmethod
    def get_last_audit_in_memory(audits: List["Audit"], user_id: str, site: str) -> Optional["Audit"]:
        return Audit.get_by_user_and_site_in_memory(audits, user_id, site)
