"""English tokenizer using spaCy"""

from typing import List, Dict, Any
import spacy


class EnglishTokenizer:
    """English text tokenizer using spaCy"""

    def __init__(self):
        """Initialize spaCy tokenizer"""
        # Load small English model
        self.nlp = spacy.load("en_core_web_sm")

    def tokenize(self, text: str) -> List[Dict[str, Any]]:
        """
        Tokenize English text into words with metadata

        Args:
            text: English text to tokenize

        Returns:
            List of tokens with surface form, lemma, POS, and more
        """
        if not text or not text.strip():
            return []

        doc = self.nlp(text)

        result = []
        for token in doc:
            # Skip punctuation and whitespace for cleaner vocabulary
            if token.is_punct or token.is_space:
                continue

            result.append({
                "surface": token.text,  # Original form
                "dictionary_form": token.lemma_,  # Base form (lemma)
                "part_of_speech": token.pos_,  # Part of speech
                "tag": token.tag_,  # Detailed POS tag
                "dependency": token.dep_,  # Syntactic dependency
                "is_stop": token.is_stop,  # Stop word flag
            })

        return result

    def tokenize_with_entities(self, text: str) -> Dict[str, Any]:
        """
        Tokenize text and extract named entities

        Args:
            text: English text

        Returns:
            Dictionary with tokens and entities
        """
        if not text or not text.strip():
            return {"tokens": [], "entities": []}

        doc = self.nlp(text)

        # Get tokens
        tokens = []
        for token in doc:
            if not token.is_punct and not token.is_space:
                tokens.append({
                    "surface": token.text,
                    "dictionary_form": token.lemma_,
                    "part_of_speech": token.pos_,
                })

        # Get named entities
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,  # PERSON, ORG, GPE, etc.
                "start": ent.start_char,
                "end": ent.end_char,
            })

        return {
            "tokens": tokens,
            "entities": entities,
        }

    def get_word_info(self, word: str) -> Dict[str, Any]:
        """
        Get detailed information for a single word

        Args:
            word: English word

        Returns:
            Dictionary with word information
        """
        doc = self.nlp(word)

        if len(doc) == 0:
            return {}

        token = doc[0]

        return {
            "surface": token.text,
            "dictionary_form": token.lemma_,
            "part_of_speech": token.pos_,
            "tag": token.tag_,
            "is_stop": token.is_stop,
            "is_alpha": token.is_alpha,
        }


# Singleton instance
_english_tokenizer = None


def get_english_tokenizer() -> EnglishTokenizer:
    """Get or create EnglishTokenizer singleton"""
    global _english_tokenizer
    if _english_tokenizer is None:
        _english_tokenizer = EnglishTokenizer()
    return _english_tokenizer
