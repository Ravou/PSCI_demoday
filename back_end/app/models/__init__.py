from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to expose them at package level
from .user import User
from .consent_log import ConsentLog
from .audit import Audit


