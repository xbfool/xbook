"""Translation API endpoints"""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.translator import TranslationService

router = APIRouter()


class TranslateRequest(BaseModel):
    """Translation request schema"""

    text: str = Field(..., description="Text to translate", min_length=1)
    source_lang: str = Field(..., description="Source language (en/ja)")
    target_lang: str = Field(..., description="Target language (zh/en/ja)")


class TranslateResponse(BaseModel):
    """Translation response schema"""

    original: str = Field(..., description="Original text")
    translation: str = Field(..., description="Translated text")
    source_lang: str = Field(..., description="Source language")
    target_lang: str = Field(..., description="Target language")
    cached: bool = Field(..., description="Was result from cache")


@router.post("", response_model=TranslateResponse, summary="Translate text")
async def translate(request: TranslateRequest):
    """
    Translate text between languages

    Currently supports mock translations for common words.
    Future: Integrate DeepL, Google Translate, or local models.

    Supported language pairs:
    - Japanese → Chinese (ja → zh)
    - English → Chinese (en → zh)
    - More coming soon...

    Features:
    - Redis caching (7 days TTL)
    - Fast response (~50ms)
    """
    service = TranslationService()
    result = await service.translate(
        text=request.text,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )

    return TranslateResponse(**result)
