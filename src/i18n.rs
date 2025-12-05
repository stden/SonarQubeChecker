use clap::ValueEnum;
use once_cell::sync::Lazy;
use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
pub struct Translations {
    pub en: HashMap<String, String>,
    pub ru: HashMap<String, String>,
}

pub static TRANSLATIONS: Lazy<Translations> = Lazy::new(|| {
    let yaml_content = include_str!("../translations.yaml");
    serde_yaml::from_str(yaml_content).unwrap_or_else(|_| {
        let mut en = HashMap::new();
        en.insert("report_title".to_string(), "SonarQube Analysis Report".to_string());
        en.insert("generated".to_string(), "Generated".to_string());
        en.insert("project".to_string(), "Project".to_string());
        en.insert("last_analysis".to_string(), "Last Analysis".to_string());
        en.insert("latest_issues".to_string(), "Latest Issues".to_string());
        en.insert("no_analysis_available".to_string(), "No analysis available".to_string());
        en.insert("no_open_issues".to_string(), "No open issues found.".to_string());
        en.insert("severity".to_string(), "Severity".to_string());
        en.insert("message".to_string(), "Message".to_string());
        en.insert("component".to_string(), "Component".to_string());
        en.insert("line".to_string(), "Line".to_string());

        let ru = HashMap::new();
        
        Translations { en, ru }
    })
});

#[derive(Debug, Clone, Copy, ValueEnum, PartialEq)]
pub enum Language {
    En,
    Ru,
}

impl Language {
    pub fn from_str(s: &str) -> Self {
        match s.to_lowercase().as_str() {
            "ru" => Language::Ru,
            _ => Language::En,
        }
    }
}

pub fn get_translation(key: &str, language: &Language) -> &str {
    let translations = match language {
        Language::En => &TRANSLATIONS.en,
        Language::Ru => &TRANSLATIONS.ru,
    };
    
    translations.get(key)
        .map(|s| s.as_str())
        .or_else(|| TRANSLATIONS.en.get(key).map(|s| s.as_str()))
        .unwrap_or(key)
}