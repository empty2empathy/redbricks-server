ARG PYTHON_VERSION=python3.8
FROM tiangolo/meinheld-gunicorn-flask:${PYTHON_VERSION} AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install --upgrade pip
RUN set -ex; \
    wget https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py -O get-poetry.py && \
    python get-poetry.py --yes && \
    rm -f get-poetry.py


FROM base AS environment
ENV MODULE_NAME="app"
ENV APP_MODULE="app:app"

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev --no-interaction --no-ansi


FROM environment AS deploy
COPY . /app
