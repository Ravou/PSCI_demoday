from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.audit import Audit
from app.persistence.database import engine

# ==========================
# Base Repository
# ==========================
class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id: str):
        pass

    @abstractmethod
    def get_all(self) -> List:
        pass

    @abstractmethod
    def update(self, obj_id: str, data: dict):
        pass

    @abstractmethod
    def delete(self, obj_id: str) -> bool:
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name: str, attr_value):
        pass

# ==========================
# SQLAlchemy Repository
# ==========================
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
            return obj

    def get(self, obj_id: str):
        with Session(engine) as session:
            return session.get(self.model, obj_id)

    def get_all(self) -> List:
        with Session(engine) as session:
            return session.query(self.model).all()

    def update(self, obj_id: str, data: dict):
        with Session(engine) as session:
            obj = session.get(self.model, obj_id)
            if not obj:
                return None
            for key, value in data.items():
                setattr(obj, key, value)
            session.commit()
            session.refresh(obj)
            return obj

    def delete(self, obj_id: str) -> bool:
        with Session(engine) as session:
            obj = session.get(self.model, obj_id)
            if not obj:
                return False
            session.delete(obj)
            session.commit()
            return True

    def get_by_attribute(self, attr_name: str, attr_value):
        if not hasattr(self.model, attr_name):
            raise ValueError(f"{attr_name} is not a valid attribute of {self.model.__name__}")
        with Session(engine) as session:
            attr = getattr(self.model, attr_name)
            return session.query(self.model).filter(attr == attr_value).first()

# ==========================
# User Repository
# ==========================
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def create(self, name: str, email: str, password: str, consent_ip: str, is_admin: bool = False) -> User:
        user = User(
            name=name,
            email=email,
            password=password,
            consent_ip=consent_ip,
            is_admin=is_admin
        )
        return self.add(user)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.get_by_attribute("email", email)

    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        user = self.get(user_id)
        if not user:
            return None

        # Hash password si présent
        if "password" in data:
            user.password_hash = user._hash_password(data.pop("password"))

        # Appliquer les autres champs
        for key, value in data.items():
            setattr(user, key, value)

        # Merge pour attacher l'objet à la session et commit
        with Session(engine) as session:
            user = session.merge(user)  # reconnecte l'objet détaché
            session.commit()
            session.refresh(user)

        return user

    def delete_user(self, user_id: str, archive_consent: bool = True) -> bool:
        user = self.get(user_id)
        if not user:
            return False
        if archive_consent:
            archived_data = user.archive_consent()
            # Ici tu peux sauvegarder archived_data si besoin
        with Session(engine) as session:
            session.delete(user)
            session.commit()
        return True

# ==========================
# Audit Repository
# ==========================
class AuditRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Audit)

    def create(self, user_id: str, site: str, content: dict, timestamp: Optional[datetime] = None) -> Audit:
        audit = Audit(
            user_id=user_id,
            site=site,
            content=content,
            timestamp=timestamp or datetime.utcnow()
        )
        return self.add(audit)

    def get_by_user_and_site(self, user_id: str, site: str) -> Optional[Audit]:
        with Session(engine) as session:
            return session.query(Audit).filter_by(user_id=user_id, site=site).first()

    def list_by_user(self, user_id: str) -> List[Audit]:
        with Session(engine) as session:
            return session.query(Audit).filter_by(user_id=user_id).all()