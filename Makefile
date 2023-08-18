# --- Help Menu ---
.PHONY: help
help:
	@echo Usage: make [COMMAND]
	@echo  ㅤ
	@echo Available commands:
	@echo  ruffㅤ		Run ruff check
	@echo  lintㅤ		Reformat code
	@echo  generateㅤ	Generate alembic migrations
	@echo  migrateㅤ	Migrate with alembic

# --- Linters & Checkers ---
.PHONY: ruff
ruff:
	ruff .

.PHONY: lint
lint: ruff

# --- Alembic Utils ---
.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head