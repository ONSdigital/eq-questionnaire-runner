from dataclasses import dataclass
from typing import Optional

from flask_babel import lazy_gettext

from app.survey_config import BusinessSurveyConfig
from app.survey_config.link import HeaderLink


@dataclass
class SocialSurveyConfig(
    BusinessSurveyConfig,
):
    survey_title: str = "ONS Social Surveys"

    def __post_init__(self):
        self.base_url: str = "https://rh.ons.gov.uk"
        super().__post_init__()

        if self.schema:
            self.data_layer: list[dict] = [
                {
                    key: self.schema.json[key]
                    for key in ["survey_id", "title"]
                    if key in self.schema.json
                }
            ]

        self.account_service_my_account_url = None
        self.account_service_todo_url = None

    def get_service_links(
        self, sign_out_url: str, *, is_authenticated: bool, ru_ref: Optional[str]
    ) -> Optional[list[dict]]:
        return [
            HeaderLink(
                lazy_gettext("Help"),
                self._get_account_service_help_url(
                    is_authenticated=is_authenticated, ru_ref=ru_ref
                ),
                id="header-link-help",
            ).__dict__
        ]
