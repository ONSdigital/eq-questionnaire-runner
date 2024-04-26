from app.utilities.json import json_loads
from tests.integration.integration_test_case import IntegrationTestCase


class TestDumpDebug(IntegrationTestCase):
    def test_dump_debug_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the questionnaire store
        self.get("/dump/debug")

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_debug_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory"
        )

        # When I attempt to dump the questionnaire store
        self.get("/dump/debug")

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

    def test_dump_debug_authenticated_with_role(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory",
            roles=["dumper"],
        )

        # And I attempt to dump the questionnaire store
        self.get("/dump/debug")

        # Then I get a 200 OK response
        self.assertStatusOK()


class TestDumpSubmission(IntegrationTestCase):
    def test_dump_submission_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the submission payload
        self.get("/dump/submission")

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_submission_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory"
        )

        # When I attempt to dump the submission payload
        self.get("/dump/submission")

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

    def test_dump_submission_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory",
            roles=["dumper"],
        )

        # When I haven't submitted any answers
        # And I attempt to dump the submission payload
        self.get("/dump/submission")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json_loads(self.getResponseData())
        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            "submission": {
                "case_id": actual["submission"]["case_id"],
                "collection_exercise_sid": "789",
                "data": {"answers": [], "lists": []},
                "data_version": "0.0.3",
                "flushed": False,
                "launch_language_code": "en",
                "origin": "uk.gov.ons.edc.eq",
                "schema_name": "test_radio_mandatory_with_detail_answer_mandatory",
                "submission_language_code": "en",
                "submitted_at": actual["submission"]["submitted_at"],
                "survey_metadata": {
                    "display_address": "68 Abingdon Road, " "Goathill",
                    "employment_date": "1983-06-02",
                    "period_id": "201604",
                    "period_str": "April 2016",
                    "ref_p_end_date": "2016-04-30",
                    "ref_p_start_date": "2016-04-01",
                    "ru_name": "Integration Testing",
                    "ru_ref": "12345678901A",
                    "survey_id": "0",
                    "trad_as": "Integration Tests",
                    "user_id": "integration-test",
                },
                "tx_id": actual["submission"]["tx_id"],
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "version": "v2",
            }
        }

        assert actual == expected

    def test_dump_submission_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(schema_name="test_radio_mandatory", roles=["dumper"])

        # When I submit an answer
        self.post(post_data={"radio-mandatory-answer": "Coffee"})

        # And I attempt to dump the submission payload
        self.get("/dump/submission")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json_loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            "submission": {
                "case_id": actual["submission"]["case_id"],
                "collection_exercise_sid": "789",
                "data": {
                    "answers": [
                        {"answer_id": "radio-mandatory-answer", "value": "Coffee"}
                    ],
                    "lists": [],
                },
                "data_version": "0.0.3",
                "flushed": False,
                "launch_language_code": "en",
                "origin": "uk.gov.ons.edc.eq",
                "schema_name": "test_radio_mandatory",
                "started_at": actual["submission"]["started_at"],
                "submission_language_code": "en",
                "submitted_at": actual["submission"]["submitted_at"],
                "survey_metadata": {
                    "display_address": "68 Abingdon Road, " "Goathill",
                    "employment_date": "1983-06-02",
                    "period_id": "201604",
                    "period_str": "April 2016",
                    "ref_p_end_date": "2016-04-30",
                    "ref_p_start_date": "2016-04-01",
                    "ru_name": "Integration Testing",
                    "ru_ref": "12345678901A",
                    "survey_id": "0",
                    "trad_as": "Integration Tests",
                    "user_id": "integration-test",
                },
                "tx_id": actual["submission"]["tx_id"],
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "version": "v2",
            }
        }
        assert actual == expected

    def test_dump_submission_authenticated_with_role_with_lists(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(schema_name="test_relationships", roles=["dumper"])

        # When I submit my answers
        self.post({"anyone-else": "Yes"})
        self.post({"first-name": "John", "last-name": "Doe"})
        self.post({"anyone-else": "No"})

        # And I attempt to dump the submission payload
        self.get("/dump/submission")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json_loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = {
            "submission": {
                "case_id": actual["submission"]["case_id"],
                "collection_exercise_sid": "789",
                "data": {
                    "answers": [
                        {
                            "answer_id": "first-name",
                            "list_item_id": actual["submission"]["data"]["answers"][0][
                                "list_item_id"
                            ],
                            "value": "John",
                        },
                        {
                            "answer_id": "last-name",
                            "list_item_id": actual["submission"]["data"]["answers"][0][
                                "list_item_id"
                            ],
                            "value": "Doe",
                        },
                        {"answer_id": "anyone-else", "value": "No"},
                    ],
                    "lists": [
                        {
                            "items": [
                                actual["submission"]["data"]["answers"][0][
                                    "list_item_id"
                                ]
                            ],
                            "name": "people",
                        }
                    ],
                },
                "data_version": "0.0.3",
                "flushed": False,
                "launch_language_code": "en",
                "origin": "uk.gov.ons.edc.eq",
                "schema_name": "test_relationships",
                "started_at": actual["submission"]["started_at"],
                "submission_language_code": "en",
                "submitted_at": actual["submission"]["submitted_at"],
                "survey_metadata": {
                    "display_address": "68 Abingdon Road, " "Goathill",
                    "employment_date": "1983-06-02",
                    "period_id": "201604",
                    "period_str": "April 2016",
                    "ref_p_end_date": "2016-04-30",
                    "ref_p_start_date": "2016-04-01",
                    "ru_name": "Integration Testing",
                    "ru_ref": "12345678901A",
                    "survey_id": "0",
                    "trad_as": "Integration Tests",
                    "user_id": "integration-test",
                },
                "tx_id": actual["submission"]["tx_id"],
                "type": "uk.gov.ons.edc.eq:surveyresponse",
                "version": "v2",
            }
        }
        assert actual == expected


class TestDumpRoute(IntegrationTestCase):
    def test_dump_route_not_authenticated(self):
        # Given I am not an authenticated user
        # When I attempt to dump the questionnaire store
        self.get("/dump/routing-path")

        # Then I receive a 401 Unauthorised response code
        self.assertStatusUnauthorised()

    def test_dump_route_authenticated_missing_role(self):
        # Given I am an authenticated user who has launched a survey
        # but does not have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory"
        )

        # When I attempt to dump the questionnaire store
        self.get("/dump/routing-path")

        # Then I receive a 403 Forbidden response code
        self.assertStatusForbidden()

    def test_dump_route_authenticated_with_role(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory",
            roles=["dumper"],
        )

        # And I attempt to dump the questionnaire store
        self.get("/dump/routing-path")

        # Then I get a 200 OK response
        self.assertStatusOK()

    def test_dump_route_authenticated_with_role_no_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(
            schema_name="test_radio_mandatory_with_detail_answer_mandatory",
            roles=["dumper"],
        )

        # When I haven't submitted any answers
        # And I attempt to dump the submission payload
        self.get("/dump/routing-path")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json_loads(self.getResponseData())
        # tx_id and submitted_at are dynamic; so copy them over
        expected = [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "routing_path": ["radio-mandatory"],
            }
        ]

        assert actual == expected

    def test_dump_submission_authenticated_with_role_with_answers(self):
        # Given I am an authenticated user who has launched a survey
        # and does have the 'dumper' role in my metadata
        self.launchSurveyV2(schema_name="test_radio_mandatory", roles=["dumper"])

        # When I submit an answer
        self.post(post_data={"radio-mandatory-answer": "Coffee"})

        # And I attempt to dump the submission payload
        self.get("/dump/routing-path")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        actual = json_loads(self.getResponseData())

        # tx_id and submitted_at are dynamic; so copy them over
        expected = [
            {
                "section_id": "default-section",
                "list_item_id": None,
                "routing_path": ["radio-mandatory"],
            }
        ]
        assert actual == expected
