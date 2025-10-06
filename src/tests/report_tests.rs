#[cfg(test)]
mod tests {
    use crate::client::IssueData;
    use crate::i18n::Language;
    use crate::report::{MarkdownReportGenerator, ProjectData};

    fn create_test_issue(severity: &str, message: &str, component: &str, line: &str) -> IssueData {
        IssueData {
            severity: severity.to_string(),
            message: message.to_string(),
            component: component.to_string(),
            line: line.to_string(),
        }
    }

    #[test]
    fn test_format_analysis_date_valid_iso() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let result = generator.format_analysis_date(Some("2024-01-15T10:30:00+00:00"));
        assert_eq!(result, "2024-01-15 10:30:00 UTC");
    }

    #[test]
    fn test_format_analysis_date_invalid_format() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let result = generator.format_analysis_date(Some("invalid-date"));
        assert_eq!(result, "invalid-date");
    }

    #[test]
    fn test_format_analysis_date_none_english() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let result = generator.format_analysis_date(None);
        assert_eq!(result, "⚠️ No analysis available");
    }

    #[test]
    fn test_format_analysis_date_none_russian() {
        let generator = MarkdownReportGenerator::new(Language::Ru);
        let result = generator.format_analysis_date(None);
        assert_eq!(result, "⚠️ Анализ недоступен");
    }

    #[test]
    fn test_generate_issues_table_empty_english() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let result = generator.generate_issues_table(&[]);
        assert_eq!(result, "✅ No open issues found.");
    }

    #[test]
    fn test_generate_issues_table_empty_russian() {
        let generator = MarkdownReportGenerator::new(Language::Ru);
        let result = generator.generate_issues_table(&[]);
        assert_eq!(result, "✅ Открытых проблем не найдено.");
    }

    #[test]
    fn test_generate_issues_table_with_issues() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let issues = vec![
            create_test_issue("CRITICAL", "NullPointer", "Main.java", "42"),
            create_test_issue("MAJOR", "Unused import", "Utils.java", "5"),
        ];

        let result = generator.generate_issues_table(&issues);
        assert!(result.contains("| 🔥 Severity | 💬 Message | 🧩 Component | 📍 Line |"));
        assert!(result.contains("|----------|---------|-----------|------|"));
        assert!(result.contains("| CRITICAL | NullPointer | Main.java | 42 |"));
        assert!(result.contains("| MAJOR | Unused import | Utils.java | 5 |"));
    }

    #[test]
    fn test_generate_issues_table_escapes_pipes() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let issues = vec![
            create_test_issue("MAJOR", "Use || instead of |", "Logic.java", "10"),
        ];

        let result = generator.generate_issues_table(&issues);
        assert!(result.contains("Use \\|\\| instead of \\|"));
    }

    #[test]
    fn test_generate_report_single_project_no_issues() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let projects = vec![
            ProjectData {
                project_key: "test-project".to_string(),
                last_analysis: Some("2024-01-15T10:30:00+00:00".to_string()),
                issues: vec![],
            }
        ];

        let report = generator.generate_report(&projects);
        
        assert!(report.contains("# 📊 SonarQube Analysis Report"));
        assert!(report.contains("🕒 Generated:"));
        assert!(report.contains("## 📁 Project: test-project"));
        assert!(report.contains("**📅 Last Analysis:** 2024-01-15 10:30:00 UTC"));
        assert!(report.contains("**🚨 Latest Issues:**"));
        assert!(report.contains("✅ No open issues found."));
    }

    #[test]
    fn test_generate_report_multiple_projects() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let projects = vec![
            ProjectData {
                project_key: "project1".to_string(),
                last_analysis: Some("2024-01-15T10:30:00+00:00".to_string()),
                issues: vec![
                    create_test_issue("CRITICAL", "Issue 1", "File1.java", "10"),
                ],
            },
            ProjectData {
                project_key: "project2".to_string(),
                last_analysis: None,
                issues: vec![],
            },
        ];

        let report = generator.generate_report(&projects);
        
        assert!(report.contains("## 📁 Project: project1"));
        assert!(report.contains("## 📁 Project: project2"));
        assert!(report.contains("| CRITICAL | Issue 1 | File1.java | 10 |"));
        assert!(report.contains("⚠️ No analysis available"));
    }

    #[test]
    fn test_generate_report_russian() {
        let generator = MarkdownReportGenerator::new(Language::Ru);
        let projects = vec![
            ProjectData {
                project_key: "тестовый-проект".to_string(),
                last_analysis: Some("2024-01-15T10:30:00+00:00".to_string()),
                issues: vec![
                    create_test_issue("BLOCKER", "Критическая ошибка", "Main.java", "100"),
                ],
            }
        ];

        let report = generator.generate_report(&projects);
        
        assert!(report.contains("# 📊 Отчёт анализа SonarQube"));
        assert!(report.contains("🕒 Создано:"));
        assert!(report.contains("## 📁 Проект: тестовый-проект"));
        assert!(report.contains("**📅 Последний анализ:** 2024-01-15 10:30:00 UTC"));
        assert!(report.contains("**🚨 Последние проблемы:**"));
        assert!(report.contains("| 🔥 Важность | 💬 Сообщение | 🧩 Компонент | 📍 Строка |"));
        assert!(report.contains("| BLOCKER | Критическая ошибка | Main.java | 100 |"));
    }

    #[test]
    fn test_generate_report_empty_projects() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let projects: Vec<ProjectData> = vec![];

        let report = generator.generate_report(&projects);
        
        assert!(report.contains("# 📊 SonarQube Analysis Report"));
        assert!(report.contains("🕒 Generated:"));
        assert!(report.contains("---"));
        // Should not contain any project sections
        assert!(!report.contains("## 📁 Project:"));
    }

    #[test]
    fn test_report_formatting_consistency() {
        let generator = MarkdownReportGenerator::new(Language::En);
        let projects = vec![
            ProjectData {
                project_key: "test".to_string(),
                last_analysis: Some("2024-01-15T10:30:00+00:00".to_string()),
                issues: vec![
                    create_test_issue("MAJOR", "Test", "Test.java", "1"),
                ],
            }
        ];

        let report = generator.generate_report(&projects);
        
        // Check markdown formatting
        assert!(report.contains("# "));  // Header
        assert!(report.contains("## "));  // Subheader
        assert!(report.contains("**"));  // Bold text
        assert!(report.contains("---"));  // Horizontal rule
        assert!(report.contains("|"));  // Table
    }
}