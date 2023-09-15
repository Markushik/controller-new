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
	@echo  worker		Run taskiq worker script
	@echo  scheduler	RUN taskiq scheduler script

# --- Linters & Checkers ---
.PHONY: ruff
ruff:
	poetry run ruff . --fix

.PHONY: lint
lint: ruff

# --- Alembic Utils ---
.PHONY: generate
generate:
	poetry run alembic revision --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head

# --- Taskiq Scripts ---
.PHONY: worker
worker:
	poetry run taskiq worker application.infrastructure.scheduler.tkq:broker --fs-discover --reload --max-async-tasks -1

.PHONY: scheduler
scheduler:
	poetry run taskiq scheduler application.infrastructure.scheduler.tkq:scheduler --fs-discover
