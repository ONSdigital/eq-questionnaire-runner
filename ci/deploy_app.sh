#!/usr/bin/env bash
set -exo pipefail

REGION="${REGION:=europe-west2}"
CPU="${CPU:=4}"
MEMORY="${MEMORY:=4G}"
CONCURRENCY="${CONCURRENCY:=80}"
CDN_URL="${CDN_URL:=https://cdn.census.gov.uk}"
NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME:=}"
NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY:=}"
COOKIE_SETTINGS_URL="${COOKIE_SETTINGS_URL:=#}"
ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL:=#}"
ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED:=False}"
ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS="${ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS:=10}"
WEB_SERVER_TYPE="${WEB_SERVER_TYPE:=gunicorn-threads}"
WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS:=7}"
WEB_SERVER_THREADS="${WEB_SERVER_THREADS:=10}"
WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES:=10}"
DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC:=True}"
MIN_INSTANCES="${MIN_INSTANCES:=1}"
MAX_INSTANCES="${MAX_INSTANCES:=1}"
EQ_NEW_RELIC_ENABLED="${EQ_NEW_RELIC_ENABLED:=False}"
EQ_SECRETS_FILE="${EQ_SECRETS_FILE:=/secrets/secrets.yml}"
EQ_KEYS_FILE="${EQ_KEYS_FILE:=/keys/keys.yml}"
EQ_STORAGE_BACKEND="${EQ_STORAGE_BACKEND:=datastore}"
EQ_ENABLE_SECURE_SESSION_COOKIE="${EQ_ENABLE_SECURE_SESSION_COOKIE:=True}"
EQ_RABBITMQ_ENABLED="${EQ_RABBITMQ_ENABLED:=False}"
EQ_ENABLE_HTML_MINIFY="${EQ_ENABLE_HTML_MINIFY:=False}"
EQ_RABBITMQ_HOST="${EQ_RABBITMQ_HOST:=rabbit}"
EQ_RABBITMQ_HOST_SECONDARY="${EQ_RABBITMQ_HOST_SECONDARY:=rabbit}"
EQ_QUESTIONNAIRE_STATE_TABLE_NAME="${EQ_QUESTIONNAIRE_STATE_TABLE_NAME:=questionnaire-state}"
EQ_SESSION_TABLE_NAME="${EQ_SESSION_TABLE_NAME:=eq-session}"
EQ_USED_JTI_CLAIM_TABLE_NAME="${EQ_USED_JTI_CLAIM_TABLE_NAME:=used-jti-claim}"
EQ_SUBMISSION_BACKEND="${EQ_SUBMISSION_BACKEND:=gcs}"
EQ_FEEDBACK_BACKEND="${EQ_FEEDBACK_BACKEND:=gcs}"
EQ_PUBLISHER_BACKEND="${EQ_PUBLISHER_BACKEND:=pubsub}"
EQ_FULFILMENT_TOPIC_ID="${EQ_FULFILMENT_TOPIC_ID:=eq-fulfilment-topic}"
EQ_INDIVIDUAL_RESPONSE_LIMIT="${EQ_INDIVIDUAL_RESPONSE_LIMIT:=75}"
EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE="${EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE:=2021-04-28T02:00:00+00:00}"
EQ_FEEDBACK_LIMIT="${EQ_FEEDBACK_LIMIT:=10}"
HTTP_KEEP_ALIVE="${HTTP_KEEP_ALIVE:=650}"
EQ_GOOGLE_TAG_MANAGER_ID="${EQ_GOOGLE_TAG_MANAGER_ID:=}"
EQ_GOOGLE_TAG_MANAGER_AUTH="${EQ_GOOGLE_TAG_MANAGER_AUTH:=}"
CDN_ASSETS_PATH="${CDN_ASSETS_PATH:=/design-system}"
CONFIRMATION_EMAIL_LIMIT="${CONFIRMATION_EMAIL_LIMIT:=10}"
EQ_SUBMISSION_CONFIRMATION_BACKEND="${EQ_SUBMISSION_CONFIRMATION_BACKEND:=cloud-tasks}"


gcloud beta run deploy eq-questionnaire-runner \
    --project="${PROJECT_ID}" --region="${REGION}" --concurrency="${CONCURRENCY}" --min-instances="${MIN_INSTANCES}" --max-instances="${MAX_INSTANCES}" \
    --port=5000 --cpu="${CPU}" --memory="${MEMORY}" \
    --image="${DOCKER_REGISTRY}/eq-questionnaire-runner:${IMAGE_TAG}" --platform=managed --allow-unauthenticated \
    --set-secrets EQ_REDIS_HOST="redis-host:latest" \
    --set-secrets EQ_REDIS_PORT="redis-port:latest" \
    --set-secrets "/keys/keys.yml"="keys:latest" \
    --set-secrets "/secrets/secrets.yml"="secrets:latest" \
    --set-env-vars EQ_STORAGE_BACKEND="${EQ_STORAGE_BACKEND}" \
    --set-env-vars EQ_ENABLE_SECURE_SESSION_COOKIE="${EQ_ENABLE_SECURE_SESSION_COOKIE}" \
    --set-env-vars EQ_SECRETS_FILE="${EQ_SECRETS_FILE}" \
    --set-env-vars EQ_KEYS_FILE="${EQ_KEYS_FILE}" \
    --set-env-vars EQ_RABBITMQ_ENABLED="${EQ_RABBITMQ_ENABLED}" \
    --set-env-vars EQ_ENABLE_HTML_MINIFY="${EQ_ENABLE_HTML_MINIFY}" \
    --set-env-vars EQ_RABBITMQ_HOST="${EQ_RABBITMQ_HOST}" \
    --set-env-vars EQ_RABBITMQ_HOST_SECONDARY="${EQ_RABBITMQ_HOST_SECONDARY}" \
    --set-env-vars EQ_QUESTIONNAIRE_STATE_TABLE_NAME="${EQ_QUESTIONNAIRE_STATE_TABLE_NAME}" \
    --set-env-vars EQ_SESSION_TABLE_NAME="${EQ_SESSION_TABLE_NAME}" \
    --set-env-vars EQ_USED_JTI_CLAIM_TABLE_NAME="${EQ_USED_JTI_CLAIM_TABLE_NAME}" \
    --set-env-vars EQ_SUBMISSION_BACKEND="${EQ_SUBMISSION_BACKEND}" \
    --set-env-vars EQ_FEEDBACK_BACKEND="${EQ_SUBMISSION_BACKEND}" \
    --set-env-vars EQ_PUBLISHER_BACKEND="${EQ_PUBLISHER_BACKEND}" \
    --set-env-vars EQ_FULFILMENT_TOPIC_ID="${EQ_FULFILMENT_TOPIC_ID}" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_LIMIT="${EQ_INDIVIDUAL_RESPONSE_LIMIT}" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE="${EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE}" \
    --set-env-vars EQ_FEEDBACK_LIMIT="${EQ_FEEDBACK_LIMIT}" \
    --set-env-vars WEB_SERVER_TYPE="${WEB_SERVER_TYPE}" \
    --set-env-vars WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS}" \
    --set-env-vars WEB_SERVER_THREADS="${WEB_SERVER_THREADS}" \
    --set-env-vars WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES}" \
    --set-env-vars DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC}" \
    --set-env-vars HTTP_KEEP_ALIVE="${HTTP_KEEP_ALIVE}" \
    --set-env-vars EQ_GCS_SUBMISSION_BUCKET_ID="${PROJECT_ID}-submission" \
    --set-env-vars EQ_GCS_FEEDBACK_BUCKET_ID="${PROJECT_ID}-feedback" \
    --set-env-vars EQ_GOOGLE_TAG_MANAGER_ID="${EQ_GOOGLE_TAG_MANAGER_ID}" \
    --set-env-vars EQ_GOOGLE_TAG_MANAGER_AUTH="${EQ_GOOGLE_TAG_MANAGER_AUTH}" \
    --set-env-vars COOKIE_SETTINGS_URL="${COOKIE_SETTINGS_URL}" \
    --set-env-vars CDN_URL="${CDN_URL}" \
    --set-env-vars CDN_ASSETS_PATH="${CDN_ASSETS_PATH}" \
    --set-env-vars ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS="${ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS}" \
    --set-env-vars EQ_NEW_RELIC_ENABLED="${EQ_NEW_RELIC_ENABLED}" \
    --set-env-vars NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY}" \
    --set-env-vars NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME}" \
    --set-env-vars CONFIRMATION_EMAIL_LIMIT="${CONFIRMATION_EMAIL_LIMIT}" \
    --set-env-vars EQ_SUBMISSION_CONFIRMATION_BACKEND="${EQ_SUBMISSION_CONFIRMATION_BACKEND}" \
    --vpc-connector="redis-vpc" \
    --service-account="cloud-run@${PROJECT_ID}.iam.gserviceaccount.com"
