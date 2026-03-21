# Changelog

All notable changes to Ludwig will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [2.0.0] - 2026-03-21

### 🎉 Complete Rewrite

Ludwig v2.0 is a complete reimagining of the framework. No more custom DSL - just pure Python.

### Added

**Core**
- Pure Python API with decorators
- Built-in HTTP server (no Flask/Django required)
- Simple ORM with dataclass models
- SQLite and PostgreSQL support

**IoT**
- Hardware-agnostic GPIO (Raspberry Pi, ESP32, Arduino)
- Sensor abstractions (motion, temperature, ultrasonic, moisture)
- Actuator classes (Motor, Light, Servo, Relay, Buzzer)
- Robot car and arm builders
- Security alarm system
- Smart home automation
- Garden watering automation
- Camera integration with motion detection

**AI**
- Voice assistant with GPT-4o
- Text-to-speech (OpenAI TTS)
- Speech recognition
- Computer vision with YOLO
- Natural language automation rules

**CLI**
- `ludwig new` with 9 project templates
- `ludwig dev` development server
- `ludwig run` file executor

### Changed

- Moved from `.ludwig` DSL to pure Python
- Moved from Laravel patterns to simple decorators
- New github organization: ludwig-framework

### Removed

- Custom `.ludwig` file format
- Artisan CLI (replaced with `ludwig` CLI)
- Framework-specific syntax

---

## [0.1.0] - 2025-06-25 (Legacy)

Initial release with Laravel-style syntax (deprecated).

---

## Contributing

When adding entries to this changelog:

1. Add entries under the `[Unreleased]` section
2. Use the format: `- Description of change`
3. Group changes by type (Added, Changed, Fixed, Removed)
4. Move entries to a versioned section when releasing
```markdown
### Added
- New embedded sensor support for temperature monitoring (#123)
- CLI command for generating robotics applications (#124)

### Fixed
- Fixed desktop layout issue on Windows (#125)
- Resolved import error in embedded framework (#126)
```
