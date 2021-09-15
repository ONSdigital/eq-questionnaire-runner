FROM python:3.9-slim-buster

EXPOSE 5000

RUN apt update && apt install -y curl unzip libsnappy-dev build-essential jq

COPY . /runner
WORKDIR /runner

ENV WEB_SERVER_TYPE gunicorn-async
ENV WEB_SERVER_WORKERS 3
ENV WEB_SERVER_THREADS 10
ENV WEB_SERVER_UWSGI_ASYNC_CORES 10
ENV HTTP_KEEP_ALIVE 2
ENV GUNICORN_CMD_ARGS -c gunicorn_config.py

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN groupadd -r appuser && useradd -r -g appuser -u 9000 appuser && chown -R appuser:appuser .
RUN pip install pipenv==2018.11.26 && pipenv install --deploy --system && make build

USER appuser

CMD ["sh", "run_app.sh"]
