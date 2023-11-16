from collections import OrderedDict
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping, MutableMapping

from werkzeug.datastructures import ImmutableDict

from app.data_models import AnswerStore
from app.data_models.answer import AnswerValueTypes, ListAnswer
from app.data_models.data_stores import DataStores
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.variants import choose_question_to_display

MetadataType = MutableMapping[str, str | int | list]


# pylint: disable=too-many-locals,too-many-nested-blocks
def convert_answers_to_payload_0_0_1(
    *,
    data_stores: DataStores,
    schema: QuestionnaireSchema,
    full_routing_path: Iterable[RoutingPath],
) -> OrderedDict[str, Any]:
    """
    Convert answers into the data format below
    list_item_id bound answers are not currently supported
    'data': {
          '001': '01-01-2016',
          '002': '30-03-2016'
        }
    :param data_stores: questionnaire data stores
    :param schema: QuestionnaireSchema class with populated schema json
    :param full_routing_path: a list of section routing paths followed in the questionnaire
    :return: data in a formatted form
    """
    data = OrderedDict()
    for routing_path in full_routing_path:
        for block_id in routing_path:
            answer_ids = schema.get_answer_ids_for_block(block_id)
            answers_in_block = data_stores.answer_store.get_answers_by_answer_id(
                answer_ids, routing_path.list_item_id
            )

            for answer_in_block in answers_in_block:
                answer_schema = None

                block: ImmutableDict = schema.get_block_for_answer_id(answer_in_block.answer_id)  # type: ignore
                current_location = Location(
                    block_id=block_id,
                    section_id=routing_path.section_id,
                    list_item_id=routing_path.list_item_id,
                )
                question = choose_question_to_display(
                    block,
                    schema,
                    data_stores,
                    current_location=current_location,
                )
                for answer_id, answer in schema.get_answers_for_question_by_id(
                    question
                ).items():
                    if answer_id == answer_in_block.answer_id:
                        answer_schema = answer
                        break

                value = answer_in_block.value

                if answer_schema is not None and value is not None:
                    if answer_schema["type"] == "Checkbox":
                        data.update(
                            _get_checkbox_answer_data(
                                data_stores.answer_store, answer_schema, value  # type: ignore
                            )
                        )
                    elif "q_code" in answer_schema:
                        answer_data = _encode_value(value)
                        if answer_data is not None:
                            data[answer_schema["q_code"]] = _format_downstream_answer(
                                answer_schema["type"],
                                answer_in_block.value,
                                answer_data,
                            )

    return data


def _format_downstream_answer(
    answer_type: str, answer_value: AnswerValueTypes, answer_data: str
) -> str:
    if isinstance(answer_value, str):
        if answer_type == "Date":
            return (
                datetime.strptime(answer_value, "%Y-%m-%d")
                .replace(tzinfo=timezone.utc)
                .strftime("%d/%m/%Y")
            )

        if answer_type == "MonthYearDate":
            return (
                datetime.strptime(answer_value, "%Y-%m")
                .replace(tzinfo=timezone.utc)
                .strftime("%m/%Y")
            )

    return answer_data


def _get_checkbox_answer_data(
    answer_store: AnswerStore, answer_schema: Mapping, value: ListAnswer
) -> dict[str, str]:
    qcodes_and_values = []
    for user_answer in value:
        # find the option in the schema which matches the users answer
        option = next(
            (
                option
                for option in answer_schema["options"]
                if option["value"] == user_answer
            ),
            None,
        )

        if option:
            if "detail_answer" in option:
                detail_answer = answer_store.get_answer(option["detail_answer"]["id"])
                if detail_answer:
                    # Ignore mypy type because the answer type can be any non strings, but user_answer is expected to be a string.
                    user_answer = detail_answer.value  # type: ignore

            qcodes_and_values.append((option.get("q_code"), user_answer))

    checkbox_answer_data: dict[str, str] = OrderedDict()

    if all(q_code is not None for (q_code, _) in qcodes_and_values):
        checkbox_answer_data.update(qcodes_and_values)
    else:
        checkbox_answer_data[answer_schema["q_code"]] = str(
            [v for (_, v) in qcodes_and_values]
        )

    return checkbox_answer_data


def _encode_value(value: AnswerValueTypes) -> str | None:
    if isinstance(value, str):
        if value == "":
            return None
        return value
    return str(value)
