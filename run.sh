#!/bin/bash

if [ -n "$SECRETS_S3_BUCKET" ]; then
    echo "Load Secrets from S3 Bucket [$SECRETS_S3_BUCKET]"
    aws s3 sync s3://"$SECRETS_S3_BUCKET"/ /secrets
fi

GUNICORN_OPTIONS = "-w $GUNICORN_WORKERS --keep-alive $GUNICORN_KEEP_ALIVE --worker-class gevent -b 0.0.0.0:5000 application:application"

if [ "$EQ_NEW_RELIC_ENABLED" == "True" ]; then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn "$GUNICORN_OPTIONS"
else
    gunicorn "$GUNICORN_OPTIONS"
fi
