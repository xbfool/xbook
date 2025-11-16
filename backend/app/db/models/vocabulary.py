"""Vocabulary models"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Boolean, DECIMAL, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Vocabulary(Base):
    """Vocabulary item (word/phrase/collocation)"""

    __tablename__ = "vocabulary"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Word data
    surface_form = Column(Text, nullable=False)  # Original form (e.g., "running", "走っている")
    dictionary_form = Column(Text, nullable=False)  # Base form (e.g., "run", "走る")
    reading = Column(Text)  # Furigana for Japanese (e.g., "はしる")
    language = Column(String(10), nullable=False, index=True)  # "en" or "ja"

    # Translations
    translations = Column(JSON, nullable=False, default=[])  # [{"lang": "zh", "text": "跑"}]
    definitions = Column(JSON, nullable=False, default=[])  # Multiple definitions

    # Context
    context_sentence = Column(Text)  # Original sentence where word was found
    context_source_id = Column(UUID(as_uuid=True), ForeignKey("texts.id", ondelete="SET NULL"))
    context_position = Column(Integer)  # Word position in source text

    # Classification
    part_of_speech = Column(String(50))  # "noun", "verb", "adjective", etc.
    word_type = Column(String(20), nullable=False, default="word")  # "word" or "phrase"
    difficulty_level = Column(String(10))  # JLPT: "N5-N1", CEFR: "A1-C2"
    frequency_rank = Column(Integer)  # Word frequency ranking

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_reviewed_at = Column(DateTime(timezone=True))
    first_seen_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Indexes
    __table_args__ = (
        Index("idx_vocab_user_dict", "user_id", "dictionary_form", "language", unique=True),
        Index("idx_vocab_lang_level", "language", "difficulty_level"),
    )

    def __repr__(self):
        return f"<Vocabulary {self.dictionary_form} ({self.language})>"


class VocabCard(Base):
    """Spaced repetition card for vocabulary"""

    __tablename__ = "vocab_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vocab_id = Column(UUID(as_uuid=True), ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # SRS Algorithm data (SM-2)
    easiness_factor = Column(DECIMAL(3, 2), nullable=False, default=Decimal("2.50"))  # EF: 1.3-2.5
    interval = Column(Integer, nullable=False, default=0)  # Days until next review
    repetitions = Column(Integer, nullable=False, default=0)  # Number of successful reviews

    # Card state
    status = Column(String(20), nullable=False, default="new")  # new, learning, review, mature
    due_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Review history tracking
    total_reviews = Column(Integer, nullable=False, default=0)
    correct_reviews = Column(Integer, nullable=False, default=0)
    last_review_grade = Column(Integer)  # 0-5 (SM-2 scale)

    # Lapse tracking
    lapses = Column(Integer, nullable=False, default=0)  # Times failed after learned
    leech_threshold = Column(Integer, nullable=False, default=8)  # Flag problematic cards
    is_suspended = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    graduated_at = Column(DateTime(timezone=True))  # When moved to 'review' status

    # Indexes
    __table_args__ = (
        Index("idx_cards_vocab_user", "vocab_id", "user_id", unique=True),
        Index("idx_cards_due", "user_id", "due_date"),
        Index("idx_cards_status", "user_id", "status"),
    )

    def __repr__(self):
        return f"<VocabCard {self.status} EF={self.easiness_factor}>"


class ReviewLog(Base):
    """Review history log"""

    __tablename__ = "review_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id = Column(UUID(as_uuid=True), ForeignKey("vocab_cards.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Review data
    review_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    grade = Column(Integer, nullable=False)  # 0-5 (SM-2)
    time_spent_ms = Column(Integer)  # Review duration in milliseconds

    # State before review
    interval_before = Column(Integer)
    easiness_before = Column(DECIMAL(3, 2))

    # State after review
    interval_after = Column(Integer)
    easiness_after = Column(DECIMAL(3, 2))

    # Context
    review_type = Column(String(20), nullable=False, default="scheduled")  # scheduled, extra, cram
    device_type = Column(String(20))  # web, mobile

    # Index
    __table_args__ = (
        Index("idx_review_logs_user_date", "user_id", "review_date"),
    )

    def __repr__(self):
        return f"<ReviewLog grade={self.grade} at {self.review_date}>"
