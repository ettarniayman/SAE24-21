import os
from datetime import timedelta

BASE_DIR = os.path.dirname(__file__)


def _resolve_db_url():
    """
    Résolution de l'URL de base de données dans l'ordre de priorité :
      1. DATABASE_URL (PostgreSQL/Supabase en prod)
      2. SQLITE_PATH  (fichier SQLite personnalisé)
      3. SQLite local par défaut (dev sans config)
    Supabase expose des URLs postgres:// — on les normalise en postgresql://.
    """
    url = os.environ.get("DATABASE_URL", "")
    if url:
        if url.startswith("postgres://"):
            url = "postgresql://" + url[len("postgres://"):]
        return url
    sqlite_path = os.environ.get("SQLITE_PATH", os.path.join(BASE_DIR, "rtvoyage.db"))
    return f"sqlite:///{sqlite_path}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production-2026")
    SQLALCHEMY_DATABASE_URI = _resolve_db_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Options de pool uniquement pour PostgreSQL
    _is_postgres = SQLALCHEMY_DATABASE_URI.startswith("postgresql")
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"pool_pre_ping": True, "pool_recycle": 300, "pool_size": 10, "max_overflow": 20}
        if _is_postgres else
        {"connect_args": {"check_same_thread": False}}
    )

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600

    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    UPLOAD_FOLDER = os.environ.get(
        "UPLOAD_FOLDER",
        os.path.join(BASE_DIR, "app", "static", "images", "uploads"),
    )
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "pdf"}
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_USERNAME", "noreply@rtvoyage.com")

    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

    ITEMS_PER_PAGE = 12
    BABEL_DEFAULT_LOCALE = "fr"
    BABEL_SUPPORTED_LOCALES = ["fr", "en"]


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    # SQLite par défaut si pas de DATABASE_URL
    SQLALCHEMY_DATABASE_URI = _resolve_db_url()


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    # Exiger DATABASE_URL en prod
    SQLALCHEMY_DATABASE_URI = _resolve_db_url()


class SQLiteConfig(DevelopmentConfig):
    """Config explicite SQLite — utile pour tests / CI / GitHub Actions."""
    _sqlite_path = os.path.join(BASE_DIR, "rtvoyage_test.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{_sqlite_path}"
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": {"check_same_thread": False}}
    WTF_CSRF_ENABLED = False


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "sqlite": SQLiteConfig,
    "default": DevelopmentConfig,
}
