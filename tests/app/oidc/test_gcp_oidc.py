import time

from cachetools.func import ttl_cache
from freezegun import freeze_time
from mock import Mock, patch

from app.oidc.gcp_oidc import TTL, OIDCCredentialsServiceGCP

TEST_SDS_OAUTH2_CLIENT_ID = "TEST_SDS_OAUTH2_CLIENT_ID"


@patch("app.oidc.gcp_oidc.Request")
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials")
def test_oidc_credentials_service_gcp(mock_token_fetch, mock_request):
    oidc_credentials_service = OIDCCredentialsServiceGCP()

    # fetch credentials and check the gcp call is made
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    mock_token_fetch.assert_called_once_with(
        audience=TEST_SDS_OAUTH2_CLIENT_ID, request=mock_request()
    )
    mock_token_fetch.return_value.refresh.assert_called_once_with(mock_request())


@freeze_time("2023-01-01T12:00:00")
@patch("app.oidc.gcp_oidc.Request", Mock)
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials")
def test_oidc_credentials_service_gcp_ttl(mock_token_fetch):
    """
    by default, TTLCache uses a cached version of time.monotonic for the timer
    which means that mocking time with freezegun doesn't work, as it won't affect the timer
    to work around this and test the caching, we can replace the timer with a time.monotonic lambda
    """
    oidc_credentials_service = OIDCCredentialsServiceGCP()

    # overwrite the timer
    oidc_credentials_service.get_credentials = ttl_cache(
        maxsize=None,
        ttl=TTL,
        timer=lambda: time.monotonic(),  # pylint: disable-next=unnecessary-lambda
    )(oidc_credentials_service.get_credentials.__wrapped__)

    # initial fetch
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    assert mock_token_fetch.call_count == 1
    assert mock_token_fetch.return_value.refresh.call_count == 1

    for datetime_str, expected_call_count in [
        ("2023-01-01T12:30:00", 1),  # still valid after 30 minutes
        ("2023-01-01T12:55:00", 2),  # becomes invalid after 55 minutes
        ("2023-01-01T13:49:00", 2),  # new fetch is valid for a further 55 minutes
        ("2023-01-01T13:50:00", 3),  # then also becomes invalid
    ]:
        # Mock the current time and check the call counter for the credentials service
        with freeze_time(datetime_str):
            oidc_credentials_service.get_credentials(
                iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID
            )
            assert mock_token_fetch.call_count == expected_call_count
            assert (
                mock_token_fetch.return_value.refresh.call_count == expected_call_count
            )
