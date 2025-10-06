# Repository Guidelines
## Project Structure & Module Organization
SonarQubeChecker is a small Python CLI; keep new modules colocated with the existing root package. `sonarqube_checker.py` hosts `SonarQubeClient` for HTTP access and `MarkdownReportGenerator` for formatting. `demo.py` provides an offline showcase of Markdown output—use it when adjusting the report layout. `test_sonarqube_checker.py` contains self-contained regression checks, and `requirements.txt` tracks runtime dependencies. Place additional fixtures or resources under a `samples/` directory if they grow beyond a few lines.

## Build, Test, and Development Commands
Create a virtual environment before editing: `python -m venv .venv && source .venv/bin/activate`. Install dependencies with `pip install -r requirements.txt`. Run the CLI with `python sonarqube_checker.py --url https://... --token <token> --projects app1,app2 [--output report.md]`. Use `python demo.py` to inspect formatted Markdown without hitting SonarQube. Execute `python test_sonarqube_checker.py` prior to commits; the script exits non-zero on any regression.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation and snake_case for functions, PascalCase for classes, mirroring the current modules. Maintain type hints for public APIs and include concise docstrings as seen throughout the repository. Prefer small, pure functions and reuse `MarkdownReportGenerator` helpers when extending reporting. Escape Markdown-sensitive characters when adding new table content.

## Testing Guidelines
Extend the existing test script with additional `test_*` functions and representative payloads. Use built-in `assert` statements and print sample output only when it clarifies failures. Cover edge cases such as empty issue lists, malformed timestamps, and network exceptions by mocking response data. Run the demo after altering formatting to ensure alignment with expected user-facing output.

## Commit & Pull Request Guidelines
Commits should mirror the short, descriptive tone in history (`Initial commit`, `Key Requirements:`) while staying imperative, e.g., `Add retry for issue fetch`. Group related changes into a single commit and include follow-up details in the body if needed. Pull requests must outline purpose, testing steps, and any screenshots or report excerpts affected by the change. Link GitHub issues with `Fixes #123` where relevant and confirm no secrets or tokens appear in diffs.

## Security & Configuration Tips
Store SonarQube tokens outside the repository; pass them via CLI arguments or environment variables. Avoid logging full URLs with credentials and redact sensitive fields before sharing output. When introducing new HTTP calls, reuse the configured session to inherit auth and timeouts.
