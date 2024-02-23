import unittest
from contextlib import contextmanager
from unittest import mock
from unittest.mock import Mock
from uuid import UUID

from flask import Flask, request
from flask_babel import Babel
from mock import patch

from app.cloud_tasks import CloudTaskPublisher
from app.oidc.gcp_oidc import OIDCCredentialsServiceGCP
from app.oidc.local_oidc import OIDCCredentialsServiceLocal
from app.publisher import LogPublisher, PubSubPublisher
from app.setup import MissingEnvironmentVariable, create_app
from app.storage.datastore import Datastore
from app.storage.dynamodb import Dynamodb
from app.submitter.submitter import (
    GCSFeedbackSubmitter,
    GCSSubmitter,
    LogSubmitter,
    RabbitMQSubmitter,
)


class TestCreateApp(unittest.TestCase):  # pylint: disable=too-many-public-methods
    def setUp(self):
        self._setting_overrides = {}

    @contextmanager
    def override_settings(self):
        """Required because although the settings are overridden on the application
        by passing _setting_overrides in, there are many functions which use the
        imported settings object - this does not get the overrides merged in. This
        helper does that.

        Note - this is not very nice, however it's better than polluting the global
        settings.

        Returns a list of contexts."""
        patches = [
            patch(f"app.setup.settings.{k}", v)
            for k, v in self._setting_overrides.items()
        ]
        for p in patches:
            p.start()
        yield patches
        for p in patches:
            p.stop()

    def test_returns_application(self):
        self.assertIsInstance(create_app(self._setting_overrides), Flask)

    def test_sets_content_length(self):
        self.assertGreater(
            create_app(self._setting_overrides).config["MAX_CONTENT_LENGTH"], 0
        )

    def test_enforces_secure_session(self):
        application = create_app(self._setting_overrides)
        self.assertTrue(application.secret_key)
        self.assertTrue(application.permanent_session_lifetime)
        self.assertTrue(application.session_interface)

        # This is derived from EQ_ENABLE_SECURE_SESSION_COOKIE which is false
        # when running tests
        self.assertFalse(application.config["SESSION_COOKIE_SECURE"])

    # localisation may not be used but is currently attached...
    def test_adds_i18n_to_application(self):
        babel = create_app(self._setting_overrides).babel  # pylint: disable=no-member
        self.assertIsInstance(babel, Babel)

    def test_adds_logging_of_request_ids(self):
        with patch("structlog.contextvars.bind_contextvars") as bind_contextvars:
            self._setting_overrides.update({"EQ_APPLICATION_VERSION": False})
            application = create_app(self._setting_overrides)

            application.test_client().get("/")
            self.assertEqual(1, bind_contextvars.call_count)
            _, kwargs = bind_contextvars.call_args
            self.assertTrue(UUID(kwargs["request_id"], version=4))

    def test_adds_logging_of_span_and_trace(self):
        with patch("structlog.contextvars.bind_contextvars") as bind_contextvars:
            self._setting_overrides.update({"EQ_APPLICATION_VERSION": False})
            application = create_app(self._setting_overrides)

            x_cloud_headers = {
                "X-Cloud-Trace-Context": "0123456789/0123456789012345678901;o=1"
            }
            application.test_client().get("/", headers=x_cloud_headers)

            self.assertEqual(2, bind_contextvars.call_count)
            _, kwargs = bind_contextvars.call_args
            self.assertTrue(kwargs["span"] == "0123456789012345678901")
            self.assertTrue(kwargs["trace"] == "0123456789")

    def test_enforces_secure_headers(self):
        self._setting_overrides["EQ_ENABLE_LIVE_RELOAD"] = False

        with create_app(self._setting_overrides).test_client() as client:
            headers = client.get(
                "/",
                headers={
                    "X-Forwarded-Proto": "https"
                },  # set protocol so that talisman sets HSTS headers
            ).headers

            self.assertEqual(
                "no-cache, no-store, must-revalidate", headers["Cache-Control"]
            )
            self.assertEqual("no-cache", headers["Pragma"])
            self.assertEqual(
                "max-age=31536000; includeSubDomains",
                headers["Strict-Transport-Security"],
            )
            self.assertEqual("DENY", headers["X-Frame-Options"])
            self.assertEqual("1; mode=block", headers["X-Xss-Protection"])
            self.assertEqual("nosniff", headers["X-Content-Type-Options"])

    def test_csp_policy_headers(self):
        cdn_url = "https://cdn.test.domain"
        address_lookup_api_url = "https://ai.test.domain"
        self._setting_overrides = {
            "EQ_ENABLE_LIVE_RELOAD": False,
            "CDN_URL": cdn_url,
            "ADDRESS_LOOKUP_API_URL": address_lookup_api_url,
        }

        with create_app(self._setting_overrides).test_client() as client:
            headers = client.get(
                "/",
                headers={
                    "X-Forwarded-Proto": "https"
                },  # set protocol so that talisman sets HSTS headers
            ).headers

            csp_policy_parts = headers["Content-Security-Policy"].split("; ")
            self.assertIn(f"default-src 'self' {cdn_url}", csp_policy_parts)
            self.assertIn(
                "script-src 'self' https://*.googletagmanager.com "
                f"{cdn_url} 'nonce-{request.csp_nonce}'",
                csp_policy_parts,
            )
            self.assertIn(
                f"style-src 'self' https://fonts.googleapis.com 'unsafe-inline' {cdn_url}",
                csp_policy_parts,
            )
            self.assertIn(
                "img-src 'self' data: https://ssl.gstatic.com https://www.gstatic.com https://*.google-analytics.com"
                f" https://*.googletagmanager.com {cdn_url}",
                csp_policy_parts,
            )
            self.assertIn(
                f"font-src 'self' data: https://fonts.gstatic.com {cdn_url}",
                csp_policy_parts,
            )
            self.assertIn(
                "connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com"
                f" https://*.googletagmanager.com {cdn_url} {address_lookup_api_url}",
                csp_policy_parts,
            )
            self.assertIn(
                "object-src 'none'",
                csp_policy_parts,
            )
            self.assertIn(
                "base-uri 'none'",
                csp_policy_parts,
            )

    # Indirectly covered by higher level integration
    # tests, keeping to highlight that create_app is where
    # it happens.
    def test_adds_blueprints(self):
        self.assertGreater(len(create_app(self._setting_overrides).blueprints), 0)

    def test_eq_submission_backend_not_set(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = ""

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Unknown EQ_SUBMISSION_BACKEND" in str(ex.exception)

    def test_adds_gcs_submitter_to_the_application(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = "gcs"
        self._setting_overrides["EQ_GCS_SUBMISSION_BUCKET_ID"] = "123"

        # When
        with patch("google.cloud.storage.Client"):
            application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["submitter"], GCSSubmitter)

    def test_gcs_submitter_bucket_name_not_set_raises_exception(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = "gcs"

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting EQ_GCS_SUBMISSION_BUCKET_ID Missing" in str(ex.exception)

    def test_adds_rabbit_submitter_to_the_application(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = "rabbitmq"
        self._setting_overrides["EQ_RABBITMQ_HOST"] = "host-1"
        self._setting_overrides["EQ_RABBITMQ_HOST_SECONDARY"] = "host-2"

        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["submitter"], RabbitMQSubmitter)

    def test_rabbit_submitter_host_not_set_raises_exception(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = "rabbitmq"
        self._setting_overrides["EQ_RABBITMQ_HOST"] = ""

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting EQ_RABBITMQ_HOST Missing" in str(ex.exception)

    def test_rabbit_submitter_secondary_host_not_set_raises_exception(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_BACKEND"] = "rabbitmq"
        self._setting_overrides["EQ_RABBITMQ_HOST"] = "host-1"
        self._setting_overrides["EQ_RABBITMQ_HOST_SECONDARY"] = ""

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting EQ_RABBITMQ_HOST_SECONDARY Missing" in str(ex.exception)

    def test_defaults_to_adding_the_log_submitter_to_the_application(self):
        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["submitter"], LogSubmitter)

    def test_eq_publisher_backend_not_set(self):
        # Given
        self._setting_overrides["EQ_PUBLISHER_BACKEND"] = ""

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Unknown EQ_PUBLISHER_BACKEND" in str(ex.exception)

    def test_adds_pub_sub_to_the_application(self):
        # Given
        self._setting_overrides["EQ_PUBLISHER_BACKEND"] = "pubsub"
        self._setting_overrides["EQ_FULFILMENT_TOPIC_ID"] = "123"

        # When
        with patch(
            "app.publisher.publisher.google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["publisher"], PubSubPublisher)

    def test_defaults_to_adding_the_log_publisher_to_the_application(self):
        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["publisher"], LogPublisher)

    def test_adds_cloud_task_publisher_to_the_application(self):
        self._setting_overrides["EQ_SUBMISSION_CONFIRMATION_BACKEND"] = "cloud-tasks"
        self._setting_overrides["EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME"] = (
            "test"
        )

        # When
        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["cloud_tasks"], CloudTaskPublisher)

    def test_submission_backend_not_set_raises_exception(self):
        # Given
        self._setting_overrides["EQ_SUBMISSION_CONFIRMATION_BACKEND"] = ""
        self._setting_overrides["EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME"] = (
            "test"
        )

        # When
        with patch(
            "google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            with self.assertRaises(Exception) as ex:
                create_app(self._setting_overrides)

        # Then
        assert "Unknown EQ_SUBMISSION_CONFIRMATION_BACKEND" in str(ex.exception)

    def test_setup_datastore(self):
        self._setting_overrides["EQ_STORAGE_BACKEND"] = "datastore"

        with patch("google.cloud.datastore.Client"):
            application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq["storage"], Datastore)

    def test_setup_dynamodb(self):
        self._setting_overrides["EQ_STORAGE_BACKEND"] = "dynamodb"

        application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq["storage"], Dynamodb)

    def test_invalid_storage(self):
        self._setting_overrides["EQ_STORAGE_BACKEND"] = "invalid"

        with self.assertRaises(Exception):
            create_app(self._setting_overrides)

    def test_eq_feedback_backend_not_set(self):
        # Given
        self._setting_overrides["EQ_FEEDBACK_BACKEND"] = ""

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Unknown EQ_FEEDBACK_BACKEND" in str(ex.exception)

    def test_adds_gcs_feedback_to_the_application(self):
        # Given
        self._setting_overrides["EQ_FEEDBACK_BACKEND"] = "gcs"
        self._setting_overrides["EQ_GCS_FEEDBACK_BUCKET_ID"] = "123456"

        # When
        with patch("google.cloud.storage.Client"):
            application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq["feedback_submitter"], GCSFeedbackSubmitter)

    def test_gcs_feedback_bucket_name_not_set_raises_exception(self):
        # Given
        self._setting_overrides["EQ_FEEDBACK_BACKEND"] = "gcs"

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting EQ_GCS_FEEDBACK_BUCKET_ID Missing" in str(ex.exception)

    def test_defaults_to_gzip_compression(self):
        application = create_app(self._setting_overrides)
        assert application.config["COMPRESS_ALGORITHM"] == ["gzip", "br", "deflate"]

    @mock.patch("yaml.safe_load")
    @mock.patch("app.secrets.REQUIRED_SECRETS", [])
    def test_conditional_expected_secret(self, mock_safe_load):
        mock_safe_load.return_value = {"secrets": {}}
        self._setting_overrides["ADDRESS_LOOKUP_API_AUTH_ENABLED"] = True
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)
        assert "Missing Secret [ADDRESS_LOOKUP_API_AUTH_TOKEN_SECRET]" in str(
            ex.exception
        )

    def test_setup_oidc_service_gcp(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = "gcp"
        self._setting_overrides["SDS_OAUTH2_CLIENT_ID"] = "1234567890"
        self._setting_overrides["CIR_OAUTH2_CLIENT_ID"] = "1234567890"

        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(
            application.eq["oidc_credentials_service"], OIDCCredentialsServiceGCP
        )

    def test_setup_oidc_service_local(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = "local"

        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(
            application.eq["oidc_credentials_service"], OIDCCredentialsServiceLocal
        )

    def test_oidc_backend_invalid_raises_exception(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = "invalid"

        # When
        with self.assertRaises(NotImplementedError) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Unknown OIDC_TOKEN_BACKEND" in str(ex.exception)

    def test_oidc_backend_missing_raises_exception(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = ""

        # When
        with self.assertRaises(MissingEnvironmentVariable) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting OIDC_TOKEN_BACKEND Missing" in str(ex.exception)

    def test_sds_oauth_2_client_id_missing_raises_exception(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = "gcp"
        self._setting_overrides["SDS_OAUTH2_CLIENT_ID"] = ""

        # When
        with self.assertRaises(MissingEnvironmentVariable) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting SDS_OAUTH2_CLIENT_ID Missing" in str(ex.exception)

    def test_cir_oauth_2_client_id_missing_raises_exception(self):
        # Given
        self._setting_overrides["OIDC_TOKEN_BACKEND"] = "gcp"
        self._setting_overrides["SDS_OAUTH2_CLIENT_ID"] = "123456789"
        self._setting_overrides["CIR_OAUTH2_CLIENT_ID"] = ""

        # When
        with self.assertRaises(MissingEnvironmentVariable) as ex:
            create_app(self._setting_overrides)

        # Then
        assert "Setting CIR_OAUTH2_CLIENT_ID Missing" in str(ex.exception)
