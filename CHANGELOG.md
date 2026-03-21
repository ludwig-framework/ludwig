# Changelog

All notable changes to Ludwig will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Planned
- Plugin system
- Visual project editor
- Package manager

## [0.1.0] - 2025-06-25

### Added
- Web framework with pure Python HTTP server
- Laravel-style Artisan CLI
- ORM with Eloquent-style syntax
- JWT authentication system
- Desktop application framework
- Embedded/IoT templates
- Project generators for all platforms
- TailwindCSS integration
- Interactive REPL

### Technical
- Python 3.9+ support
- MIT License
- Cross-platform compatibility

#### Fixed
- Bug fixes

#### Security
- Security improvements

---

## Contributing

When adding entries to this changelog:

1. Add entries under the `[Unreleased]` section
2. Use the format: `- Description of change (#PR-number)`
3. Group changes by type (Added, Changed, Fixed, etc.)
4. Move entries to a versioned section when releasing
5. Follow [Conventional Commits](https://www.conventionalcommits.org/) format

Example entry:
```markdown
### Added
- New embedded sensor support for temperature monitoring (#123)
- CLI command for generating robotics applications (#124)

### Fixed
- Fixed desktop layout issue on Windows (#125)
- Resolved import error in embedded framework (#126)
```
