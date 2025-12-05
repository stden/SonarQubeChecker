# SonarQube Checker - Rust Version

This is the Rust implementation of SonarQube Checker, a CLI tool for fetching project analysis data and issues from SonarQube/SonarCloud instances.

## Building

```bash
# Build the project
cargo build --release

# Run tests
cargo test

# Run with verbose test output
cargo test -- --nocapture
```

## Running

```bash
# Run directly with cargo
cargo run -- --url https://sonarqube.example.com --token YOUR_TOKEN --projects example-project-1,example-project-2

# Run the compiled binary
./target/release/sonarqube_checker --url https://sonarqube.example.com --token YOUR_TOKEN --projects example-project-1

# Use environment variables
export SONARQUBE_URL=https://sonarqube.example.com
export SONARQUBE_TOKEN=your_token
export SONARQUBE_PROJECTS=example-project-1,example-project-2
cargo run

# Or use .env file
cargo run
```

## Demo

Run the demo to see sample output:

```bash
cargo run --bin demo
```

## Features

- ✅ Full API compatibility with Python version
- ✅ Internationalization (English and Russian)
- ✅ Environment variable and .env file support
- ✅ Markdown report generation
- ✅ Error handling and timeout support
- ✅ Comprehensive test suite

## Dependencies

- `reqwest` - HTTP client with blocking I/O
- `clap` - Command-line argument parsing
- `serde` - Serialization/deserialization
- `chrono` - Date/time handling
- `dotenv` - .env file support
- `anyhow` - Error handling
- `once_cell` - Lazy static initialization

## Testing

The test suite includes:

- Unit tests for all modules
- Integration tests for CLI
- Mock HTTP server tests
- I18n validation tests

Run specific test modules:

```bash
cargo test client_tests
cargo test report_tests
cargo test i18n_tests
cargo test integration_tests
```

## Performance

The Rust version offers improved performance compared to the Python version:

- Faster startup time
- Lower memory usage
- Better concurrent request handling
- Native binary distribution

## Cross-compilation

Build for different platforms:

```bash
# Linux
cargo build --release --target x86_64-unknown-linux-gnu

# Windows
cargo build --release --target x86_64-pc-windows-msvc

# macOS
cargo build --release --target x86_64-apple-darwin
```