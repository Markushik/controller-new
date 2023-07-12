FROM python:3.11.4-slim-buster AS builder

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_ROOT_USER_ACTION=ignore

ENV \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

WORKDIR .

COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip \
 && pip3 install  setuptools wheel \
 && pip3 install poetry
RUN poetry install --only main --no-root


FROM debian AS runtime

WORKDIR ./application/

COPY application ./application/
COPY configs ./configs/
COPY alembic.ini alembic.ini

EXPOSE 443
ENTRYPOINT ["poetry", "run", "python3", "-m", "application.tgbot"]
