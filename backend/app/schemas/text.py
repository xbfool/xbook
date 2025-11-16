"""Text/Book schemas"""

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class TextCreate(BaseModel):
    """Schema for creating a text"""

    title: str = Field(..., description="Text title")
    content: str = Field(..., description="Text content")
    language: str = Field(..., description="Language code (en/ja)")
    author: Optional[str] = Field(None, description="Author name")
    source_type: Optional[str] = Field(None, description="Source type (epub/pdf/web/manual)")
    source_url: Optional[str] = Field(None, description="Source URL if applicable")


class TextResponse(BaseModel):
    """Schema for text response"""

    id: UUID = Field(..., description="Text ID")
    user_id: UUID = Field(..., description="User ID")
    title: str = Field(..., description="Text title")
    language: str = Field(..., description="Language code")
    author: Optional[str] = Field(None, description="Author")
    source_type: Optional[str] = Field(None, description="Source type")
    word_count: Optional[int] = Field(None, description="Word count")
    created_at: datetime = Field(..., description="Creation timestamp")

    class Config:
        from_attributes = True


class TextDetail(TextResponse):
    """Schema for detailed text with content"""

    content: str = Field(..., description="Full text content")
    unique_words: Optional[int] = Field(None, description="Unique word count")
    readability_score: Optional[float] = Field(None, description="Readability score")
    difficulty_level: Optional[str] = Field(None, description="Difficulty level")
    has_audio: bool = Field(default=False, description="Has associated audio")

    class Config:
        from_attributes = True


class TextList(BaseModel):
    """Schema for list of texts"""

    items: list[TextResponse] = Field(..., description="List of texts")
    total: int = Field(..., description="Total count")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=20, description="Page size")


class UploadResponse(BaseModel):
    """Schema for file upload response"""

    text_id: UUID = Field(..., description="Created text ID")
    title: str = Field(..., description="Text title")
    word_count: int = Field(..., description="Word count")
    language: str = Field(..., description="Detected language")
    message: str = Field(..., description="Success message")
