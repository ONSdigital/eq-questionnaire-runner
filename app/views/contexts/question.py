from typing import Any

from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire import QuestionSchemaType
from app.questionnaire.schema_utils import get_answers_from_question


def build_question_context(
    rendered_block: dict[str, QuestionSchemaType], form: QuestionnaireForm
) -> dict[str, Any]:
    question = rendered_block["question"]

    context = {
        "block": rendered_block,
        "form": {
            "errors": form.errors,
            "question_errors": form.question_errors,
            "mapped_errors": form.map_errors(),
            "answer_errors": {},
            "fields": {},
        },
    }

    answer_ids = []

    question["answers"] = get_answers_from_question(question)

    for answer in question["answers"]:
        answer_ids.append(answer["id"])

        if answer["type"] in ("Checkbox", "Radio"):
            for option in answer.get("options", []):
                if "detail_answer" in option:
                    answer_ids.append(option["detail_answer"]["id"])

    for answer_id in answer_ids:
        context["form"]["answer_errors"][answer_id] = form.answer_errors(answer_id)

        if answer_id in form:
            context["form"]["fields"][answer_id] = form[answer_id]

    return context
