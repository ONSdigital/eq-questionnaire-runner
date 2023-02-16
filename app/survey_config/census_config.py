from dataclasses import dataclass
from typing import Optional

from flask_babel import lazy_gettext
from flask_babel.speaklater import LazyString

from app.survey_config.link import Link
from app.survey_config.survey_config import SurveyConfig

EN_BASE_URL = "https://census.gov.uk"
CY_BASE_URL = "https://cyfrifiad.gov.uk"
NIR_BASE_URL = f"{EN_BASE_URL}/ni"


@dataclass
class CensusSurveyConfig(
    SurveyConfig,
):
    base_url: str = EN_BASE_URL
    account_service_log_out_url: str = f"{base_url}/en/start"
    design_system_theme: str = "census"

    survey_title: LazyString = lazy_gettext("Census 2021")
    sign_out_button_text: str = lazy_gettext("Save and complete later")
    _is_nisra: bool = False

    def get_additional_data_layer_context(self) -> list[dict]:
        return [{"nisra": self._is_nisra}]

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [
            Link(
                lazy_gettext("Help"),
                f"{EN_BASE_URL}/help/how-to-answer-questions/online-questions-help/",
            ).as_dict()
        ]

        if cookie_has_theme:
            links.append(
                Link(lazy_gettext("Contact us"), f"{EN_BASE_URL}/contact-us/").as_dict()
            )

        links.extend(
            [
                Link(
                    lazy_gettext("Languages"),
                    f"{EN_BASE_URL}/help/languages-and-accessibility/languages/",
                ).as_dict(),
                Link(
                    lazy_gettext("BSL and audio videos"),
                    f"{EN_BASE_URL}/help/languages-and-accessibility/accessibility/accessible-videos-with-bsl/",
                ).as_dict(),
            ]
        )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), f"{EN_BASE_URL}/cookies/").as_dict(),
                Link(
                    lazy_gettext("Accessibility statement"),
                    f"{EN_BASE_URL}/accessibility-statement/",
                ).as_dict(),
                Link(
                    lazy_gettext("Privacy and data protection"),
                    f"{EN_BASE_URL}/privacy-and-data-protection/",
                ).as_dict(),
                Link(
                    lazy_gettext("Terms and conditions"),
                    f"{EN_BASE_URL}/terms-and-conditions/",
                ).as_dict(),
            ]

        return None


@dataclass
class WelshCensusSurveyConfig(
    CensusSurveyConfig,
):
    base_url: str = CY_BASE_URL
    account_service_log_out_url: str = f"{base_url}/en/start"

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [
            Link(
                lazy_gettext("Help"),
                f"{CY_BASE_URL}/help/sut-i-ateb-y-cwestiynau/help-y-cwestiynau-ar-lein/",
            ).as_dict()
        ]

        if cookie_has_theme:
            links.append(
                Link(
                    lazy_gettext("Contact us"), f"{CY_BASE_URL}/cysylltu-a-ni/"
                ).as_dict()
            )
        links.extend(
            [
                Link(
                    lazy_gettext("Languages"),
                    f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/ieithoedd/",
                ).as_dict(),
                Link(
                    lazy_gettext("BSL and audio videos"),
                    f"{CY_BASE_URL}/help/ieithoedd-a-hygyrchedd/hygyrchedd/fideos-hygyrch-gyda-bsl/",
                ).as_dict(),
            ]
        )
        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), f"{CY_BASE_URL}/cwcis/").as_dict(),
                Link(
                    lazy_gettext("Accessibility statement"),
                    f"{CY_BASE_URL}/datganiad-hygyrchedd/",
                ).as_dict(),
                Link(
                    lazy_gettext("Privacy and data protection"),
                    f"{CY_BASE_URL}/preifatrwydd-a-diogelu-data/",
                ).as_dict(),
                Link(
                    lazy_gettext("Terms and conditions"),
                    f"{CY_BASE_URL}/telerau-ac-amodau/",
                ).as_dict(),
            ]

        return None


# Census and Nisra theme will no longer work as of 23/11/22
# Theming has been removed from DS in v60 (https://github.com/ONSdigital/eq-questionnaire-runner/pull/951)
@dataclass
class CensusNISRASurveyConfig(
    CensusSurveyConfig,
):
    base_url: str = NIR_BASE_URL
    account_service_log_out_url: str = base_url
    copyright_declaration: LazyString = lazy_gettext(
        "Crown copyright and database rights 2021 NIMA MOU577.501."
    )
    copyright_text: LazyString = lazy_gettext(
        "Use of address data is subject to the terms and conditions."
    )
    _is_nisra: bool = True

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [
            Link(
                lazy_gettext("Help"),
                f"{NIR_BASE_URL}/help/help-with-the-questions/online-questions-help/",
            ).as_dict()
        ]

        if cookie_has_theme:
            links.append(
                Link(
                    lazy_gettext("Contact us"), f"{NIR_BASE_URL}/contact-us/"
                ).as_dict()
            )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), f"{NIR_BASE_URL}/cookies/").as_dict(),
                Link(
                    lazy_gettext("Accessibility statement"),
                    f"{NIR_BASE_URL}/accessibility-statement/",
                ).as_dict(),
                Link(
                    lazy_gettext("Privacy and data protection"),
                    f"{NIR_BASE_URL}/privacy-and-data-protection/",
                ).as_dict(),
                Link(
                    lazy_gettext("Terms and conditions"),
                    f"{NIR_BASE_URL}/terms-and-conditions/",
                ).as_dict(),
            ]

        return None
