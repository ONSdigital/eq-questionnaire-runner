# Deploying with [Concourse](https://concourse-ci.org/)

To deploy this application with Concourse, you must have a Kubernetes cluster already provisioned and be logged in to a Concourse instance that has access to the cluster.

## Deploying credentials

Before deploying the app you need to create credentials on Kubernetes. This can be done via Concourse using the following task commands:

```sh
REGION=<cluster_region> \
PROJECT_ID=<project_id> \
EQ_KEYS_FILE=<path_to_keys_file> \
EQ_SECRETS_FILE=<path_to_secrets_file> \
fly -t <target-concourse> execute \
  --config ci/deploy_credentials.yaml
```

## Deploying the app

In addition to the environment variables specified in [Deploying the app](../README.md#deploying-the-app), when deploying with Concourse the following must also be set.

| Variable Name                             | Description                                                                          |
|-------------------------------------------|--------------------------------------------------------------------------------------|
| REGION                                    | What region to authenticate against                                                  |
| PROJECT_ID                                | The ID of the GCP target project                                                     |

To deploy the app to the cluster via Concourse, use the following task command:

```sh
fly -t <target-concourse> execute \
  --config ci/deploy_app.yaml
```

## Backing up questionnaire state

Questionnaire state can be backed up using the `backup_questionnaire_state.yaml` task. This can be done via Concourse using the following command:

```sh
PROJECT_ID=<project_id> \
fly -t <target-concourse> execute \
  --config ci/backup_questionnaire_state.yaml
```
