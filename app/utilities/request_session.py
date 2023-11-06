import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_retryable_session(
    max_retries: int, retry_status_codes: list[int], backoff_factor: float
) -> requests.Session:
    session = requests.Session()

    retries = Retry(
        total=max_retries,
        status_forcelist=retry_status_codes,
    )  # Codes to retry according to Google Docs https://cloud.google.com/storage/docs/retry-strategy#client-libraries

    retries.backoff_factor = backoff_factor

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session
