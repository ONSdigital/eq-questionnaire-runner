#!/usr/bin/env bash
set -e

if [[ -z "$SUBMISSION_BUCKET_NAME" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

helm tiller run \
    helm upgrade --install \
    survey-runner \
    k8s/helm \
    --set submissionBucket=${SUBMISSION_BUCKET_NAME} \
    --set googleTagManagerId=${GOOGLE_TAG_MANAGER_ID} \
    --set googleTagManagerAuth=${GOOGLE_TAG_MANAGER_AUTH} \
    --set googleTagManagerPreview=${GOOGLE_TAG_MANAGER_PREVIEW} \
    --set image.repository=${DOCKER_REGISTRY}/eq-questionnaire-runner \
    --set image.tag=${IMAGE_TAG} \
    --set cookieSettingsUrl=${COOKIE_SETTINGS_URL} \
    --set resources.requests.cpu=${REQUESTED_CPU_PER_POD} \
    --set rollingUpdate.maxUnavailable=${ROLLING_UPDATE_MAX_UNAVAILABLE} \
    --set rollingUpdate.maxSurge=${ROLLING_UPDATE_MAX_SURGE} \
    --set autoscaler.minReplicas=${MIN_REPLICAS} \
    --set autoscaler.maxReplicas=${MAX_REPLICAS} \
    --set autoscaler.targetCPUUtilizationPercentage=${TARGET_CPU_UTILIZATION_PERCENTAGE}
