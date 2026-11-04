# Contributing to Ludwig

Thanks for your interest in contributing.

Ludwig v2 is **pure Python** (decorators, no custom DSL). Ignore any older docs that mention `.ludwig` files, Artisan, or a custom language — those were removed in 2.0.

## Development Setup

```bash
git clone https://github.com/ludwig-framework/ludwig.git
cd ludwig
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

The PyPI project named `ludwig` is a **different** machine-learning toolkit. Install this framework from GitHub (or an editable checkout) until a distinct package name is published.

## Running Tests

```bash
pytest
pytest --cov=ludwig
```

CLI templates are compiled in the test suite. If you add a `ludwig new` template, add it to `cli.py` and make sure `pytest tests/test_templates.py` passes.

## Code Style

```bash
ruff check ludwig/ tests/
black ludwig/ tests/
mypy ludwig/
```

CI currently fails the job on pytest and on critical Ruff rules (`E9`, `F63`, `F7`, `F82`). Full style cleanup is welcome but not required for a first PR.

## Project Structure

```
ludwig/
├── ludwig/
│   ├── __init__.py      # Main exports
│   ├── core.py          # App, Config
│   ├── web.py           # HTTP server
│   ├── db.py            # Database, Model
│   ├── cli.py           # CLI + project templates
│   ├── iot/             # GPIO, sensors, robots, home, garden
│   └── ai/              # Assistant, Vision, Automator
├── docs/
├── tests/
└── templates/           # Standalone examples (keep in sync with cli.py)
```

## Pull Requests

1. Fork and create a branch (`fix/door-lock-is-on`, `docs/contributing-v2`)
2. Make the change
3. Add or update tests
4. Run pytest
5. Open a PR

## What to Contribute

- **Bug fixes** — especially templates and public APIs that do not match
- **Documentation** — examples, tutorials, typo fixes
- **Tests** — HTTP routing, IoT simulation, CLI template compile
- **IoT** — sensors, actuators, more accurate simulation
- **AI** — local-model defaults, provider fallbacks

## Reporting Issues

Include:

- Ludwig version (`python -m ludwig.cli version`)
- Python version
- Platform (Raspberry Pi, macOS, etc.)
- Steps to reproduce
- Expected vs actual behavior

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.
