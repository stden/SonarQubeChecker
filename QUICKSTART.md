# Quick Start Guide

## Installation
```bash
pip install -r requirements.txt
```

## Setup
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` with your SonarQube details:
```bash
SONARQUBE_URL=https://your-sonarqube-server.com
SONARQUBE_TOKEN=your_api_token
```

## Running
```bash
# Load environment variables and run
source .env
python sonarqube_checker.py
```

## Output
- Report is saved to `sonarqube_report.md` (or custom file if specified)
- Report is also printed to console

## Common Use Cases

### Check All Projects
```bash
python sonarqube_checker.py
```

### Check Specific Projects
```bash
export SONARQUBE_PROJECTS="project1,project2"
python sonarqube_checker.py
```

### Custom Output File
```bash
export OUTPUT_FILE="my_custom_report.md"
python sonarqube_checker.py
```

## Getting a SonarQube API Token

1. Log in to your SonarQube server
2. Click your avatar (top right) → **My Account**
3. Go to **Security** tab
4. Enter a token name and click **Generate**
5. Copy the token immediately (it won't be shown again)

## What Gets Reported

For each project:
- **Last Analysis Date**: When the project was last scanned
- **Errors**: Issues with BLOCKER or CRITICAL severity
- **Warnings**: Issues with MAJOR or MINOR severity

Each issue includes:
- Severity level
- Message/description
- File path and line number
- SonarQube rule ID
