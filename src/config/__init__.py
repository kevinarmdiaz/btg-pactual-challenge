from msilib.schema import Environment
from pathlib import Path
from pydantic import BaseModel, MongoDsn, computed_field
from pydantic_core._pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class APIUrlsSettings(BaseModel):
    """API public urls settings."""

    docs: str = "/docs"
    redoc: str = "/redoc"


class PublicApiSettings(BaseModel):
    """Configure public API service settings."""

    name: str = "CHANGEME"
    urls: APIUrlsSettings = APIUrlsSettings()


class DatabaseSettings(BaseModel):
    name: str = "db.sqlite3"

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.name}"


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


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )
    
    ENVIRONMENT: str = "TESTING"
    
    
    # Infrastructure settings
    database: DatabaseSettings = DatabaseSettings()

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
    DB_NAME: str = 'invesmentfundsdb'

    # MongoDB
    MONGODB_URI: MongoDsn = "mongodb://localhost:27017/"
    MONGODB_DB_NAME: str = "fundsappdb"

    SENTRY_DSN: str | None = None

    CORS_ORIGINS: list[str] | None = None
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] | None = None

    APP_VERSION: str = "1.0"



# Define the root path
# --------------------------------------
ROOT_PATH = Path(__file__).parent.parent.parent

# ======================================
# Load settings
# ======================================
settings = Settings(
    # NOTE: We would like to hard-code the root and applications directories
    #       to avoid overriding via environment variables
    root_dir=ROOT_PATH,
    src_dir=ROOT_PATH / "src",
)

print(settings.model_dump())

