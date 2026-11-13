# TESTING_CHECKLIST_PYTHON.md

## Before merge
- [ ] `pytest -q`
- [ ] Formatter check passes (`black --check` or project equivalent)
- [ ] Linter passes (`ruff`/`flake8`/project equivalent)
- [ ] Type checks run where configured (`mypy`/pyright)
- [ ] New logic has tests
- [ ] Bug fixes include regression tests
- [ ] DB / API boundaries covered by integration tests where relevant
- [ ] No flaky sleeps or timing hacks in tests

## Python-specific best practices
- [ ] Use `pytest.mark.parametrize` for input variants
- [ ] Prefer fixtures over giant inline setup blocks
- [ ] Mock external APIs, not your own business logic
- [ ] Keep unit tests isolated from real network/DB/filesystem
- [ ] Use temp paths / monkeypatch for env and file tests
- [ ] Assert behavior and outputs, not implementation internals
- [ ] Cover exceptions and edge cases explicitly
- [ ] Avoid hidden global state between tests

## CI minimum
- [ ] format
- [ ] lint
- [ ] unit tests
- [ ] integration tests for critical flows
