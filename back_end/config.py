import os


class Config:
    """Config de base (commune à tous les environnements)"""
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    DEBUG = False

    # Base de données (SQLite par défaut)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://username:password@localhost:5432/ma_base"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Config spécifique au développement"""
    DEBUG = True


class ProductionConfig(Config):
    """Config spécifique à la production"""
    DEBUG = False
    # En prod, on attend que DATABASE_URL soit défini
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# Dictionnaire pour sélectionner facilement une config
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}


