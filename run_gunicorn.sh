#!/bin/bash

if [ -n "$SECRETS_S3_BUCKET" ]; then
    echo "Load Secrets from S3 Bucket [$SECRETS_S3_BUCKET]"
    aws s3 sync "s3://$SECRETS_S3_BUCKET/" /secrets
fi

if [ "$EQ_NEW_RELIC_ENABLED" == "True" ]; then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn application:application
else
    gunicorn application:application
fi
