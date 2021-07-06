#!/usr/bin/env bash
set -exo pipefail

REGION="${REGION:=europe-west2}"
CDN_URL="${CDN_URL:=https://cdn.census.gov.uk}"
NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME:=}"
NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY:=}"
COOKIE_SETTINGS_URL="${COOKIE_SETTINGS_URL:=#}"
ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL:=#}"
ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED:=False}"
EQ_NEW_RELIC_ENABLED="${EQ_NEW_RELIC_ENABLED:=False}"
EQ_SECRETS_FILE="${EQ_SECRETS_FILE:=/secrets/secrets.yml}"
EQ_KEYS_FILE="${EQ_KEYS_FILE:=/keys/keys.yml}"
WEB_SERVER_TYPE="${WEB_SERVER_TYPE:=gunicorn-threads}"
WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS:=7}"
WEB_SERVER_THREADS="${WEB_SERVER_THREADS:=10}"
WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES:=10}"
DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC:=True}"
MIN_INSTANCES="${MIN_INSTANCES:=1}"
MAX_INSTANCES="${MAX_INSTANCES:=1}"


gcloud beta run deploy eq-questionnaire-runner \
    --project="${PROJECT_ID}" --region="${REGION}" --concurrency=49 --min-instances="${MIN_INSTANCES}" --max-instances="${MAX_INSTANCES}" \
    --port=5000 --cpu=4 --memory=4G \
    --image="${DOCKER_REGISTRY}/eq-questionnaire-runner:${IMAGE_TAG}" --platform=managed --allow-unauthenticated \
    --set-secrets EQ_REDIS_HOST="redis-host:latest" \
    --set-secrets EQ_REDIS_PORT="redis-port:latest" \
    --set-secrets "/keys/keys.yml"="keys:latest" \
    --set-secrets "/secrets/secrets.yml"="secrets:latest" \
    --set-env-vars EQ_STORAGE_BACKEND="datastore" \
    --set-env-vars EQ_ENABLE_SECURE_SESSION_COOKIE="True" \
    --set-env-vars EQ_SECRETS_FILE="${EQ_SECRETS_FILE}" \
    --set-env-vars EQ_KEYS_FILE="${EQ_KEYS_FILE}" \
    --set-env-vars EQ_RABBITMQ_ENABLED="False" \
    --set-env-vars EQ_ENABLE_HTML_MINIFY="False" \
    --set-env-vars EQ_RABBITMQ_HOST="rabbit" \
    --set-env-vars EQ_RABBITMQ_HOST_SECONDARY="rabbit" \
    --set-env-vars EQ_QUESTIONNAIRE_STATE_TABLE_NAME="questionnaire-state" \
    --set-env-vars EQ_SESSION_TABLE_NAME="eq-session" \
    --set-env-vars EQ_USED_JTI_CLAIM_TABLE_NAME="used-jti-claim" \
    --set-env-vars EQ_SUBMISSION_BACKEND="gcs" \
    --set-env-vars EQ_FEEDBACK_BACKEND="gcs" \
    --set-env-vars EQ_PUBLISHER_BACKEND="pubsub" \
    --set-env-vars EQ_FULFILMENT_TOPIC_ID="eq-fulfilment-topic" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_LIMIT="75" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE="2021-04-28T02:00:00+00:00" \
    --set-env-vars EQ_FEEDBACK_LIMIT="10" \
    --set-env-vars WEB_SERVER_TYPE="${WEB_SERVER_TYPE}" \
    --set-env-vars WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS}" \
    --set-env-vars WEB_SERVER_THREADS="${WEB_SERVER_THREADS}" \
    --set-env-vars WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES}" \
    --set-env-vars DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC}" \
    --set-env-vars HTTP_KEEP_ALIVE="650" \
    --set-env-vars EQ_GCS_SUBMISSION_BUCKET_ID="${PROJECT_ID}-survey-runner-submission" \
    --set-env-vars EQ_GCS_FEEDBACK_BUCKET_ID="${PROJECT_ID}-feedback" \
    --set-env-vars EQ_GOOGLE_TAG_MANAGER_ID="" \
    --set-env-vars EQ_GOOGLE_TAG_MANAGER_AUTH="" \
    --set-env-vars COOKIE_SETTINGS_URL="${COOKIE_SETTINGS_URL}" \
    --set-env-vars CDN_URL="${CDN_URL}" \
    --set-env-vars CDN_ASSETS_PATH="/design-system" \
    --set-env-vars ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS="10" \
    --set-env-vars EQ_NEW_RELIC_ENABLED="${EQ_NEW_RELIC_ENABLED}" \
    --set-env-vars NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY}" \
    --set-env-vars NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME}" \
    --set-env-vars CONFIRMATION_EMAIL_LIMIT="10" \
    --set-env-vars EQ_SUBMISSION_CONFIRMATION_BACKEND="cloud-tasks" \
    --vpc-connector="redis-vpc" \
    --service-account="cloud-run@${PROJECT_ID}.iam.gserviceaccount.com"
