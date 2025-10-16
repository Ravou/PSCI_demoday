import uuid
from datetime import datetime
import bcrypt
from . import db

class User(db.Model):
    __tablename__ = 'user'
    userid = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)
    name = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def set_password(self, raw_password: str):
        self.password_hash = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())


    def check_password(self, raw_password: str) -> bool:
        try:
            return bcrypt.checkpw(raw_password.encode('utf-8'), self.password_hash)
        except Exception:
            return False


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
