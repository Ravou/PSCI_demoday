import os
import datetime
import jwt

# Utiliser une clé secrète depuis l'environnement en prod
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-change-me")
JWT_ALG = "HS256"
JWT_EXP_MIN = 60  # minutes

def create_access_token(sub: str, extra: dict = None, expires_minutes: int = JWT_EXP_MIN):
    payload = {
        "sub": sub,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_minutes),
        "iat": datetime.datetime.utcnow()
    }
    if extra:
        payload.update(extra)
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
    # PyJWT v2 renvoie str
    return token

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

