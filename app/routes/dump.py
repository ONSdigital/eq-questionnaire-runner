from flask import Blueprint
from flask_login import current_user, login_required

from app.authentication.roles import role_required
from app.data_models import QuestionnaireStore
from app.globals import get_questionnaire_store
from app.helpers.schema_helpers import with_schema
from app.helpers.session_helpers import with_questionnaire_store
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.router import Router
from app.utilities.json import json_dumps
from app.views.handlers.submission import SubmissionHandler

dump_blueprint = Blueprint("dump", __name__)


@dump_blueprint.route("/dump/debug", methods=["GET"])
@login_required
@role_required("dumper")
def dump_debug() -> str:
    questionnaire_store = get_questionnaire_store(
        current_user.user_id, current_user.user_ik
    )
    return questionnaire_store.serialize()


@dump_blueprint.route("/dump/routing-path", methods=["GET"])
@login_required
@role_required("dumper")
@with_questionnaire_store
@with_schema
def dump_routing(
    schema: QuestionnaireSchema, questionnaire_store: QuestionnaireStore
) -> tuple[str, int]:
    router = Router(
        schema=schema,
        data_stores=questionnaire_store.stores,
    )

    response = [
        {
            "section_id": routing_path.section_id,
            "list_item_id": routing_path.list_item_id,
            "routing_path": routing_path.block_ids,
        }
        for routing_path in router.full_routing_path()
    ]

    return json_dumps(response), 200


@dump_blueprint.route("/dump/submission", methods=["GET"])
@login_required
@role_required("dumper")
@with_questionnaire_store
@with_schema
def dump_submission(
    schema: QuestionnaireSchema, questionnaire_store: QuestionnaireStore
) -> tuple[str, int]:
    router = Router(
        schema=schema,
        data_stores=questionnaire_store.stores,
    )

    routing_path = router.full_routing_path()

    submission_handler = SubmissionHandler(schema, questionnaire_store, routing_path)

    response = {"submission": submission_handler.get_payload()}
    return json_dumps(response), 200
