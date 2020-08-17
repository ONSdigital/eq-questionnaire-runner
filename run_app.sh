#!/bin/bash

set -eu

web_server=${WEB_SERVER:-gunicorn}

if [ "$web_server" = "gunicorn" ]; then
    run_command="gunicorn application:application"
elif [ "$web_server" = "uwsgi" ]; then
    run_command="uwsgi uwsgi.ini --workers ${WEB_SERVER_WORKERS}"
elif [ "$web_server" = "uwsgi-threads" ]; then
    run_command="uwsgi uwsgi.ini --workers ${WEB_SERVER_WORKERS} --enable-threads --threads ${WEB_SERVER_THREADS}"
elif [ "$web_server" = "uwsgi-async" ]; then
    run_command="uwsgi uwsgi.ini --module patched:application --workers ${WEB_SERVER_WORKERS} --single-interpreter --gevent ${WEB_SERVER_ASYNC_CORES}"
fi

if [ "$EQ_NEW_RELIC_ENABLED" = "True" ]; then
    new_relic_run_command="NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program ${run_command}"
    eval "$new_relic_run_command"
else
    eval "$run_command"
fi
