#!/usr/bin/env python3
"""Tests for the CLI entry point of sonarqube_checker."""

import contextlib
import io
import runpy
import sys
from unittest.mock import MagicMock

import pytest

import sonarqube_checker


@pytest.fixture(autouse=True)
def reset_env(monkeypatch):
    """Ensure environment variables used by argparse defaults do not leak between tests."""
    for env_var in [
        'SONARQUBE_URL',
        'SONARQUBE_TOKEN',
        'SONARQUBE_PROJECTS',
        'SONARQUBE_MAX_ISSUES',
        'SONARQUBE_REPORT_LANGUAGE',
    ]:
        monkeypatch.delenv(env_var, raising=False)


def _run_main(argv, monkeypatch):
    """Helper to execute main() with patched argv and captured I/O."""
    monkeypatch.setattr(sys, 'argv', argv)
    monkeypatch.setattr(sonarqube_checker, 'load_dotenv', lambda: None)
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        sonarqube_checker.main()
    return stdout.getvalue(), stderr.getvalue()


def test_main_prints_russian_report(monkeypatch):
    """Running the CLI with Russian language prints translated report text."""
    mock_client = MagicMock()
    mock_client.get_last_analysis_date.return_value = '2024-02-01T00:00:00+0000'
    mock_client.get_latest_issues.return_value = [
        {
            'severity': 'MAJOR',
            'message': 'Issue details',
            'component': 'project:file.py',
            'line': 12,
        }
    ]
    monkeypatch.setattr(sonarqube_checker, 'SonarQubeClient', MagicMock(return_value=mock_client))

    stdout, stderr = _run_main(
        [
            'sonarqube_checker.py',
            '--url', 'https://example.com',
            '--token', 'token',
            '--projects', 'project-key',
            '--language', 'ru',
        ],
        monkeypatch,
    )

    assert 'Отчёт анализа SonarQube' in stdout
    assert 'project-key' in stdout
    assert 'Fetching data for project: project-key' in stderr


def test_main_writes_output_file(monkeypatch, tmp_path):
    """CLI should write the report to a file when --output is provided."""
    mock_client = MagicMock()
    mock_client.get_last_analysis_date.return_value = '2024-02-01T00:00:00+0000'
    mock_client.get_latest_issues.return_value = []
    monkeypatch.setattr(sonarqube_checker, 'SonarQubeClient', MagicMock(return_value=mock_client))

    output_path = tmp_path / 'report.md'
    stdout, stderr = _run_main(
        [
            'sonarqube_checker.py',
            '--url', 'https://example.com',
            '--token', 'token',
            '--projects', 'project-key',
            '--output', str(output_path),
        ],
        monkeypatch,
    )

    assert stdout == ''
    assert f'Report saved to: {output_path}' in stderr
    file_contents = output_path.read_text(encoding='utf-8')
    assert file_contents.startswith('# 📊 SonarQube Analysis Report')


def test_main_handles_file_write_error(monkeypatch, tmp_path):
    """If writing fails the CLI should exit with an informative error."""
    mock_client = MagicMock()
    mock_client.get_last_analysis_date.return_value = None
    mock_client.get_latest_issues.return_value = []
    monkeypatch.setattr(sonarqube_checker, 'SonarQubeClient', MagicMock(return_value=mock_client))

    impossible_path = tmp_path / 'dir' / 'report.md'

    monkeypatch.setattr(sys, 'argv', [
        'sonarqube_checker.py',
        '--url', 'https://example.com',
        '--token', 'token',
        '--projects', 'project-key',
        '--output', str(impossible_path),
    ])

    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        with pytest.raises(SystemExit) as exc:
            sonarqube_checker.main()

    assert exc.value.code == 1
    assert 'Error writing to file' in stderr.getvalue()


@pytest.mark.parametrize(
    'missing_flag, expected_message',
    [
        ('--url', 'Error: --url is required'),
        ('--token', 'Error: --token is required'),
        ('--projects', 'Error: Either --projects or --project-pattern is required'),
    ],
)
def test_main_missing_required_arguments(monkeypatch, missing_flag, expected_message):
    """Missing required arguments should exit with code 1 and helpful error."""
    argv = ['sonarqube_checker.py', '--url', 'https://example.com', '--token', 'token', '--projects', 'proj']
    # Remove the selected flag and its value (if any)
    if missing_flag == '--url':
        argv = ['sonarqube_checker.py', '--token', 'token', '--projects', 'proj']
    elif missing_flag == '--token':
        argv = ['sonarqube_checker.py', '--url', 'https://example.com', '--projects', 'proj']
    elif missing_flag == '--projects':
        argv = ['sonarqube_checker.py', '--url', 'https://example.com', '--token', 'token']

    monkeypatch.setattr(sys, 'argv', argv)
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        monkeypatch.setattr(sonarqube_checker, 'load_dotenv', lambda: None)
        with pytest.raises(SystemExit) as exc:
            sonarqube_checker.main()

    assert exc.value.code == 1
    assert expected_message in stderr.getvalue()


def test_module_entrypoint_calls_main(monkeypatch, capsys):
    """Running the module via runpy executes main() without hitting the network."""

    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):  # pragma: no cover - nothing to do
            return None

        def json(self):
            return self._payload

    class DummySession:
        def __init__(self):
            self.auth = None

        def get(self, endpoint, params=None, timeout=30):
            if 'project_analyses' in endpoint:
                return DummyResponse({'analyses': [{'date': '2024-01-01T00:00:00+0000'}]})
            return DummyResponse({'issues': []})

    monkeypatch.setattr('requests.Session', lambda: DummySession())
    monkeypatch.setattr('dotenv.load_dotenv', lambda *args, **kwargs: None)
    monkeypatch.setenv('SONARQUBE_URL', 'https://example.com')
    monkeypatch.setenv('SONARQUBE_TOKEN', 'token')
    monkeypatch.setenv('SONARQUBE_PROJECTS', 'projX')
    monkeypatch.setenv('SONARQUBE_MAX_ISSUES', '5')
    monkeypatch.setenv('SONARQUBE_REPORT_LANGUAGE', 'en')
    monkeypatch.setattr(sys, 'argv', ['sonarqube_checker.py'])

    runpy.run_module('sonarqube_checker', run_name='__main__')

    captured = capsys.readouterr()
    assert 'projX' in captured.out
    assert '📅 Last Analysis' in captured.out
