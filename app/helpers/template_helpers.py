from functools import cached_property, lru_cache
from typing import Any, Type

from flask import current_app
from flask import render_template as flask_render_template
from flask import request
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale, lazy_gettext
from flask_login import current_user

from app.globals import get_metadata, get_session_store
from app.helpers.language_helper import get_languages_context
from app.questionnaire import QuestionnaireSchema
from app.settings import ACCOUNT_SERVICE_BASE_URL
from app.survey_config import (
    BusinessSurveyConfig,
    DBTBusinessSurveyConfig,
    DBTDSITBusinessSurveyConfig,
    DBTDSITNIBusinessSurveyConfig,
    DBTNIBusinessSurveyConfig,
    DESNZBusinessSurveyConfig,
    DESNZNIBusinessSurveyConfig,
    NIBusinessSurveyConfig,
    ONSNHSSocialSurveyConfig,
    ORRBusinessSurveyConfig,
    SocialSurveyConfig,
    SurveyConfig,
    UKHSAONSSocialSurveyConfig,
)
from app.survey_config.survey_type import SurveyType
from app.utilities.schema import load_schema_from_metadata

DATA_LAYER_KEYS = {"title", "survey_id", "form_type"}


class ContextHelper:
    def __init__(
        self,
        language: str,
        is_post_submission: bool,
        include_csrf_token: bool,
        survey_config: SurveyConfig,
    ) -> None:
        self._language = language
        self._is_post_submission = is_post_submission
        self._include_csrf_token = include_csrf_token
        self._survey_config = survey_config
        self._survey_title = cookie_session.get("title", lazy_gettext("ONS Surveys"))
        self._sign_out_url = url_for("session.get_sign_out")
        self._cdn_url = (
            f'{current_app.config["CDN_URL"]}{current_app.config["CDN_ASSETS_PATH"]}'
        )
        self._address_lookup_api = current_app.config["ADDRESS_LOOKUP_API_URL"]
        self._google_tag_id = current_app.config.get("EQ_GOOGLE_TAG_ID")
        self._survey_type = cookie_session.get("theme")
        self._preview_enabled = (
            self._survey_config.schema.preview_enabled
            if self._survey_config.schema
            else False
        )

    @property
    def context(self) -> dict[str, Any]:
        context = {
            "sign_out_button_text": self._survey_config.sign_out_button_text,
            "account_service_my_account_url": self._survey_config.account_service_my_account_url,
            "account_service_log_out_url": self._survey_config.account_service_log_out_url,
            "account_service_todo_url": self._survey_config.account_service_todo_url,
            "contact_us_url": self._survey_config.contact_us_url,
            "thank_you_url": url_for("post_submission.get_thank_you"),
            "service_links": self.service_links_context,
            "footer": self.footer_context,
            "languages": get_languages_context(self._language),
            "theme": self._survey_config.design_system_theme,
            "language_code": self._language,
            "survey_title": self._survey_title,
            "cdn_url": self._cdn_url,
            "address_lookup_api_url": self._address_lookup_api,
            "data_layer": self.data_layer_context,
            "include_csrf_token": self._include_csrf_token,
            "google_tag_id": self._google_tag_id,
            "survey_type": self._survey_type,
            "preview_enabled": self._preview_enabled,
            "masthead_logo": self._survey_config.masthead_logo,
            "masthead_logo_mobile": self._survey_config.masthead_logo_mobile,
        }

        if self._survey_type:
            context["cookie_settings_url"] = self._survey_config.cookie_settings_url
            context["cookie_domain"] = self._survey_config.cookie_domain

        return context

    @property
    def service_links_context(
        self,
    ) -> dict[str, dict[str, str] | list[dict]] | None:
        ru_ref = (
            metadata["ru_ref"] if (metadata := get_metadata(current_user)) else None
        )

        if service_links := self._survey_config.get_service_links(
            sign_out_url=self._sign_out_url,
            is_authenticated=current_user.is_authenticated,
            cookie_has_theme=bool(self._survey_type),
            ru_ref=ru_ref,
        ):
            return {
                "toggleServicesButton": {
                    "text": lazy_gettext("Menu"),
                    "ariaLabel": "Toggle services menu",
                },
                "itemsList": service_links,
            }

        return None

    @property
    def data_layer_context(
        self,
    ) -> list[dict]:
        tx_id_context = (
            {"tx_id": metadata.tx_id}
            if (metadata := get_metadata(current_user))
            else None
        )
        additional_context = self._survey_config.get_additional_data_layer_context()
        schema_context = {
            key: value for key in DATA_LAYER_KEYS if (value := cookie_session.get(key))
        }
        context = [*additional_context, schema_context]

        if tx_id_context:
            context.append(tx_id_context)

        flattened_context = {}
        for d in context:
            flattened_context |= d
        return flattened_context

    @property
    def footer_context(self) -> dict[str, Any]:
        context = {
            "lang": self._language,
            "crest": self._survey_config.crest,
            "newTabWarning": lazy_gettext("The following links open in a new tab"),
            "copyrightDeclaration": {
                "copyright": self._survey_config.copyright_declaration,
                "text": self._survey_config.copyright_text,
            },
        }

        if self._footer_warning:
            context["footerWarning"] = self._footer_warning

        if footer_links := self._survey_config.get_footer_links(
            cookie_has_theme=bool(self._survey_type),
        ):
            context["rows"] = [{"itemsList": footer_links}]

        if footer_legal_links := self._survey_config.get_footer_legal_links(
            cookie_has_theme=bool(self._survey_type),
        ):
            context["legal"] = [{"itemsList": footer_legal_links}]

        return context

    @cached_property
    def _footer_warning(self) -> str | None:
        if self._is_post_submission:
            footer_warning: str = lazy_gettext(
                "Make sure you <a href='{sign_out_url}'>leave this page</a> or close your browser if using a shared device"
            ).format(sign_out_url=self._sign_out_url)

            return footer_warning


@lru_cache
def survey_config_mapping(
    *, theme: SurveyType, language: str, base_url: str, schema: QuestionnaireSchema
) -> SurveyConfig:
    survey_type_to_config: dict[SurveyType, Type[SurveyConfig]] = {
        SurveyType.DEFAULT: BusinessSurveyConfig,
        SurveyType.BUSINESS: BusinessSurveyConfig,
        SurveyType.HEALTH: SocialSurveyConfig,
        SurveyType.SOCIAL: SocialSurveyConfig,
        SurveyType.NORTHERN_IRELAND: NIBusinessSurveyConfig,
        SurveyType.DBT: DBTBusinessSurveyConfig,
        SurveyType.DBT_NI: DBTNIBusinessSurveyConfig,
        SurveyType.DBT_DSIT: DBTDSITBusinessSurveyConfig,
        SurveyType.DBT_DSIT_NI: DBTDSITNIBusinessSurveyConfig,
        SurveyType.DESNZ: DESNZBusinessSurveyConfig,
        SurveyType.DESNZ_NI: DESNZNIBusinessSurveyConfig,
        SurveyType.ORR: ORRBusinessSurveyConfig,
        SurveyType.UKHSA_ONS: UKHSAONSSocialSurveyConfig,
        SurveyType.ONS_NHS: ONSNHSSocialSurveyConfig,
    }

    return survey_type_to_config[theme](
        base_url=base_url, schema=schema, language_code=language
    )


def get_survey_config(
    *,
    base_url: str | None = None,
    theme: SurveyType | None = None,
    language: str | None = None,
    schema: QuestionnaireSchema | None = None,
) -> SurveyConfig:
    # The fallback to assigning SURVEY_TYPE to theme is only being added until
    # business feedback on the differentiation between theme and SURVEY_TYPE.
    language = language or get_locale().language

    if metadata := get_metadata(current_user):
        schema = load_schema_from_metadata(metadata=metadata, language_code=language)

    survey_theme = theme or get_survey_type()

    base_url = base_url or (
        cookie_session.get("account_service_base_url") or ACCOUNT_SERVICE_BASE_URL
    )

    return survey_config_mapping(
        theme=survey_theme,
        language=language,
        base_url=base_url,
        schema=schema,
    )


def render_template(template: str, **kwargs: Any) -> str:
    session_expires_at = None
    language = get_locale().language
    if session_store := get_session_store():
        if session_expiry := session_store.expiration_time:
            session_expires_at = session_expiry.isoformat()

    survey_config = get_survey_config()

    is_post_submission = request.blueprint == "post_submission"
    include_csrf_token = bool(
        request.url_rule
        and request.url_rule.methods
        and "POST" in request.url_rule.methods
    )

    context = ContextHelper(
        language, is_post_submission, include_csrf_token, survey_config
    ).context

    template = f"{template.lower()}.html"

    return flask_render_template(
        template,
        csp_nonce=request.csp_nonce,  # type: ignore
        session_expires_at=session_expires_at,
        **context,
        **kwargs,
    )


def get_survey_type() -> SurveyType:
    survey_type = cookie_session.get("theme", current_app.config["SURVEY_TYPE"])
    return SurveyType(survey_type)
