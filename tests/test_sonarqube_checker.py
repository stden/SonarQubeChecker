#!/usr/bin/env python3
"""
Test script for SonarQube Checker functionality.
This tests the core functions without requiring a live SonarQube instance.
"""

import os
import sys

# Add the parent directory to the path to import sonarqube_checker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sonarqube_checker import MarkdownReportGenerator  # pylint: disable=wrong-import-position


def test_format_analysis_date():
    """Test date formatting function."""
    print("Testing format_analysis_date...")

    # Test with valid ISO date
    date1 = "2024-01-15T12:00:00+0000"
    generator = MarkdownReportGenerator()
    result1 = generator.format_analysis_date(date1)
    print(f"  Input: {date1}")
    print(f"  Output: {result1}")
    assert "2024-01-15" in result1, "Date formatting failed"

    # Test with None
    result2 = generator.format_analysis_date(None)
    print("  Input: None")
    print(f"  Output: {result2}")
    assert result2 == "⚠️ No analysis available", "None handling failed"

    print("✓ format_analysis_date tests passed\n")


def test_generate_issues_table():
    """Test issues table generation."""
    print("Testing generate_issues_table...")

    # Test with issues
    issues = [
        {
            'severity': 'MAJOR',
            'message': 'Remove unused variable',
            'component': 'project:src/main.py',
            'line': 42
        },
        {
            'severity': 'MINOR',
            'message': 'Add comment',
            'component': 'project:src/utils.py',
            'line': 15
        }
    ]

    generator = MarkdownReportGenerator()
    result = generator.generate_issues_table(issues)
    print(f"  Generated table:\n{result}")
    assert "| 🔥 Severity | 💬 Message | 🧩 Component | 📍 Line |" in result, "Table header missing"
    assert "MAJOR" in result, "Issue severity missing"
    assert "Remove unused variable" in result, "Issue message missing"

    # Test with empty issues
    result_empty = generator.generate_issues_table([])
    print(f"  Empty issues result: {result_empty}")
    assert "✅ No open issues found." in result_empty, "Empty issues handling failed"

    print("✓ generate_issues_table tests passed\n")


def test_generate_report():
    """Test full report generation."""
    print("Testing generate_report...")

    projects_data = [
        {
            'project_key': 'test-project',
            'last_analysis': '2024-01-15T12:00:00+0000',
            'issues': [
                {
                    'severity': 'CRITICAL',
                    'message': 'Security vulnerability detected',
                    'component': 'test-project:src/auth.py',
                    'line': 100
                }
            ]
        }
    ]

    generator = MarkdownReportGenerator()
    report = generator.generate_report(projects_data)
    print(f"  Generated report (first 500 chars):\n{report[:500]}...")

    assert "# 📊 SonarQube Analysis Report" in report, "Report title missing"
    assert "test-project" in report, "Project key missing"
    assert "CRITICAL" in report, "Issue severity missing"
    assert "Security vulnerability detected" in report, "Issue message missing"

    print("✓ generate_report tests passed\n")


def test_pipe_escaping():
    """Test that pipe characters in messages are escaped."""
    print("Testing pipe character escaping...")

    issues = [
        {
            'severity': 'MAJOR',
            'message': 'Error: expected | got something else',
            'component': 'project:file.py',
            'line': 10
        }
    ]

    generator = MarkdownReportGenerator()
    result = generator.generate_issues_table(issues)
    has_escaped_pipe = '\\|' in result
    print(f"  Result contains escaped pipe: {has_escaped_pipe}")
    assert '\\|' in result, "Pipe character not escaped"

    print("✓ pipe_escaping test passed\n")


def test_format_analysis_date_invalid_format():
    """Test date formatting with invalid date format (error case)."""
    generator = MarkdownReportGenerator()

    # Test with invalid date format that will trigger ValueError
    invalid_date = "invalid-date-format"
    result = generator.format_analysis_date(invalid_date)

    # Should return the original string when parsing fails
    assert result == invalid_date


def test_format_analysis_date_russian():
    """Test date formatting with Russian language."""
    generator = MarkdownReportGenerator(language='ru')

    # Test with None (should use Russian translation)
    result = generator.format_analysis_date(None)
    assert result == "⚠️ Анализ недоступен"

    # Test with valid date
    date = "2024-01-15T12:00:00+0000"
    result = generator.format_analysis_date(date)
    assert "2024-01-15" in result


def test_generate_issues_table_russian():
    """Test issues table generation with Russian language."""
    generator = MarkdownReportGenerator(language='ru')

    # Test with empty issues
    result = generator.generate_issues_table([])
    assert "✅ Открытых проблем не найдено." in result

    # Test with issues
    issues = [
        {
            'severity': 'MAJOR',
            'message': 'Test issue',
            'component': 'project:file.py',
            'line': 42
        }
    ]
    result = generator.generate_issues_table(issues)
    assert "| 🔥 Важность | 💬 Сообщение | 🧩 Компонент | 📍 Строка |" in result


def test_generate_report_russian():
    """Test full report generation with Russian language."""
    generator = MarkdownReportGenerator(language='ru')

    projects_data = [
        {
            'project_key': 'test-project',
            'last_analysis': '2024-01-15T12:00:00+0000',
            'issues': []
        }
    ]

    report = generator.generate_report(projects_data)
    assert "# 📊 Отчёт анализа SonarQube" in report
    assert "🕒 Создано:" in report
    assert "📁 Проект:" in report


def test_markdown_report_generator_invalid_language():
    """Test MarkdownReportGenerator with invalid language defaults to English."""
    generator = MarkdownReportGenerator(language='invalid')

    # Should default to English
    assert generator.language == 'en'

    result = generator.format_analysis_date(None)
    assert result == "⚠️ No analysis available"


if __name__ == '__main__':
    print("=" * 60)
    print("Running SonarQube Checker Tests")
    print("=" * 60 + "\n")

    try:
        test_format_analysis_date()
        test_generate_issues_table()
        test_generate_report()
        test_pipe_escaping()

        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        sys.exit(0)

    except AssertionError as error:
        print(f"\n✗ Test failed: {error}")
        sys.exit(1)
