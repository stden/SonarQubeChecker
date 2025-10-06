# CLAUDE.md

Guidance for Claude Code when collaborating on SonarQubeChecker. Use `AGENTS.md` for the canonical contributor workflow; this file highlights AI-assistant specifics only.

## Quick Orientation
- Primary module: `sonarqube_checker.py` with `SonarQubeClient`, `MarkdownReportGenerator`, and `main()` wired through argparse and `.env` loading.
- Supporting assets: `demo.py` (mock output), `test_sonarqube_checker.py` (unit assertions), and Behave scenarios in `features/`.
- Runtime dependencies: maintained in `requirements.txt` (already includes `requests`, `python-dotenv`, `behave`).

## Preferred Workflow for Claude
1. Read `AGENTS.md` to understand coding style, testing order, and security expectations.
2. When planning changes, outline the impact on Markdown formatting so both unit tests and Behave tables stay in sync.
3. Run `python test_sonarqube_checker.py`, `behave features/`, and `python demo.py` before proposing edits; surface failures directly in the assistant response.
4. Reference existing helpers in `MarkdownReportGenerator` before adding new formatting utilities.
5. Keep diffs focused. If you touch multiple concerns, split responses or commits accordingly.

## Change-Specific Tips
- When adding API calls, reuse the session defined in `SonarQubeClient` to inherit auth and the 30 s timeout.
- Avoid duplicating documentation; link to `README.md` or `AGENTS.md` rather than restating instructions.
- Preserve Markdown escaping rules—pipes and other reserved characters must be sanitized before composing tables.
- For mock data, prefer concise fixtures inside tests; only create new files under `samples/` if they exceed a few lines.
- Follow core Python hygiene: keep functions pure when practical, embrace dependency injection for external services, raise specific exceptions rather than catching `Exception`, and favour explicit over implicit behaviour (e.g., no wildcard imports, descriptive variable names, context managers for file/network resources). Uphold DRY by centralising shared helpers (tests live in `tests/`, report formatting in `MarkdownReportGenerator`), apply SOLID principles when extending classes (prefer small, single-responsibility objects over monoliths), and keep patches aligned with KISS—avoid over-engineering and favour straightforward control flow that future maintainers can scan quickly.

## Review Checklist for Claude
- Tests executed and outcomes reported (unit + Behave + demo when formatting shifts).
- New dependencies appended to `requirements.txt` and mentioned in relevant docs.
- Secrets, tokens, and live URLs absent from logs, fixtures, and output.
- Pull request guidance in `AGENTS.md` still accurate after your change; update that file instead of repeating details here when process tweaks are needed.
