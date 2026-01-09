FROM python:3.13-slim-bookworm

EXPOSE 5000

RUN apt update && apt install -y \
    curl unzip jq \
    build-essential pkg-config \
    libsnappy-dev libpq-dev libffi-dev \
    wkhtmltopdf \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
    libcairo2-dev

COPY . /runner
WORKDIR /runner

ENV WEB_SERVER_TYPE gunicorn-async
ENV WEB_SERVER_WORKERS 3
ENV WEB_SERVER_THREADS 10
ENV WEB_SERVER_UWSGI_ASYNC_CORES 10
ENV HTTP_KEEP_ALIVE 2
ENV GUNICORN_CMD_ARGS -c gunicorn_config.py

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN groupadd -r appuser && useradd -r -g appuser -u 9000 appuser && chown -R appuser:appuser .
RUN pip install "poetry==2.1.2" && \
    poetry config virtualenvs.create false && \
    poetry install --only main && \
    make build

USER appuser

CMD ["sh", "run_app.sh"]
