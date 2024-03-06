# Scripts

## Script to auto-generate code for integration test

### Details

To speed up the process of generating integration tests for Runner, there is a dev-convenience script that records the GET and POST requests of a user journey
and outputs this formatted in the style of an integration test.

### Overview

* All POSTs are recorded. To ensure only the necessary GET requests are recorded, additional logic excludes the following GET requests:
    * Session tokens
    * Initial URL requests for each page load
* Additional logic is in place to ensure that, when navigating backwards in a journey after following links (e.g. 'previous' link), it is recorded correctly.
  This is achieved by storing the previous request method at module-level so that it can be used in deciding whether to record or disregard the GET request.
* You will need to manually add your assertions in the generated test file
* When the script is launched, it will create a new file for the schema chosen. If you launch the script again for the same schema, it will overwrite the
  previous file output
* The script is intended to be run with schemas with a `test_` prefix, which would suit most scenarios for test generation. If you wish to use a schema without
  this prefix, you will need to manually amend the generated names for the file, class, and function to allow pytest to process the test file correctly
* It does **not** handle dynamic answers because these are generated at runtime - you will need to update the output script to handle `list_item_id` separately,
  as they will not be known beforehand

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
1. Add your assertions to the test file and move the file into the appropriate `test/integration/` location
