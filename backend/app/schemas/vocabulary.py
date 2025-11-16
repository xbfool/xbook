"""Vocabulary schemas"""

from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class VocabularyCreate(BaseModel):
    """Schema for creating vocabulary"""

    surface_form: str = Field(..., description="Surface form (original text)")
    dictionary_form: str = Field(..., description="Dictionary/base form")
    language: str = Field(..., description="Language code (en/ja)")
    reading: Optional[str] = Field(None, description="Reading (furigana for Japanese)")
    part_of_speech: Optional[str] = Field(None, description="Part of speech")
    translations: List[dict] = Field(default_factory=list, description="Translations")
    definitions: List[dict] = Field(default_factory=list, description="Definitions")
    context_sentence: Optional[str] = Field(None, description="Context sentence")
    context_source_id: Optional[UUID] = Field(None, description="Source text ID")


class VocabularyUpdate(BaseModel):
    """Schema for updating vocabulary"""

    translations: Optional[List[dict]] = None
    definitions: Optional[List[dict]] = None
    context_sentence: Optional[str] = None
    difficulty_level: Optional[str] = None


class VocabularyResponse(BaseModel):
    """Schema for vocabulary response"""

    id: UUID
    user_id: UUID
    surface_form: str
    dictionary_form: str
    language: str
    reading: Optional[str] = None
    part_of_speech: Optional[str] = None
    translations: List[dict] = Field(default_factory=list)
    difficulty_level: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class VocabularyDetail(VocabularyResponse):
    """Schema for detailed vocabulary"""

    definitions: List[dict] = Field(default_factory=list)
    context_sentence: Optional[str] = None
    context_source_id: Optional[UUID] = None
    last_reviewed_at: Optional[datetime] = None

    # Include card info if exists
    card_status: Optional[str] = None
    proficiency_level: Optional[int] = None

    class Config:
        from_attributes = True


class VocabularyList(BaseModel):
    """Schema for vocabulary list"""

    items: List[VocabularyResponse]
    total: int
    page: int = 1
    page_size: int = 20


class VocabularyStats(BaseModel):
    """Schema for vocabulary statistics"""

    total: int = Field(..., description="Total vocabulary count")
    by_language: dict = Field(..., description="Count by language")
    by_level: dict = Field(default_factory=dict, description="Count by proficiency level")
    recent_additions: int = Field(..., description="Added in last 7 days")
