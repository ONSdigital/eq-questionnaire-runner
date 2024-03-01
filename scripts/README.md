# Scripts

## Script to auto-generate code for integration test

### Details

To speed up the process of generating integration tests for Runner, there is a dev-convenience script that records the GET and POST requests of a user journey
and outputs this formatted in the style of an integration test.

There are a few points to note for this script:

* All GETs and POSTs will be recorded
* The dev will need to manually add their own assertions in the generated test file
* When the script is launched, it will create a new file for the schema chosen. If you launch the script again for the same schema, it will overwrite the
  previous file output
* It does **not** handle dynamic answers because these are generated at runtime - you will need to update the output script to handle list_item_ids separately,
  as they will not be known beforehand
* It handles navigating back via clicking 'previous' links etc. To do this, some additional logic was needed to filter out the beginning of the survey journey,
  after the first GET request from launcher that makes the first GET request in Runner

### Usage

Run the following make command from the project root folder:

```shell
make generate-integration-test
```

This will pause the script and open a browser pointing to the Launcher UI (make sure the application and supporting services are running). Now follow the below
steps:

1. Choose a schema and launch it - the schema name will be used for the name of the integration test output file
1. Navigate through the survey
1. When you're finished with the journey at any point, return to the command line and hit Enter
1. The output will be shown in the logs, and a formatted file will be created for you in the scripts folder. For example: `scripts/test_checkbox.py`
1. Add your own assertions to the test file and move the file into the appropriate `test/integration/` location
