from mock import patch

from app.oidc.gcp_oidc import OIDCCredentialsServiceGCP

TEST_SDS_OAUTH2_CLIENT_ID = "TEST_SDS_OAUTH2_CLIENT_ID"


@patch("app.oidc.gcp_oidc.Request")
@patch("app.oidc.gcp_oidc.fetch_id_token_credentials")
def test_oidc_credentials_service_gcp_ttl(mock_token_fetch, mock_request):
    oidc_credentials_service = OIDCCredentialsServiceGCP()

    # fetch credentials and check the gcp call is made
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    mock_token_fetch.assert_called_once_with(
        audience=TEST_SDS_OAUTH2_CLIENT_ID, request=mock_request()
    )
    mock_token_fetch.return_value.refresh.assert_called_once_with(mock_request())

    # credentials are cached
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    assert mock_token_fetch.call_count == 1
    assert mock_token_fetch.return_value.refresh.call_count == 1

    # re-fetched when cache expires
    oidc_credentials_service.get_credentials.cache_clear()
    oidc_credentials_service.get_credentials(iap_client_id=TEST_SDS_OAUTH2_CLIENT_ID)
    assert mock_token_fetch.call_count == 2
    assert mock_token_fetch.return_value.refresh.call_count == 2
