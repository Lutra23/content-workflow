# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.2.1] - 2026-02-01

### Added
- Unit tests for core modules (`tests/test_core.py`)
- Template validation with quality checks
- Quality assessment for generated content

### Fixed
- YAML syntax errors in templates
- Template variable substitution

## [v0.2.0] - 2026-02-01

### Added
- Template engine (`lib/template_engine.py`)
- YAML-based templates (`templates/content.yaml`)
- 4 content templates:
  - `article_professional` - Professional articles
  - `article_viral` - Viral content
  - `video_script_3min` - 3-min video scripts
  - `thread_x` - Twitter/X threads
- Quality assessment module (`lib/quality.py`)
- A/B testing support
- Readability, SEO, structure, engagement scoring

### Changed
- Refactored template system to YAML format

## [v0.1.1] - 2026-02-01

### Security
- Removed hardcoded API keys
- Added `.env.example` template
- Improved error messages for missing API keys

### Added
- `requirements.txt` for dependency management
- Template directory structure (`templates/`)

## [v0.1.0] - 2026-01-31

### Added
- Initial release
- Multi-provider AI support (Groq, DeepSeek, SiliconFlow, OpenRouter, Yunwu)
- Basic workflow engine (`lib/workflow.py`)
- CLI entry point (`scripts/generate.py`)
- Configuration system
- Error handling and fallback
