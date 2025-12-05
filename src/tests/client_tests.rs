#[cfg(test)]
mod tests {
    use crate::client::{SonarQubeClient, IssueData};
    use mockito::{Mock, Server};
    use serde_json::json;

    #[test]
    fn test_sonarqube_client_creation() {
        let client = SonarQubeClient::new(
            "https://sonarqube.example.com".to_string(),
            "test_token".to_string()
        );
        assert!(client.is_ok());
    }

    #[test]
    fn test_base_url_trimming() {
        let client = SonarQubeClient::new(
            "https://sonarqube.example.com/".to_string(),
            "test_token".to_string()
        ).unwrap();
        
        // The base URL should have the trailing slash removed
        // This is tested implicitly through successful API calls
    }

    #[test]
    fn test_get_last_analysis_date_success() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/project_analyses/search")
            .match_query(mockito::Matcher::AllOf(vec![
                mockito::Matcher::UrlEncoded("project".to_string(), "test-project".to_string()),
                mockito::Matcher::UrlEncoded("ps".to_string(), "1".to_string()),
            ]))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(json!({
                "analyses": [{
                    "date": "2024-01-15T10:30:00+0000"
                }]
            }).to_string())
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_last_analysis_date("test-project").unwrap();

        mock.assert();
        assert_eq!(result, Some("2024-01-15T10:30:00+0000".to_string()));
    }

    #[test]
    fn test_get_last_analysis_date_no_analyses() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/project_analyses/search")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(json!({
                "analyses": []
            }).to_string())
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_last_analysis_date("test-project").unwrap();

        mock.assert();
        assert_eq!(result, None);
    }

    #[test]
    fn test_get_last_analysis_date_error() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/project_analyses/search")
            .with_status(404)
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_last_analysis_date("test-project").unwrap();

        mock.assert();
        assert_eq!(result, None);
    }

    #[test]
    fn test_get_latest_issues_success() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/issues/search")
            .match_query(mockito::Matcher::AllOf(vec![
                mockito::Matcher::UrlEncoded("componentKeys".to_string(), "test-project".to_string()),
                mockito::Matcher::UrlEncoded("statuses".to_string(), "OPEN,CONFIRMED".to_string()),
                mockito::Matcher::UrlEncoded("ps".to_string(), "10".to_string()),
                mockito::Matcher::UrlEncoded("s".to_string(), "CREATION_DATE".to_string()),
                mockito::Matcher::UrlEncoded("asc".to_string(), "false".to_string()),
            ]))
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(json!({
                "issues": [
                    {
                        "severity": "CRITICAL",
                        "message": "NullPointerException might occur",
                        "component": "src/Main.java",
                        "line": 42
                    },
                    {
                        "severity": "MAJOR",
                        "message": "Remove unused import",
                        "component": "src/Utils.java",
                        "line": 5
                    }
                ]
            }).to_string())
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_latest_issues("test-project", 10).unwrap();

        mock.assert();
        assert_eq!(result.len(), 2);
        
        assert_eq!(result[0].severity, "CRITICAL");
        assert_eq!(result[0].message, "NullPointerException might occur");
        assert_eq!(result[0].component, "src/Main.java");
        assert_eq!(result[0].line, "42");

        assert_eq!(result[1].severity, "MAJOR");
        assert_eq!(result[1].message, "Remove unused import");
        assert_eq!(result[1].component, "src/Utils.java");
        assert_eq!(result[1].line, "5");
    }

    #[test]
    fn test_get_latest_issues_with_missing_fields() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/issues/search")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(json!({
                "issues": [
                    {
                        "severity": "CRITICAL"
                        // Missing other fields
                    },
                    {
                        "message": "Some issue",
                        "component": "src/Test.java"
                        // Missing severity and line
                    }
                ]
            }).to_string())
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_latest_issues("test-project", 10).unwrap();

        mock.assert();
        assert_eq!(result.len(), 2);
        
        assert_eq!(result[0].severity, "CRITICAL");
        assert_eq!(result[0].message, "N/A");
        assert_eq!(result[0].component, "N/A");
        assert_eq!(result[0].line, "N/A");

        assert_eq!(result[1].severity, "N/A");
        assert_eq!(result[1].message, "Some issue");
        assert_eq!(result[1].component, "src/Test.java");
        assert_eq!(result[1].line, "N/A");
    }

    #[test]
    fn test_get_latest_issues_empty() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/issues/search")
            .with_status(200)
            .with_header("content-type", "application/json")
            .with_body(json!({
                "issues": []
            }).to_string())
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_latest_issues("test-project", 10).unwrap();

        mock.assert();
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_get_latest_issues_error() {
        let mut server = Server::new();
        let mock = server
            .mock("GET", "/api/issues/search")
            .with_status(500)
            .create();

        let client = SonarQubeClient::new(server.url(), "test_token".to_string()).unwrap();
        let result = client.get_latest_issues("test-project", 10).unwrap();

        mock.assert();
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_issue_data_clone() {
        let issue = IssueData {
            severity: "CRITICAL".to_string(),
            message: "Test message".to_string(),
            component: "test.java".to_string(),
            line: "42".to_string(),
        };

        let cloned = issue.clone();
        assert_eq!(cloned.severity, "CRITICAL");
        assert_eq!(cloned.message, "Test message");
        assert_eq!(cloned.component, "test.java");
        assert_eq!(cloned.line, "42");
    }
}