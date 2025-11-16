"""Base translation service with caching"""

from typing import Optional, Dict
import hashlib
import redis.asyncio as redis
from app.core.redis import get_redis


class TranslationService:
    """
    Translation service with Redis caching

    For now, returns mock translations.
    Future: Integrate DeepL, Google Translate, or local models
    """

    def __init__(self):
        self.cache_ttl = 604800  # 7 days
        self._cache: Optional[redis.Redis] = None

    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> Dict[str, str]:
        """
        Translate text from source to target language

        Args:
            text: Text to translate
            source_lang: Source language code (en, ja, etc.)
            target_lang: Target language code

        Returns:
            Dictionary with original text and translation
        """
        # Generate cache key
        cache_key = self._generate_cache_key(text, source_lang, target_lang)

        # Try to get from cache
        async for redis_client in get_redis():
            cached = await redis_client.get(cache_key)
            if cached:
                return {
                    "original": text,
                    "translation": cached,
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "cached": True,
                }

            # For now, return mock translation
            # TODO: Integrate real translation API
            translation = await self._mock_translate(text, source_lang, target_lang)

            # Cache result
            await redis_client.setex(cache_key, self.cache_ttl, translation)

            return {
                "original": text,
                "translation": translation,
                "source_lang": source_lang,
                "target_lang": target_lang,
                "cached": False,
            }

    async def _mock_translate(
        self, text: str, source_lang: str, target_lang: str
    ) -> str:
        """
        Mock translation for testing

        In production, replace with:
        - DeepL API
        - Google Translate API
        - Local translation model
        """
        # Simple mock translations for common words
        mock_dict = {
            # Japanese to Chinese
            ("ja", "zh"): {
                "日本語": "日语",
                "勉強": "学习",
                "私": "我",
                "毎日": "每天",
                "今日": "今天",
                "明日": "明天",
                "学習": "学习",
                "テキスト": "文本",
                "これ": "这个",
                "それ": "那个",
            },
            # English to Chinese
            ("en", "zh"): {
                "hello": "你好",
                "world": "世界",
                "learn": "学习",
                "study": "学习",
                "book": "书",
                "read": "阅读",
                "language": "语言",
            },
        }

        # Get mock translation
        lang_pair = (source_lang, target_lang)
        if lang_pair in mock_dict and text in mock_dict[lang_pair]:
            return mock_dict[lang_pair][text]

        # Default mock response
        return f"[Mock translation: {text}]"

    def _generate_cache_key(
        self, text: str, source_lang: str, target_lang: str
    ) -> str:
        """Generate Redis cache key for translation"""
        content = f"{source_lang}:{target_lang}:{text}"
        hash_val = hashlib.md5(content.encode()).hexdigest()
        return f"trans:{hash_val}"


# Singleton instance
_translation_service = None


async def get_translation_service() -> TranslationService:
    """Get or create TranslationService singleton"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service
