"""Tokenizer API endpoints"""

from fastapi import APIRouter, HTTPException

from app.schemas.tokenizer import (
    TokenizeRequest,
    TokenizeResponse,
    TokenizeWithEntitiesResponse,
    Token,
    Entity,
)
from app.services.tokenizer import get_japanese_tokenizer, get_english_tokenizer

router = APIRouter()


@router.post("/japanese", response_model=TokenizeResponse, summary="Tokenize Japanese text")
async def tokenize_japanese(request: TokenizeRequest):
    """
    Tokenize Japanese text using SudachiPy

    Returns word-level tokens with:
    - Surface form (表層形)
    - Dictionary form (辞書形)
    - Reading (読み方/ふりがな)
    - Part of speech (品詞)
    """
    try:
        tokenizer = get_japanese_tokenizer()
        tokens_data = tokenizer.tokenize(request.text)

        tokens = [Token(**token_data) for token_data in tokens_data]

        return TokenizeResponse(
            language="ja",
            tokens=tokens,
            word_count=len(tokens),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tokenization failed: {str(e)}")


@router.post("/english", response_model=TokenizeResponse, summary="Tokenize English text")
async def tokenize_english(request: TokenizeRequest):
    """
    Tokenize English text using spaCy

    Returns word-level tokens with:
    - Surface form (original text)
    - Dictionary form (lemma/base form)
    - Part of speech
    - Stop word flag
    """
    try:
        tokenizer = get_english_tokenizer()
        tokens_data = tokenizer.tokenize(request.text)

        tokens = [Token(**token_data) for token_data in tokens_data]

        return TokenizeResponse(
            language="en",
            tokens=tokens,
            word_count=len(tokens),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tokenization failed: {str(e)}")


@router.post(
    "/english/entities",
    response_model=TokenizeWithEntitiesResponse,
    summary="Tokenize English with named entities",
)
async def tokenize_english_with_entities(request: TokenizeRequest):
    """
    Tokenize English text and extract named entities

    Returns:
    - Word-level tokens
    - Named entities (PERSON, ORG, GPE, DATE, etc.)
    """
    try:
        tokenizer = get_english_tokenizer()
        result = tokenizer.tokenize_with_entities(request.text)

        tokens = [Token(**token_data) for token_data in result["tokens"]]
        entities = [Entity(**ent_data) for ent_data in result["entities"]]

        return TokenizeWithEntitiesResponse(
            language="en",
            tokens=tokens,
            entities=entities,
            word_count=len(tokens),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tokenization failed: {str(e)}")
