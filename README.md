<p align="center">
<img src="https://img.shields.io/badge/License-MIT-136F63.svg?style=flat-square" alt="https://opensource.org/licenses/MIT/">
<img src="https://img.shields.io/github/last-commit/Markushik/controller-new.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/">
<img src="https://github.com/Markushik/controller-new/actions/workflows/CI.yaml/badge.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/actions/">
<img src="https://img.shields.io/badge/Docker%20Hub-controller--new-136F63?style=flat-square" alt="https://hub.docker.com/repository/docker/markushik/controller-new/">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json?style=flat-square" alt="https://github.com/astral-sh/ruff/">

> **controller** — probably the best bot for a reminder of the end of the subscription.

## 🚀 Stack

### Technologies

- [Python](https://www.python.org/) – programming language
- [Redis](https://redis.io/) – persistent storage
- [PostgreSQL](https://www.postgresql.org/) – best relational database
- [NATS JetStream](https://nats.io/) – communications system for digital systems
- [Docker](https://www.docker.com/) – containerization platform

### Frameworks & Libraries

- [aiogram](https://github.com/aiogram/aiogram) – async framework for Telegram Bot API
- [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) – developing interactive messages
- [asyncpg](https://github.com/MagicStack/asyncpg) – fast client for PostgreSQL Database
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) – SQL toolkit & ORM
- [alembic](https://github.com/sqlalchemy/alembic) – migration tool
- [taskiq](https://github.com/taskiq-python/taskiq) – distributed task queue
- [dynaconf](https://github.com/dynaconf/dynaconf) – configuration management
- [loguru](https://github.com/Delgan/loguru) – simple logging

## 🐘 Database Models

[![draw-SQL-controller-new-export-2023-06-24.png](https://i.postimg.cc/dV4hPNdG/draw-SQL-controller-new-export-2023-06-24.png)](https://postimg.cc/fVSzYK8b)

## 🐋 Deployment

**1. Clone the repository**

```
git clone https://github.com/Markushik/controller-new.git
```

**2. Create file `.secrets.toml` in folder configs and fill data**

**3. Run the command**

```
docker-compose up
```