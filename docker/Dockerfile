FROM python:3.11.1-alpine

WORKDIR .

COPY app ./app/
COPY configs ./configs/
COPY poetry.lock pyproject.toml ./

RUN pip3 install --no-cache-dir --root-user-action=ignore --upgrade pip \
 && pip3 install --no-cache-dir --root-user-action=ignore setuptools wheel \
 && pip3 install --no-cache-dir --root-user-action=ignore poetry

RUN poetry install --only main --no-root --no-interaction --no-ansi

EXPOSE 443
ENTRYPOINT ["poetry", "run", "python", "-m", "app.tgbot"]