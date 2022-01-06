#!/usr/bin/env bash
set -exo pipefail

if [[ -z "$PROJECT_ID" ]]; then
  echo "PROJECT_ID not provided"
  exit 1
fi

if [[ -z "$DOCKER_REGISTRY" ]]; then
  echo "DOCKER_REGISTRY not provided"
  exit 1
fi

if [[ -z "$IMAGE_TAG" ]]; then
  echo "IMAGE_TAG not provided"
  exit 1
fi


REGION="${REGION:=europe-west2}"

CONCURRENCY="${CONCURRENCY:=80}"
MIN_INSTANCES="${MIN_INSTANCES:=1}"
MAX_INSTANCES="${MAX_INSTANCES:=1}"
CPU="${CPU:=4}"
MEMORY="${MEMORY:=4G}"

WEB_SERVER_TYPE="${WEB_SERVER_TYPE:=gunicorn-threads}"
WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS:=7}"
WEB_SERVER_THREADS="${WEB_SERVER_THREADS:=10}"
WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES:=10}"
HTTP_KEEP_ALIVE="${HTTP_KEEP_ALIVE:=650}"

EQ_KEYS_FILE="/keys/keys.yml"
EQ_SECRETS_FILE="/secrets/secrets.yml"
DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC:=True}"
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
EQ_SUBMISSION_CONFIRMATION_BACKEND="${EQ_SUBMISSION_CONFIRMATION_BACKEND:=cloud-tasks}"
EQ_FULFILMENT_TOPIC_ID="${EQ_FULFILMENT_TOPIC_ID:=eq-fulfilment-topic}"
EQ_INDIVIDUAL_RESPONSE_LIMIT="${EQ_INDIVIDUAL_RESPONSE_LIMIT:=75}"
EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE="${EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE:=2021-04-28T02:00:00+00:00}"
EQ_FEEDBACK_LIMIT="${EQ_FEEDBACK_LIMIT:=10}"
EQ_GCS_SUBMISSION_BUCKET_ID="${PROJECT_ID}-submission"
EQ_GCS_FEEDBACK_BUCKET_ID="${PROJECT_ID}-feedback"
CDN_URL="${CDN_URL:=https://cdn.eq.gcp.onsdigital.uk}"
CDN_ASSETS_PATH="${CDN_ASSETS_PATH:=/design-system}"
ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL:=}"
ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED:=False}"
ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS="${ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS:=10}"
NEW_RELIC_ENABLED="${NEW_RELIC_ENABLED:=False}"
CONFIRMATION_EMAIL_LIMIT="${CONFIRMATION_EMAIL_LIMIT:=10}"
VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS="${VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS:=2700}"

GOOGLE_TAG_MANAGER_ID="${GOOGLE_TAG_MANAGER_ID:=}"
GOOGLE_TAG_MANAGER_AUTH="${GOOGLE_TAG_MANAGER_AUTH:=}"
NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME:=}"
NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY:=}"


gcloud beta run deploy eq-questionnaire-runner \
    --project="${PROJECT_ID}" --region="${REGION}" --concurrency="${CONCURRENCY}" --min-instances="${MIN_INSTANCES}" --max-instances="${MAX_INSTANCES}" \
    --port=5000 --cpu="${CPU}" --memory="${MEMORY}" \
    --image="${DOCKER_REGISTRY}/eq-questionnaire-runner:${IMAGE_TAG}" --platform=managed --allow-unauthenticated \
    --vpc-connector="redis-vpc" \
    --service-account="cloud-run@${PROJECT_ID}.iam.gserviceaccount.com" \
    --set-secrets EQ_REDIS_HOST="redis-host:latest" \
    --set-secrets EQ_REDIS_PORT="redis-port:latest" \
    --set-secrets "${EQ_KEYS_FILE}"="keys:latest" \
    --set-secrets "${EQ_SECRETS_FILE}"="secrets:latest" \
    --set-env-vars WEB_SERVER_TYPE="${WEB_SERVER_TYPE}" \
    --set-env-vars WEB_SERVER_WORKERS="${WEB_SERVER_WORKERS}" \
    --set-env-vars WEB_SERVER_THREADS="${WEB_SERVER_THREADS}" \
    --set-env-vars WEB_SERVER_UWSGI_ASYNC_CORES="${WEB_SERVER_UWSGI_ASYNC_CORES}" \
    --set-env-vars HTTP_KEEP_ALIVE="${HTTP_KEEP_ALIVE}" \
    --set-env-vars EQ_KEYS_FILE="${EQ_KEYS_FILE}" \
    --set-env-vars EQ_SECRETS_FILE="${EQ_SECRETS_FILE}" \
    --set-env-vars DATASTORE_USE_GRPC="${DATASTORE_USE_GRPC}" \
    --set-env-vars EQ_STORAGE_BACKEND="${EQ_STORAGE_BACKEND}" \
    --set-env-vars EQ_ENABLE_SECURE_SESSION_COOKIE="${EQ_ENABLE_SECURE_SESSION_COOKIE}" \
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
    --set-env-vars EQ_SUBMISSION_CONFIRMATION_BACKEND="${EQ_SUBMISSION_CONFIRMATION_BACKEND}" \
    --set-env-vars EQ_FULFILMENT_TOPIC_ID="${EQ_FULFILMENT_TOPIC_ID}" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_LIMIT="${EQ_INDIVIDUAL_RESPONSE_LIMIT}" \
    --set-env-vars EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE="${EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE}" \
    --set-env-vars EQ_FEEDBACK_LIMIT="${EQ_FEEDBACK_LIMIT}" \
    --set-env-vars EQ_GCS_SUBMISSION_BUCKET_ID="${EQ_GCS_SUBMISSION_BUCKET_ID}" \
    --set-env-vars EQ_GCS_FEEDBACK_BUCKET_ID="${EQ_GCS_FEEDBACK_BUCKET_ID}" \
    --set-env-vars CDN_URL="${CDN_URL}" \
    --set-env-vars CDN_ASSETS_PATH="${CDN_ASSETS_PATH}" \
    --set-env-vars ADDRESS_LOOKUP_API_URL="${ADDRESS_LOOKUP_API_URL}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_ENABLED="${ADDRESS_LOOKUP_API_AUTH_ENABLED}" \
    --set-env-vars ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS="${ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS}" \
    --set-env-vars NEW_RELIC_ENABLED="${NEW_RELIC_ENABLED}" \
    --set-env-vars CONFIRMATION_EMAIL_LIMIT="${CONFIRMATION_EMAIL_LIMIT}" \
    --set-env-vars VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS="${VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS}" \
    --set-env-vars GOOGLE_TAG_MANAGER_ID="${GOOGLE_TAG_MANAGER_ID}" \
    --set-env-vars GOOGLE_TAG_MANAGER_AUTH="${GOOGLE_TAG_MANAGER_AUTH}" \
    --set-env-vars NEW_RELIC_LICENSE_KEY="${NEW_RELIC_LICENSE_KEY}" \
    --set-env-vars NEW_RELIC_APP_NAME="${NEW_RELIC_APP_NAME}"
