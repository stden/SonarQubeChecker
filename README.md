# SonarQubeChecker

A Python tool to fetch project analysis data and open issues from SonarQube and generate Markdown reports.

## Features

- **API Connectivity**: Uses the `requests` library with Basic Auth token authentication
- **Project Analysis**: Fetches the last analysis date for each project
- **Issue Tracking**: Retrieves the latest open issues (OPEN, CONFIRMED status)
- **Markdown Reports**: Generates formatted reports with:
  - Last analysis date for each project
  - Table of latest issues (Severity, Message, Component, Line)
- **Flexible Output**: Display in console or save to a file
- **Error Handling**: Gracefully handles invalid tokens and missing data

## Requirements

- Python 3.6 or higher
- `requests` library (see Installation)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/stden/SonarQubeChecker.git
cd SonarQubeChecker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python sonarqube_checker.py --url https://sonarqube.example.com --token YOUR_API_TOKEN --projects project1,project2
```

### Save Report to File

```bash
python sonarqube_checker.py --url https://sonarqube.example.com --token YOUR_API_TOKEN --projects project1,project2 --output report.md
```

### Customize Number of Issues

```bash
python sonarqube_checker.py --url https://sonarqube.example.com --token YOUR_API_TOKEN --projects project1 --max-issues 20
```

## Command-Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--url` | Yes | SonarQube base URL | `https://sonarqube.example.com` |
| `--token` | Yes | SonarQube API token | `squ_abc123...` |
| `--projects` | Yes | Comma-separated list of project keys | `project1,project2` |
| `--max-issues` | No | Maximum issues per project (default: 10) | `20` |
| `--output` | No | Output file path (default: console) | `report.md` |

## Generating a SonarQube API Token

1. Log in to your SonarQube instance
2. Go to **My Account** → **Security**
3. Generate a new token under **Tokens**
4. Copy the token and use it with the `--token` parameter

## Example Output

```markdown
# SonarQube Analysis Report

Generated: 2024-01-15 14:30:00

---

## Project: my-project

**Last Analysis:** 2024-01-15 12:00:00 UTC

**Latest Issues:**

| Severity | Message | Component | Line |
|----------|---------|-----------|------|
| MAJOR | Remove this unused variable | my-project:src/main.py | 42 |
| MINOR | Add a comment to explain this code | my-project:src/utils.py | 15 |

---
```

## Error Handling

The tool handles common errors gracefully:
- Invalid API token: Error message displayed
- Project not found: Skips to next project
- Network issues: Timeout after 30 seconds with error message
- No analysis data: Shows "No analysis available"
- No issues found: Shows "No open issues found"

## Development

The code is organized into modular functions:
- `SonarQubeClient`: Handles all API interactions
- `MarkdownReportGenerator`: Generates formatted Markdown output
- `main()`: Command-line interface and orchestration

## License

MIT License - feel free to use and modify as needed.