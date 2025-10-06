"""Behave step definitions for testing Markdown report generation."""

# pylint: disable=missing-function-docstring, not-callable

import sys
from pathlib import Path

from behave import given, then, when

# Ensure the project root is on sys.path so we can import the application module.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sonarqube_checker import MarkdownReportGenerator  # noqa: E402


@given('the analysis date "{raw_date}"')
def step_given_analysis_date(context, raw_date):
    """Store the raw analysis date from the scenario outline."""
    context.analysis_date = None if raw_date == "None" else raw_date


@when('I format the analysis date')
def step_when_format_date(context):
    generator = MarkdownReportGenerator()
    context.formatted_date = generator.format_analysis_date(context.analysis_date)


@then('the formatted result should be "{expected}"')
def step_then_formatted_result(context, expected):
    assert context.formatted_date == expected, (
        f"Expected formatted date '{expected}' but got '{context.formatted_date}'"
    )


@given('the following issues:')
def step_given_issues(context):
    context.issues = []
    for row in context.table:
        issue = {
            'severity': row['severity'],
            'message': row['message'],
            'component': row['component'],
        }
        line_value = row.get('line', '').strip()
        if not line_value:
            issue['line'] = 'N/A'
        else:
            try:
                issue['line'] = int(line_value)
            except ValueError:
                issue['line'] = line_value
        context.issues.append(issue)


@given('no issues')
def step_given_no_issues(context):
    context.issues = []


@when('I build the issues table')
def step_when_build_table(context):
    generator = MarkdownReportGenerator()
    context.issues_table = generator.generate_issues_table(context.issues)


@then('the table should be "{expected}"')
def step_then_table_equals(context, expected):
    assert context.issues_table == expected, (
        f"Expected table '{expected}' but got '{context.issues_table}'"
    )


@then('the table should include the header')
def step_then_table_has_header(context):
    header = "| Severity | Message | Component | Line |"
    assert header in context.issues_table, "Table header is missing"


@then('the table should include the issue row "{severity}" "{message}" "{component}" "{line}"')
def step_then_table_has_row(context, severity, message, component, line):
    expected_row = f"| {severity} | {message} | {component} | {line} |"
    assert expected_row in context.issues_table, (
        f"Expected row '{expected_row}' not found in table:\n{context.issues_table}"
    )


@then('the table should contain the escaped pipe character')
def step_then_table_has_escaped_pipe(context):
    assert "\\|" in context.issues_table, "Escaped pipe character not found in table"
