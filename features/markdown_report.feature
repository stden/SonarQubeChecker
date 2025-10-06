Feature: Markdown report formatting
  The Markdown report generator converts SonarQube data into human friendly Markdown.
  These scenarios verify the critical formatting behaviors.

  Scenario Outline: Formatting analysis dates
    Given the analysis date "<raw_date>"
    When I format the analysis date
    Then the formatted result should be "<expected>"

    Examples:
      | raw_date                 | expected                   |
      | 2024-01-15T12:00:00+0000 | 2024-01-15 12:00:00 UTC    |
      | None                     | No analysis available      |
      | not-a-date               | not-a-date                 |

  Scenario: Generating issue table for populated data
    Given the following issues:
      | severity | message                | component              | line |
      | MAJOR    | Remove unused variable | project:src/main.py    | 42   |
      | MINOR    | Add comment            | project:src/utils.py   | 15   |
    When I build the issues table
    Then the table should include the header
    And the table should include the issue row "MAJOR" "Remove unused variable" "project:src/main.py" "42"
    And the table should include the issue row "MINOR" "Add comment" "project:src/utils.py" "15"

  Scenario: Generating issue table for empty data
    Given no issues
    When I build the issues table
    Then the table should be "No open issues found."

  Scenario: Escaping pipe characters in messages
    Given the following issues:
      | severity | message                              | component         | line |
      | MAJOR    | Error: expected \| got something else | project:file.py   | 10   |
    When I build the issues table
    Then the table should contain the escaped pipe character
