from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase


class TestSchema(IntegrationTestCase):
    def test_get_schema_json(self):
        self.get("/schemas/test_textfield")
        response = self.getResponseData()
        parsed_json = json_loads(response)

        self.assertIn("title", parsed_json)
        self.assertEqual(parsed_json["title"], "Other input fields")

    def test_get_schema_json_with_invalid_request(self):
        self.get("/schemas/doesnt-exist")
        self.assertStatusCode(404)

    def test_list_schemas(self):
        self.get("/schemas")
        response = self.getResponseData()
        parsed_json = json_loads(response)

        self.assertIsInstance(parsed_json, dict)
        self.assertIsInstance(parsed_json["test"][0], str)
        self.assertIn("test_textfield", parsed_json["test"])
