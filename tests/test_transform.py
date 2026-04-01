"""Tests for quote transformation logic."""

import pytest
from book_quotes_etl.pipeline.transform import transform_quotes, is_valid_quote


class TestIsValidQuote:
    """Test quote validation logic."""

    def test_valid_quote(self):
        """Valid quotes with text and author pass."""
        quote = {"quote": "Test quote", "author": "Test Author"}
        assert is_valid_quote(quote) is True

    def test_missing_quote_text(self):
        """Quote without text field is invalid."""
        quote = {"author": "Test Author"}
        assert is_valid_quote(quote) is False

    def test_empty_quote_text(self):
        """Quote with empty text is invalid."""
        quote = {"quote": "", "author": "Test Author"}
        assert is_valid_quote(quote) is False

    def test_missing_author(self):
        """Quote without author is invalid."""
        quote = {"quote": "Test quote"}
        assert is_valid_quote(quote) is False

    def test_empty_author(self):
        """Quote with empty author is invalid."""
        quote = {"quote": "Test quote", "author": ""}
        assert is_valid_quote(quote) is False


class TestTransformQuotes:
    """Test quote transformation."""

    def test_empty_list(self):
        """Empty quote list returns empty list."""
        result = transform_quotes([])
        assert result == []

    def test_single_valid_quote(self):
        """Single valid quote is transformed correctly."""
        raw_quote = {
            "quote": "  Test quote  ",
            "author": "  Test Author  ",
            "tags": ["  tag1  ", "  tag2  "]
        }
        result = transform_quotes([raw_quote])
        
        assert len(result) == 1
        assert result[0]["quote"] == "Test quote"
        assert result[0]["author"] == "Test Author"
        assert result[0]["tags"] == "tag1, tag2"

    def test_removes_invalid_quotes(self):
        """Invalid quotes are filtered out."""
        quotes = [
            {"quote": "Valid", "author": "Author", "tags": []},
            {"quote": "", "author": "Author", "tags": []},  # Invalid: empty quote
            {"quote": "Valid 2", "author": "", "tags": []},  # Invalid: empty author
            {"quote": "Valid 3", "author": "Author 3", "tags": []},
        ]
        result = transform_quotes(quotes)
        
        assert len(result) == 2
        assert result[0]["quote"] == "Valid"
        assert result[1]["quote"] == "Valid 3"

    def test_removes_duplicates(self):
        """Duplicate quotes (by text and author) are removed."""
        quotes = [
            {"quote": "Same quote", "author": "Same Author", "tags": ["tag1"]},
            {"quote": "Same quote", "author": "Same Author", "tags": ["tag2"]},  # Duplicate
            {"quote": "Different", "author": "Same Author", "tags": ["tag3"]},
        ]
        result = transform_quotes(quotes)
        
        assert len(result) == 2
        assert result[0]["quote"] == "Same quote"
        assert result[0]["tags"] == "tag1"
        assert result[1]["quote"] == "Different"

    def test_preserves_tags_order(self):
        """Tags are joined in order with proper formatting."""
        raw_quote = {
            "quote": "Test",
            "author": "Author",
            "tags": ["philosophy", "life", "wisdom"]
        }
        result = transform_quotes([raw_quote])
        
        assert result[0]["tags"] == "philosophy, life, wisdom"

    def test_handles_no_tags(self):
        """Quotes with no tags are handled gracefully."""
        raw_quote = {
            "quote": "Test",
            "author": "Author",
            "tags": []
        }
        result = transform_quotes([raw_quote])
        
        assert result[0]["tags"] == ""

    def test_logging_info(self, caplog):
        """Transform logs the number of transformed quotes."""
        import logging as log_module
        
        quotes = [
            {"quote": "Quote 1", "author": "Author 1", "tags": []},
            {"quote": "Quote 2", "author": "Author 2", "tags": []},
        ]
        
        with caplog.at_level(log_module.INFO):
            transform_quotes(quotes)
        
        assert "Transformed 2 unique quotes" in caplog.text
