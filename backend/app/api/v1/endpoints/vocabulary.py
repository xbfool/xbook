"""Vocabulary management API endpoints"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from datetime import datetime, timedelta
from uuid import UUID
import uuid

from app.core.database import get_db
from app.db.models.vocabulary import Vocabulary, VocabCard
from app.schemas.vocabulary import (
    VocabularyCreate,
    VocabularyUpdate,
    VocabularyResponse,
    VocabularyDetail,
    VocabularyList,
    VocabularyStats,
)

router = APIRouter()

# Default user ID for single-user mode
DEFAULT_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


@router.post("", response_model=VocabularyResponse, summary="Add vocabulary")
async def create_vocabulary(
    vocab_data: VocabularyCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Add a new vocabulary item

    Automatically creates from:
    - Manual input
    - Word lookup during reading
    - Tokenization results
    """
    # Check if already exists
    query = select(Vocabulary).where(
        and_(
            Vocabulary.user_id == DEFAULT_USER_ID,
            Vocabulary.dictionary_form == vocab_data.dictionary_form,
            Vocabulary.language == vocab_data.language,
        )
    )
    result = await db.execute(query)
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Vocabulary already exists",
        )

    # Create new vocabulary
    vocab = Vocabulary(
        user_id=DEFAULT_USER_ID,
        surface_form=vocab_data.surface_form,
        dictionary_form=vocab_data.dictionary_form,
        language=vocab_data.language,
        reading=vocab_data.reading,
        part_of_speech=vocab_data.part_of_speech,
        translations=vocab_data.translations,
        definitions=vocab_data.definitions,
        context_sentence=vocab_data.context_sentence,
        context_source_id=vocab_data.context_source_id,
    )

    db.add(vocab)
    await db.commit()
    await db.refresh(vocab)

    # Auto-create SRS card
    card = VocabCard(
        vocab_id=vocab.id,
        user_id=DEFAULT_USER_ID,
    )
    db.add(card)
    await db.commit()

    return VocabularyResponse.model_validate(vocab)


@router.get("", response_model=VocabularyList, summary="List vocabulary")
async def list_vocabulary(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    language: Optional[str] = Query(None, description="Filter by language"),
    search: Optional[str] = Query(None, description="Search term"),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's vocabulary with pagination and filters

    Query parameters:
    - page: Page number
    - page_size: Items per page
    - language: Filter by language (en/ja)
    - search: Search in surface_form or dictionary_form
    """
    query = select(Vocabulary).where(Vocabulary.user_id == DEFAULT_USER_ID)

    # Apply filters
    if language:
        query = query.where(Vocabulary.language == language)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            (Vocabulary.surface_form.ilike(search_term))
            | (Vocabulary.dictionary_form.ilike(search_term))
        )

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(desc(Vocabulary.created_at))

    result = await db.execute(query)
    vocabs = result.scalars().all()

    return VocabularyList(
        items=[VocabularyResponse.model_validate(v) for v in vocabs],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/stats", response_model=VocabularyStats, summary="Get vocabulary statistics")
async def get_vocabulary_stats(
    db: AsyncSession = Depends(get_db),
):
    """
    Get vocabulary statistics

    Returns:
    - Total count
    - Count by language
    - Count by proficiency level
    - Recent additions
    """
    # Total count
    total_query = select(func.count()).select_from(Vocabulary).where(
        Vocabulary.user_id == DEFAULT_USER_ID
    )
    total = (await db.execute(total_query)).scalar_one()

    # Count by language
    lang_query = (
        select(Vocabulary.language, func.count())
        .where(Vocabulary.user_id == DEFAULT_USER_ID)
        .group_by(Vocabulary.language)
    )
    lang_result = await db.execute(lang_query)
    by_language = {lang: count for lang, count in lang_result}

    # Count by difficulty level
    level_query = (
        select(Vocabulary.difficulty_level, func.count())
        .where(Vocabulary.user_id == DEFAULT_USER_ID)
        .filter(Vocabulary.difficulty_level.is_not(None))
        .group_by(Vocabulary.difficulty_level)
    )
    level_result = await db.execute(level_query)
    by_level = {level: count for level, count in level_result if level}

    # Recent additions (last 7 days)
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_query = select(func.count()).select_from(Vocabulary).where(
        and_(
            Vocabulary.user_id == DEFAULT_USER_ID,
            Vocabulary.created_at >= week_ago,
        )
    )
    recent = (await db.execute(recent_query)).scalar_one()

    return VocabularyStats(
        total=total,
        by_language=by_language,
        by_level=by_level,
        recent_additions=recent,
    )


@router.get("/{vocab_id}", response_model=VocabularyDetail, summary="Get vocabulary details")
async def get_vocabulary(
    vocab_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get detailed information for a vocabulary item"""
    query = select(Vocabulary).where(
        and_(
            Vocabulary.id == vocab_id,
            Vocabulary.user_id == DEFAULT_USER_ID,
        )
    )

    result = await db.execute(query)
    vocab = result.scalar_one_or_none()

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    # Get associated card info
    card_query = select(VocabCard).where(VocabCard.vocab_id == vocab_id)
    card_result = await db.execute(card_query)
    card = card_result.scalar_one_or_none()

    vocab_dict = VocabularyDetail.model_validate(vocab).model_dump()

    if card:
        vocab_dict["card_status"] = card.status
        vocab_dict["proficiency_level"] = card.repetitions  # Simplified

    return VocabularyDetail(**vocab_dict)


@router.put("/{vocab_id}", response_model=VocabularyResponse, summary="Update vocabulary")
async def update_vocabulary(
    vocab_id: UUID,
    vocab_data: VocabularyUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update vocabulary information"""
    query = select(Vocabulary).where(
        and_(
            Vocabulary.id == vocab_id,
            Vocabulary.user_id == DEFAULT_USER_ID,
        )
    )

    result = await db.execute(query)
    vocab = result.scalar_one_or_none()

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    # Update fields
    if vocab_data.translations is not None:
        vocab.translations = vocab_data.translations
    if vocab_data.definitions is not None:
        vocab.definitions = vocab_data.definitions
    if vocab_data.context_sentence is not None:
        vocab.context_sentence = vocab_data.context_sentence
    if vocab_data.difficulty_level is not None:
        vocab.difficulty_level = vocab_data.difficulty_level

    await db.commit()
    await db.refresh(vocab)

    return VocabularyResponse.model_validate(vocab)


@router.delete("/{vocab_id}", summary="Delete vocabulary")
async def delete_vocabulary(
    vocab_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a vocabulary item"""
    query = select(Vocabulary).where(
        and_(
            Vocabulary.id == vocab_id,
            Vocabulary.user_id == DEFAULT_USER_ID,
        )
    )

    result = await db.execute(query)
    vocab = result.scalar_one_or_none()

    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    await db.delete(vocab)
    await db.commit()

    return {"message": "Vocabulary deleted successfully", "vocab_id": vocab_id}
