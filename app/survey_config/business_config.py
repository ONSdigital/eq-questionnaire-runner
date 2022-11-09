from dataclasses import dataclass, field
from typing import Iterable, Mapping, MutableMapping, Optional
from urllib.parse import urlencode
from warnings import warn

from flask_babel import lazy_gettext

from app.survey_config.link import HeaderLink, Link
from app.survey_config.survey_config import SurveyConfig


@dataclass
class BusinessSurveyConfig(
    SurveyConfig
):
    survey_title: str = "ONS Business Surveys"
    footer_links: Iterable[MutableMapping] = field(default_factory=list)
    footer_legal_links: Iterable[Mapping] = field(default_factory=list)

    def __post_init__(self):
        self.base_url = self._stripped_base_url
        super().__post_init__()

        if not self.account_service_log_out_url:
            self.account_service_log_out_url: str = f"{self.base_url}/sign-in/logout"

        if not self.account_service_my_account_url:
            self.account_service_my_account_url: str = f"{self.base_url}/my-account"

        if not self.account_service_todo_url:
            self.account_service_todo_url: str = f"{self.base_url}/surveys/todo"

    def _get_account_service_help_url(
        self, *, is_authenticated: bool, ru_ref: Optional[str]
    ) -> str:
        if self.schema and is_authenticated and ru_ref:
            request_data = {
                "survey_ref": self.schema.json["survey_id"],
                # This is a temporary fix to send upstream only the first 11 characters of the ru_ref.
                # The ru_ref currently is concatenated with the check letter. Which upstream currently do not support.
                # The first 11 characters represents the reporting unit reference.
                # The 12th character is the check letter identifier.
                "ru_ref": ru_ref[:11],
            }
            return f"{self.base_url}/surveys/surveys-help?{urlencode(request_data)}"

        return f"{self.base_url}/help"

    def get_service_links(
        self,
        sign_out_url: str,
        *,
        is_authenticated: bool,
        cookie_has_theme: bool,
        ru_ref: Optional[str],
    ) -> Optional[list[dict]]:
        links = (
            [
                HeaderLink(
                    lazy_gettext("Help"),
                    self._get_account_service_help_url(
                        is_authenticated=is_authenticated, ru_ref=ru_ref
                    ),
                    id="header-link-help",
                ).__dict__
            ]
            if cookie_has_theme
            else []
        )
        if is_authenticated:
            links.extend(
                [
                    HeaderLink(
                        lazy_gettext("My account"),
                        self.account_service_my_account_url,
                        id="header-link-my-account",
                    ).__dict__,
                    HeaderLink(
                        lazy_gettext("Sign out"),
                        sign_out_url,
                        id="header-link-sign-out",
                    ).__dict__,
                ]
            )

        return links

    def get_footer_links(self, cookie_has_theme: bool) -> list[dict]:
        links = [Link(lazy_gettext("What we do"), self.what_we_do_url).__dict__]

        if cookie_has_theme:
            links.append(Link(lazy_gettext("Contact us"), self.contact_us_url).__dict__)

        links.append(
            Link(
                lazy_gettext("Accessibility"),
                self.accessibility_url,
            ).__dict__
        )

        return links

    def get_footer_legal_links(self, cookie_has_theme: bool) -> Optional[list[dict]]:
        if cookie_has_theme:
            return [
                Link(lazy_gettext("Cookies"), self.cookie_settings_url).__dict__,
                Link(
                    lazy_gettext("Privacy and data protection"),
                    self.privacy_and_data_protection_url,
                ).__dict__,
            ]

        return None

    def get_data_layer(self, tx_id: Optional[str] = None) -> list[dict]:
        data_layer = [{"tx_id": tx_id}] if tx_id else []
        if self.schema:
            data_layer.append(
                {
                    key: self.schema.json[key]
                    for key in ["form_type", "survey_id", "title"]
                    if key in self.schema.json
                }
            )
        return data_layer

    @property
    def _stripped_base_url(self) -> str:
        warn(
            "base_url contains extra pathing which will eventually be corrected and this function will need to be removed"
        )
        return self.base_url.replace("/surveys/todo", "")


@dataclass
class NorthernIrelandBusinessSurveyConfig(BusinessSurveyConfig):
    masthead_logo: Optional[str] = '<svg class="ons-svg-logo" xmlns="http://www.w3.org/2000/svg" focusable="false" width="296" height="56" viewBox="0 0 592 112" aria-labelledby="ni-finance-logo-alt"><title id="ni-finance-logo-alt">Northern Ireland Department of Finance logo</title><g class="ons-svg-logo__group" fill="#001f5b"><path d="M148.45 28.94H116.8v1.86h5.42v40.32h-5.42V73h18.38v-1.77h-5.42V51.76h1.78c5.76 0 6.72 1 7.18 8.38v.34h1.44V41.89h-1.44v.24c-.16 5.49-1 7-4.14 7.61a42.89 42.89 0 0 1-4.8.26V31h3.72a40.34 40.34 0 0 1 6.95.18 7.33 7.33 0 0 1 4.05 2.36c1.6 1.78 2.36 3.64 3.29 8v.26h1.43Z"/><path d="M159.95 46.86h-10.89v1.96h4.38v22.51h-4.38v1.85h15.23v-1.85h-4.34V46.86zM156.58 37.81a4.07 4.07 0 0 0 4-4 4 4 0 0 0-3.93-4.06h-.13a3.81 3.81 0 0 0-3.9 3.74v.08a1.71 1.71 0 0 0 0 .32 3.82 3.82 0 0 0 3.67 4ZM192.64 57.1c0-5-.35-6.52-1.95-8.2a10.63 10.63 0 0 0-14.9.92V47H165v1.9h4.48v22.4H165v1.85h14.8v-1.82h-3.9v-7.55c0-7.78.33-10.74 1.6-12.5a5.68 5.68 0 0 1 4.48-2.46 4 4 0 0 1 3.02 1.34c1 1.26 1.27 3.47 1.27 11.33v9.84h-4.07v1.85h14.9v-1.85h-4.48ZM223.15 70.4c-1.18 1-1.28 1-1.68 1-1.12 0-1.18 0-1.18-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.67 0-10.58 3.2-10.58 6.94a3 3 0 0 0 3 3.09h.1a3 3 0 0 0 3.06-2.83v-.27a3.1 3.1 0 0 0-1-2.24c-.24-.34-.24-.34-.24-.5 0-1 2.36-2.46 4.65-2.46a4.37 4.37 0 0 1 3.3 1.18c.67.77.85 1.28.85 5.09v4.25c-10 .24-15.48 3.38-15.48 9 0 3.91 2.87 6.52 7.28 6.52a10.15 10.15 0 0 0 8.36-4.48 5.26 5.26 0 0 0 5.6 4.46 6.9 6.9 0 0 0 4.8-2l.16-.19-1.17-1.43Zm-9.29-10.24v1a15.47 15.47 0 0 1-.85 6.4 5.13 5.13 0 0 1-4.48 2.94 3.49 3.49 0 0 1-3.73-3.23v-.07a3.31 3.31 0 0 1 0-.77c0-4 2.78-6 9.06-6.29ZM252.91 57.1c0-5-.33-6.52-1.93-8.2a10.52 10.52 0 0 0-14.84.92V47h-10.91v1.9h4.48v22.4h-4.48v1.85H240v-1.82h-3.94v-7.55c0-7.78.34-10.74 1.6-12.5a5.65 5.65 0 0 1 4.48-2.46 3.94 3.94 0 0 1 3 1.34c1 1.26 1.28 3.47 1.28 11.33v9.84h-4v1.85h14.8v-1.85H253ZM280 64.53c-1.6 4.8-4.48 7.28-8.46 7.28a5.5 5.5 0 0 1-4.32-1.76c-1-1.28-1.35-3.2-1.35-8 0-11.76 1.76-13.62 6.08-13.62 2.11 0 4.24 1 4.24 1.7l-.17.25a5.61 5.61 0 0 0-1.35 3.2A3.21 3.21 0 0 0 277.6 57h.27a3.37 3.37 0 0 0 3.41-3.34 1.7 1.7 0 0 0 0-.45c0-3.65-4.48-6.94-9.3-6.94a13.8 13.8 0 0 0-13.61 14 13.57 13.57 0 0 0 12.8 13.62c5.25 0 8.72-2.87 11.2-9.14l.16-.43h-2.24ZM305.2 64.19c-1.18 4.8-4.48 7.54-8.45 7.54a5.45 5.45 0 0 1-5-2.69c-.77-1.38-.85-2.62-.85-9.07v-1.73h17v-.34c-.51-7.1-5.07-11.66-11.76-11.66s-12.6 6.5-12.6 13.86 6.09 13.82 12.8 13.82a11.21 11.21 0 0 0 11.2-9.6V64h-2.24Zm-14.4-7.85v-1.19c0-4.91 1.38-6.72 5.09-6.72a3.79 3.79 0 0 1 4 2.37 13.51 13.51 0 0 1 .51 5.58ZM47.95 84l-12-6.94V63.01l12-7.01 12.02 7.01v14.05L47.95 84zM47.95 112l-12-6.94V91.01l12-7.01 12.02 7.01v14.05L47.95 112zM24.02 42.05 12 35.01V20.99l12.02-6.94 11.93 6.94v14.02l-11.93 7.04zM24.02 70.05 12 63.01V49.06l12.02-7.01 11.93 7.01v13.95l-11.93 7.04z"/><path d="M24.02 98.05 12 91.01V77.06l12.02-7.01 11.93 7.01v13.95l-11.93 7.04zM0 56V28l12 7.01v14.05L0 56zM0 84V56l12 7.01v14.05L0 84z"/></g><g class="ons-svg-logo__group" fill="#8b9064"><path d="m47.95 28-12-7.01V7.01l12-7.01 12.02 7.01v13.98L47.95 28zM47.95 56l-12-6.94V35.01l12-7.01 12.02 7.01v14.05L47.95 56zM72 42.05l-12.03-7.04V20.99L72 14.05l12 6.94v14.02l-12 7.04z"/><path d="m72 70.05-12.03-7.04V49.06L72 42.05l12 7.01v13.95l-12 7.04zM72 98.05l-12.03-7.04V77.06L72 70.05l12 7.01v13.95l-12 7.04zM96 56l-12-6.94V35.01L96 28v28zM96 84l-12-6.94V63.01L96 56v28z"/></g><g class="ons-svg-logo__group ons-svg-logo__group--text" fill="#001f5b"><path d="M126.11 1.6H121v15.06h5.66a5.48 5.48 0 0 0 4.48-2.24 8.14 8.14 0 0 0 1.7-5.33A8.21 8.21 0 0 0 131 3.81a5.93 5.93 0 0 0-4.89-2.21Zm-2.91 1.78h3a4.2 4.2 0 0 1 3.63 1.71A7 7 0 0 1 130.86 9a7.33 7.33 0 0 1-1.18 4.32 4.25 4.25 0 0 1-3.57 1.6h-2.91ZM144.24 11.2a6.7 6.7 0 0 0-1.38-4.48 4.55 4.55 0 0 0-3.53-1.6 5.31 5.31 0 0 0-3.75 1.6 6 6 0 0 0-1.42 4.48 6.4 6.4 0 0 0 1.42 4.24 4.73 4.73 0 0 0 3.75 1.6 5.25 5.25 0 0 0 3-.91 4.42 4.42 0 0 0 1.67-2.37l-1.76-.34a3 3 0 0 1-2.9 2.12 3.4 3.4 0 0 1-2.24-.87 4 4 0 0 1-1-3.2h8Zm-8-1.34a3.76 3.76 0 0 1 .91-2.24 2.94 2.94 0 0 1 2.24-1 2.77 2.77 0 0 1 1.6.51 3.17 3.17 0 0 1 .95 1.2 8.74 8.74 0 0 1 .33 1.6ZM151.33 5.15A3.75 3.75 0 0 0 148 7.39v-1.9h-1.69v14.89h1.85v-5.15a3.62 3.62 0 0 0 3.2 1.78 3.87 3.87 0 0 0 3.2-1.6 6.64 6.64 0 0 0 1.3-4.21 7 7 0 0 0-1.25-4.26 3.91 3.91 0 0 0-3.28-1.79Zm-.33 1.7A2.25 2.25 0 0 1 153 8a5.44 5.44 0 0 1 .77 3.2 4.84 4.84 0 0 1-.84 3.3 2.48 2.48 0 0 1-3.48.41 2 2 0 0 1-.26-.24 3.1 3.1 0 0 1-1-2V9.44a4.08 4.08 0 0 1 1-1.87 2.9 2.9 0 0 1 1.81-.72ZM166.4 14.4V9.81a5 5 0 0 0-1-3.55 4.42 4.42 0 0 0-3.31-1c-2.86 0-4.48 1-4.91 3.2l1.79.33c.26-1.28 1.26-1.95 3-1.95a3.42 3.42 0 0 1 1.6.34 2 2 0 0 1 .85.85 7.5 7.5 0 0 1 .19 1.77h-1.41a8.16 8.16 0 0 0-4.9 1.09 3.56 3.56 0 0 0-1.44 2.8 3.4 3.4 0 0 0 1 2.46 4 4 0 0 0 2.9 1 3.92 3.92 0 0 0 3.81-2.24 4.9 4.9 0 0 0 .14 1.71h1.87a10.3 10.3 0 0 1-.18-2.22Zm-5.23 1a2.43 2.43 0 0 1-1.71-.51 1.59 1.59 0 0 1-.58-1.35 1.91 1.91 0 0 1 1.12-1.78 6.33 6.33 0 0 1 3.2-.67 10.68 10.68 0 0 1 1.6 0v.69a3.75 3.75 0 0 1-1.28 2.62 3 3 0 0 1-2.37 1.07ZM174.16 5.15a2.73 2.73 0 0 0-1.6.61 4.49 4.49 0 0 0-1.44 2V5.54h-1.7v11.2h1.78v-6a4 4 0 0 1 1-2.75 2.85 2.85 0 0 1 2.24-1h.4V5.25a2 2 0 0 0-.68-.1ZM180.8 15.47c-1.1 0-1.71-.51-1.71-1.6V7h2.46V5.41h-2.35V2.53l-1.78.17v2.79h-1.93v1.6h1.93v6.4a3 3 0 0 0 2.44 3.37 2.48 2.48 0 0 0 .86 0 10.68 10.68 0 0 0 1.6 0v-1.48a12.79 12.79 0 0 1-1.52.09ZM197.12 5.84a3.62 3.62 0 0 0-2-.69 3.76 3.76 0 0 0-3.47 2.47 3.34 3.34 0 0 0-1-1.7 3.21 3.21 0 0 0-2.24-.77 3.79 3.79 0 0 0-3.3 2.24v-1.9h-1.39v11.2h1.79V10a3.21 3.21 0 0 1 .77-2.24 2.19 2.19 0 0 1 3-.66 1.64 1.64 0 0 1 .33.26 2.55 2.55 0 0 1 .67 1.92v7.42h1.86v-6.28a4.06 4.06 0 0 1 .86-2.71 2.48 2.48 0 0 1 1.85-.86 2 2 0 0 1 1.19.43 1.75 1.75 0 0 1 .67.91 6.67 6.67 0 0 1 .19 1.6v7h1.86v-7a9.87 9.87 0 0 0-.26-2.24 4.2 4.2 0 0 0-1.38-1.71ZM210.56 11.2a6.77 6.77 0 0 0-1.34-4.48 4.49 4.49 0 0 0-3.57-1.6 5.2 5.2 0 0 0-3.71 1.6 6 6 0 0 0-1.36 4.48 6.28 6.28 0 0 0 1.42 4.24 4.66 4.66 0 0 0 3.73 1.6 5.25 5.25 0 0 0 3-.91 4.45 4.45 0 0 0 1.79-2.42l-1.79-.33a2.92 2.92 0 0 1-2.87 2.11 3.35 3.35 0 0 1-2.24-.87 4 4 0 0 1-1-3.2h8Zm-7.86-1.34a3.71 3.71 0 0 1 .92-2.24 2.84 2.84 0 0 1 3.74-.44 3 3 0 0 1 .91 1.2 5.94 5.94 0 0 1 .34 1.6ZM220 5.84a3.75 3.75 0 0 0-2.12-.69 3.87 3.87 0 0 0-3.37 2.24V5.6h-1.71v11.2h1.86v-6.22a4 4 0 0 1 .83-2.72 2.71 2.71 0 0 1 2.11-1 2.07 2.07 0 0 1 1.6.59 2.81 2.81 0 0 1 .61 2.16v7.18h1.77v-6.4a7.22 7.22 0 0 0-.33-2.88A2.72 2.72 0 0 0 220 5.84ZM228.24 15.47c-1.1 0-1.71-.51-1.71-1.6V7H229V5.41h-2.46V2.53l-1.76.17v2.79h-2v1.6h2v6.4a2.93 2.93 0 0 0 2.43 3.33 3.1 3.1 0 0 0 .86 0 14.23 14.23 0 0 0 1.6 0v-1.49a9.62 9.62 0 0 1-1.43.14ZM240.48 5.15a4.69 4.69 0 0 0-3.62 1.6 6.2 6.2 0 0 0-1.44 4.25 7.06 7.06 0 0 0 1.25 4.24 4.56 4.56 0 0 0 3.67 1.68 4.74 4.74 0 0 0 3.82-1.68A6.62 6.62 0 0 0 245.6 11a6.34 6.34 0 0 0-1.34-4.15 4.55 4.55 0 0 0-3.78-1.7Zm0 10.24a2.67 2.67 0 0 1-2.08-1 5.13 5.13 0 0 1-.94-3.39 5 5 0 0 1 .84-3.2 2.73 2.73 0 0 1 2.12-1 2.85 2.85 0 0 1 2.24 1 5.1 5.1 0 0 1 .8 3.42 5 5 0 0 1-.84 3.3 2.88 2.88 0 0 1-2.2.89ZM252.8 1.44a10.71 10.71 0 0 0-1.6-.16 4 4 0 0 0-2.46.75c-.68.5-1 1.6-1 3.39h-1.86V7h1.86v9.6h1.87V7h2.61V5.42h-2.62v-.27a2.23 2.23 0 0 1 .51-1.77 2.13 2.13 0 0 1 1.6-.52 4.63 4.63 0 0 1 1 .18v-1.6ZM353.09 2h-2.24l-4.8 15h1.79l1.34-4.32h5.43l1.6 4.4h2.11L353.17 2Zm.83 9.2h-4.48l2.24-6.72ZM366.62 6.22a3.66 3.66 0 0 0-2.12-.68 3.91 3.91 0 0 0-3.4 2.12V5.87h-1.85v11.2h1.85V11a4.11 4.11 0 0 1 .9-2.76 2.74 2.74 0 0 1 2.13-1 2.11 2.11 0 0 1 1.52.59 3 3 0 0 1 .67 2.24v7.08H368v-6.53a7.22 7.22 0 0 0-.34-2.88 2.73 2.73 0 0 0-1.04-1.52ZM386.5 8.58a4.71 4.71 0 0 0 .7-2.18 4.33 4.33 0 0 0-1.2-2.86 4.81 4.81 0 0 0-3.62-1.41h-5.92v15h1.95v-6.51h4.15l2.75 6.4h2.11l-3-6.94a3.37 3.37 0 0 0 2.08-1.5Zm-8.12-4.72h4a3 3 0 0 1 2 .67 2.24 2.24 0 0 1 .77 1.76 2.68 2.68 0 0 1-.77 2 3 3 0 0 1-2.24.77h-3.84ZM393.6 5.62a4.8 4.8 0 0 0-3.6 1.6 6.45 6.45 0 0 0-1.44 4.24 6.87 6.87 0 0 0 1.33 4.2 4.31 4.31 0 0 0 3.63 1.6 4.61 4.61 0 0 0 3.67-1.6 6.39 6.39 0 0 0 1.45-4.24 6 6 0 0 0-1.36-4.14 4.3 4.3 0 0 0-3.68-1.66Zm0 10.16a2.68 2.68 0 0 1-2.1-1 5 5 0 0 1-.86-3.39 4.9 4.9 0 0 1 .86-3.2 2.6 2.6 0 0 1 2.1-1 2.71 2.71 0 0 1 2.11 1 4.93 4.93 0 0 1 .85 3.31 4.78 4.78 0 0 1-.85 3.3 2.83 2.83 0 0 1-2.19.91ZM400.53 5.87h1.86v11.15h-1.86zM400.46 2h2.03v2.11h-2.03zM412.62 6.22a3.55 3.55 0 0 0-2.09-.68 3.85 3.85 0 0 0-3.39 2.12V5.87h-1.7v11.2h1.89V11a4 4 0 0 1 .81-2.72 2.77 2.77 0 0 1 2.24-1 2.13 2.13 0 0 1 1.6.59 2.91 2.91 0 0 1 .68 2.24v7.08h1.74v-6.57a8.05 8.05 0 0 0-.34-2.88 2.66 2.66 0 0 0-1.44-1.52ZM425.6 7.74a3.58 3.58 0 0 0-3.3-2.12 3.78 3.78 0 0 0-3.37 2.24v-1.8h-1.79v11.2h1.74V11a4.05 4.05 0 0 1 .85-2.7 2.69 2.69 0 0 1 2.24-1 2 2 0 0 1 1.52.57 2.83 2.83 0 0 1 .67 2.24v7.09h1.78v-6.58a8.05 8.05 0 0 0-.34-2.88ZM387.2 38.29a4.07 4.07 0 0 0 4-4 4 4 0 0 0-3.88-4.05h-.1a4 4 0 0 0 0 8ZM390.56 47.25h-10.93v1.85h4.48v22.58h-8.37L361.6 29.23h-2.24l-14.91 42.45h-3.2v1.92h11.2v-1.92h-5.59l4.05-12.19h12.8l4 12.19h-5.57v1.92H395v-1.92h-4.48ZM362.88 57.6h-11.2l5.73-16.94ZM413.49 46.66c-2.88 0-5.09 1.85-6.87 5.66v-5.07h-10.91v1.85h4.48v22.58h-4.48v1.92h15.23v-1.92h-4.32v-5.82c0-7.62.68-11.2 2.53-14.56.61-1 1.28-1.6 1.6-1.6s.26 0 .35.68c.16 2.53 1.17 3.81 3.2 3.81a3.45 3.45 0 0 0 3.57-3.33v-.32a4 4 0 0 0-4.05-4ZM440.21 49.6s.27 0 .41.85a2.24 2.24 0 0 0 2.23 2.25h.24a2.68 2.68 0 0 0 2.69-2.65v-.27a3.2 3.2 0 0 0-3.2-3.2h-.32a6.38 6.38 0 0 0-4.48 2.52 11.25 11.25 0 0 0-7.38-2.52c-6.1 0-10.66 4-10.66 9.6a9 9 0 0 0 3.88 7.36c-3.72 2.54-5.59 5.23-5.59 8.2a5.94 5.94 0 0 0 4.37 5.7 6.28 6.28 0 0 0-4.48 5.84c0 4.48 5.49 8.11 12.24 8.11 8 0 14-5.25 14-12.43 0-5.33-2.24-7.34-8-7.34l-10.92.16c-3.2 0-3.81-.77-3.81-2.12s1.45-3.29 4.16-5a10.42 10.42 0 0 0 5 1c6.1 0 10.76-3.87 10.76-9.12a10.13 10.13 0 0 0-2-6c.36-.83.52-.94.86-.94Zm-9.81 14c-3 0-3.81-1.28-3.81-5.84 0-8.55.59-9.22 4-9.22 3 0 3.81.59 3.81 6.4 0 4.8-.18 6.18-.67 7.09a3.77 3.77 0 0 1-3.33 1.54Zm-.24 25.6c-4.66 0-7.78-2.63-7.78-6.59a6.75 6.75 0 0 1 2-4.8h.27a21.91 21.91 0 0 0 3.71.17h3.4a18.58 18.58 0 0 0 2.36 0H438c2.87 0 3.39.83 3.39 2.45-.06 4.83-5 8.8-11.26 8.8Z"/><path d="M469.73 58.58v-.34c-.5-7.1-5.06-11.66-11.76-11.66s-12.59 6.51-12.59 13.85 6.09 13.81 12.8 13.81a11.21 11.21 0 0 0 11.2-9.6v-.34h-2.24v.24c-1.19 4.8-4.48 7.54-8.45 7.54a5.43 5.43 0 0 1-5-2.69c-.76-1.37-.85-2.65-.85-9v-1.6h16.91Zm-11.92-9.91a3.76 3.76 0 0 1 4 2.39 12.92 12.92 0 0 1 .51 5.56h-9.6v-1.18c0-4.91 1.37-6.77 5.09-6.77ZM496.48 70.77c-1.2 1-1.28 1-1.71 1-1.09 0-1.19 0-1.19-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.68 0-10.57 3.2-10.57 6.94a3 3 0 0 0 2.93 3.1h.09a2.92 2.92 0 0 0 3-2.81.71.71 0 0 0 0-.29 3.18 3.18 0 0 0-1-2.24c-.24-.34-.24-.34-.24-.5 0-1 2.37-2.46 4.64-2.46a4.37 4.37 0 0 1 3.32 1.18c.67.77.84 1.28.84 5.09v4.23c-10 .25-15.5 3.39-15.5 9 0 3.9 2.9 6.52 7.28 6.52a10.21 10.21 0 0 0 8.38-4.48 5.23 5.23 0 0 0 5.57 4.48 6.87 6.87 0 0 0 4.8-2l.16-.18-1.2-1.42Zm-9.39-10.29v1a15.15 15.15 0 0 1-.85 6.4 5.16 5.16 0 0 1-4.48 2.94 3.5 3.5 0 0 1-3.76-3.2 3 3 0 0 1 0-.73c0-4.17 2.82-6.09 9.09-6.41ZM524.16 29.33h-10.91v1.85h4.48v20.16a8.42 8.42 0 0 0-7.52-4.48c-6 0-11.2 6.24-11.2 13.68s5.17 14 11.42 14a8.32 8.32 0 0 0 7.28-4.48v4h10.82v-1.92h-4.37Zm-13.44 42.86a4 4 0 0 1-3.47-2.19c-.67-1.34-.85-2.7-.85-8.62 0-6.72.27-9.23.94-10.58a4.18 4.18 0 0 1 3.28-2c3.91 0 6.72 4.91 6.72 11.76s-2.76 11.63-6.62 11.63ZM554.5 70.77c-1.2 1-1.27 1-1.68 1-1.11 0-1.2 0-1.2-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.67 0-10.58 3.2-10.58 6.94a3 3 0 0 0 3 3.1h.09a2.94 2.94 0 0 0 3.1-2.77v-.33a3.18 3.18 0 0 0-1-2.24c-.27-.34-.27-.34-.27-.5 0-1 2.38-2.46 4.66-2.46a4.39 4.39 0 0 1 3.29 1.18c.71.77.85 1.28.85 5.09v4.23c-10 .25-15.47 3.39-15.47 9 0 3.9 2.86 6.52 7.28 6.52a10.21 10.21 0 0 0 8.38-4.48 5.21 5.21 0 0 0 5.57 4.48 6.69 6.69 0 0 0 4.8-2l.18-.18-1.19-1.42Zm-9.4-10.29v1a15 15 0 0 1-.84 6.4 5.12 5.12 0 0 1-4.48 2.94 3.49 3.49 0 0 1-3.75-3.2 5 5 0 0 1 0-.77c-.03-4.13 2.82-6.05 9.07-6.37ZM564.05 38.29a4.12 4.12 0 0 0 4-4 4 4 0 0 0-4-4.05H564a3.8 3.8 0 0 0-4 3.61 1.48 1.48 0 0 0 0 .42 4 4 0 0 0 3.94 4ZM567.44 47.25h-10.82v1.93h4.29V71.7h-4.29v1.93h15.14V71.7h-4.32V47.25zM582.58 56.38c-5.24-.94-6.18-1.71-6.18-3.47a4.88 4.88 0 0 1 5.42-4.24 7.12 7.12 0 0 1 7.09 6.27v.26h1.6l-.25-8.29h-1.46l-.94 2a9.64 9.64 0 0 0-6.16-2.24 8 8 0 0 0-8.23 7.77V55c0 5.23 2.37 7.44 9.14 8.62 5 .76 5.92 2 5.92 3.88a5.15 5.15 0 0 1-5.48 4.8h-.19c-4.14 0-6.52-2.53-8.11-8.72v-.24h-1.44l.16 10.38h1.19l1.44-1.94a9.79 9.79 0 0 0 6.84 2.61 8.72 8.72 0 0 0 8.71-8.73V65c-.02-5-2.53-7.53-9.07-8.62ZM323.46 0h2.24v90.67h-2.24z"/></g></svg>'
    masthead_logo_mobile: Optional[str] = '<svg class="ons-svg-logo" xmlns="http://www.w3.org/2000/svg" focusable="false" width="184" height="35" viewBox="0 0 592 112" aria-labelledby="ni-finance-logo-mobile-alt"><title id="ni-finance-logo-mobile-alt">Northern Ireland Department of Finance logo</title><g class="ons-svg-logo__group" fill="#001f5b"><path d="M148.45 28.94H116.8v1.86h5.42v40.32h-5.42V73h18.38v-1.77h-5.42V51.76h1.78c5.76 0 6.72 1 7.18 8.38v.34h1.44V41.89h-1.44v.24c-.16 5.49-1 7-4.14 7.61a42.89 42.89 0 0 1-4.8.26V31h3.72a40.34 40.34 0 0 1 6.95.18 7.33 7.33 0 0 1 4.05 2.36c1.6 1.78 2.36 3.64 3.29 8v.26h1.43Z"/><path d="M159.95 46.86h-10.89v1.96h4.38v22.51h-4.38v1.85h15.23v-1.85h-4.34V46.86zM156.58 37.81a4.07 4.07 0 0 0 4-4 4 4 0 0 0-3.93-4.06h-.13a3.81 3.81 0 0 0-3.9 3.74v.08a1.71 1.71 0 0 0 0 .32 3.82 3.82 0 0 0 3.67 4ZM192.64 57.1c0-5-.35-6.52-1.95-8.2a10.63 10.63 0 0 0-14.9.92V47H165v1.9h4.48v22.4H165v1.85h14.8v-1.82h-3.9v-7.55c0-7.78.33-10.74 1.6-12.5a5.68 5.68 0 0 1 4.48-2.46 4 4 0 0 1 3.02 1.34c1 1.26 1.27 3.47 1.27 11.33v9.84h-4.07v1.85h14.9v-1.85h-4.48ZM223.15 70.4c-1.18 1-1.28 1-1.68 1-1.12 0-1.18 0-1.18-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.67 0-10.58 3.2-10.58 6.94a3 3 0 0 0 3 3.09h.1a3 3 0 0 0 3.06-2.83v-.27a3.1 3.1 0 0 0-1-2.24c-.24-.34-.24-.34-.24-.5 0-1 2.36-2.46 4.65-2.46a4.37 4.37 0 0 1 3.3 1.18c.67.77.85 1.28.85 5.09v4.25c-10 .24-15.48 3.38-15.48 9 0 3.91 2.87 6.52 7.28 6.52a10.15 10.15 0 0 0 8.36-4.48 5.26 5.26 0 0 0 5.6 4.46 6.9 6.9 0 0 0 4.8-2l.16-.19-1.17-1.43Zm-9.29-10.24v1a15.47 15.47 0 0 1-.85 6.4 5.13 5.13 0 0 1-4.48 2.94 3.49 3.49 0 0 1-3.73-3.23v-.07a3.31 3.31 0 0 1 0-.77c0-4 2.78-6 9.06-6.29ZM252.91 57.1c0-5-.33-6.52-1.93-8.2a10.52 10.52 0 0 0-14.84.92V47h-10.91v1.9h4.48v22.4h-4.48v1.85H240v-1.82h-3.94v-7.55c0-7.78.34-10.74 1.6-12.5a5.65 5.65 0 0 1 4.48-2.46 3.94 3.94 0 0 1 3 1.34c1 1.26 1.28 3.47 1.28 11.33v9.84h-4v1.85h14.8v-1.85H253ZM280 64.53c-1.6 4.8-4.48 7.28-8.46 7.28a5.5 5.5 0 0 1-4.32-1.76c-1-1.28-1.35-3.2-1.35-8 0-11.76 1.76-13.62 6.08-13.62 2.11 0 4.24 1 4.24 1.7l-.17.25a5.61 5.61 0 0 0-1.35 3.2A3.21 3.21 0 0 0 277.6 57h.27a3.37 3.37 0 0 0 3.41-3.34 1.7 1.7 0 0 0 0-.45c0-3.65-4.48-6.94-9.3-6.94a13.8 13.8 0 0 0-13.61 14 13.57 13.57 0 0 0 12.8 13.62c5.25 0 8.72-2.87 11.2-9.14l.16-.43h-2.24ZM305.2 64.19c-1.18 4.8-4.48 7.54-8.45 7.54a5.45 5.45 0 0 1-5-2.69c-.77-1.38-.85-2.62-.85-9.07v-1.73h17v-.34c-.51-7.1-5.07-11.66-11.76-11.66s-12.6 6.5-12.6 13.86 6.09 13.82 12.8 13.82a11.21 11.21 0 0 0 11.2-9.6V64h-2.24Zm-14.4-7.85v-1.19c0-4.91 1.38-6.72 5.09-6.72a3.79 3.79 0 0 1 4 2.37 13.51 13.51 0 0 1 .51 5.58ZM47.95 84l-12-6.94V63.01l12-7.01 12.02 7.01v14.05L47.95 84zM47.95 112l-12-6.94V91.01l12-7.01 12.02 7.01v14.05L47.95 112zM24.02 42.05 12 35.01V20.99l12.02-6.94 11.93 6.94v14.02l-11.93 7.04zM24.02 70.05 12 63.01V49.06l12.02-7.01 11.93 7.01v13.95l-11.93 7.04z"/><path d="M24.02 98.05 12 91.01V77.06l12.02-7.01 11.93 7.01v13.95l-11.93 7.04zM0 56V28l12 7.01v14.05L0 56zM0 84V56l12 7.01v14.05L0 84z"/></g><g class="ons-svg-logo__group" fill="#8b9064"><path d="m47.95 28-12-7.01V7.01l12-7.01 12.02 7.01v13.98L47.95 28zM47.95 56l-12-6.94V35.01l12-7.01 12.02 7.01v14.05L47.95 56zM72 42.05l-12.03-7.04V20.99L72 14.05l12 6.94v14.02l-12 7.04z"/><path d="m72 70.05-12.03-7.04V49.06L72 42.05l12 7.01v13.95l-12 7.04zM72 98.05l-12.03-7.04V77.06L72 70.05l12 7.01v13.95l-12 7.04zM96 56l-12-6.94V35.01L96 28v28zM96 84l-12-6.94V63.01L96 56v28z"/></g><g class="ons-svg-logo__group ons-svg-logo__group--text" fill="#001f5b"><path d="M126.11 1.6H121v15.06h5.66a5.48 5.48 0 0 0 4.48-2.24 8.14 8.14 0 0 0 1.7-5.33A8.21 8.21 0 0 0 131 3.81a5.93 5.93 0 0 0-4.89-2.21Zm-2.91 1.78h3a4.2 4.2 0 0 1 3.63 1.71A7 7 0 0 1 130.86 9a7.33 7.33 0 0 1-1.18 4.32 4.25 4.25 0 0 1-3.57 1.6h-2.91ZM144.24 11.2a6.7 6.7 0 0 0-1.38-4.48 4.55 4.55 0 0 0-3.53-1.6 5.31 5.31 0 0 0-3.75 1.6 6 6 0 0 0-1.42 4.48 6.4 6.4 0 0 0 1.42 4.24 4.73 4.73 0 0 0 3.75 1.6 5.25 5.25 0 0 0 3-.91 4.42 4.42 0 0 0 1.67-2.37l-1.76-.34a3 3 0 0 1-2.9 2.12 3.4 3.4 0 0 1-2.24-.87 4 4 0 0 1-1-3.2h8Zm-8-1.34a3.76 3.76 0 0 1 .91-2.24 2.94 2.94 0 0 1 2.24-1 2.77 2.77 0 0 1 1.6.51 3.17 3.17 0 0 1 .95 1.2 8.74 8.74 0 0 1 .33 1.6ZM151.33 5.15A3.75 3.75 0 0 0 148 7.39v-1.9h-1.69v14.89h1.85v-5.15a3.62 3.62 0 0 0 3.2 1.78 3.87 3.87 0 0 0 3.2-1.6 6.64 6.64 0 0 0 1.3-4.21 7 7 0 0 0-1.25-4.26 3.91 3.91 0 0 0-3.28-1.79Zm-.33 1.7A2.25 2.25 0 0 1 153 8a5.44 5.44 0 0 1 .77 3.2 4.84 4.84 0 0 1-.84 3.3 2.48 2.48 0 0 1-3.48.41 2 2 0 0 1-.26-.24 3.1 3.1 0 0 1-1-2V9.44a4.08 4.08 0 0 1 1-1.87 2.9 2.9 0 0 1 1.81-.72ZM166.4 14.4V9.81a5 5 0 0 0-1-3.55 4.42 4.42 0 0 0-3.31-1c-2.86 0-4.48 1-4.91 3.2l1.79.33c.26-1.28 1.26-1.95 3-1.95a3.42 3.42 0 0 1 1.6.34 2 2 0 0 1 .85.85 7.5 7.5 0 0 1 .19 1.77h-1.41a8.16 8.16 0 0 0-4.9 1.09 3.56 3.56 0 0 0-1.44 2.8 3.4 3.4 0 0 0 1 2.46 4 4 0 0 0 2.9 1 3.92 3.92 0 0 0 3.81-2.24 4.9 4.9 0 0 0 .14 1.71h1.87a10.3 10.3 0 0 1-.18-2.22Zm-5.23 1a2.43 2.43 0 0 1-1.71-.51 1.59 1.59 0 0 1-.58-1.35 1.91 1.91 0 0 1 1.12-1.78 6.33 6.33 0 0 1 3.2-.67 10.68 10.68 0 0 1 1.6 0v.69a3.75 3.75 0 0 1-1.28 2.62 3 3 0 0 1-2.37 1.07ZM174.16 5.15a2.73 2.73 0 0 0-1.6.61 4.49 4.49 0 0 0-1.44 2V5.54h-1.7v11.2h1.78v-6a4 4 0 0 1 1-2.75 2.85 2.85 0 0 1 2.24-1h.4V5.25a2 2 0 0 0-.68-.1ZM180.8 15.47c-1.1 0-1.71-.51-1.71-1.6V7h2.46V5.41h-2.35V2.53l-1.78.17v2.79h-1.93v1.6h1.93v6.4a3 3 0 0 0 2.44 3.37 2.48 2.48 0 0 0 .86 0 10.68 10.68 0 0 0 1.6 0v-1.48a12.79 12.79 0 0 1-1.52.09ZM197.12 5.84a3.62 3.62 0 0 0-2-.69 3.76 3.76 0 0 0-3.47 2.47 3.34 3.34 0 0 0-1-1.7 3.21 3.21 0 0 0-2.24-.77 3.79 3.79 0 0 0-3.3 2.24v-1.9h-1.39v11.2h1.79V10a3.21 3.21 0 0 1 .77-2.24 2.19 2.19 0 0 1 3-.66 1.64 1.64 0 0 1 .33.26 2.55 2.55 0 0 1 .67 1.92v7.42h1.86v-6.28a4.06 4.06 0 0 1 .86-2.71 2.48 2.48 0 0 1 1.85-.86 2 2 0 0 1 1.19.43 1.75 1.75 0 0 1 .67.91 6.67 6.67 0 0 1 .19 1.6v7h1.86v-7a9.87 9.87 0 0 0-.26-2.24 4.2 4.2 0 0 0-1.38-1.71ZM210.56 11.2a6.77 6.77 0 0 0-1.34-4.48 4.49 4.49 0 0 0-3.57-1.6 5.2 5.2 0 0 0-3.71 1.6 6 6 0 0 0-1.36 4.48 6.28 6.28 0 0 0 1.42 4.24 4.66 4.66 0 0 0 3.73 1.6 5.25 5.25 0 0 0 3-.91 4.45 4.45 0 0 0 1.79-2.42l-1.79-.33a2.92 2.92 0 0 1-2.87 2.11 3.35 3.35 0 0 1-2.24-.87 4 4 0 0 1-1-3.2h8Zm-7.86-1.34a3.71 3.71 0 0 1 .92-2.24 2.84 2.84 0 0 1 3.74-.44 3 3 0 0 1 .91 1.2 5.94 5.94 0 0 1 .34 1.6ZM220 5.84a3.75 3.75 0 0 0-2.12-.69 3.87 3.87 0 0 0-3.37 2.24V5.6h-1.71v11.2h1.86v-6.22a4 4 0 0 1 .83-2.72 2.71 2.71 0 0 1 2.11-1 2.07 2.07 0 0 1 1.6.59 2.81 2.81 0 0 1 .61 2.16v7.18h1.77v-6.4a7.22 7.22 0 0 0-.33-2.88A2.72 2.72 0 0 0 220 5.84ZM228.24 15.47c-1.1 0-1.71-.51-1.71-1.6V7H229V5.41h-2.46V2.53l-1.76.17v2.79h-2v1.6h2v6.4a2.93 2.93 0 0 0 2.43 3.33 3.1 3.1 0 0 0 .86 0 14.23 14.23 0 0 0 1.6 0v-1.49a9.62 9.62 0 0 1-1.43.14ZM240.48 5.15a4.69 4.69 0 0 0-3.62 1.6 6.2 6.2 0 0 0-1.44 4.25 7.06 7.06 0 0 0 1.25 4.24 4.56 4.56 0 0 0 3.67 1.68 4.74 4.74 0 0 0 3.82-1.68A6.62 6.62 0 0 0 245.6 11a6.34 6.34 0 0 0-1.34-4.15 4.55 4.55 0 0 0-3.78-1.7Zm0 10.24a2.67 2.67 0 0 1-2.08-1 5.13 5.13 0 0 1-.94-3.39 5 5 0 0 1 .84-3.2 2.73 2.73 0 0 1 2.12-1 2.85 2.85 0 0 1 2.24 1 5.1 5.1 0 0 1 .8 3.42 5 5 0 0 1-.84 3.3 2.88 2.88 0 0 1-2.2.89ZM252.8 1.44a10.71 10.71 0 0 0-1.6-.16 4 4 0 0 0-2.46.75c-.68.5-1 1.6-1 3.39h-1.86V7h1.86v9.6h1.87V7h2.61V5.42h-2.62v-.27a2.23 2.23 0 0 1 .51-1.77 2.13 2.13 0 0 1 1.6-.52 4.63 4.63 0 0 1 1 .18v-1.6ZM353.09 2h-2.24l-4.8 15h1.79l1.34-4.32h5.43l1.6 4.4h2.11L353.17 2Zm.83 9.2h-4.48l2.24-6.72ZM366.62 6.22a3.66 3.66 0 0 0-2.12-.68 3.91 3.91 0 0 0-3.4 2.12V5.87h-1.85v11.2h1.85V11a4.11 4.11 0 0 1 .9-2.76 2.74 2.74 0 0 1 2.13-1 2.11 2.11 0 0 1 1.52.59 3 3 0 0 1 .67 2.24v7.08H368v-6.53a7.22 7.22 0 0 0-.34-2.88 2.73 2.73 0 0 0-1.04-1.52ZM386.5 8.58a4.71 4.71 0 0 0 .7-2.18 4.33 4.33 0 0 0-1.2-2.86 4.81 4.81 0 0 0-3.62-1.41h-5.92v15h1.95v-6.51h4.15l2.75 6.4h2.11l-3-6.94a3.37 3.37 0 0 0 2.08-1.5Zm-8.12-4.72h4a3 3 0 0 1 2 .67 2.24 2.24 0 0 1 .77 1.76 2.68 2.68 0 0 1-.77 2 3 3 0 0 1-2.24.77h-3.84ZM393.6 5.62a4.8 4.8 0 0 0-3.6 1.6 6.45 6.45 0 0 0-1.44 4.24 6.87 6.87 0 0 0 1.33 4.2 4.31 4.31 0 0 0 3.63 1.6 4.61 4.61 0 0 0 3.67-1.6 6.39 6.39 0 0 0 1.45-4.24 6 6 0 0 0-1.36-4.14 4.3 4.3 0 0 0-3.68-1.66Zm0 10.16a2.68 2.68 0 0 1-2.1-1 5 5 0 0 1-.86-3.39 4.9 4.9 0 0 1 .86-3.2 2.6 2.6 0 0 1 2.1-1 2.71 2.71 0 0 1 2.11 1 4.93 4.93 0 0 1 .85 3.31 4.78 4.78 0 0 1-.85 3.3 2.83 2.83 0 0 1-2.19.91ZM400.53 5.87h1.86v11.15h-1.86zM400.46 2h2.03v2.11h-2.03zM412.62 6.22a3.55 3.55 0 0 0-2.09-.68 3.85 3.85 0 0 0-3.39 2.12V5.87h-1.7v11.2h1.89V11a4 4 0 0 1 .81-2.72 2.77 2.77 0 0 1 2.24-1 2.13 2.13 0 0 1 1.6.59 2.91 2.91 0 0 1 .68 2.24v7.08h1.74v-6.57a8.05 8.05 0 0 0-.34-2.88 2.66 2.66 0 0 0-1.44-1.52ZM425.6 7.74a3.58 3.58 0 0 0-3.3-2.12 3.78 3.78 0 0 0-3.37 2.24v-1.8h-1.79v11.2h1.74V11a4.05 4.05 0 0 1 .85-2.7 2.69 2.69 0 0 1 2.24-1 2 2 0 0 1 1.52.57 2.83 2.83 0 0 1 .67 2.24v7.09h1.78v-6.58a8.05 8.05 0 0 0-.34-2.88ZM387.2 38.29a4.07 4.07 0 0 0 4-4 4 4 0 0 0-3.88-4.05h-.1a4 4 0 0 0 0 8ZM390.56 47.25h-10.93v1.85h4.48v22.58h-8.37L361.6 29.23h-2.24l-14.91 42.45h-3.2v1.92h11.2v-1.92h-5.59l4.05-12.19h12.8l4 12.19h-5.57v1.92H395v-1.92h-4.48ZM362.88 57.6h-11.2l5.73-16.94ZM413.49 46.66c-2.88 0-5.09 1.85-6.87 5.66v-5.07h-10.91v1.85h4.48v22.58h-4.48v1.92h15.23v-1.92h-4.32v-5.82c0-7.62.68-11.2 2.53-14.56.61-1 1.28-1.6 1.6-1.6s.26 0 .35.68c.16 2.53 1.17 3.81 3.2 3.81a3.45 3.45 0 0 0 3.57-3.33v-.32a4 4 0 0 0-4.05-4ZM440.21 49.6s.27 0 .41.85a2.24 2.24 0 0 0 2.23 2.25h.24a2.68 2.68 0 0 0 2.69-2.65v-.27a3.2 3.2 0 0 0-3.2-3.2h-.32a6.38 6.38 0 0 0-4.48 2.52 11.25 11.25 0 0 0-7.38-2.52c-6.1 0-10.66 4-10.66 9.6a9 9 0 0 0 3.88 7.36c-3.72 2.54-5.59 5.23-5.59 8.2a5.94 5.94 0 0 0 4.37 5.7 6.28 6.28 0 0 0-4.48 5.84c0 4.48 5.49 8.11 12.24 8.11 8 0 14-5.25 14-12.43 0-5.33-2.24-7.34-8-7.34l-10.92.16c-3.2 0-3.81-.77-3.81-2.12s1.45-3.29 4.16-5a10.42 10.42 0 0 0 5 1c6.1 0 10.76-3.87 10.76-9.12a10.13 10.13 0 0 0-2-6c.36-.83.52-.94.86-.94Zm-9.81 14c-3 0-3.81-1.28-3.81-5.84 0-8.55.59-9.22 4-9.22 3 0 3.81.59 3.81 6.4 0 4.8-.18 6.18-.67 7.09a3.77 3.77 0 0 1-3.33 1.54Zm-.24 25.6c-4.66 0-7.78-2.63-7.78-6.59a6.75 6.75 0 0 1 2-4.8h.27a21.91 21.91 0 0 0 3.71.17h3.4a18.58 18.58 0 0 0 2.36 0H438c2.87 0 3.39.83 3.39 2.45-.06 4.83-5 8.8-11.26 8.8Z"/><path d="M469.73 58.58v-.34c-.5-7.1-5.06-11.66-11.76-11.66s-12.59 6.51-12.59 13.85 6.09 13.81 12.8 13.81a11.21 11.21 0 0 0 11.2-9.6v-.34h-2.24v.24c-1.19 4.8-4.48 7.54-8.45 7.54a5.43 5.43 0 0 1-5-2.69c-.76-1.37-.85-2.65-.85-9v-1.6h16.91Zm-11.92-9.91a3.76 3.76 0 0 1 4 2.39 12.92 12.92 0 0 1 .51 5.56h-9.6v-1.18c0-4.91 1.37-6.77 5.09-6.77ZM496.48 70.77c-1.2 1-1.28 1-1.71 1-1.09 0-1.19 0-1.19-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.68 0-10.57 3.2-10.57 6.94a3 3 0 0 0 2.93 3.1h.09a2.92 2.92 0 0 0 3-2.81.71.71 0 0 0 0-.29 3.18 3.18 0 0 0-1-2.24c-.24-.34-.24-.34-.24-.5 0-1 2.37-2.46 4.64-2.46a4.37 4.37 0 0 1 3.32 1.18c.67.77.84 1.28.84 5.09v4.23c-10 .25-15.5 3.39-15.5 9 0 3.9 2.9 6.52 7.28 6.52a10.21 10.21 0 0 0 8.38-4.48 5.23 5.23 0 0 0 5.57 4.48 6.87 6.87 0 0 0 4.8-2l.16-.18-1.2-1.42Zm-9.39-10.29v1a15.15 15.15 0 0 1-.85 6.4 5.16 5.16 0 0 1-4.48 2.94 3.5 3.5 0 0 1-3.76-3.2 3 3 0 0 1 0-.73c0-4.17 2.82-6.09 9.09-6.41ZM524.16 29.33h-10.91v1.85h4.48v20.16a8.42 8.42 0 0 0-7.52-4.48c-6 0-11.2 6.24-11.2 13.68s5.17 14 11.42 14a8.32 8.32 0 0 0 7.28-4.48v4h10.82v-1.92h-4.37Zm-13.44 42.86a4 4 0 0 1-3.47-2.19c-.67-1.34-.85-2.7-.85-8.62 0-6.72.27-9.23.94-10.58a4.18 4.18 0 0 1 3.28-2c3.91 0 6.72 4.91 6.72 11.76s-2.76 11.63-6.62 11.63ZM554.5 70.77c-1.2 1-1.27 1-1.68 1-1.11 0-1.2 0-1.2-5.75v-8.8c0-5.66 0-6.17-1.6-7.79a11 11 0 0 0-8-2.86c-5.67 0-10.58 3.2-10.58 6.94a3 3 0 0 0 3 3.1h.09a2.94 2.94 0 0 0 3.1-2.77v-.33a3.18 3.18 0 0 0-1-2.24c-.27-.34-.27-.34-.27-.5 0-1 2.38-2.46 4.66-2.46a4.39 4.39 0 0 1 3.29 1.18c.71.77.85 1.28.85 5.09v4.23c-10 .25-15.47 3.39-15.47 9 0 3.9 2.86 6.52 7.28 6.52a10.21 10.21 0 0 0 8.38-4.48 5.21 5.21 0 0 0 5.57 4.48 6.69 6.69 0 0 0 4.8-2l.18-.18-1.19-1.42Zm-9.4-10.29v1a15 15 0 0 1-.84 6.4 5.12 5.12 0 0 1-4.48 2.94 3.49 3.49 0 0 1-3.75-3.2 5 5 0 0 1 0-.77c-.03-4.13 2.82-6.05 9.07-6.37ZM564.05 38.29a4.12 4.12 0 0 0 4-4 4 4 0 0 0-4-4.05H564a3.8 3.8 0 0 0-4 3.61 1.48 1.48 0 0 0 0 .42 4 4 0 0 0 3.94 4ZM567.44 47.25h-10.82v1.93h4.29V71.7h-4.29v1.93h15.14V71.7h-4.32V47.25zM582.58 56.38c-5.24-.94-6.18-1.71-6.18-3.47a4.88 4.88 0 0 1 5.42-4.24 7.12 7.12 0 0 1 7.09 6.27v.26h1.6l-.25-8.29h-1.46l-.94 2a9.64 9.64 0 0 0-6.16-2.24 8 8 0 0 0-8.23 7.77V55c0 5.23 2.37 7.44 9.14 8.62 5 .76 5.92 2 5.92 3.88a5.15 5.15 0 0 1-5.48 4.8h-.19c-4.14 0-6.52-2.53-8.11-8.72v-.24h-1.44l.16 10.38h1.19l1.44-1.94a9.79 9.79 0 0 0 6.84 2.61 8.72 8.72 0 0 0 8.71-8.73V65c-.02-5-2.53-7.53-9.07-8.62ZM323.46 0h2.24v90.67h-2.24z"/></g></svg>'
