#!/usr/bin/env python3
"""
Test script for SonarQube Checker functionality.
This tests the core functions without requiring a live SonarQube instance.
"""

import sys
import os

# Add the parent directory to the path to import sonarqube_checker
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sonarqube_checker import MarkdownReportGenerator


def test_format_analysis_date():
    """Test date formatting function."""
    print("Testing format_analysis_date...")
    
    # Test with valid ISO date
    date1 = "2024-01-15T12:00:00+0000"
    result1 = MarkdownReportGenerator.format_analysis_date(date1)
    print(f"  Input: {date1}")
    print(f"  Output: {result1}")
    assert "2024-01-15" in result1, "Date formatting failed"
    
    # Test with None
    result2 = MarkdownReportGenerator.format_analysis_date(None)
    print(f"  Input: None")
    print(f"  Output: {result2}")
    assert result2 == "No analysis available", "None handling failed"
    
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
    
    result = MarkdownReportGenerator.generate_issues_table(issues)
    print(f"  Generated table:\n{result}")
    assert "| Severity | Message | Component | Line |" in result, "Table header missing"
    assert "MAJOR" in result, "Issue severity missing"
    assert "Remove unused variable" in result, "Issue message missing"
    
    # Test with empty issues
    result_empty = MarkdownReportGenerator.generate_issues_table([])
    print(f"  Empty issues result: {result_empty}")
    assert "No open issues found" in result_empty, "Empty issues handling failed"
    
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
    
    report = MarkdownReportGenerator.generate_report(projects_data)
    print(f"  Generated report (first 500 chars):\n{report[:500]}...")
    
    assert "# SonarQube Analysis Report" in report, "Report title missing"
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
    
    result = MarkdownReportGenerator.generate_issues_table(issues)
    print(f"  Result contains escaped pipe: {'\\|' in result}")
    assert '\\|' in result, "Pipe character not escaped"
    
    print("✓ pipe_escaping test passed\n")


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
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
