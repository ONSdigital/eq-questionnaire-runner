#!/usr/bin/env bash
set -exo pipefail

if [[ -z "$SUBMISSION_BUCKET_NAME" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

helm tiller run \
    helm upgrade --install \
    survey-runner \
    k8s/helm \
    --set-string submissionBucket="${SUBMISSION_BUCKET_NAME}" \
    --set-string googleTagManagerId="${GOOGLE_TAG_MANAGER_ID}" \
    --set-string googleTagManagerAuth="${GOOGLE_TAG_MANAGER_AUTH}" \
    --set-string googleTagManagerPreview="${GOOGLE_TAG_MANAGER_PREVIEW}" \
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
    --set-string newRelic.appName="${NEW_RELIC_APP_NAME}"
