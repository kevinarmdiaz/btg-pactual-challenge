import os
from pathlib import Path
from pydantic import BaseModel, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIUrlsSettings(BaseModel):
    """API public urls settings."""
    
    docs: str = "/docs"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API service settings."""
    
    name: str = "CHANGEME"
    urls: APIUrlsSettings = APIUrlsSettings()


class LoggingSettings(BaseModel):
    """Configure the logging engine."""
    
    # The time field can be formatted using more human-friendly tokens.
    # These constitute a subset of the one used by the Pendulum library
    # https://pendulum.eustace.io/docs/#tokens
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}"
    
    # The .log filename
    file: str = "CHANGEME"
    
    # The .log file Rotation
    rotation: str = "10MB"
    
    # The type of compression
    compression: str = "zip"


class SettingsBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    ENVIRONMENT: str = "TESTING"
    
    # Application configuration
    root_dir: Path
    src_dir: Path
    debug: bool = True
    public_api: PublicApiSettings = PublicApiSettings()
    logging: LoggingSettings = LoggingSettings()
    
    SITE_DOMAIN: str = "invesmentfundsbtgapp.com"
    
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # ENVIRONMENT: Environment = Environment.PRODUCTION
    
    FUNDSAPP_UVICORN_HOST: str
    FUNDSAPP_UVICORN_PORT: int
    DB_NAME: str = "invesmentfundsdb"
    MONGODB_DB_HOST: str = 'localhost'
    MONGODB_DB_PORT: int = 27017
    
    # MongoDB
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "fundsappdb"
    
    SENTRY_DSN: str | None = None
    

    
    APP_VERSION: str = "1.0"


# Define the root path
# --------------------------------------
ROOT_PATH = Path(__file__).parent.parent.parent


# ======================================
# Load settings
# ======================================


class LocalSettings(SettingsBase):
    FUNDSAPP_UVICORN_HOST: str = "127.0.0.1"
    FUNDSAPP_UVICORN_PORT: int = 8000
    MONGODB_DB_HOST: str = 'localhost'
    MONGODB_DB_PORT: int = 27017
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017/invesmentfunds"
    


# Docker configuration
class DockerSettings(SettingsBase):
    FUNDSAPP_UVICORN_HOST: str = "0.0.0.0"
    FUNDSAPP_UVICORN_PORT: int = 8000
    MONGODB_DB_HOST: str = 'db'
    MONGODB_DB_PORT: int = 27017
    MONGODB_URI: MongoDsn = "mongodb://db:27017/invesmentfunds"


# Production configuration
class ProductionSettings(SettingsBase):
    FUNDSAPP_UVICORN_HOST: str = "0.0.0.0"
    FUNDSAPP_UVICORN_PORT: int = 8000
    MONGODB_DB_HOST: str = 'db'
    MONGODB_DB_PORT: int = 27017
    MONGODB_URI: MongoDsn = "mongodb://db:27017/invesmentfunds"
    DEBUG: bool = False


def get_settings() -> SettingsBase:
    environment = os.getenv("ENVIRONMENT", "local")
    
    if environment == "development":
        return DockerSettings(root_dir=ROOT_PATH, src_dir=ROOT_PATH / "src")
    elif environment == "production":
        return ProductionSettings(root_dir=ROOT_PATH, src_dir=ROOT_PATH / "src")
    else:
        return LocalSettings(root_dir=ROOT_PATH, src_dir=ROOT_PATH / "src")


settings = get_settings()

print(settings.model_dump())
