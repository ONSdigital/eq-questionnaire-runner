import simplejson as json
from flask import Blueprint, Response, request, session, current_app
from sdc.crypto.decrypter import decrypt
from sdc.crypto.encrypter import encrypt
from structlog import get_logger

from app.authentication.user import User
from app.globals import get_answer_store, get_questionnaire_store, get_metadata
from app.keys import KEY_PURPOSE_AUTHENTICATION, KEY_PURPOSE_SUBMISSION
from app.questionnaire.path_finder import PathFinder
from app.submitter.converter import convert_answers
from app.submitter.submission_failed import SubmissionFailedException
from app.utilities.schema import load_schema_from_metadata

flush_blueprint = Blueprint('flush', __name__)

logger = get_logger()


@flush_blueprint.route('/flush', methods=['POST'])
def flush_data():
    if session:
        session.clear()

    encrypted_token = request.args.get('token')

    if not encrypted_token or encrypted_token is None:
        return Response(status=403)

    decrypted_token = decrypt(
        token=encrypted_token,
        key_store=current_app.eq['key_store'],
        key_purpose=KEY_PURPOSE_AUTHENTICATION,
        leeway=current_app.config['EQ_JWT_LEEWAY_IN_SECONDS'],
    )

    roles = decrypted_token.get('roles')

    if roles and 'flusher' in roles:
        user = _get_user(decrypted_token['response_id'])
        metadata = get_metadata(user)
        if 'tx_id' in metadata:
            logger.bind(tx_id=metadata['tx_id'])
        if _submit_data(user):
            return Response(status=200)
        return Response(status=404)
    return Response(status=403)


def _submit_data(user):
    answer_store = get_answer_store(user)

    if answer_store:
        questionnaire_store = get_questionnaire_store(user.user_id, user.user_ik)
        answer_store = questionnaire_store.answer_store
        metadata = questionnaire_store.metadata
        progress_store = questionnaire_store.progress_store
        list_store = questionnaire_store.list_store

        schema = load_schema_from_metadata(metadata)

        path_finder = PathFinder(
            schema, answer_store, metadata, progress_store, list_store
        )
        full_routing_path = path_finder.full_routing_path()

        message = json.dumps(
            convert_answers(
                schema, questionnaire_store, full_routing_path, flushed=True
            ),
            for_json=True,
        )

        encrypted_message = encrypt(
            message, current_app.eq['key_store'], KEY_PURPOSE_SUBMISSION
        )

        sent = current_app.eq['submitter'].send_message(
            encrypted_message,
            tx_id=metadata.get('tx_id'),
            questionnaire_id=metadata.get('questionnaire_id'),
            case_id=metadata.get('case_id'),
        )

        if not sent:
            raise SubmissionFailedException()

        get_questionnaire_store(user.user_id, user.user_ik).delete()
        logger.info("successfully flushed answers")
        return True

    logger.info("no answers found to flush")
    return False


def _get_user(response_id):
    id_generator = current_app.eq['id_generator']
    user_id = id_generator.generate_id(response_id)
    user_ik = id_generator.generate_ik(response_id)
    return User(user_id, user_ik)
