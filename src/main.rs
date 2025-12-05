mod client;
mod i18n;
mod report;

use anyhow::{Context, Result};
use clap::Parser;
use dotenv::dotenv;
use std::fs;

use crate::client::SonarQubeClient;
use crate::i18n::Language;
use crate::report::{MarkdownReportGenerator, ProjectData};

#[derive(Parser)]
#[command(
    name = "sonarqube_checker",
    about = "Fetch SonarQube project analysis data and generate a Markdown report.",
    after_help = "Examples:\n  sonarqube_checker --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1,project2\n  sonarqube_checker --url https://sonarqube.example.com --token YOUR_TOKEN --projects project1 --output report.md\n\n  # Or use environment variables from .env file:\n  sonarqube_checker"
)]
struct Args {
    #[arg(
        long,
        env = "SONARQUBE_URL",
        help = "SonarQube base URL (e.g., https://sonarqube.example.com)"
    )]
    url: Option<String>,

    #[arg(
        long,
        env = "SONARQUBE_TOKEN",
        help = "SonarQube API token for authentication"
    )]
    token: Option<String>,

    #[arg(
        long,
        env = "SONARQUBE_PROJECTS",
        help = "Comma-separated list of project keys (e.g., project1,project2)"
    )]
    projects: Option<String>,

    #[arg(
        long,
        env = "SONARQUBE_MAX_ISSUES",
        default_value = "10",
        help = "Maximum number of issues to fetch per project"
    )]
    max_issues: i32,

    #[arg(
        long,
        help = "Output file path (e.g., report.md). If not specified, prints to console"
    )]
    output: Option<String>,

    #[arg(
        long,
        env = "SONARQUBE_REPORT_LANGUAGE",
        default_value = "en",
        value_enum,
        help = "Report language"
    )]
    language: Language,
}

fn main() -> Result<()> {
    dotenv().ok();

    let args = Args::parse();

    let url = args.url
        .context("Error: --url is required (or set SONARQUBE_URL environment variable)")?;
    
    let token = args.token
        .context("Error: --token is required (or set SONARQUBE_TOKEN environment variable)")?;
    
    let projects = args.projects
        .context("Error: --projects is required (or set SONARQUBE_PROJECTS environment variable)")?;

    let project_keys: Vec<&str> = projects.split(',').map(|s| s.trim()).collect();

    let client = SonarQubeClient::new(url, token)?;

    let mut projects_data = Vec::new();
    
    for project_key in project_keys {
        eprintln!("Fetching data for project: {}...", project_key);

        let last_analysis = client.get_last_analysis_date(project_key)?;
        let issues = client.get_latest_issues(project_key, args.max_issues)?;

        projects_data.push(ProjectData {
            project_key: project_key.to_string(),
            last_analysis,
            issues,
        });
    }

    let generator = MarkdownReportGenerator::new(args.language);
    let report = generator.generate_report(&projects_data);

    if let Some(output_path) = args.output {
        fs::write(&output_path, report)
            .context(format!("Error writing to file: {}", output_path))?;
        eprintln!("Report saved to: {}", output_path);
    } else {
        print!("{}", report);
    }

    Ok(())
}