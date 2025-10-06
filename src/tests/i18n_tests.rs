#[cfg(test)]
mod tests {
    use crate::i18n::{get_translation, Language, TRANSLATIONS};

    #[test]
    fn test_language_from_str() {
        assert_eq!(Language::from_str("en"), Language::En);
        assert_eq!(Language::from_str("EN"), Language::En);
        assert_eq!(Language::from_str("ru"), Language::Ru);
        assert_eq!(Language::from_str("RU"), Language::Ru);
        assert_eq!(Language::from_str("unknown"), Language::En);
        assert_eq!(Language::from_str(""), Language::En);
    }

    #[test]
    fn test_get_translation_english() {
        assert_eq!(get_translation("report_title", &Language::En), "📊 SonarQube Analysis Report");
        assert_eq!(get_translation("generated", &Language::En), "🕒 Generated");
        assert_eq!(get_translation("project", &Language::En), "📁 Project");
        assert_eq!(get_translation("last_analysis", &Language::En), "📅 Last Analysis");
        assert_eq!(get_translation("latest_issues", &Language::En), "🚨 Latest Issues");
        assert_eq!(get_translation("no_analysis_available", &Language::En), "⚠️ No analysis available");
        assert_eq!(get_translation("no_open_issues", &Language::En), "✅ No open issues found.");
        assert_eq!(get_translation("severity", &Language::En), "🔥 Severity");
        assert_eq!(get_translation("message", &Language::En), "💬 Message");
        assert_eq!(get_translation("component", &Language::En), "🧩 Component");
        assert_eq!(get_translation("line", &Language::En), "📍 Line");
    }

    #[test]
    fn test_get_translation_russian() {
        assert_eq!(get_translation("report_title", &Language::Ru), "📊 Отчёт анализа SonarQube");
        assert_eq!(get_translation("generated", &Language::Ru), "🕒 Создано");
        assert_eq!(get_translation("project", &Language::Ru), "📁 Проект");
        assert_eq!(get_translation("last_analysis", &Language::Ru), "📅 Последний анализ");
        assert_eq!(get_translation("latest_issues", &Language::Ru), "🚨 Последние проблемы");
        assert_eq!(get_translation("no_analysis_available", &Language::Ru), "⚠️ Анализ недоступен");
        assert_eq!(get_translation("no_open_issues", &Language::Ru), "✅ Открытых проблем не найдено.");
        assert_eq!(get_translation("severity", &Language::Ru), "🔥 Важность");
        assert_eq!(get_translation("message", &Language::Ru), "💬 Сообщение");
        assert_eq!(get_translation("component", &Language::Ru), "🧩 Компонент");
        assert_eq!(get_translation("line", &Language::Ru), "📍 Строка");
    }

    #[test]
    fn test_get_translation_missing_key() {
        // When a key doesn't exist, it should return the key itself
        assert_eq!(get_translation("non_existent_key", &Language::En), "non_existent_key");
        assert_eq!(get_translation("non_existent_key", &Language::Ru), "non_existent_key");
    }

    #[test]
    fn test_translations_loaded() {
        // Verify that translations are loaded correctly
        assert!(!TRANSLATIONS.en.is_empty());
        assert!(!TRANSLATIONS.ru.is_empty());
        
        // Verify essential keys exist
        assert!(TRANSLATIONS.en.contains_key("report_title"));
        assert!(TRANSLATIONS.ru.contains_key("report_title"));
    }

    #[test]
    fn test_all_keys_in_both_languages() {
        // Ensure all keys in English also exist in Russian
        for key in TRANSLATIONS.en.keys() {
            assert!(
                TRANSLATIONS.ru.contains_key(key),
                "Key '{}' missing in Russian translations", 
                key
            );
        }

        // Ensure all keys in Russian also exist in English
        for key in TRANSLATIONS.ru.keys() {
            assert!(
                TRANSLATIONS.en.contains_key(key),
                "Key '{}' missing in English translations", 
                key
            );
        }
    }

    #[test]
    fn test_language_equality() {
        assert_eq!(Language::En, Language::En);
        assert_eq!(Language::Ru, Language::Ru);
        assert_ne!(Language::En, Language::Ru);
    }

    #[test]
    fn test_language_copy() {
        let lang1 = Language::En;
        let lang2 = lang1;  // Copy
        assert_eq!(lang1, lang2);
    }
}