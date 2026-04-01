"""Tests for database schema creation and management."""

import sqlite3
import tempfile
from pathlib import Path

import pytest
from book_quotes_etl.db.models import create_tables


@pytest.fixture
def temp_db():
    """Create a temporary in-memory database for testing."""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


class TestCreateTables:
    """Test database table creation."""

    def test_creates_jobs_table(self, temp_db):
        """Creates the jobs table with correct schema."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        assert cursor.fetchone() is not None

    def test_creates_quotes_table(self, temp_db):
        """Creates the quotes table with correct schema."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quotes'")
        assert cursor.fetchone() is not None

    def test_jobs_table_columns(self, temp_db):
        """Jobs table has all required columns."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute("PRAGMA table_info(jobs)")
        columns = {row[1] for row in cursor.fetchall()}
        
        expected = {"id", "status", "started_at", "finished_at", "error_message"}
        assert expected.issubset(columns)

    def test_quotes_table_columns(self, temp_db):
        """Quotes table has all required columns."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute("PRAGMA table_info(quotes)")
        columns = {row[1] for row in cursor.fetchall()}
        
        expected = {"id", "quote", "author", "tags"}
        assert expected.issubset(columns)

    def test_quotes_unique_constraint(self, temp_db):
        """Quotes table enforces UNIQUE(quote, author)."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        
        # Insert a quote
        cursor.execute(
            "INSERT INTO quotes (quote, author, tags) VALUES (?, ?, ?)",
            ("Test quote", "Test Author", "tag1, tag2")
        )
        temp_db.commit()
        
        # Attempt to insert duplicate
        with pytest.raises(sqlite3.IntegrityError):
            cursor.execute(
                "INSERT INTO quotes (quote, author, tags) VALUES (?, ?, ?)",
                ("Test quote", "Test Author", "tag3")
            )
            temp_db.commit()

    def test_idempotent_creation(self, temp_db):
        """Creating tables twice doesn't raise errors (IF NOT EXISTS)."""
        create_tables(temp_db)
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name IN ('jobs', 'quotes')")
        count = cursor.fetchone()[0]
        
        # Should have 2 user tables (jobs and quotes)
        assert count == 2

    def test_can_insert_job(self, temp_db):
        """Can insert a job record after schema creation."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute(
            "INSERT INTO jobs (status, started_at) VALUES (?, ?)",
            ("running", "2026-03-31T10:00:00")
        )
        temp_db.commit()
        
        cursor.execute("SELECT COUNT(*) FROM jobs")
        assert cursor.fetchone()[0] == 1

    def test_can_insert_quote(self, temp_db):
        """Can insert a quote record after schema creation."""
        create_tables(temp_db)
        
        cursor = temp_db.cursor()
        cursor.execute(
            "INSERT INTO quotes (quote, author, tags) VALUES (?, ?, ?)",
            ("Test quote", "Test Author", "test, quote")
        )
        temp_db.commit()
        
        cursor.execute("SELECT COUNT(*) FROM quotes")
        assert cursor.fetchone()[0] == 1
