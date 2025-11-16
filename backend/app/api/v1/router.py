"""API v1 main router"""

from fastapi import APIRouter

from .endpoints import tokenizer

# Create main API router
api_router = APIRouter()

# Include tokenizer endpoints
api_router.include_router(tokenizer.router, prefix="/tokenizer", tags=["tokenizer"])

# Import and include sub-routers here as they are created
# from .endpoints import auth, users, texts, vocabulary, reviews

# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(texts.router, prefix="/texts", tags=["texts"])
# api_router.include_router(vocabulary.router, prefix="/vocabulary", tags=["vocabulary"])
# api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])


@api_router.get("/ping", tags=["health"])
async def ping():
    """Ping endpoint for API health check"""
    return {"message": "pong"}
