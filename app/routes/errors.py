from typing import Any

from flask import Blueprint, request
from flask.helpers import url_for
from flask_babel import lazy_gettext
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import contextvars, get_logger
from werkzeug.exceptions import (
    BadRequest,
    Forbidden,
    MethodNotAllowed,
    NotFound,
    Unauthorized,
)

from app.authentication.no_questionnaire_state_exception import (
    NoQuestionnaireStateException,
)
from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.helpers.language_helper import handle_language
from app.helpers.template_helpers import get_survey_config, render_template
from app.services.supplementary_data import (
    InvalidSupplementaryData,
    MissingSupplementaryDataKey,
    SupplementaryDataRequestFailed,
)
from app.settings import ACCOUNT_SERVICE_BASE_URL_SOCIAL
from app.submitter.previously_submitted_exception import PreviouslySubmittedException
from app.submitter.submission_failed import SubmissionFailedException
from app.survey_config.survey_type import SurveyType
from app.views.handlers.confirm_email import (
    ConfirmationEmailFulfilmentRequestPublicationFailed,
)
from app.views.handlers.feedback import FeedbackLimitReached, FeedbackUploadFailed
from app.views.handlers.individual_response import (
    IndividualResponseFulfilmentRequestPublicationFailed,
    IndividualResponseLimitReached,
)

logger = get_logger()

errors_blueprint = Blueprint("errors", __name__)


def log_exception(exception: Exception, status_code: int) -> None:
    if metadata := get_metadata(current_user):
        contextvars.bind_contextvars(tx_id=metadata.tx_id)

    log = logger.warning if status_code < 500 else logger.error

    log(
        "an error has occurred",
        exc_info=exception,
        url=request.url,
        status_code=status_code,
    )


def _render_error_page(
    status_code: int, template: str | int | None = None, **kwargs: Any
) -> tuple[str, int]:
    handle_language()
    business_survey_config = get_survey_config(theme=SurveyType.BUSINESS)
    other_survey_config = get_survey_config(
        theme=SurveyType.SOCIAL, base_url=ACCOUNT_SERVICE_BASE_URL_SOCIAL
    )

    business_logout_url = business_survey_config.account_service_log_out_url
    other_logout_url = other_survey_config.account_service_log_out_url
    business_contact_us_url = business_survey_config.contact_us_url
    other_contact_us_url = other_survey_config.contact_us_url
    template = template or status_code

    return (
        render_template(
            template=f"errors/{template}",
            business_logout_url=business_logout_url,
            other_logout_url=other_logout_url,
            business_contact_us_url=business_contact_us_url,
            other_contact_us_url=other_contact_us_url,
            **kwargs,
        ),
        status_code,
    )


@errors_blueprint.app_errorhandler(400)
@errors_blueprint.app_errorhandler(BadRequest)
def bad_request(
    exception: BadRequest,
) -> tuple[str, int]:
    log_exception(exception, 400)
    return _render_error_page(400, template="500")


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(CSRFError)
@errors_blueprint.app_errorhandler(NoTokenException)
@errors_blueprint.app_errorhandler(NoQuestionnaireStateException)
@errors_blueprint.app_errorhandler(Unauthorized)
def unauthorized(
    exception: (
        CSRFError | NoTokenException | NoQuestionnaireStateException | Unauthorized
    ),
) -> tuple[str, int]:
    log_exception(exception, 401)
    return _render_error_page(401, template="401")


@errors_blueprint.app_errorhandler(PreviouslySubmittedException)
def previously_submitted(
    exception: PreviouslySubmittedException,
) -> tuple[str, int]:
    log_exception(exception, 401)
    return _render_error_page(401, "previously-submitted")


@errors_blueprint.app_errorhandler(InvalidTokenException)
def forbidden(exception: InvalidTokenException) -> tuple[str, int]:
    log_exception(exception, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(405)
def method_not_allowed(exception: MethodNotAllowed) -> tuple[str, int]:
    log_exception(exception, 405)
    return _render_error_page(405, template="404")


@errors_blueprint.app_errorhandler(403)
@errors_blueprint.app_errorhandler(404)
def http_exception(exception: NotFound | Forbidden) -> tuple[str, int]:
    log_exception(exception, exception.code)
    return _render_error_page(exception.code)


@errors_blueprint.app_errorhandler(Exception)
def internal_server_error(exception: Exception) -> tuple[str, int]:
    try:
        log_exception(exception, 500)
        return _render_error_page(500)
    except Exception:  # pylint:disable=broad-except
        logger.exception(
            "an error has occurred when rendering 500 error",
            url=request.url,
            status_code=500,
        )
        return render_template(template="errors/500"), 500


@errors_blueprint.app_errorhandler(IndividualResponseLimitReached)
def too_many_individual_response_requests(
    exception: IndividualResponseLimitReached,
) -> tuple[str, int]:
    log_exception(exception, 429)
    title = lazy_gettext(
        "You have reached the maximum number of individual access codes"
    )
    contact_us_message = lazy_gettext(
        "If you need more individual access codes, please <a href='{contact_us_url}'>contact us</a>."
    )

    return _render_error_page(
        429,
        template="error",
        page_title=title,
        heading=title,
        contact_us_message=contact_us_message,
    )


@errors_blueprint.app_errorhandler(FeedbackLimitReached)
def too_many_feedback_requests(
    exception: FeedbackLimitReached,
) -> tuple[str, int]:
    log_exception(exception, 429)
    title = lazy_gettext(
        "You have reached the maximum number of times for submitting feedback"
    )
    contact_us_message = lazy_gettext(
        "If you need to give more feedback, please <a href='{contact_us_url}'>contact us</a>."
    )

    return _render_error_page(
        429,
        template="error",
        page_title=title,
        heading=title,
        contact_us_message=contact_us_message,
    )


@errors_blueprint.app_errorhandler(SupplementaryDataRequestFailed)
@errors_blueprint.app_errorhandler(MissingSupplementaryDataKey)
@errors_blueprint.app_errorhandler(InvalidSupplementaryData)
def supplementary_data_request_failed(
    exception: (
        SupplementaryDataRequestFailed
        | MissingSupplementaryDataKey
        | InvalidSupplementaryData
    ),
) -> tuple[str, int]:
    log_exception(exception, 500)
    return _render_error_page(500, template=500)


@errors_blueprint.app_errorhandler(SubmissionFailedException)
def submission_failed(
    exception: SubmissionFailedException,
) -> tuple[str, int]:
    log_exception(exception, 500)
    return _render_error_page(500, template="submission-failed")


@errors_blueprint.app_errorhandler(IndividualResponseFulfilmentRequestPublicationFailed)
def individual_response_fulfilment_request_publication_failed(
    exception: IndividualResponseFulfilmentRequestPublicationFailed,
) -> tuple[str, int]:
    log_exception(exception, 500)

    if "mobile_number" in request.args:
        blueprint_method = (
            "individual_response.individual_response_text_message_confirm"
        )
    else:
        blueprint_method = (
            "individual_response.individual_response_post_address_confirm"
        )

    title = lazy_gettext("Sorry, there was a problem sending the access code")
    retry_url = url_for(
        blueprint_method,
        # Type ignore: Request will be not None as this function will only run when a request handle raises and exception
        list_item_id=request.view_args["list_item_id"],  # type: ignore
        **request.args,  # type: ignore
    )
    retry_message = lazy_gettext(
        "You can try to <a href='{retry_url}'>request a new access code again</a>."
    )
    contact_us_message = lazy_gettext(
        "If this problem keeps happening, please <a href='{contact_us_url}'>contact us</a> for help."
    )

    return _render_error_page(
        500,
        template="error",
        page_title=title,
        heading=title,
        retry_url=retry_url,
        retry_message=retry_message,
        contact_us_message=contact_us_message,
    )


@errors_blueprint.app_errorhandler(ConfirmationEmailFulfilmentRequestPublicationFailed)
def confirmation_email_fulfilment_request_publication_failed(
    exception: ConfirmationEmailFulfilmentRequestPublicationFailed,
) -> tuple[str, int]:
    log_exception(exception, 500)

    title = lazy_gettext("Sorry, there was a problem sending the confirmation email")
    retry_message = lazy_gettext(
        "You can try to <a href='{retry_url}'>send the email again</a>."
    )
    contact_us_message = lazy_gettext(
        "If this problem keeps happening, please <a href='{contact_us_url}'>contact us</a> for help."
    )

    return _render_error_page(
        500,
        template="error",
        page_title=title,
        heading=title,
        retry_url=request.url,
        retry_message=retry_message,
        contact_us_message=contact_us_message,
    )


@errors_blueprint.app_errorhandler(FeedbackUploadFailed)
def feedback_upload_failed(exception: FeedbackUploadFailed) -> tuple[str, int]:
    log_exception(exception, 500)
    title = lazy_gettext("Sorry, there is a problem")
    retry_message = lazy_gettext(
        "You can try to <a href='{retry_url}'>submit your feedback again</a>."
    )
    contact_us_message = lazy_gettext(
        "If this problem keeps happening, please <a href='{contact_us_url}'>contact us</a> for help."
    )
    return _render_error_page(
        500,
        template="error",
        page_title=title,
        heading=title,
        retry_url=request.url,
        retry_message=retry_message,
        contact_us_message=contact_us_message,
    )
