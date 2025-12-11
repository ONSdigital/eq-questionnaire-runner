## eQ Questionnaire Runner

[![Build Status](https://github.com/ONSdigital/eq-questionnaire-runner/actions/workflows/main.yml/badge.svg)](https://github.com/ONSdigital/eq-questionnaire-runner/actions/workflows/main.yml)
[![Build Status](https://github.com/ONSdigital/eq-questionnaire-runner/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ONSdigital/eq-questionnaire-runner/actions/workflows/codeql-analysis.yml)
![Coverage](https://img.shields.io/badge/Coverage-100%25-2FC050.svg)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![poetry-managed](https://img.shields.io/badge/poetry-managed-blue)](https://python-poetry.org/)
[![License - MIT](https://img.shields.io/badge/licence%20-MIT-1ac403.svg)](https://github.com/ONSdigital/eq-questionnaire-runner/blob/main/LICENSE)

## Run with Docker

Install [Docker](https://www.docker.com/) for your system. Make sure that you've installed both docker and docker-compose packages, preferably using Homebrew:

``` shell
brew install docker
brew install docker-compose
```

On MacOS install container runtimes, eg. [Colima](https://github.com/abiosoft/colima):
```shell
brew install colima
```

Make sure Colima is started every time you want to use Docker images:
```shell
colima start
```

To get eq-questionnaire-runner running the following command will build and run the containers

``` shell
RUNNER_ENV_FILE=.development.env docker compose up -d
```

To launch a survey, navigate to [http://localhost:8000/](http://localhost:8000/)

When the containers are running you are able to access the application as normal, and code changes will be reflected in the running application.
However, any new dependencies that are added would require a re-build.

To rebuild the eq-questionnaire-runner container, the following command can be used.

``` shell
RUNNER_ENV_FILE=.development.env docker compose build
```

If you need to rebuild the container from scratch to re-load any dependencies then you can run the following

``` shell
RUNNER_ENV_FILE=.development.env docker compose build --no-cache
```

## Run locally

### Clone the repository

``` shell
git clone git@github.com:ONSdigital/eq-questionnaire-runner.git
```

### Pre-Requisites

In order to run locally you'll need Node.js, snappy, pyenv, jq and wkhtmltopdf installed

``` shell
brew install snappy npm pyenv jq wkhtmltopdf
```

### Setup

#### Application version

Create `.application-version` for local development

This file is automatically created and populated with the git revision id during CI for anything other than development,
but the file is absent when the repo is first cloned and is required for running the app locally. Setting the contents
to `local` removes the implication that any particular revision is used when run locally.

``` shell
echo "local" > .application-version
```
#### Python version

It is preferable to use the version of Python locally that matches that
used on deployment. This project has a `.python_version` file for this
purpose.

#### Pyenv

It is recommended to install the `pyenv` Python version management tool to easily switch between Python versions.
To install `pyenv` use this command:
```shell
curl https://pyenv.run | bash
```
After the installation it should tell you to execute a command to add `pyenv` to path. It should look something like this:
```shell
export PYENV_ROOT="$HOME/.pyenv"

command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"

eval "$(pyenv init -)"
```
Python versions can be changed with the `pyenv local` or `pyenv global` commands suffixed with the desired version (e.g. 3.13.5). Different versions of Python can be installed first with the `pyenv install` command. Refer to the pyenv project Readme [here](https://github.com/pyenv/pyenv). To avoid confusion, check the current Python version at any given time using `python --version` or `python3 --version`.

#### Python & dependencies

Inside the project directory install python version, upgrade pip:

``` shell
pyenv install
pip install --upgrade pip setuptools
```

Install poetry, poetry dotenv plugin and install dependencies:

``` shell
curl -sSL https://install.python-poetry.org | python3 - --version 2.1.2
poetry self add poetry-plugin-dotenv
poetry install
```

We use [poetry-plugin-up](https://github.com/MousaZeidBaker/poetry-plugin-up) to update dependencies in the `pyproject.toml` file:

``` shell
poetry self add poetry-plugin-up
```

#### Design system templates

To update the design system templates run:

``` shell
make load-design-system-templates
```

#### Schemas

To download the latest schemas from the [Questionnaire Registry](https://github.com/ONSdigital/eq-questionnaire-schemas):

``` shell
make load-schemas
```

#### Run server

Run the server inside the virtual env created by Poetry with:

``` shell
make run
```

### Supporting services

Runner requires five supporting services - a questionnaire launcher, a storage backend, a cache, the supplementary data service and the collection instrument registry.

#### Run supporting services with Docker

First, authenticate to make sure Docker can pull from GAR
```shell
gcloud auth login
```

To run the app locally, but the supporting services in Docker, make sure you have Docker and Colima installed [from this step](#run-with-docker), then run:

``` shell
make dev-compose-up
```

Note that on Linux you will need to use:

``` shell
make dev-compose-up-linux
```

#### Run supporting services locally

##### [Questionnaire launcher](https://github.com/ONSDigital/eq-questionnaire-launcher)

``` shell
docker run -e SURVEY_RUNNER_SCHEMA_URL=http://host.docker.internal:5000 -e SDS_API_BASE_URL=http://host.docker.internal:5003 -e CIR_API_BASE_URL=http://host.docker.internal:5004 -it -p 8000:8000 europe-west2-docker.pkg.dev/ons-eq-ci/docker-images/eq-questionnaire-launcher:latest
```

##### [Mock Supplementary data service](https://github.com/ONSDigital/eq-runner-mock-sds)

``` shell
docker run -it -p 5003:5003 europe-west2-docker.pkg.dev/ons-eq-ci/docker-images/sds:latest
```

##### [Mock Collection Instrument Registry](https://github.com/ONSDigital/eq-runner-mock-cir)

``` shell
docker run -it -p 5004:5004 europe-west2-docker.pkg.dev/ons-eq-ci/docker-images/cir:latest
```

##### Storage backends

[DynamoDB](https://github.com/ONSDigital/eq-docker-dynamodb)

``` shell
docker run -it -p 6060:8000 onsdigital/eq-docker-dynamodb:latest
```

or

[Google Datastore](https://hub.docker.com/r/knarz/datastore-emulator/)

``` shell
docker run -it -p 8432:8432 knarz/datastore-emulator:latest
```

##### Cache

``` shell
docker run -it -p 6379:6379 redis:4
```

#### Using Google Cloud Platform for supporting services

To use `EQ_STORAGE_BACKEND` as `datastore` or `EQ_SUBMISSION_BACKEND` as `gcs` directly on GCP and not a docker image, you need to set the GCP project using the following command:

``` shell
gcloud config set project <gcp_project_id>
```

Or set the `GOOGLE_CLOUD_PROJECT` environment variable to your gcp project id.

---


## Integration Tests
There is a dev-convenience script that auto generates the lines of code for a user journey. See [README](scripts/README.md) for more information and how to run
the script.

## Frontend Tests

The frontend tests use NodeJS to run. To handle different versions of NodeJS it is recommended to install `Node Version Manager` (`nvm`). It is similar to pyenv but for Node versions.
To install `nvm` use the command below (make sure to replace "v0.39.5" with the current latest version in [releases](https://github.com/nvm-sh/nvm/releases/):
``` shell
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
```
You will need to have the correct node version installed to run the tests. To do this, use the following commands:

``` shell
nvm install
nvm use
```

Fetch npm dependencies:

``` shell
npm install
```

Available commands:

| Command                | Task                                                                                                      |
|------------------------| --------------------------------------------------------------------------------------------------------- |
| `make test-functional` | Runs the functional tests through Webdriver (requires app running on localhost:5000 and generated pages). |
| `make generate-pages`  | Generates the functional test pages.                                                                      |
| `make lint-js`         | Lints the JS, reporting errors/warnings.                                                                  |
| `make format-js`       | Format the json schemas.                                                                                  |

---

### Development with functional tests

The tests are written using [WebdriverIO](https://webdriver.io/docs/gettingstarted), [Chai](https://www.chaijs.com/), and [Mocha](https://mochajs.org/)

### Functional test options

The functional tests use a set of selectors that are generated from each of the test schemas. These make it quick to add new functional tests.

To run the functional tests first runner needs to be spin up with:

``` shell
RUNNER_ENV_FILE=.functional-tests.env make run
```

This will set the correct environment variables for running the functional tests.

Then you can run either:

``` shell
make test-functional
```
or

``` shell
make test-functional-headless
```

This will delete the `tests/functional/generated_pages` directory and regenerate all the files in it from the schemas.

To generate the pages manually you can run the `generate_pages` scripts with the schema directory. Run it from the `tests/functional` directory as follows:

``` shell
./generate_pages.py ../../schemas/test/en/ ./generated_pages -r "../../base_pages"
```

To generate a spec file with the imports included, you can pass the schema name as an argument without the file extension, e.g. `SCHEMA=test_address`:
``` shell
make generate-spec SCHEMA=<schema-name>
```

If you have already built the generated pages, then the functional tests can be executed with:

``` shell
make test-functional
```

This can be limited to a single spec where argument needed is the remainder of the path after `./tests/functional/spec/` (which is included in the command):

``` shell
make test-functional-spec SPEC=<spec>
```

To run a single test, add `.only` into the name of any `describe` or `it` function:

`describe.only('Skip Conditions', function() {...}` or

`it.only('Given this is a test', function() {...}`

Test suites are configured in the `wdio.conf.js` file.
An individual test suite can be run using the suite names as the argument to this command. The suites that can be used with command below are:
* timeout_modal_expired
* timeout_modal_extended
* timeout_modal_extended_new_window
* features
* general
* components

``` shell
make test-functional-suite SUITE=<suite>
```

To run the tests against a remote deployment you will need to specify the environment variable of EQ_FUNCTIONAL_TEST_ENV eg:

``` shell
EQ_FUNCTIONAL_TEST_ENV=https://staging-new-surveys.dev.eq.ons.digital/ npm run test_functional
```

---

## Deploying

For deploying with Concourse see the [CI README](./ci/README.md).

### Deployment with [gcloud](https://cloud.google.com/sdk/gcloud)

To deploy this application with gcloud, you must be logged in using `gcloud auth login` and `gcloud auth application-default login`.

When deploying with gcloud the environment variables specified in [Deploying the app](./README.md#deploying-the-app) must be set.

Then call the following command with environment variables set:

``` shell
./ci/deploy_app.sh
```

### Deploying credentials

Before deploying the app to GCP you need to create the application credentials. Run the following command to provision the credentials:

``` shell
PROJECT_ID=PROJECT_ID EQ_KEYS_FILE=PATH_TO_KEYS_FILE EQ_SECRETS_FILE=PATH_TO_SECRETS_FILE ./ci/deploy_credentials.sh
```

For example:

``` shell
PROJECT_ID=eq-test EQ_KEYS_FILE=dev-keys.yml EQ_SECRETS_FILE=dev-secrets.yml ./ci/deploy_credentials.sh
```

### Deploying the app

The following environment variables must be set when deploying the app.

| Variable Name   | Description                            |
| --------------- | -------------------------------------- |
| PROJECT_ID      | The ID of the GCP target project       |
| DOCKER_REGISTRY | The FQDN of the target Docker registry |
| IMAGE_TAG       |                                        |

The following environment variables are optional:

| Variable Name                | Default          | Description                                                                                                    |
|------------------------------| ---------------- |----------------------------------------------------------------------------------------------------------------|
| REGION                       | europe-west2     | The region that will be used for your Cloud Run service                                                        |
| CONCURRENCY                  | 80               | The maximum number of requests that can be processed simultaneously by a given container instance              |
| MIN_INSTANCES                | 1                | The minimum number of container instances that can be used for your Cloud Run service                          |
| MAX_INSTANCES                | 1                | The maximum number of container instances that can be used for your Cloud Run service                          |
| CPU                          | 4                | The number of CPUs to allocate for each Cloud Run container instance                                           |
| MEMORY                       | 4G               | The amount of memory to allocate for each Cloud Run container instance                                         |
| GOOGLE_TAG_ID                |                  | The Google Tag ID - Specifies the GTM account                                                                  |
| WEB_SERVER_TYPE              | gunicorn-threads | Web server type used to run the application. This also determines the worker class which can be async/threaded |
| WEB_SERVER_WORKERS           | 7                | The number of worker processes                                                                                 |
| WEB_SERVER_THREADS           | 10               | The number of worker threads per worker                                                                        |
| WEB_SERVER_UWSGI_ASYNC_CORES | 10               | The number of cores to initialise when using "uwsgi-async" web server worker type                              |
| DATASTORE_USE_GRPC           | False            | Determines whether to use gRPC for Datastore. gRPC is currently only supported for threaded web servers        |

To deploy the app, run the following command:

``` shell
./ci/deploy_app.sh
```

---

## Internationalisation

We use flask-babel to do internationalisation. To extract messages from source and create the messages.pot file, in the project root run the following command.

``` shell
make translation-templates
```

```make translation-templates``` is a command that uses pybabel to extract static messages.

This will extract messages and place them in the .pot files ready for translation.

These .pot files will then need to be translated. The translation process is documented in Confluence [here](https://collaborate2.ons.gov.uk/confluence/display/SDC/Translation+Process)

Once we have the translated .po files they can be added to the source code and used by the application

## Environment Variables

The following env variables can be used

| Variable Name                             | Default                      | Description                                                                                                    |
|-------------------------------------------|------------------------------|----------------------------------------------------------------------------------------------------------------|
| EQ_SESSION_TIMEOUT_SECONDS                | 2700 (45 mins)               | The duration of the flask session                                                                              |
| EQ_PROFILING                              | False                        | Enables or disables profiling (True/False) Default False/Disabled                                              |
| EQ_GOOGLE_TAG_ID                          |                              | The Google Tag Manger ID - Specifies the GTM account                                                           |
| EQ_ENABLE_HTML_MINIFY                     | True                         | Enable minification of html                                                                                    |
| EQ_ENABLE_SECURE_SESSION_COOKIE           | True                         | Set secure session cookies                                                                                     |
| EQ_MAX_HTTP_POST_CONTENT_LENGTH           | 65536                        | The maximum http post content length that the system wil accept                                                |
| EQ_MINIMIZE_ASSETS                        | True                         | Should JS and CSS be minimized                                                                                 |
| MAX_CONTENT_LENGTH                        | 65536                        | max request payload size in bytes                                                                              |
| EQ_APPLICATION_VERSION_PATH               | .application-version         | the location of a file containing the application version number                                               |
| EQ_ENABLE_LIVE_RELOAD                     | False                        | Enable livereload of browser when scripts, styles or templates are updated                                     |
| EQ_SECRETS_FILE                           | secrets.yml                  | The location of the secrets file                                                                               |
| EQ_KEYS_FILE                              | keys.yml                     | The location of the keys file                                                                                  |
| EQ_SUBMISSION_BACKEND                     |                              | Which submission backend to use ( gcs, rabbitmq, log )                                                         |
| EQ_GCS_SUBMISSION_BUCKET_ID               |                              | The bucket name in GCP to store the submissions in                                                             |
| EQ_GCS_FEEDBACK_BUCKET_ID                 |                              | The bucket name in GCP to store the feedback in                                                                |
| EQ_RABBITMQ_HOST                          |                              |                                                                                                                |
| EQ_RABBITMQ_HOST_SECONDARY                |                              |                                                                                                                |
| EQ_RABBITMQ_PORT                          | 5672                         |                                                                                                                |
| EQ_RABBITMQ_QUEUE_NAME                    | submit_q                     | The name of the submission queue                                                                               |
| EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS | 10000                        |                                                                                                                |
| EQ_STORAGE_BACKEND                        | datastore                    |                                                                                                                |
| EQ_DYNAMODB_ENDPOINT                      |                              |                                                                                                                |
| EQ_REDIS_HOST                             |                              | Hostname of Redis instance used for ephemeral storage                                                          |
| EQ_REDIS_PORT                             |                              | Port number of Redis instance used for ephemeral storage                                                       |
| EQ_DYNAMODB_MAX_RETRIES                   | 5                            |                                                                                                                |
| EQ_DYNAMODB_MAX_POOL_CONNECTIONS          | 30                           |                                                                                                                |
| EQ_QUESTIONNAIRE_STATE_TABLE_NAME         |                              |                                                                                                                |
| EQ_SESSION_TABLE_NAME                     |                              |                                                                                                                |
| EQ_USED_JTI_CLAIM_TABLE_NAME              |                              |                                                                                                                |
| WEB_SERVER_TYPE                           |                              | Web server type used to run the application. This also determines the worker class which can be async/threaded |
| WEB_SERVER_WORKERS                        |                              | The number of worker processes                                                                                 |
| WEB_SERVER_THREADS                        |                              | The number of worker threads per worker                                                                        |
| WEB_SERVER_UWSGI_ASYNC_CORES              |                              | The number of cores to initialise when using "uwsgi-async" web server worker type                              |
| DATASTORE_USE_GRPC                        | False                        | Determines whether to use gRPC for Datastore. gRPC is currently only supported for threaded web servers        |
| ACCOUNT_SERVICE_BASE_URL                  | `https://surveys.ons.gov.uk` | The base URL of the account service used to launch the survey                                                  |
| ONS_URL                                   | `https://www.ons.gov.uk`     | The URL of the ONS website where static content is sourced, e.g. accessibility info                            |
| SDS_API_BASE_URL                          |                              | The base URL of the SDS API used for fetching supplementary data                                               |
| CIR_API_BASE_URL                          |                              | The base URL of the CIR API used for fetching collection instruments                                           |
| OIDC_TOKEN_BACKEND                        | gcp                          | The backend to use when fetching the Open ID Connect token                                                     |
| OIDC_TOKEN_LEEWAY_IN_SECONDS              | 300                          | The leeway to use when validating OIDC tokens                                                                  |
| SDS_OAUTH2_CLIENT_ID                      |                              | The OAuth2 Client ID used when setting up IAP on the SDS                                                       |
| CIR_OAUTH2_CLIENT_ID                      |                              | The OAuth2 Client ID used when setting up IAP on the CIR                                                       |

The following env variables can be used when running tests

``` shell
EQ_FUNCTIONAL_TEST_ENV - the pre-configured environment [local, docker, preprod] or the url of the environment that should be targeted
```

---

## JWT Integration

Integration with the survey runner requires the use of a signed JWT using public and private key pair (see [https://jwt.io](https://jwt.io),
[https://tools.ietf.org/html/rfc7519](https://tools.ietf.org/html/rfc7519), [https://tools.ietf.org/html/rfc7515](https://tools.ietf.org/html/rfc7515)).

Once signed the JWT must be encrypted using JWE (see [https://tools.ietf.org/html/rfc7516](https://tools.ietf.org/html/rfc7516)).

The JWT payload must contain the following claims:

- exp - expiration time
- iat - issued at time

The header of the JWT must include the following:

- alg - the signing algorithm (must be RS256)
- type - the token type (must be JWT)
- kid - key identification (must be EDCRRM)

The JOSE header of the final JWE must include:

- alg - the key encryption algorithm (must be RSA-OAEP)
- enc - the key encryption encoding (must be A256GCM)

To access the application you must provide a valid JWT. To do this browse to the /session url and append a token parameter.
This parameter must be set to a valid JWE encrypted JWT token. Only encrypted tokens are allowed.

There is a python script for generating tokens for use in development, to run:

``` shell
python token_generator.py
```

---

## Profiling

Refer to our [profiling document](doc/profiling.md).

---

## Updating / Installing dependencies

### Python
To add a new dependency, use:
``` shell
poetry add [package-name]
```
This will add the required packages to your pyproject.toml and install them

To update a dependency, use:
```shell
poetry update [package-name]
```
This will resolve the required dependencies of the project and write the exact versions into poetry.lock

Using the poetry up plugin we can update dependencies and bump their versions in the pyproject.toml file

To update dependencies to the latest compatible version with respect to their version constraints specified in the pyproject.toml file:
```shell
poetry up
```

To update dependencies to their latest compatible version:
```shell
poetry up --latest
```

NB: both the pyproject.toml and poetry.lock files are required in source control to accurately pin dependencies.

### JavaScript
To add a new dependency, use `npm install [dev dependency] --save-dev` or `npm install [dependency]` then use `npm install` to install all the packages locally.

---

## Testing Design System changes (locally) without pushing to actual CDN

### On [Design System](https://github.com/ONSdigital/design-system) Repo
Checkout branch with new changes on

You will need to install the Design System dependencies. If you haven't installed Yarn, install it with `npm i -g yarn`. To install the dependencies run `yarn` in the terminal. If you haven't
you will also need to install gulp.

Then in the terminal run:

``` shell
yarn cdn-bundle
cd build
browser-sync start --cwd -s --http --port 5678
```

You should now see output indicating that files are being served from `localhost:5678`. So main.css for example will now be served on `http://localhost:5678//css/main.css`

Now switch to the eQ Questionnaire Runner Repo

### On eQ Questionnaire Runner Repo
In a separate terminal window/tab:
Checkout the runner branch you want to test on

Edit your .development.env with following:

``` shell
CDN_URL=http://localhost:5678
CDN_ASSETS_PATH=
```

Edit the Makefile to remove `load-design-system-templates` from the build command. Should now look like this:

``` shell
build: load-schemas translate
```

Run `make load-design-system-templates` in the terminal to make sure you have the Design System templates loaded

Then edit the first line in the `templates/layout/_template.njk` file to remove the version number. Should now look like this:

``` shell
{% set release_version = '' %}
```

Then spin up launcher and runner with `make dev-compose-up` and `make run`

Now when navigating to localhost:8000 and launching a schema, this will now be using the local cdn with the changes from the Design System branch
