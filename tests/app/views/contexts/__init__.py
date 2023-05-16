def assert_summary_context(context, summary_item_type="question"):
    summary_context = context["summary"]
    for key_value in ("sections", "answers_are_editable", "summary_type"):
        assert (
            key_value in summary_context
        ), f"Key value {key_value} missing from context['summary']"

    for section in summary_context["sections"]:
        for group in section["groups"]:
            assert "id" in group
            assert "blocks" in group
            for block in group["blocks"]:
                assert summary_item_type in block
                assert "title" in block[summary_item_type]
                assert "answers" in block[summary_item_type]
                for answer in block[summary_item_type]["answers"]:
                    assert "id" in answer
                    assert "value" in answer
                    assert "type" in answer


def assert_preview_context(context):
    for key_value in ("blocks", "title", "id"):
        assert (
            key_value in context["sections"][0]
        ), f"Key value {key_value} missing from context"

    for block in context["sections"][0]["blocks"]:
        assert "question" in block
        for answers in block["question"]["answers"]:
            assert len(answers) != 0
