"""
Internationalization (i18n) support for SonarQube Checker.

This module provides translations for report generation in multiple languages.
Translations are loaded from translations.yaml file.
"""

import os
import yaml

# Cache for loaded translations
_TRANSLATIONS_CACHE = None


def _load_translations() -> dict:
    """
    Load translations from YAML file.

    Returns:
        Dictionary with translations for all supported languages
    """
    global _TRANSLATIONS_CACHE

    if _TRANSLATIONS_CACHE is not None:
        return _TRANSLATIONS_CACHE

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    translations_file = os.path.join(script_dir, 'translations.yaml')

    try:
        with open(translations_file, 'r', encoding='utf-8') as f:
            _TRANSLATIONS_CACHE = yaml.safe_load(f)
            return _TRANSLATIONS_CACHE
    except FileNotFoundError:
        # Fallback to hardcoded English translations if file not found
        return {
            'en': {
                'report_title': 'SonarQube Analysis Report',
                'generated': 'Generated',
                'project': 'Project',
                'last_analysis': 'Last Analysis',
                'latest_issues': 'Latest Issues',
                'no_analysis_available': 'No analysis available',
                'no_open_issues': 'No open issues found.',
                'severity': 'Severity',
                'message': 'Message',
                'component': 'Component',
                'line': 'Line',
            }
        }


# Load translations on module import
TRANSLATIONS = _load_translations()


def get_translation(key: str, language: str = 'en') -> str:
    """
    Get translated string for the given key and language.

    Args:
        key: Translation key
        language: Language code ('en' or 'ru')

    Returns:
        Translated string, or English fallback if not found
    """
    # Validate language
    if language not in TRANSLATIONS:
        language = 'en'

    # Get translation or fallback to English
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS['en'].get(key, key))


def get_all_translations(language: str = 'en') -> dict:
    """
    Get all translations for a specific language.

    Args:
        language: Language code ('en' or 'ru')

    Returns:
        Dictionary of all translations for the language
    """
    if language not in TRANSLATIONS:
        language = 'en'

    return TRANSLATIONS[language]
