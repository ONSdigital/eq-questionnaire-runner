from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional

from flask_babel import lazy_gettext

from app.settings import ACCOUNT_SERVICE_BASE_URL_SOCIAL, ONS_URL, ONS_URL_CY, read_file
from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class SocialSurveyConfig(
    SurveyConfig,
):
    base_url: str = ACCOUNT_SERVICE_BASE_URL_SOCIAL
    survey_title: str = "ONS Social Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self) -> None:
        super().__post_init__()

        upstream_base_url = f"{self.base_url}/{self.language_code}"
        ons_url = ONS_URL_CY if self.language_code == "cy" else ONS_URL

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = f"{upstream_base_url}/start/"

        self.cookie_settings_url: str = f"{upstream_base_url}/cookies/"
        self.privacy_and_data_protection_url: str = (
            f"{upstream_base_url}/privacy-and-data-protection/"
        )

        self.contact_us_url: str = f"{ons_url}/aboutus/contactus/surveyenquiries/"
        self.accessibility_url: str = f"{ons_url}/help/accessibility/"
        self.what_we_do_url: str = f"{ons_url}/aboutus/whatwedo/"

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [Link(lazy_gettext("What we do"), self.what_we_do_url).as_dict()]

        if cookie_has_theme:
            links.append(
                Link(lazy_gettext("Contact us"), self.contact_us_url).as_dict()
            )

        links.append(
            Link(
                lazy_gettext("Accessibility"),
                self.accessibility_url,
            ).as_dict()
        )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), self.cookie_settings_url).as_dict(),
                Link(
                    lazy_gettext("Privacy and data protection"),
                    self.privacy_and_data_protection_url,
                ).as_dict(),
            ]

        return None


@dataclass
class UKHSAONSSocialSurveyConfig(SocialSurveyConfig):
    masthead_logo: str = read_file(
        "./templates/assets/images/ons-logo-stacked.svg"
    ) + read_file("./templates/assets/images/ukhsa-logo-stacked.svg")
    masthead_logo_mobile: str = read_file(
        "./templates/assets/images/ons-logo-stacked.svg"
    ) + read_file("./templates/assets/images/ukhsa-logo-stacked.svg")
