FROM python:3.11-slim as requirements-stage

WORKDIR /tmp

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.7.1

RUN pip install --upgrade pip && \
    pip install "poetry==$POETRY_VERSION"

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --extras migrations


FROM python:3.11-slim-buster

WORKDIR /opt/migrations

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get install -y --no-install-recommends gettext

COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ./migrations ./migrations
COPY ./src/db/entities ./src/db/entities
COPY ./src/configs ./src/configs
COPY ./src/utils/__init__.py ./src/utils/__init__.py
COPY ./src/utils/settings.py ./src/utils/settings.py
COPY ./src/utils/sqlalchemy.py ./src/utils/sqlalchemy.py
COPY ./alembic.ini ./

RUN sed -i 's/\r$//g'  ./migrations/entrypoint.sh && \
    chmod +x  ./migrations/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["sh", "migrations/entrypoint.sh"]