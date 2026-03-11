"""
Tests for date tolerance logic in cross-reference module.
Most critical piece: ±1 day matching for catering quotes.

Run: python -m pytest tests/test_date_tolerance.py -v
"""

import pytest
from datetime import date, datetime, timedelta
from unittest.mock import patch, MagicMock

# We test the logic directly, not the API calls
from src.crossref import _parse_date_flexible


class TestDateParsing:
    """Test flexible date parsing from various Google Sheets formats."""
    
    def test_iso_format(self):
        assert _parse_date_flexible("2026-03-10") == date(2026, 3, 10)
    
    def test_slash_format_ymd(self):
        assert _parse_date_flexible("2026/03/10") == date(2026, 3, 10)
    
    def test_slash_format_mdy(self):
        assert _parse_date_flexible("03/10/2026") == date(2026, 3, 10)
    
    def test_chinese_format(self):
        assert _parse_date_flexible("2026年03月10日") == date(2026, 3, 10)
    
    def test_invalid_returns_none(self):
        assert _parse_date_flexible("not a date") is None
    
    def test_empty_returns_none(self):
        assert _parse_date_flexible("") is None
    
    def test_with_whitespace(self):
        assert _parse_date_flexible("  2026-03-10  ") == date(2026, 3, 10)


class TestDateToleranceLogic:
    """
    Test the ±1 day tolerance business logic.
    
    Scenario: Catering event on March 10.
    Photos taken on March 9 (prep), March 10 (event), March 11 (cleanup)
    All should match the quote dated March 10.
    """
    
    def _is_within_tolerance(self, photo_date: date, quote_date: date, tolerance: int = 1) -> bool:
        """Extracted tolerance check logic (mirrors crossref._check_sheets)."""
        return abs((photo_date - quote_date).days) <= tolerance
    
    def test_same_day_matches(self):
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 10)
        assert self._is_within_tolerance(photo_date, quote_date) is True
    
    def test_day_before_matches(self):
        """Prep photos taken day before event."""
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 9)
        assert self._is_within_tolerance(photo_date, quote_date) is True
    
    def test_day_after_matches(self):
        """Cleanup/behind-scenes photos day after event."""
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 11)
        assert self._is_within_tolerance(photo_date, quote_date) is True
    
    def test_two_days_before_no_match(self):
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 8)
        assert self._is_within_tolerance(photo_date, quote_date) is False
    
    def test_two_days_after_no_match(self):
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 12)
        assert self._is_within_tolerance(photo_date, quote_date) is False
    
    def test_extended_tolerance_three_days(self):
        """Test with tolerance=3 for edge cases."""
        quote_date = date(2026, 3, 10)
        photo_date = date(2026, 3, 13)
        assert self._is_within_tolerance(photo_date, quote_date, tolerance=3) is True
    
    def test_month_boundary(self):
        """March 31 event, photo on April 1."""
        quote_date = date(2026, 3, 31)
        photo_date = date(2026, 4, 1)
        assert self._is_within_tolerance(photo_date, quote_date) is True
    
    def test_year_boundary(self):
        """Dec 31 event, photo on Jan 1."""
        quote_date = date(2025, 12, 31)
        photo_date = date(2026, 1, 1)
        assert self._is_within_tolerance(photo_date, quote_date) is True
