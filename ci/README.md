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
  --input eq-questionnaire-runner-repo=.
```

For example:

```sh
EQ_KEYS_FILE=dev-keys.yml \
EQ_SECRETS_FILE=dev-secrets.yml \
PROJECT_ID=my-project-id \
REGION=europe-west2 \
fly -t census-eq execute \
  --config ci/deploy_credentials.yaml \
  --input eq-questionnaire-runner-repo=.
```

## Deploying the app

The following environment variables should be set when deploying the app.

| Variable Name                             | Description                                                                          |
|-------------------------------------------|--------------------------------------------------------------------------------------|
| REQUESTED_CPU_PER_POD                     | No. of CPUs to request per Pod                                                       |
| ROLLING_UPDATE_MAX_UNAVAILABLE            | The maximum number of Pods that can be unavailable during the update process.        |
| ROLLING_UPDATE_MAX_SURGE                  | The maximum number of Pods that can be created over the desired number of Pods.      |
| MIN_REPLICAS                              | Minimum no. of replicated Pods                                                       |
| MAX_REPLICAS                              | Maximum no. of replicated Pods                                                       |
| TARGET_CPU_UTILIZATION_PERCENTAGE         | The average CPU utilization usage before auto scaling applies                        |
| PROJECT_ID                                | The ID of the GCP target project                                                     |
| SUBMISSION_BUCKET_NAME                    | The name of the bucket that submissions will be stored in                            |

There are further *optional* environment variables that can also be set if neded:

| Variable Name                             | Default                | Description                                                                          |
|-------------------------------------------|------------------------|--------------------------------------------------------------------------------------|
| DOCKER_REGISTRY                           | eu.gcr.io/census-eq-ci |                                                                                      |
| IMAGE_TAG                                 | latest                 |                                                                                      |
| GOOGLE_TAG_MANAGER_ID                     |                        |                                                                                      |
| GOOGLE_TAG_MANAGER_AUTH                   |                        |                                                                                      |
| GOOGLE_TAG_MANAGER_PREVIEW                |                        |                                                                                      |

To deploy the app to the cluster via concourse, use the following task command:

```sh
fly -t <target-concourse> execute \
  --config ci/deploy_app.yaml \
  --input eq-questionnaire-runner-repo=.
```

For example:

```sh
fly -t census-eq execute \
  --config ci/deploy_app.yaml \
  --input eq-questionnaire-runner-repo=.
```
