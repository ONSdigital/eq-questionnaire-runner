from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire import QuestionSchemaType


def build_question_context(
    rendered_block: dict[str, QuestionSchemaType], form: QuestionnaireForm
) -> dict:
    question = rendered_block["question"]

    context: dict[str, dict] = {
        "block": rendered_block,
        "form": {
            "errors": form.errors,
            "question_errors": form.question_errors,
            "mapped_errors": form.map_errors(),
            "answer_errors": {},
            "fields": {},
        },
    }

    answer_ids: list[str] = []

    for answer in question["answers"]:
        answer_ids.append(answer["id"])

        if answer["type"] in ("Checkbox", "Radio"):
            answer_ids.extend(
                option["detail_answer"]["id"]
                for option in answer.get("options", [])
                if "detail_answer" in option
            )

    for answer_id in answer_ids:
        context["form"]["answer_errors"][answer_id] = form.answer_errors(answer_id)

        if answer_id in form:
            context["form"]["fields"][answer_id] = form[answer_id]

    return context
