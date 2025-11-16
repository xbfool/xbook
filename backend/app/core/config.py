"""Application configuration"""

import json
from typing import List, Any
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
    BACKEND_CORS_ORIGINS: str = ""

    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from string"""
        if not self.BACKEND_CORS_ORIGINS:
            return []
        # Try to parse as JSON first
        if self.BACKEND_CORS_ORIGINS.startswith("["):
            try:
                return json.loads(self.BACKEND_CORS_ORIGINS)
            except json.JSONDecodeError:
                pass
        # Otherwise split by comma
        return [i.strip() for i in self.BACKEND_CORS_ORIGINS.split(",") if i.strip()]

    # Environment
    ENVIRONMENT: str = "development"

    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_EXTENSIONS: str = "pdf,epub,txt,mp3,wav,m4a"

    def get_allowed_extensions(self) -> List[str]:
        """Parse allowed extensions from string"""
        if not self.ALLOWED_EXTENSIONS:
            return []
        return [i.strip() for i in self.ALLOWED_EXTENSIONS.split(",") if i.strip()]

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
