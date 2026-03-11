"""
Tests for transformer.py -- filename building and WebP conversion logic.

Run: python -m pytest tests/test_transformer.py -v
"""

import pytest
from datetime import datetime
from src.transformer import build_filename, slugify


class TestSlugify:

    def test_basic_ascii(self):
        assert slugify("Hello World") == "hello-world"

    def test_special_chars_removed(self):
        result = slugify("cafe brasserie!")
        assert "!" not in result

    def test_max_len_respected(self):
        result = slugify("a" * 50, max_len=10)
        assert len(result) <= 10

    def test_hyphens_not_duplicated(self):
        assert slugify("foo--bar") == "foo-bar"

    def test_empty_string(self):
        assert slugify("") == ""


class TestBuildFilename:

    def test_basic_filename(self):
        dt = datetime(2026, 3, 10, 12, 0, 0)
        result = build_filename(dt, "tainan-wedding", ["milkfish", "panfry", "taiwanese"])
        assert result == "20260310_tainan-wedding_milkfish-panfry-taiwanese.webp"

    def test_webp_extension(self):
        dt = datetime(2026, 3, 10)
        result = build_filename(dt, "catering", ["food"])
        assert result.endswith(".webp")

    def test_date_prefix_format(self):
        dt = datetime(2026, 1, 5)
        result = build_filename(dt, "test", ["kw"])
        assert result.startswith("20260105_")

    def test_empty_project_uses_maplab(self):
        dt = datetime(2026, 3, 10)
        result = build_filename(dt, "", ["food"])
        assert "maplab" in result

    def test_none_project_uses_maplab(self):
        dt = datetime(2026, 3, 10)
        result = build_filename(dt, None, ["food"])
        assert "maplab" in result

    def test_max_three_keywords(self):
        dt = datetime(2026, 3, 10)
        result = build_filename(dt, "proj", ["kw1", "kw2", "kw3", "kw4", "kw5"])
        parts = result.replace(".webp", "").split("_")
        kw_part = parts[2]
        assert kw_part.count("-") == 2

    def test_filename_length_under_80(self):
        dt = datetime(2026, 3, 10)
        result = build_filename(
            dt,
            "very-long-project-name-that-exceeds-normal-limits",
            ["keyword-one", "keyword-two", "keyword-three"]
        )
        assert len(result) <= 80


class TestEnvSettings:

    def test_webp_quality_is_int(self):
        import src.transformer as t
        assert isinstance(t.WEBP_QUALITY, int)
        assert 1 <= t.WEBP_QUALITY <= 100

    def test_max_width_is_int(self):
        import src.transformer as t
        assert isinstance(t.MAX_WIDTH, int)
        assert t.MAX_WIDTH > 0
