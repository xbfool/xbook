"""Text and audio models"""

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Boolean, DECIMAL, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.sql import func
import uuid

from app.core.database import Base


class TextModel(Base):
    """Text/Book model"""

    __tablename__ = "texts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Content
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, index=True)

    # Metadata
    source_type = Column(String(20))  # epub, pdf, web, manual
    source_url = Column(Text)
    author = Column(Text)

    # Processing
    word_count = Column(Integer)
    unique_words = Column(Integer)
    readability_score = Column(DECIMAL(5, 2))  # Flesch-Kincaid or similar
    difficulty_level = Column(String(10))  # JLPT/CEFR level estimate

    # Audio
    audio_url = Column(Text)  # Path to audio file
    has_alignment = Column(Boolean, nullable=False, default=False)
    alignment_data = Column(JSON)  # Word-level timestamps

    # Stats
    times_read = Column(Integer, nullable=False, default=0)
    reading_time_minutes = Column(Integer, nullable=False, default=0)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_read_at = Column(DateTime(timezone=True))

    # Full-text search (PostgreSQL tsvector)
    content_tsv = Column(TSVECTOR)

    # Indexes
    __table_args__ = (
        Index("idx_texts_user_lang", "user_id", "language"),
        Index("idx_texts_fts", "content_tsv", postgresql_using="gin"),
    )

    def __repr__(self):
        return f"<Text {self.title} ({self.language})>"


class AudioFile(Base):
    """Audio file model"""

    __tablename__ = "audio_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    text_id = Column(UUID(as_uuid=True), ForeignKey("texts.id", ondelete="CASCADE"))

    # File info
    filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    file_size = Column(Integer)  # Bytes
    duration_seconds = Column(Integer)  # Audio duration
    format = Column(String(10))  # mp3, wav, m4a

    # Processing status
    is_processed = Column(Boolean, nullable=False, default=False)
    has_alignment = Column(Boolean, nullable=False, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<AudioFile {self.filename}>"


class AudioAlignment(Base):
    """Audio-text alignment data (word-level timestamps)"""

    __tablename__ = "audio_alignments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audio_file_id = Column(UUID(as_uuid=True), ForeignKey("audio_files.id", ondelete="CASCADE"), nullable=False)
    text_id = Column(UUID(as_uuid=True), ForeignKey("texts.id", ondelete="CASCADE"), nullable=False)

    # Alignment data
    # Format: [{"word": "hello", "start": 0.5, "end": 1.2}, ...]
    alignments = Column(JSON, nullable=False, default=[])

    # Processing info
    alignment_method = Column(String(50))  # aeneas, whisper, etc.
    confidence_score = Column(DECIMAL(3, 2))  # 0.00-1.00

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Index
    __table_args__ = (
        Index("idx_alignment_audio", "audio_file_id", unique=True),
    )

    def __repr__(self):
        return f"<AudioAlignment for audio={self.audio_file_id}>"
