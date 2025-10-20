import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        """Sauvegarder l'objet dans la base (placeholder)"""
        self.updated_at = datetime.utcnow()
        # Implémenter la logique de persistance ici
        pass

    def to_dict(self):
        """Retourner un dict représentant l'objet"""
        return self.__dict__

    def delete(self):
        """Supprimer l'objet de la base (placeholder)"""
        # Implémenter la suppression ici
        pass
