"""Database models"""

from app.core.database import Base

# Import all models here so Alembic can detect them
from .user import User
from .vocabulary import Vocabulary, VocabCard, ReviewLog
from .text import TextModel, AudioFile, AudioAlignment
from .reading import ReadingProgress
from .stats import UserStats
from .collocation import Collocation, UserCollocation

__all__ = [
    "Base",
    "User",
    "Vocabulary",
    "VocabCard",
    "ReviewLog",
    "TextModel",
    "AudioFile",
    "AudioAlignment",
    "ReadingProgress",
    "UserStats",
    "Collocation",
    "UserCollocation",
]
