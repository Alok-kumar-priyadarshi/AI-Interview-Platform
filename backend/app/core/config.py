"""Application configuration.

All runtime configuration is loaded once, at startup, from environment
variables (and, for local development, ``.env.local`` / ``.env``). No other
module in the codebase should read ``os.environ`` directly — everything flows
through the :data:`settings` singleton exposed here.

See ``docs/08-deployment/environment-variables.md`` for the authoritative list
of variables and ``docs/03-architecture/backend-architecture.md`` (Configuration
section) for the design rationale.
"""

from __future__ import annotations

from functools import cached_property
from typing import Literal

from pydantic import Field, PostgresDsn, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["local", "ci", "staging", "production"]


class Settings(BaseSettings):
    """Strongly-typed, validated application settings.

    Instantiating this class validates the entire configuration. Missing
    required secrets (database URL, JWT secret, OAuth credentials, Groq key)
    raise a ``ValidationError`` at startup — the application fails fast rather
    than running in a partially-configured state.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- Application --------------------------------------------------------
    APP_NAME: str = "AI Career Interview Platform"
    APP_VERSION: str = "1.0.0"
    APP_ENV: Environment = "local"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    API_V1_PREFIX: str = "/api/v1"

    # --- Database -----------------------------------------------------------
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_ECHO: bool = False

    # --- Authentication: Google OAuth --------------------------------------
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    # --- Authentication: JWT -----------------------------------------------
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    # Access tokens are short-lived per docs/05-api-design/authentication.md (15 min).
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # --- AI: Groq -----------------------------------------------------------
    GROQ_API_KEY: str
    GROQ_MODEL: str = "openai/gpt-oss-120b"
    GROQ_TRANSCRIPTION_MODEL: str = "whisper-large-v3"
    # gpt-oss models are reasoning models: this controls how many reasoning
    # tokens they spend (low = fastest/cheapest, high = most thorough). It is
    # forwarded to Groq via ``extra_body`` and ignored by non-reasoning models.
    GROQ_REASONING_EFFORT: Literal["low", "medium", "high"] = "medium"
    GROQ_TIMEOUT: int = 60
    GROQ_MAX_RETRIES: int = 3

    # --- Object storage -----------------------------------------------------
    # STORAGE_PROVIDER selects the file-storage backend. "local" keeps files on
    # the application filesystem (Version 1 default); "s3" targets any
    # S3-compatible service, including Cloudflare R2.
    STORAGE_PROVIDER: Literal["local", "s3"] = "local"
    STORAGE_LOCAL_DIR: str = "storage"
    STORAGE_BUCKET: str | None = None
    STORAGE_ENDPOINT: str | None = None
    STORAGE_REGION: str | None = None
    STORAGE_ACCESS_KEY: str | None = None
    STORAGE_SECRET_KEY: str | None = None
    MAX_UPLOAD_SIZE_BYTES: int = 10 * 1024 * 1024  # 10 MB (resume API limit)

    # --- Security -----------------------------------------------------------
    CORS_ALLOWED_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    ALLOWED_HOSTS: list[str] = Field(default_factory=lambda: ["*"])
    RATE_LIMIT_PER_MINUTE: int = 100
    COOKIE_SECURE: bool = True
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"
    # Frontend URL the OAuth callback redirects back to after issuing tokens.
    FRONTEND_URL: str = "http://localhost:5173"

    # --- Logging ------------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "json"
    ENABLE_REQUEST_LOGGING: bool = True

    # --- Feature flags ------------------------------------------------------
    ENABLE_AI_FEEDBACK: bool = True
    ENABLE_HEALTH_CHECKS: bool = True

    # ------------------------------------------------------------------ #
    # Validators / derived values                                        #
    # ------------------------------------------------------------------ #
    @field_validator("CORS_ALLOWED_ORIGINS", "ALLOWED_HOSTS", mode="before")
    @classmethod
    def _split_comma_separated(cls, value: object) -> object:
        """Accept comma-separated strings for list fields.

        Deployment platforms typically inject list-style config as a single
        string (e.g. ``CORS_ALLOWED_ORIGINS=https://a.com,https://b.com``).
        """
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def _reject_weak_jwt_secret(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("JWT_SECRET_KEY must be at least 32 characters long.")
        return value

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def async_database_url(self) -> str:
        """Database URL guaranteed to use the asyncpg driver.

        A plain ``postgresql://`` URL (as provided by most managed Postgres
        hosts) is normalised to ``postgresql+asyncpg://`` so the async engine
        can consume it directly.
        """
        url = str(self.DATABASE_URL)
        if url.startswith("postgresql+asyncpg://"):
            return url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+asyncpg://", 1)
        return url

    @cached_property
    def sync_database_url(self) -> str:
        """Synchronous URL for tooling that cannot use asyncpg (e.g. some
        Alembic autogenerate paths). Uses the psycopg driver family."""
        return self.async_database_url.replace("+asyncpg", "+psycopg", 1)


def get_settings() -> Settings:
    """Return the process-wide settings singleton.

    Instantiation is deferred to first call so that test suites can populate
    the environment before configuration is validated.
    """
    global _settings
    if _settings is None:
        _settings = Settings()  # type: ignore[call-arg]
    return _settings


_settings: Settings | None = None
