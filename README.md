# SonarQubeChecker

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=example_project&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=example_project)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=example_project&metric=bugs)](https://sonarcloud.io/summary/new_code?id=example_project)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=example_project&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=example_project)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=example_project&metric=coverage)](https://sonarcloud.io/summary/new_code?id=example_project)

🐍 Python CLI tool to fetch SonarQube analysis data and issues, generating Markdown reports. Supports bilingual reports 🇬🇧 English / 🇷🇺 Russian.

## 📦 Installation

```bash
git clone https://github.com/stden/SonarQubeChecker.git
cd SonarQubeChecker

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies from pyproject.toml
uv sync

# Configure credentials
cp .env.example .env
# Edit .env with your SonarQube URL, token, and projects
```

## 🚀 Usage

```bash
# Using .env configuration
python sonarqube_checker.py
python sonarqube_checker.py --output report.md

# Using CLI arguments
python sonarqube_checker.py --url https://sonarcloud.io --token TOKEN --projects proj1,proj2

# Russian report
python sonarqube_checker.py --language ru --output отчёт.md
```

## ⚙️ Configuration

| Option | Env Variable | Default | Description |
|--------|--------------|---------|-------------|
| `--url` | `SONARQUBE_URL` | - | 🔗 SonarQube server URL |
| `--token` | `SONARQUBE_TOKEN` | - | 🔑 API authentication token |
| `--projects` | `SONARQUBE_PROJECTS` | - | 📂 Project keys (comma-separated) |
| `--max-issues` | `SONARQUBE_MAX_ISSUES` | `10` | 🔢 Max issues per project |
| `--output` | - | console | 📄 Output file path |
| `--language` | `SONARQUBE_REPORT_LANGUAGE` | `en` | 🌐 Report language (`en`/`ru`) |

**Generate API Token:** SonarQube → My Account → Security → Tokens

## 📊 Example Output

```markdown
# SonarQube Analysis Report
Generated: 2024-01-15 14:30:00
---
## Project: my-project
**Last Analysis:** 2024-01-15 12:00:00 UTC

| Severity | Message | Component | Line |
|----------|---------|-----------|------|
| MAJOR | Remove unused variable | my-project:src/main.py | 42 |
```

## 🔧 Development

```bash
# Run tests with coverage
pytest tests/ --cov=sonarqube_checker --cov=i18n
```

**Coverage:** 99% (152/153 statements) | **Tests:** 37 passing

## ☁️ SonarCloud Setup

1. Connect [sonarcloud.io](https://sonarcloud.io) to GitHub
2. Import repository and create project
3. **Disable Automatic Analysis**: Administration → Analysis Method → Turn OFF "Automatic Analysis"
4. Generate token: My Account → Security → Tokens
5. Add GitHub secret: `SONAR_TOKEN` (Settings → Secrets → Actions → New secret)
6. Push to trigger CI-based analysis

[📈 View Dashboard](https://sonarcloud.io/summary/new_code?id=stden_SonarQubeChecker&branch=main)

## 📄 License

MIT

## Testing

- Repository-wide testing/TDD guide: `TESTING_TDD_GUIDE.md`
- Stack checklist: `TESTING_CHECKLIST_RUST.md`
- Stack checklist: `TESTING_CHECKLIST_PYTHON.md`
