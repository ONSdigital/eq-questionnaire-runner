#!/usr/bin/env bash
set -exo pipefail

if [[ -z "$SUBMISSION_BUCKET_NAME" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

if [[ -z "$FEEDBACK_BUCKET_NAME" ]]; then
  echo "FEEDBACK_BUCKET_NAME is mandatory"
  exit 1
fi

helm upgrade --install \
    questionnaire-runner \
    k8s/helm \
    --set-string submissionBucket="${SUBMISSION_BUCKET_NAME}" \
    --set-string feedbackBucket="${FEEDBACK_BUCKET_NAME}" \
    --set-string individualResponsePostalDeadline="${INDIVIDUAL_RESPONSE_POSTAL_DEADLINE}" \
    --set-string googleTagManagerId="${GOOGLE_TAG_MANAGER_ID}" \
    --set-string googleTagManagerAuth="${GOOGLE_TAG_MANAGER_AUTH}" \
    --set-string image.repository="${DOCKER_REGISTRY}/eq-questionnaire-runner" \
    --set-string image.tag="${IMAGE_TAG}" \
    --set-string cookieSettingsUrl="${COOKIE_SETTINGS_URL}" \
    --set-string resources.requests.cpu="${REQUESTED_CPU_PER_POD}" \
    --set-string rollingUpdate.maxUnavailable="${ROLLING_UPDATE_MAX_UNAVAILABLE}" \
    --set-string rollingUpdate.maxSurge="${ROLLING_UPDATE_MAX_SURGE}" \
    --set-string autoscaler.minReplicas="${MIN_REPLICAS}" \
    --set-string autoscaler.maxReplicas="${MAX_REPLICAS}" \
    --set-string autoscaler.targetCPUUtilizationPercentage="${TARGET_CPU_UTILIZATION_PERCENTAGE}" \
    --set-string newRelic.enabled="${EQ_NEW_RELIC_ENABLED}" \
    --set-string newRelic.licenseKey="${NEW_RELIC_LICENSE_KEY}" \
    --set-string newRelic.appName="${NEW_RELIC_APP_NAME}" \
    --set-string webServer.type="${WEB_SERVER_TYPE}" \
    --set-string webServer.workers="${WEB_SERVER_WORKERS}" \
    --set-string webServer.threads="${WEB_SERVER_THREADS}" \
    --set-string webServer.uwsgiAsyncCores="${WEB_SERVER_UWSGI_ASYNC_CORES}" \
    --set-string datastore.useGRPC="${DATASTORE_USE_GRPC}" \
    --set-string addressLookupApi.url="${ADDRESS_LOOKUP_API_URL}" \
    --set-string addressLookupApi.authEnabled="${ADDRESS_LOOKUP_API_AUTH_ENABLED}"

kubectl rollout restart deployment.v1.apps/runner
kubectl rollout status deployment.v1.apps/runner
