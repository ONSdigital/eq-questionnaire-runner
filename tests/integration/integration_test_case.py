import os
import re
import unittest
import zlib
from unittest.mock import Mock

import fakeredis
from bs4 import BeautifulSoup
from itsdangerous import base64_decode
from mock import patch
from sdc.crypto.key_store import KeyStore

from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.setup import create_app
from app.utilities.json import json_loads
from application import configure_logging
from tests.app.app_context_test_case import MockDatastore
from tests.integration.create_token import TokenGenerator

EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID = "709eb42cfee5570058ce0711f730bfbb7d4c8ade"
SR_USER_AUTHENTICATION_PUBLIC_KEY_KID = "e19091072f920cbf3ca9f436ceba309e7d814a62"

EQ_SUBMISSION_SDX_PRIVATE_KEY = "2225f01580a949801274a5f3e6861947018aff5b"
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY = "fe425f951a0917d7acdd49230b23a5c405c28510"

KEYS_FOLDER = "./tests/jwt-test-keys"


def get_file_contents(filename, trim=False):
    with open(os.path.join(KEYS_FOLDER, filename), "r", encoding="utf-8") as f:
        data = f.read()
        if trim:
            data = data.rstrip("\r\n")
    return data


class IntegrationTestCase(unittest.TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        # Cache for requests
        self.last_url = None
        self.last_response = None
        self.last_csrf_token = None
        self.redirect_url = None
        self.last_response_headers = None

        # Perform setup steps
        self._set_up_app()

    @property
    def test_app(self):
        return self._application

    def _set_up_app(self, setting_overrides=None):
        self._ds = patch("app.setup.datastore.Client", MockDatastore)
        self._ds.start()

        self._redis = patch("app.setup.redis.Redis", fakeredis.FakeStrictRedis)
        self._redis.start()

        configure_logging()

        overrides = {
            "EQ_ENABLE_HTML_MINIFY": False,
            "EQ_SUBMISSION_CONFIRMATION_BACKEND": "log",
        }

        if setting_overrides:
            overrides = overrides | setting_overrides

        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            self._application = create_app(overrides)

        self._key_store = KeyStore(
            {
                "keys": {
                    EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID: {
                        "purpose": KEY_PURPOSE_AUTHENTICATION,
                        "type": "private",
                        "value": get_file_contents(
                            "sdc-rrm-authentication-signing-private-v1.pem"
                        ),
                    },
                    SR_USER_AUTHENTICATION_PUBLIC_KEY_KID: {
                        "purpose": KEY_PURPOSE_AUTHENTICATION,
                        "type": "public",
                        "value": get_file_contents(
                            "sdc-sr-authentication-encryption-public-v1.pem"
                        ),
                    },
                    EQ_SUBMISSION_SDX_PRIVATE_KEY: {
                        "purpose": KEY_PURPOSE_SUBMISSION,
                        "type": "private",
                        "value": get_file_contents(
                            "sdc-sdx-submission-encryption-private-v1.pem"
                        ),
                    },
                    EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY: {
                        "purpose": KEY_PURPOSE_SUBMISSION,
                        "type": "public",
                        "value": get_file_contents(
                            "sdc-sr-submission-signing-private-v1.pem"
                        ),
                    },
                }
            }
        )

        self.token_generator = TokenGenerator(
            self._key_store,
            EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_KID,
            SR_USER_AUTHENTICATION_PUBLIC_KEY_KID,
        )

        self._client = self._application.test_client()
        self.session = self._client.session_transaction()

    def tearDown(self):
        self._ds.stop()
        self._redis.stop()

    def launchSurvey(self, schema_name="test_dates", **payload_kwargs):
        """
        Launch a survey as an authenticated user and follow re-directs
        :param schema_name: The name of the schema to load
        """
        token = self.token_generator.create_token(
            schema_name=schema_name, **payload_kwargs
        )
        self.get("/session?token=" + token)

    def dumpAnswers(self):

        self.get("/dump/answers")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        dump_answers = json_loads(self.getResponseData())
        return dump_answers

    def dumpSubmission(self):

        self.get("/dump/submission")

        # Then I get a 200 OK response
        self.assertStatusOK()

        # And the JSON response contains the data I submitted
        dump_submission = json_loads(self.getResponseData())
        return dump_submission

    def dump_debug(self):
        self.get("/dump/debug")
        self.assertStatusOK()
        return json_loads(self.getResponseData())

    def get(self, url, follow_redirects=True, **kwargs):
        """
        GETs the specified URL, following any redirects.

        If the response contains a CSRF token; it is cached to be use on
        the next POST.

        The URL will be cached for future POST requests.

        :param url: the URL to GET
        """
        response = self._client.get(url, follow_redirects=follow_redirects, **kwargs)

        self._cache_response(response)

    def post(self, post_data=None, url=None, action=None, **kwargs):
        """
        POSTs to the specified URL with post_data and performs a GET
        with the URL from the re-direct.

        Will add the last received CSRF token to the post_data automatically.

        :param url: the URL to POST to; use None to use the last received URL
        :param post_data: the data to POST
        :param action: The button action to post
        """
        if url is None:
            url = self.last_url

        self.assertIsNotNone(url)

        _post_data = (post_data.copy() or {}) if post_data else {}
        if self.last_csrf_token is not None:
            _post_data.update({"csrf_token": self.last_csrf_token})

        if action:
            _post_data.update({f"action[{action}]": ""})

        response = self._client.post(
            url, data=_post_data, follow_redirects=True, **kwargs
        )

        self._cache_response(response)

    def head(self, url, **kwargs):
        """
        Send a HEAD request to the specified URL.

        :param url: the URL to send a HEAD request to
        """
        response = self._client.head(url, **kwargs)

        self._cache_response(response)

    def options(self, url, **kwargs):
        """
        Send an OPTIONS request to the specified URL.

        :param url: the URL to send an OPTION request to
        """
        response = self._client.options(url, **kwargs)

        self._cache_response(response)

    def sign_out(self):
        selected = self.getHtmlSoup().find("a", {"data-qa": "btn-save-sign-out"})
        return self.get(selected["href"])

    def exit(self):
        """
        GETs the sign-out url from the exit button. Does not follow the external
        redirect.
        """
        url = self.getHtmlSoup().find("a", {"data-qa": "btn-exit"})["href"]
        self.get(url, follow_redirects=False)

    def previous(self):
        selector = "#top-previous"
        selected = self.getHtmlSoup().select(selector)
        return self.get(selected[0].get("href"))

    def _cache_response(self, response):
        environ = response.request.environ

        self.last_csrf_token = (
            self._extract_csrf_token(response.get_data(True))
            if response.mimetype == "text/html"
            else None
        )
        self.redirect_url = response.headers.get("Location")
        self.last_response = response
        self.last_response_headers = dict(response.headers)
        self.last_url = environ["PATH_INFO"]
        if environ["QUERY_STRING"]:
            self.last_url += "?" + environ["QUERY_STRING"]

    @staticmethod
    def _extract_csrf_token(html):
        match = re.search(
            r'<input id="csrf_token" name="csrf_token" type="hidden" value="(.+?)"/>',
            html,
        )
        return (match.group(1) or None) if match else None

    def getResponseData(self):
        """
        Returns the last received response data
        """
        return self.last_response.get_data(True)

    def getCookie(self):
        """
        Returns the last received response cookie session
        """
        cookie = self.last_response.headers["Set-Cookie"]
        cookie_session = cookie.split("session=.")[1].split(";")[0]
        decoded_cookie_session = decode_flask_cookie(cookie_session)
        return json_loads(decoded_cookie_session)

    def deleteCookie(self):
        """
        Deletes the test client cookie
        """
        self._client.delete_cookie("localhost", "session")

    def getHtmlSoup(self):
        """
        Returns the last received response data as a BeautifulSoup HTML object
        See https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        :return: a BeautifulSoup object for the response data
        """
        return BeautifulSoup(self.getResponseData(), "html.parser")

    # Extra Helper Assertions
    def assertInHead(self, content):
        self.assertInSelector(content, "head")

    # Extra Helper Assertions
    def assertInBody(self, content):
        self.assertInSelector(content, "body")

    # Extra Helper Assertions
    def assertNotInHead(self, content):
        self.assertNotInSelector(content, "head")

    # Extra Helper Assertions
    def assertNotInBody(self, content):
        self.assertNotInSelector(content, "body")

    def assertInSelector(self, content, selector):
        data = self.getHtmlSoup().select(selector)
        message = f"\n{content} not in \n{data}"

        # intentionally not using assertIn to avoid duplicating the output message
        self.assertTrue(content in str(data), msg=message)

    def assertAnswerInSummary(self, answer, *, answer_id):
        # Get answer using data qa
        data = self.getHtmlSoup().find(attrs={"data-qa": answer_id})
        self.assertTrue(
            data is not None, msg=f"Element not found for answer_id: {answer_id}"
        )

        # Get answer as list to handle all answer types
        clean_data = [i.strip() for i in data.text.split("\n") if i.strip()]
        answer_as_list = answer if isinstance(answer, list) else [answer]

        self.assertTrue(
            answer_as_list == clean_data, msg=f"\n{answer} not in \n{clean_data}"
        )

    def assertInSelectorCSS(self, content, *selectors, **kwargs):
        data = self.getHtmlSoup().find(*selectors, **kwargs)
        message = f"\n{content} not in \n{data}"

        # intentionally not using assertIn to avoid duplicating the output message
        self.assertTrue(content in str(data), msg=message)

    def assertNotInSelector(self, content, selector):
        data = self.getHtmlSoup().select(selector)
        message = f"\n{content} in \n{data}"

        # intentionally not using assertIn to avoid duplicating the output message
        self.assertFalse(content in str(data), msg=message)

    def assertNotInPage(self, content, message=None):

        self.assertNotIn(
            member=str(content), container=self.getResponseData(), msg=str(message)
        )

    def assertRegexPage(self, regex, message=None):

        self.assertRegex(
            text=self.getResponseData(), expected_regex=str(regex), msg=str(message)
        )

    def assertEqualPageTitle(self, title):
        self.assertEqual(title, self.getHtmlSoup().title.string)

    def assertStatusOK(self):
        self.assertStatusCode(200)

    def assertBadRequest(self):
        self.assertStatusCode(400)

    def assertStatusUnauthorised(self):
        self.assertStatusCode(401)

    def assertStatusForbidden(self):
        self.assertStatusCode(403)

    def assertStatusNotFound(self):
        self.assertStatusCode(404)
        self.assertInBody("Page not found")

    def assertStatusCode(self, status_code):
        if self.last_response is not None:
            self.assertEqual(status_code, self.last_response.status_code)
        else:
            self.fail("last_response is invalid")

    def assertEqualUrl(self, url):
        if self.last_url:
            self.assertEqual(url, self.last_url)
        else:
            self.fail("last_url is invalid")

    def assertInUrl(self, content):
        if self.last_url:
            self.assertIn(content, self.last_url)
        else:
            self.fail("last_url is invalid")

    def assertNotInUrl(self, content):
        if self.last_url:
            self.assertNotIn(content, self.last_url)
        else:
            self.fail("last_url is invalid")

    def assertRegexUrl(self, regex):
        if self.last_url:
            self.assertRegex(text=self.last_url, expected_regex=regex)
        else:
            self.fail("last_url is invalid")

    def assertInRedirect(self, content):
        if self.redirect_url:
            self.assertIn(content, self.redirect_url)
        else:
            self.fail("no redirect found")


def decode_flask_cookie(cookie):
    """Decode a Flask cookie."""
    data = cookie.split(".")[0]
    data = base64_decode(data)
    data = zlib.decompress(data)
    return data.decode("utf-8")
