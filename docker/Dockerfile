FROM python:3.11.1-slim-buster as builder

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_ROOT_USER_ACTION=ignore

ENV \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

WORKDIR .

COPY app ./app/
COPY configs ./configs/
COPY poetry.lock pyproject.toml ./

RUN pip3 install --upgrade pip \
 && pip3 install  setuptools wheel \
 && pip3 install poetry

RUN poetry install --only main --no-root

EXPOSE 443
ENTRYPOINT ["poetry", "run", "python", "-m", "app.tgbot"]