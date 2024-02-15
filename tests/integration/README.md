# Integration Tests

## Script to auto-generate code for integration test

To generate the GET and POST requests of a user journey that can be run as an integration test, run the following make command from the project root folder:

```shell
make generate-integration-test
```

This will launch a browser pointing to the Launcher UI (make sure the application and supporting services are running). Now follow the below steps:

1. Choose a schema and launch it - the schema name will be used for the name of the file
1. Navigate through the survey. **Note:** all GETs and POSTs will be recorded
1. When you're finished with the journey at any point, return to the command line and hit Enter
1. The output will be shown in the logs, and a formatted file will be created for you in the scripts folder. For example: `scripts/test_checkbox.py`
