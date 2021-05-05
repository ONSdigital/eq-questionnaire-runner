import json
from datetime import datetime

from tests.integration.integration_test_case import IntegrationTestCase

# pylint: disable=arguments-differ
from tests.integration.questionnaire import SUBMIT_URL_PATH


class MultipleClientTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()

        self.cache = {}

    def launchSurvey(self, client, schema_name="test_textfield", **payload_kwargs):
        token = self.token_generator.create_token(schema_name, **payload_kwargs)
        self.get(client, "/session?token=" + token)

    def get(self, client, url, **kwargs):
        environ, response = client.get(
            url, as_tuple=True, follow_redirects=True, **kwargs
        )

        self._cache_response(client, environ, response)

    def dumpSubmission(self, client):
        cache = self.cache[client]

        self.get(client, "/dump/submission")

        self.assertEqual(cache["last_response"].status_code, 200)

        # And the JSON response contains the data I submitted
        dump_submission = json.loads(cache.get("last_response").get_data(True))
        return dump_submission

    def post(self, client, post_data=None, url=None, action=None, **kwargs):
        cache = self.cache[client]

        if url is None:
            url = cache.get("last_url")

        self.assertIsNotNone(url)

        _post_data = (post_data.copy() or {}) if post_data else {}
        last_csrf_token = cache.get("last_csrf_token")
        if last_csrf_token is not None:
            _post_data.update({"csrf_token": last_csrf_token})

        if action:
            _post_data.update({"action[{action}]".format(action=action): ""})

        environ, response = client.post(
            url, data=_post_data, as_tuple=True, follow_redirects=True, **kwargs
        )

        self._cache_response(client, environ, response)

    def _cache_response(self, client, environ, response):
        cache = self.cache[client]

        cache["last_csrf_token"] = self._extract_csrf_token(response.get_data(True))
        cache["last_response"] = response
        cache["last_url"] = environ["PATH_INFO"]
        if environ["QUERY_STRING"]:
            cache["last_url"] += "?" + environ["QUERY_STRING"]


class TestMultipleLogin(MultipleClientTestCase):
    def setUp(self):
        super().setUp()

        self.client_a = self._application.test_client()
        self.client_b = self._application.test_client()

        self.cache = {self.client_a: {}, self.client_b: {}}

    def test_multiple_users_same_survey(self):
        """Tests that multiple sessions can be created which work on the same
        survey
        """
        input_data = "foo bar"

        # user A inputs an answer
        self.launchSurvey(self.client_a, "test_textfield")
        self.post(self.client_a, {"name-answer": input_data})

        # user B gets taken straight to summary as survey is complete
        self.launchSurvey(self.client_b, "test_textfield")
        last_url_b = self.cache[self.client_b]["last_url"]
        self.assertIn(SUBMIT_URL_PATH, last_url_b)

        # user B manually navigates to answer and can view the value that user A entered
        self.get(self.client_b, "/questionnaire/name-block")
        last_response_b = self.cache[self.client_b]["last_response"]
        self.assertEqual(last_response_b.status_code, 200)
        self.assertIn(input_data, last_response_b.get_data(True))

        # user A continues through playback page and submits
        self.post(self.client_a)
        self.post(self.client_a)

        # user B tries to submit value
        self.post(self.client_b, {"name-answer": "bar baz"})
        last_response_b = self.cache[self.client_b]["last_response"]
        self.assertEqual(last_response_b.status_code, 401)

    def test_concurrent_users_same_survey_different_languages(self):
        """Tests that multiple sessions can be created which work on the same
        survey in different languages
        """

        # user A launches the test language questionnaire in Gaeilge
        self.launchSurvey(self.client_a, "test_language", language_code="ga")
        self.post(self.client_a)
        last_response_a = self.cache[self.client_a]["last_response"]
        self.assertIn("Iontráil ainm", last_response_a.get_data(True))

        # user A changes language to English and has the option to change back
        self.get(self.client_a, "/questionnaire/name-block/?language_code=en")
        last_response_a = self.cache[self.client_a]["last_response"]
        self.assertIn("Please enter a name", last_response_a.get_data(True))
        self.assertIn("Gaeilge", last_response_a.get_data(True))

        # user B launches the same questionnaire but in Welsh
        self.launchSurvey(self.client_b, "test_language", language_code="cy")
        self.post(self.client_b)
        last_response_b = self.cache[self.client_b]["last_response"]
        self.assertIn("Rhowch enw", last_response_b.get_data(True))

        # user B posts an answer and the questionnaire language is still Welsh
        self.post(self.client_b, {"first-name": "John", "last-name": "Smith"})
        last_response_b = self.cache[self.client_b]["last_response"]
        self.assertIn(
            "Beth yw dyddiad geni John Smith?", last_response_b.get_data(True)
        )

        # user A refreshes the page and sees the answers from B
        self.get(self.client_a, "/questionnaire/name-block/")
        last_response_a = self.cache[self.client_a]["last_response"]
        self.assertIn("John", last_response_a.get_data(True))
        self.assertIn("Smith", last_response_a.get_data(True))

        # user A language is still English, but with the option to change it to Gaeilge
        self.assertIn("Please enter a name", last_response_a.get_data(True))
        self.assertIn("Gaeilge", last_response_a.get_data(True))

        # user A changes language to Gaeilge
        self.get(self.client_a, "/questionnaire/name-block/?language_code=ga")
        last_response_a = self.cache[self.client_a]["last_response"]
        self.assertIn("Iontráil ainm", last_response_a.get_data(True))


class TestCollectionMetadataStorage(MultipleClientTestCase):
    def setUp(self):
        super().setUp()

        self.client_a = self._application.test_client()
        self.client_b = self._application.test_client()

        self.cache = {self.client_a: {}, self.client_b: {}}

    def test_multiple_logins_have_same_started_at(self):
        """
        Ensure that started_at is retained between collections
        """
        # User A starts a survey
        self.launchSurvey(self.client_a, "test_introduction", roles=["dumper"])
        # And starts the questionnaire
        self.post(self.client_a, action="start_questionnaire")

        # We dump their submission
        a_submission = self.dumpSubmission(self.client_a)["submission"]

        # User B loads the survey
        self.launchSurvey(self.client_b, "test_introduction", roles=["dumper"])
        # And we dump their submission
        b_submission = self.dumpSubmission(self.client_b)["submission"]

        # Making sure that the started_at field is a datetime and that
        # it is the same for both users
        self.assertEqual(a_submission["started_at"], b_submission["started_at"])

        started_at_datetime = datetime.strptime(
            a_submission["started_at"], "%Y-%m-%dT%H:%M:%S.%f"
        )

        self.assertIsNotNone(started_at_datetime)
