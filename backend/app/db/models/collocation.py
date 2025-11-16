"""Collocation models"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, ARRAY, DECIMAL, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class Collocation(Base):
    """Collocation/Phrase database"""

    __tablename__ = "collocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phrase = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, index=True)

    # Components
    words = Column(ARRAY(Text), nullable=False)  # Individual words in the collocation
    syntactic_relation = Column(String(50))  # adj-noun, verb-adv, noun-verb, etc.

    # Metadata
    frequency_score = Column(DECIMAL(10, 6))  # How often this collocation appears
    significance_score = Column(DECIMAL(10, 6))  # Statistical significance
    example_sentences = Column(JSON, nullable=False, default=[])  # Example usage

    # Index
    __table_args__ = (
        Index("idx_collocation_phrase_lang", "phrase", "language", unique=True),
    )

    def __repr__(self):
        return f"<Collocation '{self.phrase}' ({self.language})>"


class UserCollocation(Base):
    """User's known collocations"""

    __tablename__ = "user_collocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    collocation_id = Column(UUID(as_uuid=True), ForeignKey("collocations.id", ondelete="CASCADE"), nullable=False)

    # Proficiency tracking
    proficiency_level = Column(Integer, nullable=False, default=0)  # 0-5
    times_encountered = Column(Integer, nullable=False, default=0)
    last_seen_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Index
    __table_args__ = (
        Index("idx_user_coll", "user_id", "collocation_id", unique=True),
    )

    def __repr__(self):
        return f"<UserCollocation level={self.proficiency_level}>"
