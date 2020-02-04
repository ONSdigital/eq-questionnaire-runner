#!/usr/bin/env bash
set -euxo pipefail

if [[ -z "$EQ_KEYS_FILE" ]]; then
  echo "EQ_KEYS_FILE not provided"
  exit 1
fi

if [[ -z "$EQ_SECRETS_FILE" ]]; then
  echo "EQ_SECRETS_FILE not provided"
  exit 1
fi

  gcloud auth activate-service-account --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"

  helm init --client-only
  helm plugin install https://github.com/rimusz/helm-tiller

  gcloud container clusters get-credentials survey-runner --region "${REGION}" --project "${PROJECT_ID}"

kubectl create secret generic keys \
    --from-file=keys.yml=${EQ_KEYS_FILE} \
    --dry-run -o yaml | kubectl apply -f -

kubectl create secret generic secrets \
    --from-file=secrets.yml=${EQ_SECRETS_FILE} \
    --dry-run -o yaml | kubectl apply -f -
