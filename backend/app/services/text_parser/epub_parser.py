"""EPUB file parser"""

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re


class EPUBParser:
    """Parse EPUB files and extract text content"""

    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Parse EPUB file and extract metadata and content

        Args:
            file_path: Path to EPUB file

        Returns:
            Dictionary with title, author, content, and metadata
        """
        try:
            book = epub.read_epub(file_path)

            # Extract metadata
            title = self._get_metadata(book, 'title') or 'Untitled'
            author = self._get_metadata(book, 'creator') or 'Unknown'
            language = self._get_metadata(book, 'language') or 'unknown'

            # Extract content
            content = self._extract_content(book)

            # Calculate statistics
            word_count = len(content.split())

            return {
                'title': title,
                'author': author,
                'language': language,
                'content': content,
                'word_count': word_count,
                'source_type': 'epub',
                'success': True,
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'error_type': type(e).__name__,
            }

    def _get_metadata(self, book: epub.EpubBook, key: str) -> Optional[str]:
        """Extract metadata from EPUB"""
        try:
            metadata = book.get_metadata('DC', key)
            if metadata and len(metadata) > 0:
                return metadata[0][0]
        except:
            pass
        return None

    def _extract_content(self, book: epub.EpubBook) -> str:
        """Extract text content from all documents in EPUB"""
        content_parts = []

        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # Parse HTML content
                html_content = item.get_content()
                soup = BeautifulSoup(html_content, 'html.parser')

                # Remove script and style tags
                for script in soup(['script', 'style']):
                    script.decompose()

                # Extract text
                text = soup.get_text()

                # Clean up whitespace
                text = self._clean_text(text)

                if text.strip():
                    content_parts.append(text)

        return '\n\n'.join(content_parts)

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        # Remove leading/trailing whitespace from lines
        lines = [line.strip() for line in text.split('\n')]
        text = '\n'.join(lines)

        return text.strip()
