from flask import url_for


def build_feedback_context(question_schema, form):
    context = {
        "form": {
            "errors": form.errors,
            "mapped_errors": form.map_errors(),
            "answer_errors": {},
            "fields": {},
        },
        "hide_sign_out_button": False,
        "question": question_schema,
        "sign_out_url": url_for("session.get_sign_out"),
    }

    answer_ids = []
    for answer in question_schema["answers"]:
        answer_ids.append(answer["id"])
        if answer["type"] in ("Checkbox", "Radio"):
            for option in answer["options"]:
                if "detail_answer" in option:
                    answer_ids.append(option["detail_answer"]["id"])

    for answer_id in answer_ids:
        context["form"]["answer_errors"][answer_id] = form.answer_errors(answer_id)
        if answer_id in form:
            context["form"]["fields"][answer_id] = form[answer_id]
    return context
