<p align="center">
<img src="https://img.shields.io/badge/Telegram-%40sub__controller__bot-blue?style=flat-square" alt="https://t.me/sub_controller_bot/">
<img src="https://img.shields.io/badge/Docker%20Hub-controller--new-green?style=flat-square" alt="https://hub.docker.com/repository/docker/markushik/controller-new/">

<img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="https://opensource.org/licenses/MIT/">
<img src="https://img.shields.io/github/stars/Markushik/controller-new.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/stargazers">
<img src="https://img.shields.io/github/last-commit/Markushik/controller-new.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/">
<img src="https://img.shields.io/github/repo-size/Markushik/controller-new.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/">

<img src="https://github.com/Markushik/controller-new/actions/workflows/CI.yaml/badge.svg?style=flat-square" alt="https://github.com/Markushik/controller-new/actions/">
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
- [nats-py](https://github.com/nats-io/nats.py) - Python client for NATS
- [taskiq](https://github.com/taskiq-python/taskiq) – distributed task queue
- [dynaconf](https://github.com/dynaconf/dynaconf) – configuration management
- [loguru](https://github.com/Delgan/loguru) – simple (stupid) logging

### Auxiliary Libraries

- [lz4](https://github.com/lz4/lz4) – compression technology
- [ormsgpack](https://github.com/aviramha/ormsgpack) – msgpack serialization
- [orjson](https://github.com/ijl/orjson) – fast JSON serializer
- [markupsafe](https://github.com/pallets/markupsafe) – safely add untrusted strings to HTML
- [fluent.runtime](https://github.com/projectfluent/python-fluent) – localization / internationalization

## ⭐ Application Schema
[![application-schema.png](https://i.postimg.cc/YCg4LRKZ/application-schema.png)](https://github.com/Markushik/controller-new/)

## 🐘 Database Schema

[![database-scheme.png](https://i.postimg.cc/BbYFNnMz/database-scheme.png)](https://drawsql.app/teams/marqezs-team/diagrams/controller-new/)

## 🪛 Installation

### 🐳 Docker

**1. Clone the repository:**

```
git clone https://github.com/Markushik/controller-new.git
```

**2. Create file `.secrets.toml` in folder `configs` and fill data**

**3. Run the command:**

```
docker-compose up
```

### 💻 Default

**1. Clone the repository:**

```
git clone https://github.com/Markushik/controller-new.git
```

**2. Create file `.secrets.toml` in folder `configs` and fill data**

**3. Bring up PostgreSQL, Redis and NATS**

**4. First run the `taskiq` scripts:**

```
taskiq worker application.infrastructure.scheduler.tkq:broker --fs-discover --reload
```

```
taskiq scheduler application.infrastructure.scheduler.tkq:scheduler --fs-discover
```

**5. Second run the `bot`:**

```
python -m application.tgbot
```

## ✅ ToDo's

- Changing subscription options
- Renewal Subscription
- Common services table