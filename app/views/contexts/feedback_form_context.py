from flask import url_for


def build_feedback_context(question_schema, form):
    context = {
        "show_sign_out_warning": True,
        "form": {
            "errors": form.errors,
            "mapped_errors": form.map_errors(),
            "answer_errors": {},
            "fields": {},
        },
        "hide_signout_button": False,
        "question": question_schema,
        "sign_out_url": url_for("session.get_sign_out"),
    }

    answer_ids = (answer["id"] for answer in question_schema["answers"])

    for answer_id in answer_ids:
        context["form"]["answer_errors"][answer_id] = form.answer_errors(answer_id)
        if answer_id in form:
            context["form"]["fields"][answer_id] = form[answer_id]
    return context
