use chrono::Utc;
use std::collections::HashMap;

fn main() {
    let projects = vec![
        HashMap::from([
            ("project_key", "example-project-1"),
            ("last_analysis", "2024-01-15T10:30:00Z"),
        ]),
        HashMap::from([
            ("project_key", "example-project-2"),
            ("last_analysis", "2024-01-14T15:45:00Z"),
        ]),
        HashMap::from([
            ("project_key", "example-project-3"),
            ("last_analysis", ""),
        ]),
    ];

    let issues_data = vec![
        vec![
            HashMap::from([
                ("severity", "CRITICAL"),
                ("message", "NullPointerException might occur here"),
                ("component", "src/main/java/com/example/UserService.java"),
                ("line", "42"),
            ]),
            HashMap::from([
                ("severity", "MAJOR"),
                ("message", "Remove this unused import 'java.util.List'"),
                ("component", "src/main/java/com/example/UserService.java"),
                ("line", "5"),
            ]),
            HashMap::from([
                ("severity", "MINOR"),
                ("message", "Replace this if-then-else | with a single return"),
                ("component", "src/main/java/com/example/Utils.java"),
                ("line", "128"),
            ]),
        ],
        vec![
            HashMap::from([
                ("severity", "BLOCKER"),
                ("message", "SQL injection vulnerability detected"),
                ("component", "src/main/java/com/example/DatabaseManager.java"),
                ("line", "87"),
            ]),
        ],
        vec![],
    ];

    println!("=== English Report ===\n");
    generate_demo_report("en", &projects, &issues_data);
    
    println!("\n\n=== Russian Report ===\n");
    generate_demo_report("ru", &projects, &issues_data);
}

fn generate_demo_report(lang: &str, projects: &[HashMap<&str, &str>], issues_data: &[Vec<HashMap<&str, &str>>]) {
    let translations = match lang {
        "ru" => HashMap::from([
            ("report_title", "📊 Отчёт анализа SonarQube"),
            ("generated", "🕒 Создано"),
            ("project", "📁 Проект"),
            ("last_analysis", "📅 Последний анализ"),
            ("latest_issues", "🚨 Последние проблемы"),
            ("no_analysis_available", "⚠️ Анализ недоступен"),
            ("no_open_issues", "✅ Открытых проблем не найдено."),
            ("severity", "🔥 Важность"),
            ("message", "💬 Сообщение"),
            ("component", "🧩 Компонент"),
            ("line", "📍 Строка"),
        ]),
        _ => HashMap::from([
            ("report_title", "📊 SonarQube Analysis Report"),
            ("generated", "🕒 Generated"),
            ("project", "📁 Project"),
            ("last_analysis", "📅 Last Analysis"),
            ("latest_issues", "🚨 Latest Issues"),
            ("no_analysis_available", "⚠️ No analysis available"),
            ("no_open_issues", "✅ No open issues found."),
            ("severity", "🔥 Severity"),
            ("message", "💬 Message"),
            ("component", "🧩 Component"),
            ("line", "📍 Line"),
        ]),
    };

    println!("# {}\n", translations["report_title"]);
    println!("{}: {}\n", translations["generated"], Utc::now().format("%Y-%m-%d %H:%M:%S"));
    println!("---\n");

    for (i, project) in projects.iter().enumerate() {
        println!("## {}: {}\n", translations["project"], project["project_key"]);

        let last_analysis = if project["last_analysis"].is_empty() {
            translations["no_analysis_available"]
        } else {
            project["last_analysis"]
        };
        
        println!("**{}:** {}\n", translations["last_analysis"], last_analysis);
        println!("**{}:**\n", translations["latest_issues"]);

        if issues_data[i].is_empty() {
            println!("{}\n", translations["no_open_issues"]);
        } else {
            println!("| {} | {} | {} | {} |", 
                translations["severity"], 
                translations["message"], 
                translations["component"], 
                translations["line"]);
            println!("|----------|---------|-----------|------|");
            
            for issue in &issues_data[i] {
                let message = issue["message"].replace('|', "\\|");
                println!("| {} | {} | {} | {} |", 
                    issue["severity"], 
                    message,
                    issue["component"], 
                    issue["line"]);
            }
            println!();
        }
        
        println!("---\n");
    }
}