#!/usr/bin/env python3
"""
Demo script showing SonarQube Checker output with mock data.
This demonstrates what the report looks like without requiring a live SonarQube instance.
"""

from sonarqube_checker import MarkdownReportGenerator


def demo_report():
    """Generate a demo report with sample data."""

    # Sample project data
    projects_data = [
        {
            'project_key': 'my-web-app',
            'last_analysis': '2024-01-15T14:30:00+0000',
            'issues': [
                {
                    'severity': 'CRITICAL',
                    'message': 'SQL injection vulnerability detected',
                    'component': 'my-web-app:src/database/queries.py',
                    'line': 45
                },
                {
                    'severity': 'MAJOR',
                    'message': 'Remove this unused import',
                    'component': 'my-web-app:src/utils/helpers.py',
                    'line': 3
                },
                {
                    'severity': 'MAJOR',
                    'message': 'Refactor this function to reduce its Cognitive Complexity',
                    'component': 'my-web-app:src/services/processor.py',
                    'line': 128
                },
                {
                    'severity': 'MINOR',
                    'message': 'Add a docstring to this function',
                    'component': 'my-web-app:src/utils/validators.py',
                    'line': 22
                }
            ]
        },
        {
            'project_key': 'api-backend',
            'last_analysis': '2024-01-14T09:15:00+0000',
            'issues': [
                {
                    'severity': 'BLOCKER',
                    'message': (
                        'Make sure this weak hash algorithm is not used in a sensitive context'
                    ),
                    'component': 'api-backend:src/auth/password.py',
                    'line': 67
                },
                {
                    'severity': 'MAJOR',
                    'message': 'Extract this nested conditional into a separate method',
                    'component': 'api-backend:src/controllers/user_controller.py',
                    'line': 156
                },
                {
                    'severity': 'INFO',
                    'message': 'This branch duplicates the one on line 89',
                    'component': 'api-backend:src/validators/input.py',
                    'line': 92
                }
            ]
        },
        {
            'project_key': 'mobile-app',
            'last_analysis': None,
            'issues': []
        }
    ]

    # Generate the report
    generator = MarkdownReportGenerator()
    return generator.generate_report(projects_data)


if __name__ == '__main__':
    print("Generating demo SonarQube report...\n")
    print("=" * 80)
    report_text = demo_report()
    print(report_text)
    print("=" * 80)
    print("\nDemo completed! This shows the format of a real report.")
