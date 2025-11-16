"""User statistics model"""

from datetime import datetime, date
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class UserStats(Base):
    """User learning statistics and achievements"""

    __tablename__ = "user_stats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    # Vocabulary stats
    total_words = Column(Integer, nullable=False, default=0)
    words_learning = Column(Integer, nullable=False, default=0)
    words_known = Column(Integer, nullable=False, default=0)
    words_mastered = Column(Integer, nullable=False, default=0)

    # Reading stats
    total_texts_read = Column(Integer, nullable=False, default=0)
    total_reading_time_minutes = Column(Integer, nullable=False, default=0)
    total_words_read = Column(Integer, nullable=False, default=0)

    # Review stats
    total_reviews = Column(Integer, nullable=False, default=0)
    current_streak_days = Column(Integer, nullable=False, default=0)
    longest_streak_days = Column(Integer, nullable=False, default=0)
    last_review_date = Column(Date)

    # Updated timestamp
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<UserStats total_words={self.total_words} streak={self.current_streak_days}>"
