class SessionData:
    def __init__(
        self,
        tx_id,
        schema_name,
        period_str,
        language_code,
        launch_language_code,
        survey_url,
        ru_name,
        ru_ref,
        response_id,
        case_id,
        case_ref=None,
        account_service_base_url=None,
        account_service_log_out_url=None,
        trad_as=None,
        display_address=None,
        confirmation_email_count=0,
        feedback_count=0,
        **_,
    ):  # pylint: disable=too-many-locals
        self.tx_id = tx_id
        self.schema_name = schema_name
        self.period_str = period_str
        self.language_code = language_code
        self.launch_language_code = launch_language_code
        self.survey_url = survey_url
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
