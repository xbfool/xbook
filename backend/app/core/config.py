"""Application configuration"""

from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "XBook"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Smart Language Learning Platform"

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    # Environment
    ENVIRONMENT: str = "development"

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "epub", "txt", "mp3", "wav", "m4a"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Translation APIs (optional)
    DEEPL_API_KEY: str = ""
    GOOGLE_TRANSLATE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Create settings instance
settings = Settings()
