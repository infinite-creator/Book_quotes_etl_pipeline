"""Tests for pipeline smoke behavior and integration."""

import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from book_quotes_etl.pipeline.orchestrator import run_pipeline
from book_quotes_etl.db.database import get_connection
from book_quotes_etl.config.settings import SQLITE_DB, OUTPUT_DIR


@pytest.fixture
def mock_extract():
    """Mock extract_all_quotes to return test data."""
    with patch('book_quotes_etl.pipeline.orchestrator.extract_all_quotes') as mock:
        mock.return_value = [
            {"quote": "Test quote 1", "author": "Author 1", "tags": ["tag1", "tag2"]},
            {"quote": "Test quote 2", "author": "Author 2", "tags": ["tag3"]},
        ]
        yield mock


@pytest.fixture
def temp_output_dir(tmp_path):
    """Use a temporary directory for output."""
    with patch('book_quotes_etl.pipeline.orchestrator.OUTPUT_DIR', tmp_path):
        yield tmp_path


class TestRunPipeline:
    """Test pipeline execution."""

    def test_pipeline_accepts_keyword_args(self, mock_extract):
        """Pipeline accepts keyword arguments for control."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    # Should not raise
                    run_pipeline(skip_csv=True, skip_db=True)

    def test_pipeline_creates_output_directory(self, mock_extract, temp_output_dir):
        """Pipeline creates output directory if it doesn't exist."""
        custom_output = temp_output_dir / "custom"
        
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    run_pipeline(output_dir=custom_output, skip_csv=True, skip_db=True)
        
        assert custom_output.exists()

    def test_pipeline_calls_extract(self, mock_extract):
        """Pipeline calls extract_all_quotes."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    run_pipeline(skip_csv=True, skip_db=True)
        
        mock_extract.assert_called_once()

    def test_pipeline_skips_csv_when_requested(self, mock_extract):
        """Pipeline skips CSV loading when skip_csv=True."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv') as mock_csv:
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    run_pipeline(skip_csv=True, skip_db=True)
        
        mock_csv.assert_not_called()

    def test_pipeline_loads_csv_by_default(self, mock_extract):
        """Pipeline loads to CSV by default."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv') as mock_csv:
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    run_pipeline(skip_db=True)
        
        mock_csv.assert_called_once()

    def test_pipeline_skips_db_when_requested(self, mock_extract):
        """Pipeline skips database loading when skip_db=True."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite') as mock_db:
                    run_pipeline(skip_csv=True, skip_db=True)
        
        mock_db.assert_not_called()

    def test_pipeline_uses_provided_connection(self, mock_extract):
        """Pipeline uses a provided database connection."""
        mock_conn = MagicMock()
        
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite') as mock_load:
                    run_pipeline(conn=mock_conn, skip_csv=True)
        
        # Verify the mock connection was passed to load_to_sqlite
        mock_load.assert_called_once()
        args = mock_load.call_args[0]
        assert args[1] is mock_conn

    def test_pipeline_closes_owned_connection(self, mock_extract):
        """Pipeline closes database connection if it created one."""
        mock_conn = MagicMock()
        
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    with patch('book_quotes_etl.pipeline.orchestrator.get_connection', return_value=mock_conn):
                        run_pipeline(skip_csv=True)
        
        mock_conn.close.assert_called_once()

    def test_pipeline_does_not_close_external_connection(self, mock_extract):
        """Pipeline does not close an externally provided connection."""
        mock_conn = MagicMock()
        
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                    run_pipeline(conn=mock_conn, skip_csv=True)
        
        mock_conn.close.assert_not_called()

    def test_pipeline_calls_log_indicators(self, mock_extract):
        """Pipeline calls log indicators."""
        with patch('book_quotes_etl.pipeline.orchestrator.set_logger'):
            with patch('book_quotes_etl.pipeline.orchestrator.log_run_indicator') as mock_log:
                with patch('book_quotes_etl.pipeline.orchestrator.load_to_csv'):
                    with patch('book_quotes_etl.pipeline.orchestrator.load_to_sqlite'):
                        run_pipeline(skip_csv=True, skip_db=True)
        
        # Should be called twice: START and END
        assert mock_log.call_count >= 2


class TestDatabaseConnection:
    """Test database connection behavior."""

    def test_get_connection_creates_db_dir(self, tmp_path):
        """get_connection creates parent directory if needed."""
        with patch('book_quotes_etl.db.database.SQLITE_DB', tmp_path / "subdir" / "test.db"):
            try:
                conn = get_connection()
                assert (tmp_path / "subdir").exists()
                conn.close()
            except Exception:
                # May fail if can't actually connect, but dir should exist
                assert (tmp_path / "subdir").exists()

    def test_get_connection_initializes_schema(self):
        """get_connection creates schema on first connect."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        
        try:
            with patch('book_quotes_etl.db.database.SQLITE_DB', Path(db_path)):
                conn = get_connection()
                
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = {row[0] for row in cursor.fetchall()}
                
                assert "jobs" in tables
                assert "quotes" in tables
                
                conn.close()
        finally:
            Path(db_path).unlink(missing_ok=True)
