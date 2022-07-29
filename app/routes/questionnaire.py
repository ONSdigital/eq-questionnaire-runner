from __future__ import annotations

from typing import Union

import flask_babel
from flask import Blueprint, g, redirect, request, send_file
from flask import session as cookie_session
from flask import url_for
from flask_babel import get_locale
from flask_login import current_user, login_required
from itsdangerous import BadSignature
from structlog import get_logger
from werkzeug import Response
from werkzeug.exceptions import BadRequest, NotFound

from app.authentication.no_questionnaire_state_exception import (
    NoQuestionnaireStateException,
)
from app.data_models import QuestionnaireStore
from app.globals import (
    get_metadata,
    get_questionnaire_store,
    get_session_timeout_in_seconds,
)
from app.helpers import url_safe_serializer
from app.helpers.language_helper import handle_language
from app.helpers.schema_helpers import with_schema
from app.helpers.session_helpers import with_questionnaire_store, with_session_store
from app.helpers.template_helpers import render_template
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.router import Router
from app.submitter.previously_submitted_exception import PreviouslySubmittedException
from app.utilities.schema import load_schema_from_metadata
from app.views.contexts import HubContext
from app.views.handlers.block_factory import get_block_handler
from app.views.handlers.confirm_email import ConfirmEmail
from app.views.handlers.confirmation_email import (
    ConfirmationEmail,
    ConfirmationEmailLimitReached,
    ConfirmationEmailNotEnabled,
)
from app.views.handlers.feedback import Feedback, FeedbackNotEnabled
from app.views.handlers.section import SectionHandler
from app.views.handlers.submission import SubmissionHandler
from app.views.handlers.submit_questionnaire import SubmitQuestionnaireHandler
from app.views.handlers.thank_you import ThankYou
from app.views.handlers.view_submitted_response import (
    ViewSubmittedResponse,
    ViewSubmittedResponseExpired,
    ViewSubmittedResponseNotEnabled,
)
from app.views.handlers.view_submitted_response_pdf import ViewSubmittedResponsePDF

logger = get_logger()

questionnaire_blueprint = Blueprint(
    name="questionnaire", import_name=__name__, url_prefix="/questionnaire/"
)

post_submission_blueprint = Blueprint(
    name="post_submission", import_name=__name__, url_prefix="/submitted/"
)


@questionnaire_blueprint.before_request
@login_required
def before_questionnaire_request():
    if request.method == "OPTIONS":
        return None

    if cookie_session.get("submitted"):
        raise PreviouslySubmittedException(
            "The Questionnaire has been previously submitted"
        )

    metadata = get_metadata(current_user)
    if not metadata:
        raise NoQuestionnaireStateException(401)

    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )

    if questionnaire_store.submitted_at:
        return redirect(url_for("post_submission.get_thank_you"))

    logger.bind(
        tx_id=metadata["tx_id"],
        schema_name=metadata["schema_name"],
        ce_id=metadata["collection_exercise_sid"],
    )

    logger.info(
        "questionnaire request", method=request.method, url_path=request.full_path
    )

    handle_language(metadata)

    g.schema = load_schema_from_metadata(
        metadata=metadata, language_code=get_locale().language
    )


@post_submission_blueprint.before_request
@login_required
def before_post_submission_request():
    if request.method == "OPTIONS":
        return None

    metadata = get_metadata(current_user)
    if not metadata:
        raise NoQuestionnaireStateException(401)

    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )

    if not questionnaire_store.submitted_at:
        raise NotFound

    handle_language(metadata)

    g.schema = load_schema_from_metadata(
        metadata=metadata, language_code=get_locale().language
    )

    logger.bind(
        tx_id=metadata.get("tx_id"),
        schema_name=metadata.get("schema_name"),
    )

    logger.info(
        "questionnaire request", method=request.method, url_path=request.full_path
    )


@questionnaire_blueprint.route("/", methods=["GET", "POST"])
@with_questionnaire_store
@with_schema
def get_questionnaire(schema, questionnaire_store):
    router = Router(
        schema,
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        questionnaire_store.progress_store,
        questionnaire_store.metadata,
        questionnaire_store.response_metadata,
    )

    if not router.can_access_hub():
        redirect_location_url = (
            router.get_first_incomplete_location_in_questionnaire_url()
        )
        return redirect(redirect_location_url)

    if request.method == "POST":
        if router.is_questionnaire_complete:
            submission_handler = SubmissionHandler(
                schema, questionnaire_store, router.full_routing_path()
            )
            submission_handler.submit_questionnaire()
            return redirect(url_for("post_submission.get_thank_you"))
        return redirect(router.get_first_incomplete_location_in_questionnaire_url())

    hub_context = HubContext(
        language=flask_babel.get_locale().language,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
    )
    context = hub_context(
        survey_complete=router.is_questionnaire_complete,
        enabled_section_ids=router.enabled_section_ids,
    )
    return render_template(
        "hub",
        content=context,
        page_title=context["title"],
    )


@questionnaire_blueprint.route("submit/", methods=["GET", "POST"])
@with_questionnaire_store
@with_schema
def submit_questionnaire(
    schema: QuestionnaireSchema, questionnaire_store: QuestionnaireStore
) -> Union[Response, str]:
    try:
        submit_questionnaire_handler = SubmitQuestionnaireHandler(
            schema, questionnaire_store, flask_babel.get_locale().language
        )
    except InvalidLocationException as exc:
        raise NotFound from exc

    if not submit_questionnaire_handler.router.is_questionnaire_complete:
        return redirect(
            submit_questionnaire_handler.router.get_first_incomplete_location_in_questionnaire_url()
        )

    if request.method == "POST":
        submit_questionnaire_handler.handle_post()
        return redirect(url_for("post_submission.get_thank_you"))

    context = submit_questionnaire_handler.get_context()
    return render_template(
        submit_questionnaire_handler.template,
        content=context,
        page_title=context["title"],
        previous_location_url=submit_questionnaire_handler.get_previous_location_url(),
    )


@questionnaire_blueprint.route("sections/<section_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route(
    "sections/<section_id>/<list_item_id>/", methods=["GET", "POST"]
)
@with_questionnaire_store
@with_schema
def get_section(schema, questionnaire_store, section_id, list_item_id=None):
    try:
        section_handler = SectionHandler(
            schema=schema,
            questionnaire_store=questionnaire_store,
            section_id=section_id,
            list_item_id=list_item_id,
            language=flask_babel.get_locale().language,
        )
    except InvalidLocationException as exc:
        raise NotFound from exc

    if request.method != "POST":
        if section_handler.can_display_summary():
            section_context = section_handler.get_context()
            return _render_page(
                template="SectionSummary",
                context=section_context,
                previous_location_url=section_handler.get_previous_location_url(),
                schema=schema,
                page_title=section_context["summary"]["page_title"],
            )

        return redirect(section_handler.get_resume_url())

    return redirect(section_handler.get_next_location_url())


# pylint: disable=too-many-return-statements
@questionnaire_blueprint.route("<block_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route("<list_name>/<block_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route(
    "<list_name>/<list_item_id>/<block_id>/", methods=["GET", "POST"]
)
@with_questionnaire_store
@with_schema
def block(schema, questionnaire_store, block_id, list_name=None, list_item_id=None):
    try:
        block_handler = get_block_handler(
            schema=schema,
            block_id=block_id,
            list_name=list_name,
            list_item_id=list_item_id,
            questionnaire_store=questionnaire_store,
            language=flask_babel.get_locale().language,
            request_args=request.args,
            form_data=request.form,
        )
    except InvalidLocationException as exc:
        raise NotFound from exc

    if "action[clear_radios]" in request.form:
        block_handler.clear_radio_answers()
        return redirect(block_handler.current_location.url())

    if request.method != "POST" or (
        hasattr(block_handler, "form") and not block_handler.form.validate()
    ):
        return _render_page(
            template=block_handler.rendered_block["type"],
            context=block_handler.get_context(),
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
            page_title=block_handler.page_title,
        )

    block_handler.handle_post()
    next_location_url = block_handler.get_next_location_url()
    return redirect(next_location_url)


@questionnaire_blueprint.route(
    "relationships/",
    methods=["GET", "POST"],
)
@questionnaire_blueprint.route(
    "relationships/<list_name>/<list_item_id>/to/<to_list_item_id>/",
    methods=["GET", "POST"],
)
@questionnaire_blueprint.route(
    "relationships/<list_name>/<list_item_id>/<block_id>/", methods=["GET", "POST"]
)
@with_questionnaire_store
@with_schema
def relationships(
    schema,
    questionnaire_store,
    list_name=None,
    list_item_id=None,
    to_list_item_id=None,
    block_id="relationships",
):
    try:
        block_handler = get_block_handler(
            schema=schema,
            block_id=block_id,
            list_item_id=list_item_id,
            to_list_item_id=to_list_item_id,
            questionnaire_store=questionnaire_store,
            list_name=list_name,
            language=flask_babel.get_locale().language,
            request_args=request.args,
            form_data=request.form,
        )
    except InvalidLocationException as exc:
        raise NotFound from exc

    if not list_name:
        if "last" in request.args:
            return redirect(block_handler.get_last_location_url())
        return redirect(block_handler.get_first_location_url())

    if request.method != "POST" or (
        hasattr(block_handler, "form") and not block_handler.form.validate()
    ):
        return _render_page(
            template=block_handler.block["type"],
            context=block_handler.get_context(),
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
            page_title=block_handler.page_title,
        )

    block_handler.handle_post()
    next_location_url = block_handler.get_next_location_url()
    return redirect(next_location_url)


@post_submission_blueprint.route("thank-you/", methods=["GET", "POST"])
@with_questionnaire_store
@with_session_store
@with_schema
def get_thank_you(schema, session_store, questionnaire_store):
    thank_you = ThankYou(schema, session_store, questionnaire_store.submitted_at)

    if request.method == "POST":
        confirmation_email = thank_you.confirmation_email
        if not confirmation_email:
            return redirect(url_for(".get_thank_you"))

        if confirmation_email.form.validate():
            return redirect(
                url_for(
                    ".confirm_confirmation_email",
                    email=confirmation_email.get_url_safe_serialized_email(),
                )
            )

        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        logger.info(
            "email validation error",
            error_message=str(confirmation_email.form.errors["email"][0]),
        )

    show_feedback_call_to_action = Feedback.is_enabled(
        schema
    ) and not Feedback.is_limit_reached(session_store.session_data)

    return render_template(
        template=thank_you.template,
        content={
            **thank_you.get_context(),
            "show_feedback_call_to_action": show_feedback_call_to_action,
        },
        survey_id=schema.json["survey_id"],
        page_title=thank_you.get_page_title(),
    )


@post_submission_blueprint.route("view-response/", methods=["GET"])
@with_questionnaire_store
@with_schema
def get_view_submitted_response(schema, questionnaire_store):
    try:
        view_submitted_response = ViewSubmittedResponse(
            schema,
            questionnaire_store,
            flask_babel.get_locale().language,
        )

    except ViewSubmittedResponseNotEnabled as exc:
        raise NotFound from exc

    return view_submitted_response.get_rendered_html()


@post_submission_blueprint.route("download-pdf", methods=["GET"])
@with_questionnaire_store
@with_schema
def get_view_submitted_response_pdf(
    schema: QuestionnaireSchema, questionnaire_store: QuestionnaireStore
) -> Response:
    """
    :param schema: The questionnaire schema object.
    :type schema: QuestionnaireSchema
    :param questionnaire_store: The questionnaire store object.
    :type questionnaire_store: QuestionnaireStore
    :return: A response object with the contents of a file to the client.
    :rtype: Response
    """

    try:
        view_submitted_response_pdf = ViewSubmittedResponsePDF(
            schema,
            questionnaire_store,
            flask_babel.get_locale().language,
        )
    except ViewSubmittedResponseNotEnabled as exc:
        raise NotFound from exc
    except ViewSubmittedResponseExpired:
        return redirect(url_for(".get_view_submitted_response"))

    return send_file(
        path_or_file=view_submitted_response_pdf.get_pdf(),
        mimetype=view_submitted_response_pdf.mimetype,
        as_attachment=True,
        download_name=view_submitted_response_pdf.filename,
    )


@post_submission_blueprint.route("confirmation-email/send", methods=["GET", "POST"])
@with_schema
@with_session_store
def send_confirmation_email(session_store, schema):
    try:
        confirmation_email = ConfirmationEmail(
            session_store, schema, serialised_email=request.args.get("email")
        )
    except (ConfirmationEmailLimitReached, ConfirmationEmailNotEnabled):
        return redirect(url_for(".get_thank_you"))

    if request.method == "POST":
        if confirmation_email.form.validate():
            return redirect(
                url_for(
                    ".confirm_confirmation_email",
                    email=confirmation_email.get_url_safe_serialized_email(),
                )
            )

        # pylint: disable=no-member
        # wtforms Form parents are not discoverable in the 2.3.3 implementation
        logger.info(
            "email validation error",
            error_message=str(confirmation_email.form.errors["email"][0]),
        )

    return render_template(
        template="confirmation-email",
        content=confirmation_email.get_context(),
        hide_sign_out_button=True,
        page_title=confirmation_email.get_page_title(),
    )


@post_submission_blueprint.route("confirmation-email/confirm", methods=["GET", "POST"])
@with_questionnaire_store
@with_schema
@with_session_store
def confirm_confirmation_email(session_store, schema, questionnaire_store):
    try:
        confirm_email = ConfirmEmail(
            questionnaire_store,
            schema,
            session_store,
            request.args["email"],
            form_data=request.form,
        )
    except (ConfirmationEmailLimitReached, ConfirmationEmailNotEnabled):
        return redirect(url_for(".get_thank_you"))

    if request.method == "POST" and confirm_email.form.validate():
        confirm_email.handle_post()
        next_location_url = confirm_email.get_next_location_url()
        return redirect(next_location_url)

    return render_template(
        template="confirm-email",
        content=confirm_email.get_context(),
        page_title=confirm_email.get_page_title(),
    )


@post_submission_blueprint.route("confirmation-email/sent", methods=["GET"])
@with_schema
@with_session_store
def get_confirmation_email_sent(session_store, schema):
    if not session_store.session_data.confirmation_email_count:
        raise NotFound

    try:
        email = url_safe_serializer().loads(request.args["email"])
    except BadSignature as exc:
        raise BadRequest from exc

    show_send_another_email_guidance = not ConfirmationEmail.is_limit_reached(
        session_store.session_data
    )
    show_feedback_call_to_action = Feedback.is_enabled(
        schema
    ) and not Feedback.is_limit_reached(session_store.session_data)

    return render_template(
        template="confirmation-email-sent",
        content={
            "email": email,
            "send_confirmation_email_url": url_for(
                "post_submission.send_confirmation_email"
            ),
            "hide_sign_out_button": False,
            "show_send_another_email_guidance": show_send_another_email_guidance,
            "sign_out_url": url_for("session.get_sign_out"),
            "show_feedback_call_to_action": show_feedback_call_to_action,
        },
    )


@post_submission_blueprint.route("feedback/send", methods=["GET", "POST"])
@with_questionnaire_store
@with_session_store
@with_schema
def send_feedback(schema, session_store, questionnaire_store):
    try:
        feedback = Feedback(
            questionnaire_store, schema, session_store, form_data=request.form
        )
    except FeedbackNotEnabled as exc:
        raise NotFound from exc

    if request.method == "POST" and feedback.form.validate():
        feedback.handle_post()
        return redirect(url_for(".get_feedback_sent"))

    return render_template(
        template="feedback",
        content=feedback.get_context(),
        page_title=feedback.get_page_title(),
    )


@post_submission_blueprint.route("feedback/sent", methods=["GET"])
@with_session_store
def get_feedback_sent(session_store):
    if not session_store.session_data.feedback_count:
        raise NotFound

    return render_template(
        template="feedback-sent",
        content={
            "hide_sign_out_button": False,
            "sign_out_url": url_for("session.get_sign_out"),
        },
    )


def _render_page(template, context, previous_location_url, schema, page_title):
    session_timeout = get_session_timeout_in_seconds(schema)

    return render_template(
        template=template,
        content=context,
        previous_location_url=previous_location_url,
        session_timeout=session_timeout,
        legal_basis=schema.json.get("legal_basis"),
        page_title=page_title,
    )
