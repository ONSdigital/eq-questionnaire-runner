from typing import Union

from flask import url_for

from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire import QuestionSchemaType
from app.views.contexts.question import build_question_context


def build_feedback_context(
    question_schema: QuestionSchemaType, form: QuestionnaireForm
) -> dict[str, Union[str, bool, dict]]:
    block = {"question": question_schema}
    context = build_question_context(block, form)
    context["hide_sign_out_button"] = False # TODO: Needed now?
    context["question"] = question_schema
    context["sign_out_url"] = url_for("session.get_sign_out") # TODO: Needed now?

    return context
