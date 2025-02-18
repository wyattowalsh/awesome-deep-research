# Makefile for awesome-deep-research
# Requires: uv, Python (version in .python-version)

.ONESHELL:
.DEFAULT_GOAL := help

# https://www.gnu.org/prep/standards/html_node/Makefile-Basics.html#Makefile-Basics
SHELL := /bin/bash
PYTHON_VERSION := $(shell cat .python-version)
VENV := .venv
LOGS_DIR := logs

.PHONY: help setup clean format lint test update-stars update-table all

help:  ## Display this help message
	@echo "awesome-deep-research Makefile"
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*##"; printf "\033[36m\033[0m"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development Setup

setup: ## Initialize development environment
	@echo "🔧 Setting up development environment..."
	@mkdir -p $(LOGS_DIR)
	@command -v uv >/dev/null 2>&1 || { echo "⚠️  uv is required but not installed. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	@echo "✨ Installing dependencies..."
	@uv venv
	@uv pip install --upgrade pip
	@uv add .
	@uv sync
	@echo "✨ Setup complete"

clean: ## Clean up generated files and caches
	@echo "🧹 Cleaning up..."
	@rm -rf $(LOGS_DIR)/* .coverage .pytest_cache .mypy_cache .ruff_cache __pycache__ */__pycache__ *.egg-info
	@echo "✨ Cleanup complete"

##@ Code Quality

format: ## Format code using isort, autoflake, and yapf
	@echo "🎨 Formatting code..."
	@uv sync --group format
	@uv run isort scripts/ tests/
	@uv run autoflake --recursive scripts/ tests/
	@uv run yapf -i --recursive scripts/ tests/
	@echo "✨ Code formatting complete"

lint: ## Run all linters (ruff, mypy, pylint)
	@echo "🔍 Running linters..."
	@uv sync --group lint
	@uv run ruff check scripts/ tests/
	@uv run mypy scripts/ tests/
	@uv run pylint scripts/ tests/
	@echo "✨ Linting complete"

test: ## Run tests with pytest
	@echo "🧪 Running tests..."
	@mkdir -p $(LOGS_DIR)
	@uv sync --group test
	@uv run pytest tests/
	@echo "✨ Tests complete"

##@ Data Updates

update-stars: ## Update GitHub star counts
	@echo "⭐ Updating star counts..."
	@python scripts/update_stars.py
	@echo "✨ Star counts updated"

update-table: ## Update README table
	@echo "📊 Updating README table..."
	@python scripts/update_readme.py
	@echo "✨ Table updated"

##@ CI/CD

ci: format lint test  ## Run all CI checks (format, lint, test)
	@echo "✅ All CI checks passed"

all: setup ci update-stars update-table  ## Run complete workflow (setup, ci, updates)
	@echo "🎉 Complete workflow finished successfully"