# --- Help Menu ---
.PHONY: help
help:
	@echo Usage: make [COMMAND]
	@echo ㅤ
	@echo Available commands:
	@echo  ruff			Run ruff check
	@echo  lint			Reformat code
	@echo  generate		Generate alembic migrations
	@echo  migrate		Migrate with alembic

# --- Linters & Checkers ---
.PHONY: ruff
ruff:
	ruff . --fix

.PHONY: lint
lint: ruff

# --- Alembic Utils ---
.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head