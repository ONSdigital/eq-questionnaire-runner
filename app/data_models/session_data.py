from typing import Optional, Union

METADATA_MAPPING_TYPE = Optional[Union[str, int, list]]


class SessionData:
    def __init__(
        self,
        tx_id: METADATA_MAPPING_TYPE,
        schema_name: METADATA_MAPPING_TYPE,
        period_str: METADATA_MAPPING_TYPE,
        language_code: METADATA_MAPPING_TYPE,
        launch_language_code: METADATA_MAPPING_TYPE,
        survey_url: METADATA_MAPPING_TYPE,
        ru_name: METADATA_MAPPING_TYPE,
        ru_ref: METADATA_MAPPING_TYPE,
        response_id: METADATA_MAPPING_TYPE,
        case_id: METADATA_MAPPING_TYPE,
        case_ref: METADATA_MAPPING_TYPE = None,
        account_service_base_url: METADATA_MAPPING_TYPE = None,
        account_service_log_out_url: METADATA_MAPPING_TYPE = None,
        trad_as: METADATA_MAPPING_TYPE = None,
        display_address: str = None,
        confirmation_email_count: int = 0,
        feedback_count: int = 0,
        **_: str,
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
