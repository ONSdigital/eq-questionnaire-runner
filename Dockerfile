FROM python:3.11-slim-bullseye

EXPOSE 5000

RUN apt update && apt install -y curl unzip libsnappy-dev build-essential jq wkhtmltopdf

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
RUN pip install "poetry==1.7.1"| python3 - && poetry install && make build

USER appuser

CMD ["sh", "run_app.sh"]
