FROM python:3.8-slim-buster

EXPOSE 5000

RUN apt update && apt install -y curl unzip libsnappy-dev build-essential jq

COPY . /runner
WORKDIR /runner

ENV WEB_SERVER gunicorn
ENV WEB_SERVER_WORKERS 3
ENV GUNICORN_KEEP_ALIVE 2
ENV GUNICORN_CMD_ARGS -c gunicorn_config.py
ENV WEB_SERVER_THREADS 10
ENV WEB_SERVER_ASYNC_CORES 10

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pip install pipenv==2018.11.26

RUN pipenv install --deploy --system
RUN make load-schemas
RUN make build

CMD ["sh", "run_app.sh"]
