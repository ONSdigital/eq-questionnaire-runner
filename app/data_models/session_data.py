# pylint: disable=unused-argument
from typing import Any, Optional


class SessionData:
    def __init__(
        self,
        language_code: Optional[str],
        tx_id: Optional[str],
        schema_name: Optional[str],
        period_str: Optional[str],
        launch_language_code: Optional[str],
        ru_name: Optional[str],
        ru_ref: Optional[str],
        response_id: Optional[str],
        case_id: Optional[str],
        case_ref: Optional[str] = None,
        account_service_base_url: Optional[str] = None,
        account_service_log_out_url: Optional[str] = None,
        trad_as: Optional[str] = None,
        display_address: Optional[str] = None,
        confirmation_email_count: int = 0,
        feedback_count: int = 0,
        schema_url: Optional[str] = None,
        survey_url: Optional[str] = None,  # pylint: disable=unused-argument
        **_: Any,
    ):  # pylint: disable=too-many-locals
        self.language_code = language_code
        self.confirmation_email_count = confirmation_email_count
        self.feedback_count = feedback_count

        # :TODO: To be removed when we migrate to get these vars from questionnaire_store.metadata.
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
