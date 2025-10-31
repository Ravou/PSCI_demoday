import uuid
from datetime import datetime
from app.persistence.database import Base

class BaseModel(Base):
    __abstract__ = True

    def __init__(self, id=None, created_at=None, updated_at=None):
        self.id = id or str(uuid.uuid4())
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def to_dict(self, seen=None):
        if seen is None:
            seen = set()

        if id(self) in seen:
            return f"<Recursion detected for object {self.id}>"
        seen.add(id(self))

        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, BaseModel):
                result[key] = value.to_dict(seen)
            elif isinstance(value, list):
                result[key] = [item.to_dict(seen) if isinstance(item, BaseModel) else item for item in value]
            elif isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data):
        created_at = datetime.fromisoformat(data["created_at"]) if "created_at" in data else None
        updated_at = datetime.fromisoformat(data["updated_at"]) if "updated_at" in data else None

        obj = cls(
                id=data.get("id"),
                created_at=created_at,
                updated_at=updated_at
        )
        return obj

    def update(self, data):
        updated = False
        for key, value in data.items():
            if key in self.allowed_update_fields and hasattr(self, key):
                setattr(self, key, value)
                updated = True
        if updated:
            self.save()


    def __repr__(self):
        return f"BaseModel(id='{self.id}', created_at='{self.created_at.isoformat()}', updated_at='{self.updated_at.isoformat()}')"

    def __str__(self):
        return self.__repr__()