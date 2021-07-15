# Deploying with [Concourse](https://concourse-ci.org/)

To deploy this application with Concourse, you must be logged in to a Concourse instance that has access to the GCP project.

## Deploying credentials

Before deploying the app you need to create credentials. This can be done via Concourse using the following task commands:

```sh
PROJECT_ID=<project_id> \
EQ_KEYS_FILE=<path_to_keys_file> \
EQ_SECRETS_FILE=<path_to_secrets_file> \
fly -t <target-concourse> execute \
  --config ci/deploy_credentials.yaml
```

## Deploying the app

When deploying with Concourse the environment variables specified in [Deploying the app](../README.md#deploying-the-app) must be set.

To deploy the app via Concourse, use the following task command:
```sh
fly -t <target-concourse> execute \
  --config ci/deploy_app.yaml
```

## Backing up questionnaire state

Questionnaire state can be backed up using the `backup_questionnaire_state.yaml` task. This can be done via Concourse using the following command:

```sh
PROJECT_ID=<project_id> \
BUCKET_NAME=<bucket_name> \
fly -t <target-concourse> execute \
  --config ci/backup_questionnaire_state.yaml
```

- `BUCKET_NAME` should not contain `gs://`

## Restoring questionnaire state

Questionnaire state can be restored using the `restore_questionnaire_state.yaml` task. This can be done via Concourse using the following command:

```sh
PROJECT_ID=<project_id> \
BUCKET_NAME=<bucket_name> \
BACKUP_NAME=<backup_name> \
fly -t <target-concourse> execute \
  --config ci/restore_questionnaire_state.yaml
```

- `BUCKET_NAME` should not contain `gs://`
- `BACKUP_NAME` is the timestamped folder name containing the backup files and folders e.g. `2021-01-05T09:37:15_88808`

## Purge expired sessions

Expired sessions can be purged from Datastore using the `purge_expired_sessions.yaml` task. This can be done via Concourse using the following command:

```sh
PROJECT_ID=<project_id> \
DATAFLOW_TEMPLATE_VERSION=<dataflow_template_version> \
EXPIRATION_TIME_OFFSET_IN_SECONDS=<expiration_time_offset_in_seconds> \
fly -t <target-concourse> execute \
  --config ci/purge_expired_sessions.yaml
```
There are defaults for both DATAFLOW_TEMPLATE_VERSION and EXPIRATION_TIME_OFFSET_IN_SECONDS if not set

- `DATAFLOW_TEMPLATE_VERSION` is the template version on GCP you want to use
- `EXPIRATION_TIME_OFFSET_IN_SECONDS` is the offset in seconds expired sessions will be purged from (i.e 3600 would delete all sessions more than an hour old)
