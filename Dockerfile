FROM --platform=$TARGETPLATFORM python:3.13-slim-bookworm

ARG TARGETPLATFORM
RUN echo "TARGETPLATFORM=${TARGETPLATFORM}"

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
# POC from arm64 Mac so don't use my lock file
# COPY Pipfile.lock Pipfile.lock

RUN groupadd -r appuser && useradd -r -g appuser -u 9000 appuser && chown -R appuser:appuser .
# RUN pip install pipenv==2018.11.26 && pipenv install --deploy --system && \
# let it recreate lock file while POC and don't translate
RUN pip install pipenv==2023.12.1 && pipenv install --system
RUN make load-schemas
# ...the github release only exists for 32.1.3-census
# https://github.com/ONSdigital/design-system/releases/tag/32.1.3-census
RUN echo 32.1.3-census > .design-system-version
RUN make load-design-system-templates
RUN grep "set release_version =" /runner/templates/layout/_template.njk
# ...but the CDN only has 32.2.2-census
# https://cdn.eq.gcp.onsdigital.uk/design-system/32.2.2-census/css/census.css
RUN sed -i "s/32\.1\.3-census/32.2.2-census/g" /runner/templates/layout/_template.njk
RUN grep "set release_version =" /runner/templates/layout/_template.njk
USER appuser

CMD ["sh", "run_app.sh"]
