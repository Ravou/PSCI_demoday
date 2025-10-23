import json
from datetime import datetime
from typing import List, Dict, Optional
from app.models.base_model import BaseModel


class Audit(BaseModel):

    STORAGE_FILE = "audits.json"

    def __init__(
        self,
        user_id: str,
        site: str,
        content: dict,
        timestamp: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.site = site
        self.content = content
        self.timestamp = timestamp or datetime.now() 

    # ---------------------------
    # Conversion & sérialisation
    # ---------------------------
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

    # ---------------------------
    # Chargement / Sauvegarde
    # ---------------------------
    @classmethod
    def load_all(cls) -> List[dict]:
        """Charge tous les audits depuis le fichier JSON."""
        try:
            with open(cls.STORAGE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @classmethod
    def save_all(cls, audits: List[dict]):
        """Sauvegarde la liste complète des audits dans le fichier."""
        with open(cls.STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(audits, f, ensure_ascii=False, indent=4)

    # ---------------------------
    # Sauvegarde individuelle
    # ---------------------------
    def save(self):
        """
        Ajoute ou met à jour un audit existant pour ce user et ce site.
        Si un audit existe déjà → il est remplacé.
        Sinon → il est ajouté à la liste.
        """
        audits = self.load_all()
        updated = False

        for i, audit in enumerate(audits):
            if audit["user_id"] == self.user_id and audit["site"] == self.site:
                audits[i] = self.to_dict()
                updated = True
                break

        if not updated:
            audits.append(self.to_dict())

        self.save_all(audits)

    # ---------------------------
    # Méthodes de récupération
    # ---------------------------
    @classmethod
    def get_by_user(cls, user_id: str) -> List[dict]:
        """Récupère tous les audits d'un utilisateur donné."""
        audits = cls.load_all()
        return [a for a in audits if a.get("user_id") == user_id]

    @classmethod
    def get_by_user_and_site(cls, user_id: str, site: str) -> Optional[dict]:
        """Récupère un audit spécifique pour un utilisateur et un site."""
        audits = cls.load_all()
        for audit in audits:
            if audit.get("user_id") == user_id and audit.get("site") == site:
                return audit
        return None

    @classmethod
    def delete_audit(cls, user_id: str, site: str) -> bool:
        """Supprime un audit donné pour un utilisateur et un site."""
        audits = cls.load_all()
        new_audits = [
            a for a in audits if not (a["user_id"] == user_id and a["site"] == site)
        ]

        if len(new_audits) == len(audits):
            return False  # Aucun audit supprimé
        cls.save_all(new_audits)
        return True

    # ---------------------------
    # Historique / logs
    # ---------------------------
    @classmethod
    def list_sites_for_user(cls, user_id: str) -> List[str]:
        """Retourne la liste des sites audités par un utilisateur."""
        audits = cls.get_by_user(user_id)
        return list({a["site"] for a in audits})

    @classmethod
    def get_last_audit(cls, user_id: str, site: str) -> Optional[dict]:
        """Retourne le dernier audit sauvegardé pour ce site."""
        audit = cls.get_by_user_and_site(user_id, site)
        return audit or None
