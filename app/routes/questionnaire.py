import flask_babel

from flask import Blueprint, g, redirect, request, url_for, jsonify
from flask_login import current_user, login_required
from structlog import get_logger
from app.authentication.no_token_exception import NoTokenException
from app.globals import get_metadata, get_session_store, get_session_timeout_in_seconds
from app.helpers.language_helper import handle_language
from app.helpers.schema_helpers import with_schema
from app.helpers.session_helpers import with_questionnaire_store
from app.helpers.template_helper import render_template
from app.questionnaire.location import InvalidLocationException
from app.questionnaire.router import Router

from app.utilities.schema import load_schema_from_session_data
from app.views.contexts.hub_context import HubContext
from app.views.contexts.metadata_context import (
    build_metadata_context_for_survey_completed,
)
from app.views.handlers.block_factory import get_block_handler
from app.views.handlers.section import SectionHandler
from app.views.handlers.submission import SubmissionHandler

END_BLOCKS = "Summary", "Confirmation"

logger = get_logger()

questionnaire_blueprint = Blueprint(
    name="questionnaire", import_name=__name__, url_prefix="/questionnaire/"
)

post_submission_blueprint = Blueprint(
    name="post_submission", import_name=__name__, url_prefix="/submitted/"
)


@questionnaire_blueprint.before_request
def before_questionnaire_request():
    metadata = get_metadata(current_user)
    if not metadata:
        raise NoTokenException(401)

    logger.bind(
        tx_id=metadata["tx_id"],
        schema_name=metadata["schema_name"],
        ce_id=metadata["collection_exercise_sid"],
        questionnaire_id=metadata["questionnaire_id"],
    )

    logger.info(
        "questionnaire request", method=request.method, url_path=request.full_path
    )

    handle_language()

    session_store = get_session_store()
    g.schema = load_schema_from_session_data(session_store.session_data)


@post_submission_blueprint.before_request
def before_post_submission_request():
    session_store = get_session_store()
    if not session_store or not session_store.session_data:
        raise NoTokenException(401)

    session_data = session_store.session_data

    handle_language()

    g.schema = load_schema_from_session_data(session_data)

    logger.bind(tx_id=session_data.tx_id, schema_name=session_data.schema_name)

    logger.info(
        "questionnaire request", method=request.method, url_path=request.full_path
    )


@questionnaire_blueprint.route("/", methods=["GET"])
@login_required
@with_questionnaire_store
@with_schema
def get_questionnaire(schema, questionnaire_store):
    router = Router(
        schema,
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        questionnaire_store.progress_store,
        questionnaire_store.metadata,
    )

    if not router.can_access_hub():
        redirect_location_url = router.get_first_incomplete_location_in_survey_url()
        return redirect(redirect_location_url)

    language_code = get_session_store().session_data.language_code

    hub = HubContext(
        language=language_code,
        schema=schema,
        answer_store=questionnaire_store.answer_store,
        list_store=questionnaire_store.list_store,
        progress_store=questionnaire_store.progress_store,
        metadata=questionnaire_store.metadata,
    )

    hub_context = hub.get_context(
        router.is_survey_complete(), router.enabled_section_ids
    )

    return render_template("hub", content=hub_context)


@questionnaire_blueprint.route("/", methods=["POST"])
@login_required
@with_questionnaire_store
@with_schema
def post_questionnaire(schema, questionnaire_store):
    router = Router(
        schema,
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        questionnaire_store.progress_store,
        questionnaire_store.metadata,
    )

    if schema.is_hub_enabled() and router.is_survey_complete():
        submission_handler = SubmissionHandler(
            schema, questionnaire_store, router.full_routing_path()
        )
        submission_handler.submit_questionnaire()
        return redirect(url_for("post_submission.get_thank_you"))

    return redirect(router.get_first_incomplete_location_in_survey_url())


@questionnaire_blueprint.route("sections/<section_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route(
    "sections/<section_id>/<list_item_id>/", methods=["GET", "POST"]
)
@login_required
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
    except InvalidLocationException:
        return redirect(url_for(".get_questionnaire"))

    if request.method == "GET":
        if section_handler.can_display_summary():
            return _render_page(
                template="SectionSummary",
                context=section_handler.context(),
                current_location=section_handler.current_location,
                previous_location_url=section_handler.get_previous_location_url(),
                schema=schema,
                page_title=section_handler.get_page_title(),
            )

        return redirect(section_handler.get_resume_url())

    return redirect(section_handler.get_next_location_url())


# pylint: disable=too-many-return-statements
@questionnaire_blueprint.route("<block_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route("<list_name>/<block_id>/", methods=["GET", "POST"])
@questionnaire_blueprint.route(
    "<list_name>/<list_item_id>/<block_id>/", methods=["GET", "POST"]
)
@login_required
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
    except InvalidLocationException:
        return redirect(url_for(".get_questionnaire"))

    if block_handler.block["type"] == "RelationshipCollector":
        return redirect(block_handler.get_first_location_url())

    if "action[clear_radios]" in request.form:
        block_handler.clear_radio_answers()
        return redirect(request.url)

    if request.method == "GET" or (
        hasattr(block_handler, "form") and not block_handler.form.validate()
    ):
        return _render_page(
            template=block_handler.rendered_block["type"],
            context=block_handler.get_context(),
            current_location=block_handler.current_location,
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
            page_title=block_handler.page_title,
        )

    if block_handler.block["type"] in END_BLOCKS:
        submission_handler = SubmissionHandler(
            schema, questionnaire_store, block_handler.router.full_routing_path()
        )
        submission_handler.submit_questionnaire()
        return redirect(url_for("post_submission.get_thank_you"))

    block_handler.handle_post()

    next_location_url = block_handler.get_next_location_url()
    return redirect(next_location_url)


@questionnaire_blueprint.route(
    "<block_id>/<list_item_id>/to/<to_list_item_id>/", methods=["GET", "POST"]
)
@login_required
@with_questionnaire_store
@with_schema
def relationship(schema, questionnaire_store, block_id, list_item_id, to_list_item_id):
    try:
        block_handler = get_block_handler(
            schema=schema,
            block_id=block_id,
            list_item_id=list_item_id,
            to_list_item_id=to_list_item_id,
            questionnaire_store=questionnaire_store,
            language=flask_babel.get_locale().language,
            request_args=request.args,
            form_data=request.form,
        )
    except InvalidLocationException:
        return redirect(url_for(".get_questionnaire"))

    if request.method == "GET" or (
        hasattr(block_handler, "form") and not block_handler.form.validate()
    ):
        return _render_page(
            template=block_handler.block["type"],
            context=block_handler.get_context(),
            current_location=block_handler.current_location,
            previous_location_url=block_handler.get_previous_location_url(),
            schema=schema,
            page_title=block_handler.page_title,
        )

    block_handler.handle_post()
    next_location_url = block_handler.get_next_location_url()
    return redirect(next_location_url)


@post_submission_blueprint.route("thank-you/", methods=["GET"])
@login_required
@with_schema
def get_thank_you(schema):
    session_store = get_session_store()
    session_data = session_store.session_data

    if not session_data.submitted_time:
        return redirect(url_for("questionnaire.get_questionnaire"))

    metadata_context = build_metadata_context_for_survey_completed(session_data)

    return render_template(
        template="thank-you",
        metadata=metadata_context,
        survey_id=schema.json["survey_id"],
        hide_signout_button=True,
    )


def _render_page(
    template, context, current_location, previous_location_url, schema, page_title
):
    if request_wants_json():
        return jsonify(context)

    session_timeout = get_session_timeout_in_seconds(schema)

    return render_template(
        template=template,
        content=context,
        current_location=current_location,
        previous_location_url=previous_location_url,
        session_timeout=session_timeout,
        legal_basis=schema.json.get("legal_basis"),
        page_title=page_title,
    )


def request_wants_json():
    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    return (
        best == "application/json"
        and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]
    )
