#!/usr/bin/env python3
"""
SonarQube Checker - A tool to fetch project analysis data and issues from SonarQube.

This script connects to a SonarQube instance, retrieves project analysis dates,
and fetches the latest open issues, then generates a Markdown report.
"""

import argparse
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from i18n import get_translation


class SonarQubeClient:
    """Client for interacting with SonarQube API."""

    def __init__(self, base_url: str, api_token: str):
        """
        Initialize the SonarQube client.

        Args:
            base_url: Base URL of the SonarQube instance (e.g., https://sonarqube.example.com)
            api_token: API token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(api_token, '')
        self.session = requests.Session()
        self.session.auth = self.auth

    def get_last_analysis_date(self, project_key: str) -> Optional[str]:
        """
        Fetch the last analysis date for a project.

        Args:
            project_key: The project key in SonarQube

        Returns:
            Last analysis date as a string, or None if not available
        """
        endpoint = f"{self.base_url}/api/project_analyses/search"
        params = {
            'project': project_key,
            'ps': 1  # Page size: limit to 1 (most recent)
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            analyses = data.get('analyses', [])
            if analyses:
                # Return the date of the most recent analysis
                return analyses[0].get('date')
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error fetching analysis date for {project_key}: {e}", file=sys.stderr)
            return None

    def get_latest_issues(self, project_key: str, max_issues: int = 10) -> List[Dict]:
        """
        Fetch the latest open issues for a project.

        Args:
            project_key: The project key in SonarQube
            max_issues: Maximum number of issues to retrieve (default: 10)

        Returns:
            List of issue dictionaries containing severity, message, component, and line
        """
        endpoint = f"{self.base_url}/api/issues/search"
        params = {
            'componentKeys': project_key,
            'statuses': 'OPEN,CONFIRMED',
            'ps': max_issues,  # Page size
            's': 'CREATION_DATE',  # Sort by creation date
            'asc': 'false'  # Descending order (newest first)
        }

        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            issues = []
            for issue in data.get('issues', []):
                issues.append({
                    'severity': issue.get('severity', 'N/A'),
                    'message': issue.get('message', 'N/A'),
                    'component': issue.get('component', 'N/A'),
                    'line': issue.get('line', 'N/A')
                })

            return issues

        except requests.exceptions.RequestException as e:
            print(f"Error fetching issues for {project_key}: {e}", file=sys.stderr)
            return []


class MarkdownReportGenerator:
    """Generator for Markdown reports with i18n support."""

    def __init__(self, language: str = 'en'):
        """
        Initialize the report generator with a specific language.

        Args:
            language: Language code ('en' or 'ru'), default: 'en'
        """
        self.language = language if language in ['en', 'ru'] else 'en'

    def format_analysis_date(self, date_str: Optional[str]) -> str:
        """
        Format the analysis date for display.

        Args:
            date_str: ISO format date string

        Returns:
            Formatted date string
        """
        if not date_str:
            return get_translation('no_analysis_available', self.language)

        try:
            # Parse ISO format date and format it nicely
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, AttributeError):
            return date_str

    def generate_issues_table(self, issues: List[Dict]) -> str:
        """
        Generate a Markdown table for issues.

        Args:
            issues: List of issue dictionaries

        Returns:
            Markdown formatted table as a string
        """
        if not issues:
            return get_translation('no_open_issues', self.language)

        # Create table header with translations
        severity_col = get_translation('severity', self.language)
        message_col = get_translation('message', self.language)
        component_col = get_translation('component', self.language)
        line_col = get_translation('line', self.language)

        table = f"| {severity_col} | {message_col} | {component_col} | {line_col} |\n"
        table += "|----------|---------|-----------|------|\n"

        # Add rows for each issue
        for issue in issues:
            severity = issue.get('severity', 'N/A')
            message = issue.get('message', 'N/A').replace('|', '\\|')  # Escape pipes
            component = issue.get('component', 'N/A').replace('|', '\\|')
            line = str(issue.get('line', 'N/A'))

            table += f"| {severity} | {message} | {component} | {line} |\n"

        return table

    def generate_report(self, projects_data: List[Dict]) -> str:
        """
        Generate a complete Markdown report.

        Args:
            projects_data: List of dictionaries containing project data
                          Each dict should have 'project_key', 'last_analysis', and 'issues'

        Returns:
            Complete Markdown report as a string
        """
        report_title = get_translation('report_title', self.language)
        generated_label = get_translation('generated', self.language)
        project_label = get_translation('project', self.language)
        last_analysis_label = get_translation('last_analysis', self.language)
        latest_issues_label = get_translation('latest_issues', self.language)

        report = f"# {report_title}\n\n"
        report += f"{generated_label}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "---\n\n"

        for project in projects_data:
            project_key = project.get('project_key', 'Unknown')
            last_analysis = project.get('last_analysis')
            issues = project.get('issues', [])

            report += f"## {project_label}: {project_key}\n\n"

            # Add last analysis date
            formatted_date = self.format_analysis_date(last_analysis)
            report += f"**{last_analysis_label}:** {formatted_date}\n\n"

            # Add issues section
            report += f"**{latest_issues_label}:**\n\n"
            report += self.generate_issues_table(issues)
            report += "\n\n---\n\n"

        return report


def main():
    """Main entry point for the SonarQube Checker tool."""
    # Load environment variables from .env file if it exists
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Fetch SonarQube project analysis data and generate a Markdown report.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1,project2
  %(prog)s --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1 --output report.md

  # Or use environment variables from .env file:
  %(prog)s
        """
    )

    parser.add_argument(
        '--url',
        default=os.getenv('SONARQUBE_URL'),
        help=(
            'SonarQube base URL (e.g., https://sonarqube.example.com). '
            'Can be set via SONARQUBE_URL environment variable.'
        ),
    )

    parser.add_argument(
        '--token',
        default=os.getenv('SONARQUBE_TOKEN'),
        help=(
            'SonarQube API token for authentication. '
            'Can be set via SONARQUBE_TOKEN environment variable.'
        ),
    )

    parser.add_argument(
        '--projects',
        default=os.getenv('SONARQUBE_PROJECTS'),
        help=(
            'Comma-separated list of project keys (e.g., project1,project2). '
            'Can be set via SONARQUBE_PROJECTS environment variable.'
        ),
    )

    parser.add_argument(
        '--max-issues',
        type=int,
        default=int(os.getenv('SONARQUBE_MAX_ISSUES', '10')),
        help=(
            'Maximum number of issues to fetch per project (default: 10). '
            'Can be set via SONARQUBE_MAX_ISSUES environment variable.'
        ),
    )

    parser.add_argument(
        '--output',
        help='Output file path (e.g., report.md). If not specified, prints to console.',
    )

    parser.add_argument(
        '--language',
        default=os.getenv('SONARQUBE_REPORT_LANGUAGE', 'en'),
        choices=['en', 'ru'],
        help=(
            'Report language (en or ru, default: en). '
            'Can be set via SONARQUBE_REPORT_LANGUAGE environment variable.'
        ),
    )

    args = parser.parse_args()

    # Validate required arguments
    if not args.url:
        print(
            "Error: --url is required (or set SONARQUBE_URL environment variable)",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.token:
        print(
            "Error: --token is required (or set SONARQUBE_TOKEN environment variable)",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.projects:
        print(
            "Error: --projects is required (or set SONARQUBE_PROJECTS environment variable)",
            file=sys.stderr,
        )
        sys.exit(1)

    # Parse project keys
    project_keys = [key.strip() for key in args.projects.split(',')]

    # Initialize SonarQube client
    client = SonarQubeClient(args.url, args.token)

    # Fetch data for each project
    projects_data = []
    for project_key in project_keys:
        print(f"Fetching data for project: {project_key}...", file=sys.stderr)

        last_analysis = client.get_last_analysis_date(project_key)
        issues = client.get_latest_issues(project_key, args.max_issues)

        projects_data.append({
            'project_key': project_key,
            'last_analysis': last_analysis,
            'issues': issues
        })

    # Generate Markdown report with selected language
    generator = MarkdownReportGenerator(language=args.language)
    report = generator.generate_report(projects_data)

    # Output the report
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.output}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report)


if __name__ == '__main__':
    main()
