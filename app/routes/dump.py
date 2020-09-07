from functools import wraps

import simplejson as json
from flask import Blueprint, g
from flask_login import current_user, login_required

from app.authentication.roles import role_required
from app.globals import get_questionnaire_store, get_session_store
from app.helpers.session_helpers import with_questionnaire_store
from app.questionnaire.router import Router
from app.utilities.schema import load_schema_from_session_data
from app.views.handlers.submission import SubmissionHandler

dump_blueprint = Blueprint("dump", __name__)


def requires_schema(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session = get_session_store()
        g.schema = load_schema_from_session_data(session.session_data)
        result = func(g.schema, *args, **kwargs)
        return result

    return wrapper


@dump_blueprint.route("/dump/debug", methods=["GET"])
@login_required
@role_required("dumper")
def dump_debug():
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    return questionnaire_store.serialize()


@dump_blueprint.route("/dump/routing-path", methods=["GET"])
@login_required
@role_required("dumper")
@with_questionnaire_store
@requires_schema
def dump_routing(schema, questionnaire_store):
    router = Router(
        schema,
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        questionnaire_store.progress_store,
        questionnaire_store.metadata,
    )

    response = [
        {
            "section_id": routing_path.section_id,
            "list_item_id": routing_path.list_item_id,
            "routing_path": routing_path.block_ids,
        }
        for routing_path in router.full_routing_path()
    ]

    return json.dumps(response, for_json=True), 200


@dump_blueprint.route("/dump/submission", methods=["GET"])
@login_required
@role_required("dumper")
@with_questionnaire_store
@requires_schema
def dump_submission(schema, questionnaire_store):
    router = Router(
        schema,
        questionnaire_store.answer_store,
        questionnaire_store.list_store,
        questionnaire_store.progress_store,
        questionnaire_store.metadata,
    )

    routing_path = router.full_routing_path()
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )

    submission_handler = SubmissionHandler(schema, questionnaire_store, routing_path)

    response = {"submission": submission_handler.get_payload()}
    return json.dumps(response, for_json=True), 200
