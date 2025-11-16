"""Tokenizer request/response schemas"""

from typing import List, Optional
from pydantic import BaseModel, Field


class TokenizeRequest(BaseModel):
    """Request schema for tokenization"""

    text: str = Field(..., description="Text to tokenize", min_length=1)


class Token(BaseModel):
    """Token information"""

    surface: str = Field(..., description="Surface form (original text)")
    dictionary_form: str = Field(..., description="Dictionary/base form")
    part_of_speech: str = Field(..., description="Part of speech")
    reading: Optional[str] = Field(None, description="Reading (furigana for Japanese)")
    tag: Optional[str] = Field(None, description="Detailed POS tag (English)")
    is_stop: Optional[bool] = Field(None, description="Is stop word (English)")


class TokenizeResponse(BaseModel):
    """Response schema for tokenization"""

    language: str = Field(..., description="Language code (en/ja)")
    tokens: List[Token] = Field(..., description="List of tokens")
    word_count: int = Field(..., description="Total number of tokens")


class Entity(BaseModel):
    """Named entity information"""

    text: str = Field(..., description="Entity text")
    label: str = Field(..., description="Entity type (PERSON, ORG, GPE, etc.)")
    start: int = Field(..., description="Start character position")
    end: int = Field(..., description="End character position")


class TokenizeWithEntitiesResponse(BaseModel):
    """Response with tokens and named entities"""

    language: str = Field(..., description="Language code")
    tokens: List[Token] = Field(..., description="List of tokens")
    entities: List[Entity] = Field(..., description="Named entities")
    word_count: int = Field(..., description="Total number of tokens")
