"""Text management API endpoints"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
import uuid
import os
from pathlib import Path

from app.core.database import get_db
from app.db.models.text import TextModel
from app.db.models.user import User
from app.schemas.text import TextCreate, TextResponse, TextDetail, TextList, UploadResponse
from app.services.text_parser import EPUBParser, PDFParser

router = APIRouter()

# File upload directory
UPLOAD_DIR = Path("/data/books")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Default user ID for single-user mode
DEFAULT_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


@router.post("/create", response_model=TextResponse, summary="Create text manually")
async def create_text(
    text_data: TextCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Manually create a text entry (for testing or direct input)

    Use this endpoint to add text without uploading a file.
    """
    text = TextModel(
        user_id=DEFAULT_USER_ID,
        title=text_data.title,
        content=text_data.content,
        language=text_data.language,
        author=text_data.author,
        source_type=text_data.source_type or 'manual',
        source_url=text_data.source_url,
        word_count=len(text_data.content.split()),
    )

    db.add(text)
    await db.commit()
    await db.refresh(text)

    return TextResponse.model_validate(text)


@router.post("/upload", response_model=UploadResponse, summary="Upload book file")
async def upload_book(
    file: UploadFile = File(..., description="EPUB or PDF file"),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload and parse an EPUB or PDF book file

    Supports:
    - EPUB files (.epub)
    - PDF files (.pdf)

    Returns:
    - Parsed text with metadata
    - Automatically detects language
    - Extracts title and author
    """
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.epub', '.pdf']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Only .epub and .pdf are supported."
        )

    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        saved_file_path = UPLOAD_DIR / f"{file_id}{file_ext}"

        with open(saved_file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Parse file based on type
        if file_ext == '.epub':
            parser = EPUBParser()
        else:  # .pdf
            parser = PDFParser()

        parsed_data = parser.parse(str(saved_file_path))

        if not parsed_data.get('success'):
            # Clean up file
            os.remove(saved_file_path)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse file: {parsed_data.get('error')}"
            )

        # Calculate proper word count based on language
        content = parsed_data['content']
        language = parsed_data['language']

        if language == 'ja':
            # Japanese: count characters (excluding spaces and punctuation)
            import re
            word_count = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', content))
        else:
            # English: count words by splitting
            word_count = len(content.split())

        # Create text record in database
        text = TextModel(
            user_id=DEFAULT_USER_ID,
            title=parsed_data['title'],
            content=content,
            language=language,
            author=parsed_data.get('author'),
            source_type=parsed_data['source_type'],
            word_count=word_count,
        )

        db.add(text)
        await db.commit()
        await db.refresh(text)

        return UploadResponse(
            text_id=text.id,
            title=text.title,
            word_count=text.word_count,
            language=text.language,
            message=f"Successfully uploaded and parsed {file.filename}"
        )

    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if it exists
        if saved_file_path.exists():
            os.remove(saved_file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("", response_model=TextList, summary="List all texts")
async def list_texts(
    page: int = 1,
    page_size: int = 20,
    language: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """
    List all texts for the user

    Query parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20)
    - language: Filter by language (optional)
    """
    query = select(TextModel).where(TextModel.user_id == DEFAULT_USER_ID)

    if language:
        query = query.where(TextModel.language == language)

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get paginated results
    query = query.offset((page - 1) * page_size).limit(page_size)
    query = query.order_by(TextModel.created_at.desc())

    result = await db.execute(query)
    texts = result.scalars().all()

    return TextList(
        items=[TextResponse.model_validate(text) for text in texts],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{text_id}", response_model=TextDetail, summary="Get text details")
async def get_text(
    text_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Get detailed information for a specific text

    Returns:
    - Full text content
    - Metadata
    - Statistics
    """
    query = select(TextModel).where(
        TextModel.id == text_id,
        TextModel.user_id == DEFAULT_USER_ID
    )

    result = await db.execute(query)
    text = result.scalar_one_or_none()

    if not text:
        raise HTTPException(status_code=404, detail="Text not found")

    return TextDetail.model_validate(text)


@router.delete("/{text_id}", summary="Delete text")
async def delete_text(
    text_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a text"""
    query = select(TextModel).where(
        TextModel.id == text_id,
        TextModel.user_id == DEFAULT_USER_ID
    )

    result = await db.execute(query)
    text = result.scalar_one_or_none()

    if not text:
        raise HTTPException(status_code=404, detail="Text not found")

    await db.delete(text)
    await db.commit()

    return {"message": "Text deleted successfully", "text_id": text_id}
