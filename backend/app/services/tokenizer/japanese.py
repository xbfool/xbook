"""Japanese tokenizer using SudachiPy"""

from typing import List, Dict, Any
from sudachipy import tokenizer, dictionary


class JapaneseTokenizer:
    """Japanese text tokenizer using SudachiPy"""

    def __init__(self):
        """Initialize SudachiPy tokenizer"""
        self.tokenizer_obj = dictionary.Dictionary().create()
        # Mode C: Longest match (best for language learning)
        self.mode = tokenizer.Tokenizer.SplitMode.C

    def tokenize(self, text: str) -> List[Dict[str, Any]]:
        """
        Tokenize Japanese text into words with metadata

        Args:
            text: Japanese text to tokenize

        Returns:
            List of tokens with surface form, dictionary form, reading, and POS
        """
        if not text or not text.strip():
            return []

        tokens = self.tokenizer_obj.tokenize(text, self.mode)

        result = []
        for token in tokens:
            result.append({
                "surface": token.surface(),  # 表層形（実際の形）
                "dictionary_form": token.dictionary_form(),  # 辞書形（基本形）
                "reading": token.reading_form(),  # 読み方（ふりがな）
                "part_of_speech": self._get_pos_tag(token),  # 品詞
                "normalized": token.normalized_form(),  # 正規化形
            })

        return result

    def _get_pos_tag(self, token) -> str:
        """Extract simplified POS tag"""
        pos_tags = token.part_of_speech()
        # Return main POS category (first element)
        return pos_tags[0] if pos_tags else "unknown"

    def get_word_info(self, word: str) -> Dict[str, Any]:
        """
        Get detailed information for a single word

        Args:
            word: Japanese word

        Returns:
            Dictionary with word information
        """
        tokens = self.tokenize(word)
        if not tokens:
            return {}

        # Return info for first token (single word)
        return tokens[0] if len(tokens) == 1 else {
            "surface": word,
            "tokens": tokens,  # Multiple tokens
            "is_compound": True,
        }


# Singleton instance
_japanese_tokenizer = None


def get_japanese_tokenizer() -> JapaneseTokenizer:
    """Get or create JapaneseTokenizer singleton"""
    global _japanese_tokenizer
    if _japanese_tokenizer is None:
        _japanese_tokenizer = JapaneseTokenizer()
    return _japanese_tokenizer
