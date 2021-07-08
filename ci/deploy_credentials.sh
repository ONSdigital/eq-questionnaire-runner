#!/usr/bin/env bash
set -euxo pipefail

if [[ -z "$PROJECT_ID" ]]; then
  echo "PROJECT_ID not provided"
  exit 1
fi

if [[ -z "$EQ_KEYS_FILE" ]]; then
  echo "EQ_KEYS_FILE not provided"
  exit 1
fi

if [[ -z "$EQ_SECRETS_FILE" ]]; then
  echo "EQ_SECRETS_FILE not provided"
  exit 1
fi

gcloud secrets create keys --replication-policy="automatic" --project="$PROJECT_ID" || true
gcloud secrets create secrets --replication-policy="automatic" --project="$PROJECT_ID" || true

gcloud secrets versions add keys --data-file="${EQ_KEYS_FILE}" --project="$PROJECT_ID"
gcloud secrets versions add secrets --data-file="${EQ_SECRETS_FILE}" --project="$PROJECT_ID"
