from tests.integration.integration_test_case import IntegrationTestCase


def add_person(test_case: IntegrationTestCase, first_name: str, last_name: str):
    test_case.post({"anyone-else": "Yes"})
    test_case.post({"first-name": first_name, "last-name": last_name})
