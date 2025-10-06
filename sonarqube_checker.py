#!/usr/bin/env python3
"""
SonarQube Checker - A tool to fetch project analysis data and issues from SonarQube.

This script connects to a SonarQube instance, retrieves project analysis dates,
and fetches the latest open issues, then generates a Markdown report.
"""

import argparse
import sys
from datetime import datetime
from typing import List, Dict, Optional
import requests
from requests.auth import HTTPBasicAuth


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
    """Generator for Markdown reports."""
    
    @staticmethod
    def format_analysis_date(date_str: Optional[str]) -> str:
        """
        Format the analysis date for display.
        
        Args:
            date_str: ISO format date string
            
        Returns:
            Formatted date string
        """
        if not date_str:
            return "No analysis available"
        
        try:
            # Parse ISO format date and format it nicely
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        except (ValueError, AttributeError):
            return date_str
    
    @staticmethod
    def generate_issues_table(issues: List[Dict]) -> str:
        """
        Generate a Markdown table for issues.
        
        Args:
            issues: List of issue dictionaries
            
        Returns:
            Markdown formatted table as a string
        """
        if not issues:
            return "No open issues found."
        
        # Create table header
        table = "| Severity | Message | Component | Line |\n"
        table += "|----------|---------|-----------|------|\n"
        
        # Add rows for each issue
        for issue in issues:
            severity = issue.get('severity', 'N/A')
            message = issue.get('message', 'N/A').replace('|', '\\|')  # Escape pipes
            component = issue.get('component', 'N/A').replace('|', '\\|')
            line = str(issue.get('line', 'N/A'))
            
            table += f"| {severity} | {message} | {component} | {line} |\n"
        
        return table
    
    @staticmethod
    def generate_report(projects_data: List[Dict]) -> str:
        """
        Generate a complete Markdown report.
        
        Args:
            projects_data: List of dictionaries containing project data
                          Each dict should have 'project_key', 'last_analysis', and 'issues'
            
        Returns:
            Complete Markdown report as a string
        """
        report = "# SonarQube Analysis Report\n\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "---\n\n"
        
        for project in projects_data:
            project_key = project.get('project_key', 'Unknown')
            last_analysis = project.get('last_analysis')
            issues = project.get('issues', [])
            
            report += f"## Project: {project_key}\n\n"
            
            # Add last analysis date
            formatted_date = MarkdownReportGenerator.format_analysis_date(last_analysis)
            report += f"**Last Analysis:** {formatted_date}\n\n"
            
            # Add issues section
            report += "**Latest Issues:**\n\n"
            report += MarkdownReportGenerator.generate_issues_table(issues)
            report += "\n\n---\n\n"
        
        return report


def main():
    """Main entry point for the SonarQube Checker tool."""
    parser = argparse.ArgumentParser(
        description='Fetch SonarQube project analysis data and generate a Markdown report.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1,project2
  %(prog)s --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1 --output report.md
        """
    )
    
    parser.add_argument(
        '--url',
        required=True,
        help='SonarQube base URL (e.g., https://sonarqube.example.com)'
    )
    
    parser.add_argument(
        '--token',
        required=True,
        help='SonarQube API token for authentication'
    )
    
    parser.add_argument(
        '--projects',
        required=True,
        help='Comma-separated list of project keys (e.g., project1,project2)'
    )
    
    parser.add_argument(
        '--max-issues',
        type=int,
        default=10,
        help='Maximum number of issues to fetch per project (default: 10)'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (e.g., report.md). If not specified, prints to console.'
    )
    
    args = parser.parse_args()
    
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
    
    # Generate Markdown report
    report = MarkdownReportGenerator.generate_report(projects_data)
    
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
