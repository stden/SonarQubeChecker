use anyhow::{Context, Result};
use reqwest::blocking::{Client, Response};
use reqwest::header::{HeaderMap, HeaderValue, AUTHORIZATION};
use serde::Deserialize;
use std::time::Duration;

#[derive(Debug, Deserialize)]
pub struct ProjectAnalysesResponse {
    pub analyses: Vec<Analysis>,
}

#[derive(Debug, Deserialize)]
pub struct Analysis {
    pub date: String,
}

#[derive(Debug, Deserialize)]
pub struct IssuesResponse {
    pub issues: Vec<Issue>,
}

#[derive(Debug, Deserialize)]
pub struct Issue {
    pub severity: Option<String>,
    pub message: Option<String>,
    pub component: Option<String>,
    pub line: Option<i32>,
}

#[derive(Debug, Clone)]
pub struct IssueData {
    pub severity: String,
    pub message: String,
    pub component: String,
    pub line: String,
}

pub struct SonarQubeClient {
    base_url: String,
    client: Client,
}

impl SonarQubeClient {
    pub fn new(base_url: String, api_token: String) -> Result<Self> {
        let mut headers = HeaderMap::new();
        let auth_value = base64::encode(format!("{}:", api_token));
        headers.insert(
            AUTHORIZATION,
            HeaderValue::from_str(&format!("Basic {}", auth_value))?,
        );

        let client = Client::builder()
            .default_headers(headers)
            .timeout(Duration::from_secs(30))
            .build()?;

        Ok(Self {
            base_url: base_url.trim_end_matches('/').to_string(),
            client,
        })
    }

    pub fn get_last_analysis_date(&self, project_key: &str) -> Result<Option<String>> {
        let url = format!("{}/api/project_analyses/search", self.base_url);
        
        let response: Response = self.client
            .get(&url)
            .query(&[("project", project_key), ("ps", "1")])
            .send()
            .context("Failed to send request")?;

        if !response.status().is_success() {
            eprintln!("Error fetching analysis date for {}: HTTP {}", project_key, response.status());
            return Ok(None);
        }

        let data: ProjectAnalysesResponse = response.json()
            .context("Failed to parse response")?;

        Ok(data.analyses.first().map(|a| a.date.clone()))
    }

    pub fn get_latest_issues(&self, project_key: &str, max_issues: i32) -> Result<Vec<IssueData>> {
        let url = format!("{}/api/issues/search", self.base_url);
        
        let response: Response = self.client
            .get(&url)
            .query(&[
                ("componentKeys", project_key),
                ("statuses", "OPEN,CONFIRMED"),
                ("ps", &max_issues.to_string()),
                ("s", "CREATION_DATE"),
                ("asc", "false"),
            ])
            .send()
            .context("Failed to send request")?;

        if !response.status().is_success() {
            eprintln!("Error fetching issues for {}: HTTP {}", project_key, response.status());
            return Ok(Vec::new());
        }

        let data: IssuesResponse = response.json()
            .context("Failed to parse response")?;

        let issues = data.issues.into_iter().map(|issue| IssueData {
            severity: issue.severity.unwrap_or_else(|| "N/A".to_string()),
            message: issue.message.unwrap_or_else(|| "N/A".to_string()),
            component: issue.component.unwrap_or_else(|| "N/A".to_string()),
            line: issue.line.map(|l| l.to_string()).unwrap_or_else(|| "N/A".to_string()),
        }).collect();

        Ok(issues)
    }
}