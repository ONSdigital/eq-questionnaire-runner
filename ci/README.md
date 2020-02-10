# Deploying with [Concourse](https://concourse-ci.org/)

To deploy this application with Concourse, you must have a Kubernetes cluster already provisioned and be logged in to a Concourse instance that has access to the cluster.

## Deploying credentials

Before deploying the app you need to create credentials on Kubernetes. This can be done via Concourse using the following task commands:

```sh
EQ_KEYS_FILE=<path_to_keys_file> \
EQ_SECRETS_FILE=<path_to_secrets_file> \
PROJECT_ID=<project_id> \
REGION=<cluster_region> \
fly -t <target-concourse> execute \
  --config ci/deploy_credentials.yaml \
```

## Deploying the app

In addition to the environment variables specified in [Deploying the app](../README.md#deploying-the-app), when deploying with concourse the following must also be set.

| Variable Name                             | Description                                                                          |
|-------------------------------------------|--------------------------------------------------------------------------------------|
| PROJECT_ID                                | The ID of the GCP target project                                                     |
| REGION                                    | What region to authenticate against                                                  |

To deploy the app to the cluster via concourse, use the following task command:

```sh
fly -t <target-concourse> execute \
  --config ci/deploy_app.yaml
```
