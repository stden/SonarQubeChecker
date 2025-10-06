#!/usr/bin/env python3
"""
SonarQube Checker Script

This script connects to a SonarQube server via its Web API to monitor specified projects.
It retrieves the date of the last analysis for each project, fetches the latest open issues
(errors and warnings), and generates a Markdown-formatted report.
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import requests
from requests.auth import HTTPBasicAuth


class SonarQubeChecker:
    """Class to interact with SonarQube API and generate reports."""
    
    def __init__(self, base_url: str, token: str):
        """
        Initialize the SonarQube checker.
        
        Args:
            base_url: SonarQube server URL (e.g., 'https://sonarqube.example.com')
            token: API token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(token, '')
        self.session = requests.Session()
        self.session.auth = self.auth
        
    def get_projects(self) -> List[Dict]:
        """
        Retrieve list of all projects from SonarQube.
        
        Returns:
            List of project dictionaries
        """
        url = f"{self.base_url}/api/projects/search"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('components', [])
    
    def get_project_analysis_date(self, project_key: str) -> Optional[str]:
        """
        Get the date of the last analysis for a project.
        
        Args:
            project_key: The project key
            
        Returns:
            Last analysis date as a string or None if not available
        """
        url = f"{self.base_url}/api/project_analyses/search"
        params = {'project': project_key, 'ps': 1}
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        analyses = data.get('analyses', [])
        if analyses:
            # Parse and format the date
            date_str = analyses[0].get('date')
            if date_str:
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
                except ValueError:
                    return date_str
        return None
    
    def get_project_issues(self, project_key: str) -> Dict[str, List[Dict]]:
        """
        Fetch the latest open issues (errors and warnings) for a project.
        
        Args:
            project_key: The project key
            
        Returns:
            Dictionary with 'errors' and 'warnings' lists
        """
        issues = {'errors': [], 'warnings': []}
        
        # Fetch bugs and vulnerabilities (errors)
        for severity in ['BLOCKER', 'CRITICAL', 'MAJOR']:
            url = f"{self.base_url}/api/issues/search"
            params = {
                'componentKeys': project_key,
                'severities': severity,
                'statuses': 'OPEN,CONFIRMED,REOPENED',
                'ps': 100  # Page size
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            for issue in data.get('issues', []):
                issue_info = {
                    'severity': issue.get('severity'),
                    'type': issue.get('type'),
                    'message': issue.get('message'),
                    'component': issue.get('component'),
                    'line': issue.get('line'),
                    'rule': issue.get('rule')
                }
                
                if severity in ['BLOCKER', 'CRITICAL']:
                    issues['errors'].append(issue_info)
                else:
                    issues['warnings'].append(issue_info)
        
        # Fetch minor issues (warnings)
        url = f"{self.base_url}/api/issues/search"
        params = {
            'componentKeys': project_key,
            'severities': 'MINOR',
            'statuses': 'OPEN,CONFIRMED,REOPENED',
            'ps': 100
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        for issue in data.get('issues', []):
            issue_info = {
                'severity': issue.get('severity'),
                'type': issue.get('type'),
                'message': issue.get('message'),
                'component': issue.get('component'),
                'line': issue.get('line'),
                'rule': issue.get('rule')
            }
            issues['warnings'].append(issue_info)
        
        return issues
    
    def generate_markdown_report(self, project_keys: Optional[List[str]] = None) -> str:
        """
        Generate a Markdown report for specified projects.
        
        Args:
            project_keys: List of project keys to include. If None, includes all projects.
            
        Returns:
            Markdown-formatted report as a string
        """
        report_lines = [
            "# SonarQube Analysis Report",
            "",
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Get projects to report on
        if project_keys is None:
            projects = self.get_projects()
            project_keys = [p['key'] for p in projects]
        
        # Generate report for each project
        for project_key in project_keys:
            try:
                report_lines.append(f"## Project: {project_key}")
                report_lines.append("")
                
                # Get last analysis date
                analysis_date = self.get_project_analysis_date(project_key)
                if analysis_date:
                    report_lines.append(f"**Last Analysis:** {analysis_date}")
                else:
                    report_lines.append("**Last Analysis:** Not available")
                report_lines.append("")
                
                # Get issues
                issues = self.get_project_issues(project_key)
                
                # Report errors
                errors = issues['errors']
                report_lines.append(f"### Errors: {len(errors)}")
                report_lines.append("")
                
                if errors:
                    for idx, error in enumerate(errors[:20], 1):  # Limit to first 20
                        component = error['component'].split(':')[-1] if error['component'] else 'N/A'
                        line = f" (Line {error['line']})" if error.get('line') else ""
                        report_lines.append(f"{idx}. **[{error['severity']}]** {error['message']}")
                        report_lines.append(f"   - File: `{component}`{line}")
                        report_lines.append(f"   - Rule: `{error['rule']}`")
                        report_lines.append("")
                    
                    if len(errors) > 20:
                        report_lines.append(f"_...and {len(errors) - 20} more errors_")
                        report_lines.append("")
                else:
                    report_lines.append("No errors found.")
                    report_lines.append("")
                
                # Report warnings
                warnings = issues['warnings']
                report_lines.append(f"### Warnings: {len(warnings)}")
                report_lines.append("")
                
                if warnings:
                    for idx, warning in enumerate(warnings[:20], 1):  # Limit to first 20
                        component = warning['component'].split(':')[-1] if warning['component'] else 'N/A'
                        line = f" (Line {warning['line']})" if warning.get('line') else ""
                        report_lines.append(f"{idx}. **[{warning['severity']}]** {warning['message']}")
                        report_lines.append(f"   - File: `{component}`{line}")
                        report_lines.append(f"   - Rule: `{warning['rule']}`")
                        report_lines.append("")
                    
                    if len(warnings) > 20:
                        report_lines.append(f"_...and {len(warnings) - 20} more warnings_")
                        report_lines.append("")
                else:
                    report_lines.append("No warnings found.")
                    report_lines.append("")
                
                report_lines.append("---")
                report_lines.append("")
                
            except Exception as e:
                report_lines.append(f"Error processing project {project_key}: {str(e)}")
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")
        
        return "\n".join(report_lines)


def main():
    """Main entry point for the script."""
    # Get configuration from environment variables
    sonarqube_url = os.getenv('SONARQUBE_URL')
    sonarqube_token = os.getenv('SONARQUBE_TOKEN')
    project_keys_str = os.getenv('SONARQUBE_PROJECTS', '')
    output_file = os.getenv('OUTPUT_FILE', 'sonarqube_report.md')
    
    # Validate configuration
    if not sonarqube_url:
        print("Error: SONARQUBE_URL environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    if not sonarqube_token:
        print("Error: SONARQUBE_TOKEN environment variable is required", file=sys.stderr)
        sys.exit(1)
    
    # Parse project keys if provided
    project_keys = None
    if project_keys_str:
        project_keys = [key.strip() for key in project_keys_str.split(',') if key.strip()]
    
    try:
        # Initialize checker
        checker = SonarQubeChecker(sonarqube_url, sonarqube_token)
        
        # Generate report
        print(f"Generating SonarQube report...")
        if project_keys:
            print(f"Projects to analyze: {', '.join(project_keys)}")
        else:
            print("Analyzing all projects...")
        
        report = checker.generate_markdown_report(project_keys)
        
        # Save report to file
        with open(output_file, 'w') as f:
            f.write(report)
        
        print(f"Report successfully generated: {output_file}")
        
        # Also print to stdout
        print("\n" + "=" * 80)
        print(report)
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to SonarQube: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
