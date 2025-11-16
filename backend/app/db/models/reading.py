"""Reading progress model"""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, DECIMAL, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class ReadingProgress(Base):
    """User reading progress for texts"""

    __tablename__ = "reading_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    text_id = Column(UUID(as_uuid=True), ForeignKey("texts.id", ondelete="CASCADE"), nullable=False)

    # Progress tracking
    current_position = Column(Integer, nullable=False, default=0)  # Character/word position
    completion_percentage = Column(DECIMAL(5, 2), nullable=False, default=0)  # 0.00-100.00

    # Stats
    words_looked_up = Column(Integer, nullable=False, default=0)
    reading_time_seconds = Column(Integer, nullable=False, default=0)
    sessions_count = Column(Integer, nullable=False, default=0)

    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_read_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True))

    # Index
    __table_args__ = (
        Index("idx_progress_user_text", "user_id", "text_id", unique=True),
    )

    def __repr__(self):
        return f"<ReadingProgress {self.completion_percentage}% for text={self.text_id}>"
