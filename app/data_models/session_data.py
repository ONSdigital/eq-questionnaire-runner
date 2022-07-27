# pylint: disable=unused-argument
from typing import Any, Optional


class SessionData:
    def __init__(
        self,
        *,
        language_code: Optional[str],
        confirmation_email_count: int = 0,
        feedback_count: int = 0,
        **_: Any,
    ):  # pylint: disable=too-many-locals
        self.language_code = language_code
        self.confirmation_email_count = confirmation_email_count
        self.feedback_count = feedback_count

        # :TODO: Will be removed in the next deployment, kept temporarily to support in-flight sessions and potential rollback
        self.tx_id = None
        self.schema_name = None
        self.period_str = None
        self.launch_language_code = None
        self.ru_name = None
        self.ru_ref = None
        self.response_id = None
        self.case_id = None
        self.case_ref = None
        self.trad_as = None
        self.account_service_base_url = None
        self.account_service_log_out_url = None
        self.display_address = None
        self.schema_url = None

        # :TODO: Remove once `schema_url` has been rolled out successfully.
        # This is only to support a rollback in the event `schema_url` deploy is not successful.
        # Survey URL will not be used to load surveys.
        self.survey_url = None
