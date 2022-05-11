from typing import Any, Optional


class SessionData:
    def __init__(
        self,
        tx_id: Optional[str],
        schema_name: Optional[str],
        period_str: Optional[str],
        language_code: Optional[str],
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
        self.tx_id = tx_id
        self.schema_name = schema_name
        self.period_str = period_str
        self.language_code = language_code
        self.launch_language_code = launch_language_code
        self.ru_name = ru_name
        self.ru_ref = ru_ref
        self.response_id = response_id
        self.case_id = case_id
        self.case_ref = case_ref
        self.trad_as = trad_as
        self.account_service_base_url = account_service_base_url
        self.account_service_log_out_url = account_service_log_out_url
        self.display_address = display_address
        self.confirmation_email_count = confirmation_email_count
        self.feedback_count = feedback_count
        self.schema_url = schema_url

        # :TODO: Remove once `schema_url` has been rolled out successfully.
        # This is only to support a rollback in the event `schema_url` deploy is not successful.
        # Survey URL will not be used to load surveys.
        self.survey_url = None
