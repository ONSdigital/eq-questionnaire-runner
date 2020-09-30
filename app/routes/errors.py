from flask import Blueprint, redirect, request
from flask import session as cookie_session
from flask.helpers import url_for
from flask_login import current_user
from flask_wtf.csrf import CSRFError
from sdc.crypto.exceptions import InvalidTokenException
from structlog import get_logger

from app.authentication.no_questionnaire_state_exception import (
    NoQuestionnaireStateException,
)
from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata
from app.helpers.language_helper import handle_language
from app.helpers.template_helpers import render_template
from app.settings import EQ_SESSION_ID
from app.submitter.submission_failed import SubmissionFailedException
from app.views.handlers.individual_response import FulfilmentRequestFailedException

logger = get_logger()

errors_blueprint = Blueprint("errors", __name__)


def log_error(error, status_code):
    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata["tx_id"])

    log = logger.warning if status_code < 500 else logger.error

    log(
        "an error has occurred",
        exc_info=error,
        url=request.url,
        status_code=status_code,
    )


def _render_error_page(status_code, template=None):
    handle_language()
    template = template or status_code
    using_edge = request.user_agent.browser == "edge"

    return (
        render_template(template=f"errors/{template}", using_edge=using_edge),
        status_code,
    )


@errors_blueprint.app_errorhandler(401)
@errors_blueprint.app_errorhandler(CSRFError)
@errors_blueprint.app_errorhandler(NoTokenException)
@errors_blueprint.app_errorhandler(NoQuestionnaireStateException)
def unauthorized(error=None):
    log_error(error, 401)
    if EQ_SESSION_ID not in cookie_session:
        return _render_error_page(401, "no-cookie")
    if cookie_session.get("submitted", False):
        return _render_error_page(401, "submission-complete")
    return _render_error_page(401, "session-expired")


@errors_blueprint.app_errorhandler(InvalidTokenException)
def forbidden(error=None):
    log_error(error, 403)
    return _render_error_page(403)


@errors_blueprint.app_errorhandler(405)
def method_not_allowed(error=None):
    log_error(error, 405)
    return _render_error_page(405, template="404")


@errors_blueprint.app_errorhandler(SubmissionFailedException)
@errors_blueprint.app_errorhandler(Exception)
def internal_server_error(error=None):
    try:
        log_error(error, 500)
        return _render_error_page(500)
    except Exception:  # pylint:disable=broad-except
        logger.error(
            "an error has occurred when rendering 500 error",
            exc_info=True,
            url=request.url,
            status_code=500,
        )
        return render_template(template="errors/500"), 500


@errors_blueprint.app_errorhandler(403)
@errors_blueprint.app_errorhandler(404)
def http_exception(error):
    log_error(error, error.code)
    return _render_error_page(error.code)


@errors_blueprint.app_errorhandler(FulfilmentRequestFailedException)
def fulfilment_request_failed(error):
    logger.exception(
        "An individual response fulfilment request failed",
        url=request.url,
        status_code=500,
    )

    if "mobile_number" in request.args:
        blueprint_method = (
            "individual_response.individual_response_text_message_confirm"
        )
    else:
        blueprint_method = (
            "individual_response.individual_response_post_address_confirm"
        )

    retry_url = url_for(
        blueprint_method, list_item_id=request.view_args["list_item_id"], **request.args
    )

    return (
        render_template(template="errors/fulfilment_request", retry_url=retry_url),
        500,
    )
