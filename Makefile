# Ludwig Framework Makefile

.PHONY: help install install-dev test lint format clean build

help: ## Show this help message
	@echo "Ludwig Framework - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Ludwig
	pip install -e .

install-dev: ## Install with development dependencies
	pip install -e ".[dev]"

install-all: ## Install with all optional dependencies
	pip install -e ".[all,dev]"

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=ludwig --cov-report=html

lint: ## Run linting
	ruff check ludwig/

format: ## Format code
	black ludwig/
	ruff check ludwig/ --fix

typecheck: ## Run type checking
	mypy ludwig/ --ignore-missing-imports

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	python -m build

publish-test: ## Publish to TestPyPI
	python -m twine upload --repository testpypi dist/*

publish: ## Publish to PyPI
	python -m twine upload dist/*

create-web: ## Create a sample web project
	./bin/ludwig-setup sample_web web

create-desktop: ## Create a sample desktop project
	./bin/ludwig-setup sample_desktop desktop

# Development commands
run-examples: ## Run example applications
	@echo "Running desktop calculator example..."
	python src/cli/artisan.py run examples/desktop/mycalculator_app.ludwig

dev-setup: install-dev ## Complete development setup
	@echo "Ludwig development environment ready!"
	@echo "Try: make shell"
	@echo "Or:  make create-web"
