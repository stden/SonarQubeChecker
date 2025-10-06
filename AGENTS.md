# Repository Guidelines
## Project Structure & Module Organization
Core logic lives in `sonarqube_checker.py`, pairing `SonarQubeClient` for HTTP access with `MarkdownReportGenerator` for formatting. `demo.py` renders canned output for quick visual checks. Tests are split between the lightweight assertions in `test_sonarqube_checker.py` and Behave scenarios under `features/`. Track new runtime dependencies in `requirements.txt`, and place sizeable fixtures in a sibling `samples/` directory to keep modules tidy.

## Build, Test, and Development Commands
Create a virtual environment (`python -m venv .venv && source .venv/bin/activate`) and install requirements with `pip install -r requirements.txt`. Behave is already listed, so no extra install step is needed. Use `.env` (see `.env.example`) or CLI flags when running the checker; refer to `README.md` for full argument descriptions. For local validation run `python test_sonarqube_checker.py`, `behave features/`, and `python demo.py` in that order when formatting changes occur.

## Coding Style & Naming Conventions
Follow PEP 8 with four-space indentation, snake_case for functions, PascalCase for classes, and type hints on public helpers. Keep docstrings short and purposeful, mirroring the current modules. When extending reporting, prefer extracting reusable helpers inside `MarkdownReportGenerator` and always escape Markdown-reserved characters before adding user-supplied text to tables.

## Testing Guidelines
Augment `test_sonarqube_checker.py` with focused `test_*` functions that exercise new branches and regression cases (empty data, malformed timestamps, rare severity labels). Expand Behave tables when Markdown layout expectations shift so downstream tooling highlights diffs. Demo output should remain human-friendly—compare it before and after changes whenever headings, separators, or column order moves.

## Commit & Pull Request Guidelines
Use imperative, sub-60 character summaries (e.g., `Add retry for issue fetch`) and group related edits in a single commit. PRs should describe intent, list verification commands run, and attach updated report snippets or screenshots when presentation changes. Reference tracked issues with `Fixes #123` and double-check that secrets or SonarQube tokens never appear in diffs.

## Security & Configuration Tips
Store credentials outside the repo—either via environment variables or shell prompts. Avoid logging sensitive tokens or full URLs; redact them before sharing debug traces. Reuse the shared `requests.Session` so new HTTP calls inherit authentication and the 30-second timeout unless tighter bounds are justified.
