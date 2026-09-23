# Stage 1: wkhtmltopdf from Debian 12 (bookworm).

# Debian 13 no longer packages wkhtmltopdf, and upstream's patched-Qt build
# can't render the Design System CSS. This copies Debian 12's apt build,
# the Qt plugins it needs, and their libraries. glibc and the C++ runtime
# are skipped so Debian 13's versions are used.

FROM python:3.13-slim-bookworm AS wkhtmltopdf
RUN apt-get update && \
    apt-get install -y --no-install-recommends wkhtmltopdf && \
    mkdir -p /opt/wkhtmltopdf/lib /opt/wkhtmltopdf/plugins && \
    cp /usr/bin/wkhtmltopdf /opt/wkhtmltopdf/ && \
    mkdir -p /opt/wkhtmltopdf/plugins/platforms && \
    cp /usr/lib/*-linux-gnu/qt5/plugins/platforms/libqoffscreen.so /opt/wkhtmltopdf/plugins/platforms/ && \
    cp -r /usr/lib/*-linux-gnu/qt5/plugins/imageformats /opt/wkhtmltopdf/plugins/ && \
    { ldd /usr/bin/wkhtmltopdf; find /opt/wkhtmltopdf/plugins -name '*.so' -exec ldd {} \; ; } \
      | awk '/=> \// {print $3}' | sort -u \
      | grep -vE '/(libc|libm|libpthread|libdl|librt|libresolv|libstdc\+\+|libgcc_s)\.so|ld-linux' \
      | xargs -I{} cp -L {} /opt/wkhtmltopdf/lib/

# Stage 2: Runner on Debian 13 (trixie).
FROM python:3.13-slim-trixie

EXPOSE 5000

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl unzip libsnappy-dev build-essential jq \
        fontconfig fonts-dejavu-core xfonts-base xfonts-75dpi && \
    rm -rf /var/lib/apt/lists/*

COPY --from=wkhtmltopdf /opt/wkhtmltopdf /opt/wkhtmltopdf

# Wrapper so only wkhtmltopdf uses the copied Debian 12 libraries.
# The build fails if any library is missing.
RUN printf '%s\n' \
        '#!/bin/sh' \
        'export LD_LIBRARY_PATH=/opt/wkhtmltopdf/lib' \
        'export QT_PLUGIN_PATH=/opt/wkhtmltopdf/plugins' \
        'export QT_QPA_PLATFORM=offscreen' \
        'exec /opt/wkhtmltopdf/wkhtmltopdf "$@"' \
    > /usr/local/bin/wkhtmltopdf && \
    chmod +x /usr/local/bin/wkhtmltopdf && \
    ! LD_LIBRARY_PATH=/opt/wkhtmltopdf/lib ldd /opt/wkhtmltopdf/wkhtmltopdf | grep "not found" && \
    wkhtmltopdf --version

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
