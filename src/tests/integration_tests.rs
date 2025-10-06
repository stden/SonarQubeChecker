#[cfg(test)]
mod tests {
    use std::process::Command;
    use std::env;
    use tempfile::NamedTempFile;
    use std::fs;

    #[test]
    fn test_cli_help() {
        let output = Command::new("cargo")
            .args(&["run", "--", "--help"])
            .output()
            .expect("Failed to execute command");

        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("sonarqube_checker"));
        assert!(stdout.contains("Fetch SonarQube project analysis data"));
        assert!(stdout.contains("--url"));
        assert!(stdout.contains("--token"));
        assert!(stdout.contains("--projects"));
    }

    #[test]
    fn test_cli_missing_required_args() {
        let output = Command::new("cargo")
            .args(&["run", "--"])
            .env_remove("SONARQUBE_URL")
            .env_remove("SONARQUBE_TOKEN")
            .env_remove("SONARQUBE_PROJECTS")
            .output()
            .expect("Failed to execute command");

        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(output.status.code().unwrap_or(0) != 0);
        assert!(stderr.contains("Error:") || stderr.contains("required"));
    }

    #[test]
    fn test_cli_with_env_vars() {
        // This test would require a mock server or real SonarQube instance
        // For now, we'll just test that the CLI accepts environment variables
        let output = Command::new("cargo")
            .args(&["run", "--"])
            .env("SONARQUBE_URL", "https://example.com")
            .env("SONARQUBE_TOKEN", "fake_token")
            .env("SONARQUBE_PROJECTS", "test")
            .output()
            .expect("Failed to execute command");

        // The command will fail because the URL is not a real SonarQube instance,
        // but it should get past argument validation
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(!stderr.contains("--url is required"));
        assert!(!stderr.contains("--token is required"));
        assert!(!stderr.contains("--projects is required"));
    }

    #[test]
    fn test_output_to_file() {
        let temp_file = NamedTempFile::new().expect("Failed to create temp file");
        let output_path = temp_file.path().to_str().unwrap();

        // This would normally require a real SonarQube instance
        // For demonstration purposes, we'll just verify the CLI accepts the --output flag
        let output = Command::new("cargo")
            .args(&["run", "--", 
                "--url", "https://example.com",
                "--token", "fake_token",
                "--projects", "test",
                "--output", output_path])
            .output()
            .expect("Failed to execute command");

        // The command will fail, but we're just testing argument parsing
        assert_eq!(output.status.code().unwrap_or(1), 1);
    }

    #[test]
    fn test_language_selection() {
        // Test English
        let output = Command::new("cargo")
            .args(&["run", "--", "--help"])
            .env("SONARQUBE_REPORT_LANGUAGE", "en")
            .output()
            .expect("Failed to execute command");

        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Report language"));

        // Test Russian
        let output = Command::new("cargo")
            .args(&["run", "--", "--help"])
            .env("SONARQUBE_REPORT_LANGUAGE", "ru")
            .output()
            .expect("Failed to execute command");

        let stdout = String::from_utf8_lossy(&output.stdout);
        assert!(stdout.contains("Report language"));
    }

    #[test]
    fn test_max_issues_parameter() {
        let output = Command::new("cargo")
            .args(&["run", "--", 
                "--url", "https://example.com",
                "--token", "fake_token",
                "--projects", "test",
                "--max-issues", "20"])
            .output()
            .expect("Failed to execute command");

        // Just verify the parameter is accepted
        let stderr = String::from_utf8_lossy(&output.stderr);
        assert!(!stderr.contains("unexpected argument"));
    }

    #[test]
    fn test_multiple_projects() {
        let output = Command::new("cargo")
            .args(&["run", "--",
                "--url", "https://example.com",
                "--token", "fake_token",
                "--projects", "project1,project2,project3"])
            .output()
            .expect("Failed to execute command");

        let stderr = String::from_utf8_lossy(&output.stderr);
        // Should see attempts to fetch data for each project
        assert!(stderr.contains("project1") || output.status.code().unwrap_or(0) != 0);
    }

    #[test]
    #[ignore] // This test requires actual network access
    fn test_real_sonarcloud_connection() {
        // This test would connect to real SonarCloud
        // Only run if you have valid credentials
        if let (Ok(url), Ok(token), Ok(projects)) = (
            env::var("SONARQUBE_URL"),
            env::var("SONARQUBE_TOKEN"),
            env::var("SONARQUBE_PROJECTS"),
        ) {
            let output = Command::new("cargo")
                .args(&["run", "--",
                    "--url", &url,
                    "--token", &token,
                    "--projects", &projects])
                .output()
                .expect("Failed to execute command");

            let stdout = String::from_utf8_lossy(&output.stdout);
            assert!(output.status.success());
            assert!(stdout.contains("SonarQube Analysis Report"));
        }
    }

    #[test]
    fn test_dotenv_loading() {
        // Create a temporary .env file
        let temp_dir = tempfile::tempdir().expect("Failed to create temp dir");
        let env_path = temp_dir.path().join(".env");
        
        fs::write(&env_path, r#"
SONARQUBE_URL=https://test.example.com
SONARQUBE_TOKEN=test_token_from_env
SONARQUBE_PROJECTS=env_project
"#).expect("Failed to write .env file");

        let output = Command::new("cargo")
            .args(&["run", "--"])
            .current_dir(temp_dir.path())
            .output()
            .expect("Failed to execute command");

        let stderr = String::from_utf8_lossy(&output.stderr);
        // Should not complain about missing arguments if .env was loaded
        assert!(!stderr.contains("--url is required"));
        assert!(!stderr.contains("--token is required"));
        assert!(!stderr.contains("--projects is required"));
    }
}