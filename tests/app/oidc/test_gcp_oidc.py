import time

import pytest
import responses
from cachetools.func import ttl_cache
from freezegun import freeze_time
from google.auth.exceptions import RefreshError, TransportError
from google.auth.transport.requests import Request
from mock import Mock, patch

from app.oidc.gcp_oidc import TTL, OIDCCredentialsServiceGCP

TEST_SDS_OAUTH2_CLIENT_ID = "TEST_SDS_OAUTH2_CLIENT_ID"
MOCK_TOKEN_URL = "http://mock-url"


@pytest.fixture
def oidc_credentials_service():
    oidc_credentials_service = OIDCCredentialsServiceGCP()
    yield oidc_credentials_service

    # the get credentials method is static, and other tests are affected by the cache, so ensure it is cleared in the fixture teardown
    oidc_credentials_service.get_credentials.cache.clear()


@pytest.fixture
def patch_authentication():
    # this fixture allows reaching the _metadata.get call with dummy credentials data, to observe a mocked request
    with (
        patch(
            "google.auth.compute_engine._metadata.get_service_account_info",
            Mock(return_value={"email": "mock-email@gcp.com"}),
        ),
        patch(
            "google.auth.compute_engine._metadata.ping",
            Mock(return_value=True),
        ),
        patch(
            "google.auth.compute_engine.credentials.jwt._unverified_decode",
            Mock(return_value=(None, {"exp": 1672576200}, None, None)),
        ),
        patch(
            "google.auth._helpers.update_query",
            Mock(return_value=MOCK_TOKEN_URL),
        ),
    ):
        yield


@patch("app.oidc.gcp_oidc.Request")
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials")
def test_get_credentials(mock_token_fetch, mock_request, oidc_credentials_service):
    """
    fetch credentials and check the gcp call is made
    """
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    mock_token_fetch.assert_called_once_with(
        audience=TEST_SDS_OAUTH2_CLIENT_ID, request=mock_request()
    )
    mock_token_fetch.return_value.refresh.assert_called_once_with(mock_request())


@patch("app.oidc.gcp_oidc.Request", Mock)
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials", Mock(side_effect=RefreshError))
def test_get_credentials_failure(oidc_credentials_service):
    """
    Check that if the request for credentials fails, the cache does not get updated
    """
    with pytest.raises(RefreshError):
        oidc_credentials_service.get_credentials(
            iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID
        )

    assert not oidc_credentials_service.get_credentials.cache


@freeze_time("2023-01-01T12:00:00")
@patch("app.oidc.gcp_oidc.Request", Mock)
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials")
def test_get_credentials_ttl(mock_token_fetch, oidc_credentials_service):
    """
    by default, TTLCache uses a cached version of time.monotonic for the timer
    which means that mocking time with freezegun doesn't work, as it won't affect the timer
    to work around this and test the caching, we can replace the timer
    (as per https://github.com/spulec/freezegun/issues/477 )
    """
    # overwrite the timer
    oidc_credentials_service.get_credentials = ttl_cache(
        maxsize=None, ttl=TTL, timer=time.monotonic
    )(oidc_credentials_service.get_credentials.__wrapped__)

    # initial fetch
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    assert mock_token_fetch.call_count == 1
    assert mock_token_fetch.return_value.refresh.call_count == 1

    for datetime_to_invoke_at, expected_call_count in [
        # still valid after 30 minutes (valid until 12:55)
        ("2023-01-01T12:30:00", 1),
        # becomes invalid after 55 minutes (this new call makes it valid until 13:50)
        ("2023-01-01T12:55:00", 2),
        # this fetch is valid for another 1 minute until 13:50
        ("2023-01-01T13:49:00", 2),
        # then at 13:50 it becomes invalid so new call is made
        ("2023-01-01T13:50:00", 3),
    ]:
        # Mock the current time and check the call counter for the credentials service
        with freeze_time(datetime_to_invoke_at):
            oidc_credentials_service.get_credentials(
                iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID
            )
            assert mock_token_fetch.call_count == expected_call_count
            assert (
                mock_token_fetch.return_value.refresh.call_count == expected_call_count
            )


@pytest.mark.usefixtures("patch_authentication")
@freeze_time("2023-01-01T12:00:00")
@responses.activate
def test_get_credentials_with_retry(oidc_credentials_service):
    """
    Test that fetching the credentials is implemented with a retry.
    If the library changes, this test will fail, and we will need to implement our own.
    """
    responses.add(responses.GET, url=MOCK_TOKEN_URL, body=TransportError())
    responses.add(responses.GET, url=MOCK_TOKEN_URL, body=TransportError())
    responses.add(responses.GET, url=MOCK_TOKEN_URL, json={}, status=200)

    # use a side effect of Request so that the code executes as normal but the call count can be tracked
    tracked_request = Mock(side_effect=Request())

    with patch("app.oidc.gcp_oidc.Request", Mock(return_value=tracked_request)):
        credentials = oidc_credentials_service.get_credentials(
            iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID
        )
        assert credentials.valid
        # the request should have 3 attempts, the two transport failures and the success
        assert tracked_request.call_count == 3


@pytest.mark.usefixtures("patch_authentication")
def test_get_credentials_transport_failure(oidc_credentials_service):
    """
    If the request repeatedly fails with transport error, we get a refresh error
    don't assert the error message as it could change, but check the error is raised
    """
    failing_request = Mock(side_effect=TransportError)
    with patch("app.oidc.gcp_oidc.Request", Mock(return_value=failing_request)):
        with pytest.raises(RefreshError):
            oidc_credentials_service.get_credentials(
                iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID
            )
