use crate::client::IssueData;
use crate::i18n::{get_translation, Language};
use chrono::{DateTime, Utc};
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct ProjectData {
    pub project_key: String,
    pub last_analysis: Option<String>,
    pub issues: Vec<IssueData>,
}

pub struct MarkdownReportGenerator {
    language: Language,
}

impl MarkdownReportGenerator {
    pub fn new(language: Language) -> Self {
        Self { language }
    }

    pub fn format_analysis_date(&self, date_str: Option<&str>) -> String {
        match date_str {
            None => get_translation("no_analysis_available", &self.language).to_string(),
            Some(date) => {
                match DateTime::parse_from_rfc3339(date) {
                    Ok(dt) => dt.format("%Y-%m-%d %H:%M:%S UTC").to_string(),
                    Err(_) => date.to_string(),
                }
            }
        }
    }

    pub fn generate_issues_table(&self, issues: &[IssueData]) -> String {
        if issues.is_empty() {
            return get_translation("no_open_issues", &self.language).to_string();
        }

        let severity_col = get_translation("severity", &self.language);
        let message_col = get_translation("message", &self.language);
        let component_col = get_translation("component", &self.language);
        let line_col = get_translation("line", &self.language);

        let mut table = format!("| {} | {} | {} | {} |\n", severity_col, message_col, component_col, line_col);
        table.push_str("|----------|---------|-----------|------|\n");

        for issue in issues {
            let message = issue.message.replace('|', "\\|");
            let component = issue.component.replace('|', "\\|");
            table.push_str(&format!("| {} | {} | {} | {} |\n", 
                issue.severity, message, component, issue.line));
        }

        table
    }

    pub fn generate_report(&self, projects_data: &[ProjectData]) -> String {
        let report_title = get_translation("report_title", &self.language);
        let generated_label = get_translation("generated", &self.language);
        let project_label = get_translation("project", &self.language);
        let last_analysis_label = get_translation("last_analysis", &self.language);
        let latest_issues_label = get_translation("latest_issues", &self.language);

        let mut report = format!("# {}\n\n", report_title);
        let now: DateTime<Utc> = Utc::now();
        report.push_str(&format!("{}: {}\n\n", generated_label, now.format("%Y-%m-%d %H:%M:%S")));
        report.push_str("---\n\n");

        for project in projects_data {
            report.push_str(&format!("## {}: {}\n\n", project_label, project.project_key));

            let formatted_date = self.format_analysis_date(project.last_analysis.as_deref());
            report.push_str(&format!("**{}:** {}\n\n", last_analysis_label, formatted_date));

            report.push_str(&format!("**{}:**\n\n", latest_issues_label));
            report.push_str(&self.generate_issues_table(&project.issues));
            report.push_str("\n\n---\n\n");
        }

        report
    }
}