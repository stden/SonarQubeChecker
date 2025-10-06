# SonarQubeChecker

A Python script that connects to a SonarQube server via its Web API to monitor specified projects. The script retrieves the date of the last analysis for each project, fetches the latest open issues (errors and warnings), and generates a Markdown-formatted report.

## Features

- **API Connectivity**: Uses the `requests` library for HTTP requests
- **Authentication**: Supports Basic Auth using API tokens generated from SonarQube
- **Project Monitoring**: Retrieves last analysis date for each project
- **Issue Tracking**: Fetches latest open issues including:
  - Errors (BLOCKER, CRITICAL severities)
  - Warnings (MAJOR, MINOR severities)
- **Markdown Reports**: Generates well-formatted Markdown reports with sections for each project

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

## Configuration

The script uses environment variables for configuration:

- **SONARQUBE_URL** (required): The base URL of your SonarQube server
  - Example: `https://sonarqube.example.com`
  
- **SONARQUBE_TOKEN** (required): Your SonarQube API token
  - Generate a token in SonarQube: User Settings → Security → Generate Tokens
  
- **SONARQUBE_PROJECTS** (optional): Comma-separated list of project keys to analyze
  - Example: `project1,project2,project3`
  - If not provided, all projects will be analyzed
  
- **OUTPUT_FILE** (optional): Path to the output Markdown file
  - Default: `sonarqube_report.md`

## Usage

### Basic Usage

Set the required environment variables and run the script:

```bash
export SONARQUBE_URL="https://sonarqube.example.com"
export SONARQUBE_TOKEN="your_api_token_here"
python sonarqube_checker.py
```

### Analyze Specific Projects

```bash
export SONARQUBE_URL="https://sonarqube.example.com"
export SONARQUBE_TOKEN="your_api_token_here"
export SONARQUBE_PROJECTS="project1,project2"
python sonarqube_checker.py
```

### Custom Output File

```bash
export SONARQUBE_URL="https://sonarqube.example.com"
export SONARQUBE_TOKEN="your_api_token_here"
export OUTPUT_FILE="custom_report.md"
python sonarqube_checker.py
```

### Using a .env File

Create a `.env` file with your configuration:

```bash
SONARQUBE_URL=https://sonarqube.example.com
SONARQUBE_TOKEN=your_api_token_here
SONARQUBE_PROJECTS=project1,project2
OUTPUT_FILE=report.md
```

Then source it before running:

```bash
source .env
python sonarqube_checker.py
```

## Report Format

The generated Markdown report includes:

- Report generation timestamp
- For each project:
  - Project name
  - Last analysis date
  - List of errors (up to 20 shown)
    - Severity level
    - Issue message
    - File location and line number
    - SonarQube rule identifier
  - List of warnings (up to 20 shown)
    - Same details as errors

See [example_report.md](example_report.md) for a complete example report.

Example output:

```markdown
# SonarQube Analysis Report

Generated on: 2024-10-06 12:30:45

## Project: my-project

**Last Analysis:** 2024-10-06 10:15:30 UTC

### Errors: 3

1. **[CRITICAL]** Null pointer dereference
   - File: `src/main/MyClass.java` (Line 42)
   - Rule: `java:S2259`

### Warnings: 5

1. **[MAJOR]** Cognitive Complexity of method is too high
   - File: `src/main/Utils.java` (Line 100)
   - Rule: `java:S3776`
```

## Requirements

- Python 3.6 or higher
- requests library (see requirements.txt)

## Troubleshooting

### Authentication Issues

If you encounter authentication errors:
- Verify your API token is correct and has not expired
- Ensure the token has the necessary permissions to read projects and issues
- Check that you're using the token correctly (not the username/password)

### Connection Issues

If you can't connect to SonarQube:
- Verify the SONARQUBE_URL is correct and accessible
- Check if there's a firewall or proxy blocking the connection
- Ensure your SonarQube server is running and accessible

### No Projects Found

If no projects are returned:
- Verify your token has permission to view projects
- Check that projects exist on your SonarQube server
- Try accessing the projects through the SonarQube web interface with the same token

## API Documentation

This script uses the following SonarQube Web API endpoints:
- `/api/projects/search` - List all projects
- `/api/project_analyses/search` - Get project analysis history
- `/api/issues/search` - Search for issues in projects

For more information, see the [SonarQube Web API documentation](https://docs.sonarqube.org/latest/extend/web-api/).

## License

This project is open source and available for use and modification.