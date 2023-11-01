import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_BACKOFF_FACTOR = 0.2
DEFAULT_MAX_RETRIES = (
    2  # Totals no. of request should be 3. The initial request + DEFAULT_MAX_RETRIES
)
DEFAULT_RETRY_STATUS_CODES = [
    408,
    429,
    500,
    502,
    503,
    504,
]


def get_retryable_session(
    *,
    max_retries: int = DEFAULT_MAX_RETRIES,
    retry_status_codes: list[int] | None = None,
    backoff_factor: float = DEFAULT_BACKOFF_FACTOR,
) -> requests.Session:
    session = requests.Session()

    retries = Retry(
        total=max_retries,
        status_forcelist=retry_status_codes or DEFAULT_RETRY_STATUS_CODES,
    )  # Codes to retry according to Google Docs https://cloud.google.com/storage/docs/retry-strategy#client-libraries

    retries.backoff_factor = backoff_factor

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session
