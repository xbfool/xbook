"""PDF file parser"""

import fitz  # PyMuPDF
from typing import Dict, Any
import re


class PDFParser:
    """Parse PDF files and extract text content"""

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse PDF file and extract metadata and content

        Args:
            file_path: Path to PDF file

        Returns:
            Dictionary with title, author, content, and metadata
        """
        try:
            doc = fitz.open(file_path)

            # Extract metadata
            metadata = doc.metadata
            title = metadata.get('title') or 'Untitled'
            author = metadata.get('author') or 'Unknown'

            # Extract content from all pages
            content_parts = []
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()

                if text.strip():
                    # Clean text
                    text = self._clean_text(text)
                    content_parts.append(text)

            content = '\n\n'.join(content_parts)

            # Calculate statistics
            word_count = len(content.split())

            # Try to detect language from content
            language = self._detect_language_simple(content)

            doc.close()

            return {
                'title': title,
                'author': author,
                'language': language,
                'content': content,
                'word_count': word_count,
                'page_count': len(doc),
                'source_type': 'pdf',
                'success': True,
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
            }

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text.strip()

    def _detect_language_simple(self, text: str) -> str:
        """
        Simple language detection based on character patterns

        Args:
            text: Text content

        Returns:
            Language code (en, ja, or unknown)
        """
        if not text:
            return 'unknown'

        # Count Japanese characters (Hiragana, Katakana, Kanji)
        japanese_chars = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]', text))

        # Count ASCII alphabetic characters
        ascii_chars = len(re.findall(r'[a-zA-Z]', text))

        total_chars = len(text)

        if total_chars == 0:
            return 'unknown'

        # Calculate ratios
        japanese_ratio = japanese_chars / total_chars
        ascii_ratio = ascii_chars / total_chars

        # Simple heuristic
        if japanese_ratio > 0.2:
            return 'ja'
        elif ascii_ratio > 0.5:
            return 'en'
        else:
            return 'unknown'
