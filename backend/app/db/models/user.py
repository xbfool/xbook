"""User model"""

from datetime import datetime
from sqlalchemy import Column, String, DateTime, ARRAY, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Language preferences
    native_language = Column(String(10), nullable=False, default="zh")  # Chinese
    target_languages = Column(ARRAY(String), nullable=False, default=["en", "ja"])

    # Settings
    settings = Column(JSON, nullable=False, default={})

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User {self.username}>"
