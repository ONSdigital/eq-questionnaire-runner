def assert_summary_context(context):
    summary_context = context["summary"]
    for key_value in ("groups", "answers_are_editable", "summary_type"):
        assert (
            key_value in summary_context
        ), f"Key value {key_value} missing from context['summary']"

    for group in summary_context["groups"]:
        assert "id" in group
        assert "blocks" in group
        for block in group["blocks"]:
            assert "question" in block
            assert "title" in block["question"]
            assert "answers" in block["question"]
            for answer in block["question"]["answers"]:
                assert "id" in answer
                assert "value" in answer
                assert "type" in answer


def assert_preview_context(context):
    for key_value in ("blocks", "title", "id"):
        assert (
            key_value in context
        ), f"Key value {key_value} missing from context"

    for block in context["blocks"]:
        assert "question" in block
        for answers in block["question"]["answers"]:
            assert len(answers) != 0
