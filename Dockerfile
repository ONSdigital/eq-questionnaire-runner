FROM python:3.13-slim-bookworm

EXPOSE 5000

# wkhtmltopdf is installed from the upstream packaging release rather than apt
ARG WKHTMLTOX_VERSION=0.12.6.1-3
ARG WKHTMLTOX_DISTRO=bookworm
ARG WKHTMLTOX_SHA256_AMD64=98ba0d157b50d36f23bd0dedf4c0aa28c7b0c50fcdcdc54aa5b6bbba81a3941d
ARG WKHTMLTOX_SHA256_ARM64=b6606157b27c13e044d0abbe670301f88de4e1782afca4f9c06a5817f3e03a9c
ARG TARGETARCH

RUN apt-get update && \
apt-get install -y --no-install-recommends \
curl unzip libsnappy-dev build-essential jq \
xfonts-base xfonts-75dpi fontconfig \
libjpeg62-turbo libxrender1 libxext6 && \
case "${TARGETARCH}" in \
amd64) WK_SHA256="${WKHTMLTOX_SHA256_AMD64}" ;; \
arm64) WK_SHA256="${WKHTMLTOX_SHA256_ARM64}" ;; \
esac && \
curl -fsSL -o /tmp/wkhtmltox.deb \
"https://github.com/wkhtmltopdf/packaging/releases/download/${WKHTMLTOX_VERSION}/wkhtmltox_${WKHTMLTOX_VERSION}.${WKHTMLTOX_DISTRO}_${TARGETARCH}.deb" && \
echo "EXPECTED=[${WK_SHA256}]" && \
echo "ACTUAL=[$(sha256sum /tmp/wkhtmltox.deb | cut -d' ' -f1)]" && \
test "$(sha256sum /tmp/wkhtmltox.deb | cut -d' ' -f1)" = "${WK_SHA256}" && \
apt-get install -y --no-install-recommends /tmp/wkhtmltox.deb && \
rm -f /tmp/wkhtmltox.deb && \
rm -rf /var/lib/apt/lists/* && \
wkhtmltopdf --version | grep -qi "with patched qt"

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
