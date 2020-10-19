def build_feedback_context(question_schema, form):
    context = {
        "question": question_schema,
        "form": {
            "errors": form.errors,
            "mapped_errors": form.map_errors(),
            "answer_errors": {},
            "fields": {},
        },
    }

    answer_ids = []
    for answer in question_schema["answers"]:
        answer_ids.append(answer["id"])

    for answer_id in answer_ids:
        context["form"]["answer_errors"][answer_id] = form.answer_errors(answer_id)
        if answer_id in form:
            context["form"]["fields"][answer_id] = form[answer_id]
    return context
