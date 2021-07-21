#!/bin/bash

set -e

if [ "$WEB_SERVER_TYPE" = "gunicorn-async" ]; then
    run_command="gunicorn application:application --worker-class gevent --timeout 0"
elif [ "$WEB_SERVER_TYPE" = "gunicorn-threads" ]; then
    run_command="gunicorn application:application --worker-class gthread --timeout 0"
elif [ "$WEB_SERVER_TYPE" = "uwsgi" ]; then
    run_command="uwsgi uwsgi.ini --workers ${WEB_SERVER_WORKERS} --http-keepalive=${HTTP_KEEP_ALIVE}"
elif [ "$WEB_SERVER_TYPE" = "uwsgi-threads" ]; then
    run_command="uwsgi uwsgi.ini --workers ${WEB_SERVER_WORKERS} --enable-threads --threads ${WEB_SERVER_THREADS} --http-keepalive=${HTTP_KEEP_ALIVE}"
elif [ "$WEB_SERVER_TYPE" = "uwsgi-async" ]; then
    run_command="uwsgi uwsgi.ini --module patched:application --workers ${WEB_SERVER_WORKERS} --gevent ${WEB_SERVER_UWSGI_ASYNC_CORES} --http-keepalive=${HTTP_KEEP_ALIVE}"
fi

if [ "$EQ_NEW_RELIC_ENABLED" = "True" ]; then
    new_relic_run_command="NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program ${run_command}"
    eval "$new_relic_run_command"
else
    eval "$run_command"
fi
