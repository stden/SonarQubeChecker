#!/usr/bin/env python3
"""
Tests for i18n (internationalization) module.
"""

import sys
import os
import importlib

import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from i18n import get_translation, get_all_translations, TRANSLATIONS


class TestI18n:
    """Test i18n translation functions."""

    def test_get_translation_english(self):
        """Test getting English translations."""
        assert get_translation('report_title', 'en') == '📊 SonarQube Analysis Report'
        assert get_translation('generated', 'en') == '🕒 Generated'
        assert get_translation('severity', 'en') == '🔥 Severity'

    def test_get_translation_russian(self):
        """Test getting Russian translations."""
        assert get_translation('report_title', 'ru') == '📊 Отчёт анализа SonarQube'
        assert get_translation('generated', 'ru') == '🕒 Создано'
        assert get_translation('severity', 'ru') == '🔥 Важность'

    def test_get_translation_default_language(self):
        """Test default language is English."""
        assert get_translation('report_title') == '📊 SonarQube Analysis Report'

    def test_get_translation_invalid_language(self):
        """Test fallback to English for invalid language."""
        assert get_translation('report_title', 'fr') == '📊 SonarQube Analysis Report'
        assert get_translation('generated', 'de') == '🕒 Generated'

    def test_get_translation_missing_key(self):
        """Test handling of missing translation key."""
        result = get_translation('nonexistent_key', 'en')
        # Should return the key itself if not found
        assert result == 'nonexistent_key'

    def test_get_all_translations_english(self):
        """Test getting all English translations."""
        translations = get_all_translations('en')
        assert isinstance(translations, dict)
        assert 'report_title' in translations
        assert translations['report_title'] == '📊 SonarQube Analysis Report'

    def test_get_all_translations_russian(self):
        """Test getting all Russian translations."""
        translations = get_all_translations('ru')
        assert isinstance(translations, dict)
        assert 'report_title' in translations
        assert translations['report_title'] == '📊 Отчёт анализа SonarQube'

    def test_get_all_translations_invalid_language(self):
        """Test fallback for invalid language in get_all_translations."""
        translations = get_all_translations('invalid')
        assert isinstance(translations, dict)
        assert translations == TRANSLATIONS['en']

    def test_translations_loaded(self):
        """Test that TRANSLATIONS dictionary is properly loaded."""
        assert 'en' in TRANSLATIONS
        assert 'ru' in TRANSLATIONS
        assert isinstance(TRANSLATIONS['en'], dict)
        assert isinstance(TRANSLATIONS['ru'], dict)

    def test_all_keys_present_in_both_languages(self):
        """Test that all translation keys are present in both languages."""
        en_keys = set(TRANSLATIONS['en'].keys())
        ru_keys = set(TRANSLATIONS['ru'].keys())
        assert en_keys == ru_keys, "Translation keys mismatch between en and ru"

    def test_no_empty_translations(self):
        """Test that no translations are empty strings."""
        for lang in ['en', 'ru']:
            for key, value in TRANSLATIONS[lang].items():
                assert value != '', f"Empty translation for {lang}.{key}"
                assert isinstance(value, str), f"Non-string translation for {lang}.{key}"

    def test_load_translations_cache(self):
        """Test that _load_translations uses cache on subsequent calls."""
        from i18n import _load_translations

        # Call twice
        result1 = _load_translations()
        result2 = _load_translations()

        # Should return the exact same object (cached)
        assert result1 is result2

    def test_load_translations_fallback(self, monkeypatch):
        """Reloading the module with a missing file should use built-in defaults."""
        import i18n as i18n_module
        import builtins

        # Save original open
        original_open = builtins.open

        monkeypatch.setattr(i18n_module, '_TRANSLATIONS_CACHE', None)
        def fake_open(*args, **kwargs):
            raise FileNotFoundError()

        monkeypatch.setattr('builtins.open', fake_open)

        fallback_module = importlib.reload(i18n_module)
        assert fallback_module.TRANSLATIONS['en']['report_title'] == 'SonarQube Analysis Report'

        # Restore real open before reloading to get real translations
        monkeypatch.setattr('builtins.open', original_open)

        # Restore real translations for subsequent tests
        monkeypatch.setattr(fallback_module, '_TRANSLATIONS_CACHE', None)
        importlib.reload(fallback_module)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
