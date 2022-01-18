from app.authentication.no_token_exception import NoTokenException


def test_no_token_exception():
    no_token = NoTokenException("test")
    assert "test" == str(no_token)
