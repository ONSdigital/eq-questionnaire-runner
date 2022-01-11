import os
from datetime import datetime

from structlog import get_logger

logger = get_logger()


def ensure_min(value, minimum):
    if value < minimum:
        logger.warning("value below minimum", value=value, minimum=minimum)
        return minimum
    return value


def parse_mode(string):
    return string.upper() != "FALSE"


def read_file(file_name):
    if file_name and os.path.isfile(file_name):
        logger.debug("reading from file", filename=file_name)
        with open(
            file_name,
            "r",
            encoding="UTF-8",
        ) as file:
            return file.read()
    else:
        logger.info(
            "Did not load file because filename supplied was None or not a file",
            filename=file_name,
        )
        return None


def get_env_or_fail(key):
    value = os.getenv(key)
    if value is None:
        raise Exception(f"Setting '{key}' Missing")

    return value


def utcoffset_or_fail(date_value, key):
    if date_value.utcoffset() is None:
        raise Exception(f"'{key}' datetime offset missing")
    return date_value


DATASTORE_USE_GRPC = parse_mode(os.getenv("DATASTORE_USE_GRPC", "True"))
CDN_URL = os.getenv("CDN_URL", "https://cdn.eq.gcp.onsdigital.uk")
CDN_ASSETS_PATH = os.getenv("CDN_ASSETS_PATH", "/design-system")
EQ_MINIMIZE_ASSETS = parse_mode(os.getenv("EQ_MINIMIZE_ASSETS", "True"))
# max request payload size in bytes
MAX_CONTENT_LENGTH = int(os.getenv("EQ_MAX_HTTP_POST_CONTENT_LENGTH", "65536"))

EQ_ENABLE_LIVE_RELOAD = parse_mode(os.getenv("EQ_ENABLE_LIVE_RELOAD", "False"))

EQ_SECRETS_FILE = os.getenv("EQ_SECRETS_FILE", "secrets.yml")
EQ_KEYS_FILE = os.getenv("EQ_KEYS_FILE", "keys.yml")

EQ_PUBLISHER_BACKEND = os.getenv("EQ_PUBLISHER_BACKEND")
EQ_FULFILMENT_TOPIC_ID = os.getenv("EQ_FULFILMENT_TOPIC_ID", "eq-fulfilment-topic")
EQ_SUBMISSION_CONFIRMATION_QUEUE = os.getenv(
    "EQ_SUBMISSION_CONFIRMATION_QUEUE", "eq-submission-confirmation"
)
EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME = os.getenv(
    "EQ_SUBMISSION_CONFIRMATION_CLOUD_FUNCTION_NAME",
    "eq-submission-confirmation-consumer",
)
EQ_SUBMISSION_CONFIRMATION_BACKEND = os.getenv("EQ_SUBMISSION_CONFIRMATION_BACKEND")
EQ_INDIVIDUAL_RESPONSE_LIMIT = int(os.getenv("EQ_INDIVIDUAL_RESPONSE_LIMIT", "1"))
EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE = utcoffset_or_fail(
    datetime.fromisoformat(get_env_or_fail("EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE")),
    "EQ_INDIVIDUAL_RESPONSE_POSTAL_DEADLINE",
)

EQ_FEEDBACK_LIMIT = int(os.getenv("EQ_FEEDBACK_LIMIT", "10"))
EQ_FEEDBACK_BACKEND = os.getenv("EQ_FEEDBACK_BACKEND")
EQ_GCS_FEEDBACK_BUCKET_ID = os.getenv("EQ_GCS_FEEDBACK_BUCKET_ID")

EQ_SUBMISSION_BACKEND = os.getenv("EQ_SUBMISSION_BACKEND")
EQ_GCS_SUBMISSION_BUCKET_ID = os.getenv("EQ_GCS_SUBMISSION_BUCKET_ID")

EQ_RABBITMQ_HOST = os.getenv("EQ_RABBITMQ_HOST")
EQ_RABBITMQ_HOST_SECONDARY = os.getenv("EQ_RABBITMQ_HOST_SECONDARY")
EQ_RABBITMQ_PORT = int(os.getenv("EQ_RABBITMQ_PORT", "5672"))
EQ_RABBITMQ_QUEUE_NAME = os.getenv("EQ_RABBITMQ_QUEUE_NAME", "submit_q")

EQ_SESSION_TIMEOUT_SECONDS = int(os.getenv("EQ_SESSION_TIMEOUT_SECONDS", str(45 * 60)))

EQ_GOOGLE_TAG_MANAGER_ID = os.getenv("EQ_GOOGLE_TAG_MANAGER_ID")
EQ_GOOGLE_TAG_MANAGER_AUTH = os.getenv("EQ_GOOGLE_TAG_MANAGER_AUTH")

EQ_NEW_RELIC_ENABLED = parse_mode(os.getenv("EQ_NEW_RELIC_ENABLED", "False"))
EQ_APPLICATION_VERSION_PATH = ".application-version"
EQ_APPLICATION_VERSION = read_file(EQ_APPLICATION_VERSION_PATH)

EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS = ensure_min(
    int(os.getenv("EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS", "10000")), 1000
)

EQ_STORAGE_BACKEND = os.getenv("EQ_STORAGE_BACKEND", "datastore")
EQ_DYNAMODB_ENDPOINT = os.getenv("EQ_DYNAMODB_ENDPOINT")
EQ_DYNAMODB_MAX_RETRIES = int(os.getenv("EQ_DYNAMODB_MAX_RETRIES", "5"))
EQ_DYNAMODB_MAX_POOL_CONNECTIONS = int(
    os.getenv("EQ_DYNAMODB_MAX_POOL_CONNECTIONS", "30")
)
EQ_QUESTIONNAIRE_STATE_TABLE_NAME = get_env_or_fail("EQ_QUESTIONNAIRE_STATE_TABLE_NAME")
EQ_SESSION_TABLE_NAME = get_env_or_fail("EQ_SESSION_TABLE_NAME")
EQ_USED_JTI_CLAIM_TABLE_NAME = get_env_or_fail("EQ_USED_JTI_CLAIM_TABLE_NAME")

EQ_REDIS_HOST = get_env_or_fail("EQ_REDIS_HOST")
EQ_REDIS_PORT = get_env_or_fail("EQ_REDIS_PORT")

EQ_ENABLE_SECURE_SESSION_COOKIE = parse_mode(
    os.getenv("EQ_ENABLE_SECURE_SESSION_COOKIE", "True")
)

EQ_ENABLE_HTML_MINIFY = parse_mode(os.getenv("EQ_ENABLE_HTML_MINIFY", "True"))

EQ_JWT_LEEWAY_IN_SECONDS = 120
DEFAULT_LOCALE = "en_GB"

USER_IK = "user_ik"
EQ_SESSION_ID = "eq-session-id"

EQ_LIST_ITEM_ID_LENGTH = 6
MAX_NUMBER = 9999999999

CONFIRMATION_EMAIL_LIMIT = int(os.getenv("CONFIRMATION_EMAIL_LIMIT", "10"))

ADDRESS_LOOKUP_API_URL = os.getenv("ADDRESS_LOOKUP_API_URL")
ADDRESS_LOOKUP_API_AUTH_ENABLED = parse_mode(
    os.getenv("ADDRESS_LOOKUP_API_AUTH_ENABLED", "False")
)
ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS = int(
    os.getenv("ADDRESS_LOOKUP_API_AUTH_TOKEN_LEEWAY_IN_SECONDS", "300")
)

VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS = int(
    os.getenv("VIEW_SUBMITTED_RESPONSE_EXPIRATION_IN_SECONDS", "2700")
)

SURVEY_TYPE = os.getenv("SURVEY_TYPE", "business")


ACCOUNT_SERVICE_BASE_URL = os.getenv(
    "ACCOUNT_SERVICE_BASE_URL", "https://surveys.ons.gov.uk"
)

PRINT_STYLE_SHEET_FILE_PATH = os.getenv(
    "PRINT_STYLE_SHEET_FILEPATH", "templates/assets/styles"
)

ONS_URL = os.getenv("ONS_URL", "https://www.ons.gov.uk")
