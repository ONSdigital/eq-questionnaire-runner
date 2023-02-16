from app.views.contexts.preview_context import PreviewContext
from tests.app.views.contexts import assert_preview_context


def test_build_preview_rendering_context(
    test_introduction_preview_linear_schema,
    answer_store,
    list_store,
    progress_store,
    questionnaire_store,
):

    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        answer_store,
        list_store,
        progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
        questionnaire_store=questionnaire_store,
    )

    preview_context = preview_context()

    assert_preview_context(preview_context)


def test_build_preview_context(
    test_introduction_preview_linear_schema,
    answer_store,
    list_store,
    progress_store,
    questionnaire_store,
):

    preview_context = PreviewContext(
        "en",
        test_introduction_preview_linear_schema,
        answer_store,
        list_store,
        progress_store,
        metadata=questionnaire_store.metadata,
        response_metadata=questionnaire_store.response_metadata,
        questionnaire_store=questionnaire_store,
    )
    context = preview_context()

    assert "groups" in context
    assert_preview_context(context)
    assert len(context["groups"][0]) == 2
    assert "blocks" in context["groups"][0]
