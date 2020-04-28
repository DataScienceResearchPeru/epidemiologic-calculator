import os
from abc import ABC

from dotenv import find_dotenv, load_dotenv


class SettingsInterface(ABC):
    pass


class Settings(SettingsInterface):
    load_dotenv(find_dotenv())

    MODE_DEBUGGER = os.environ.get("MODE_DEBUGGER", True)
    SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")
    PORT = os.environ.get("PORT", "8080")
    HOST = os.environ.get("HOST", "0.0.0.0")
    HOST_URL = os.environ.get("HOST_URL", f"http://{HOST}:{PORT}/")

    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///epidemiologic.db")

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = os.environ.get("MAIL_PORT", 465)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    AWS_REGION = os.environ.get("AWS_REGION", "")
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY", "")
    AWS_ACCESS_SECRET = os.environ.get("AWS_ACCESS_SECRET", "")
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET", "")
