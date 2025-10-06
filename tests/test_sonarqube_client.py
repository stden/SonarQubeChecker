#!/usr/bin/env python3
"""
Tests for SonarQubeClient API interactions.
Uses mocking to avoid real API calls.
"""

import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pytest
import requests

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sonarqube_checker import SonarQubeClient


class TestSonarQubeClientBasics:
    """Test SonarQubeClient class."""

    def test_init(self):
        """Test client initialization."""
        client = SonarQubeClient('https://sonarqube.example.com', 'test_token')
        assert client.base_url == 'https://sonarqube.example.com'
        assert client.auth.username == 'test_token'
        assert client.auth.password == ''

    def test_init_strips_trailing_slash(self):
        """Test that trailing slash is removed from base URL."""
        client = SonarQubeClient('https://sonarqube.example.com/', 'test_token')
        assert client.base_url == 'https://sonarqube.example.com'

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_last_analysis_date_success(self, mock_get):
        """Test successful retrieval of last analysis date."""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'analyses': [
                {'date': '2024-01-15T12:00:00+0000'}
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_last_analysis_date('test-project')

        assert result == '2024-01-15T12:00:00+0000'
        mock_get.assert_called_once()

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_last_analysis_date_no_analyses(self, mock_get):
        """Test when no analyses are available."""
        mock_response = Mock()
        mock_response.json.return_value = {'analyses': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_last_analysis_date('test-project')

        assert result is None

    def test_get_last_analysis_date_error(self):
        """Test error handling for analysis date retrieval."""
        client = SonarQubeClient('https://sonarqube.example.com', 'token')

        # Mock the session.get to raise an exception
        with patch.object(client.session, 'get', side_effect=requests.exceptions.RequestException('Network error')):
            result = client.get_last_analysis_date('test-project')

        assert result is None

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_latest_issues_success(self, mock_get):
        """Test successful retrieval of issues."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'issues': [
                {
                    'severity': 'MAJOR',
                    'message': 'Test issue',
                    'component': 'test:file.py',
                    'line': 42
                },
                {
                    'severity': 'MINOR',
                    'message': 'Another issue',
                    'component': 'test:other.py',
                    'line': 10
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_latest_issues('test-project', max_issues=10)

        assert len(result) == 2
        assert result[0]['severity'] == 'MAJOR'
        assert result[0]['message'] == 'Test issue'
        assert result[1]['line'] == 10

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_latest_issues_no_issues(self, mock_get):
        """Test when no issues are found."""
        mock_response = Mock()
        mock_response.json.return_value = {'issues': []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_latest_issues('test-project')

        assert result == []

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_latest_issues_missing_fields(self, mock_get):
        """Test handling of issues with missing fields."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'issues': [
                {
                    'severity': 'MAJOR'
                    # Missing message, component, line
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_latest_issues('test-project')

        assert len(result) == 1
        assert result[0]['severity'] == 'MAJOR'
        assert result[0]['message'] == 'N/A'
        assert result[0]['component'] == 'N/A'
        assert result[0]['line'] == 'N/A'

    def test_get_latest_issues_error(self):
        """Test error handling for issues retrieval."""
        client = SonarQubeClient('https://sonarqube.example.com', 'token')

        # Mock the session.get to raise an exception
        with patch.object(client.session, 'get', side_effect=requests.exceptions.RequestException('Network error')):
            result = client.get_latest_issues('test-project')

        assert result == []


class TestSonarQubeClientProjectDiscovery:
    """Test project discovery and filtering functionality."""

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_projects_success(self, mock_get):
        """Test successful retrieval of all projects in single page."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'components': [
                {'key': 'project1'},
                {'key': 'project2'},
                {'key': 'MyProject.service'}
            ],
            'paging': {'total': 3}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_projects()

        assert len(result) == 3
        assert 'project1' in result
        assert 'project2' in result
        assert 'MyProject.service' in result

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_projects_with_pattern(self, mock_get):
        """Test project filtering with RegExp pattern."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'components': [
                {'key': 'project1'},
                {'key': 'MyProject.service'},
                {'key': 'MyProject.api'},
                {'key': 'OtherProject.app'}
            ],
            'paging': {'total': 4}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_projects(pattern=r'MyProject\.')

        assert len(result) == 2
        assert 'MyProject.service' in result
        assert 'MyProject.api' in result
        assert 'project1' not in result
        assert 'OtherProject.app' not in result

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_projects_no_matches(self, mock_get):
        """Test when no projects match the pattern."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'components': [
                {'key': 'project1'},
                {'key': 'project2'}
            ],
            'paging': {'total': 2}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_projects(pattern=r'NonExistent\.')

        assert result == []

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_projects_empty_response(self, mock_get):
        """Test when SonarQube returns no projects."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'components': [],
            'paging': {'total': 0}
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_projects()

        assert result == []

    def test_get_projects_error(self):
        """Test error handling for project retrieval."""
        client = SonarQubeClient('https://sonarqube.example.com', 'token')

        # Mock the session.get to raise an exception
        with patch.object(client.session, 'get', side_effect=requests.exceptions.RequestException('Network error')):
            result = client.get_projects()

        assert result == []

    @patch('sonarqube_checker.requests.Session.get')
    def test_get_projects_pagination(self, mock_get):
        """Test that pagination works correctly."""
        # Simulate multiple pages
        responses = []
        for i in range(3):
            mock_resp = Mock()
            mock_resp.json.return_value = {
                'components': [{'key': f'project{i*100 + j}'} for j in range(100)],
                'paging': {'total': 250}
            }
            mock_resp.raise_for_status = Mock()
            responses.append(mock_resp)

        mock_get.side_effect = responses

        client = SonarQubeClient('https://sonarqube.example.com', 'token')
        result = client.get_projects()

        # Should have made 3 requests (300 projects total, which is > 250 total)
        assert mock_get.call_count == 3
        assert len(result) == 300


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
