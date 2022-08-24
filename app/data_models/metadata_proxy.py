from typing import Any, Mapping, Optional


class MetadataProxy:
    def __init__(self, metadata: Optional[Mapping[str, Any]]):
        self.metadata = metadata
        self.tx_id = self.get_metadata_value("tx_id")
        self.ru_ref = self.get_metadata_value("ru_ref")
        self.schema_name = self.get_metadata_value("schema_name")
        self.period_str = self.get_metadata_value("period_str")
        self.language_code = self.get_metadata_value("language_code")
        self.ru_name = self.get_metadata_value("ru_name")
        self.response_id = self.get_metadata_value("response_id")
        self.case_id = self.get_metadata_value("case_id")
        self.case_ref = self.get_metadata_value("case_id")
        self.account_service_url = self.get_metadata_value("account_service_url")
        self.trad_as = self.get_metadata_value("trad_as")
        self.display_address = self.get_metadata_value("display_address")
        self.schema_url = self.get_metadata_value("schema_url")
        self.ref_p_start_date = self.get_metadata_value("ref_p_start_date")
        self.ref_p_end_date = self.get_metadata_value("ref_p_end_date")
        self.period_id = self.get_metadata_value("period_id")
        self.employment_date = self.get_metadata_value("employment_date")
        self.form_type = self.get_metadata_value("form_type")
        self.case_type = self.get_metadata_value("case_type")
        self.user_id = self.get_metadata_value("user_id")
        self.region_code = self.get_metadata_value("region_code")
        self.version = self.get_metadata_value("version")
        self.collection_exercise_sid = self.get_metadata_value(
            "collection_exercise_sid"
        )

    def get_metadata_value(self, key: str) -> Any:
        if self.metadata:
            if key in self.metadata:
                return self.metadata[key]
            if (
                self.metadata.get("survey_metadata")
                and key in self.metadata["survey_metadata"]["data"]
            ):
                return self.metadata["survey_metadata"]["data"][key]
        return None
