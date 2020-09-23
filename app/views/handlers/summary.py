from flask_babel import lazy_gettext

from app.views.contexts import QuestionnaireSummaryContext
from app.views.handlers.content import Content


class Summary(Content):
    def get_context(self):
        questionnaire_summary_context = QuestionnaireSummaryContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
        )
        block = self._schema.get_block(self._current_location.block_id)
        collapsible = block.get("collapsible", False)
        context = questionnaire_summary_context(collapsible)

        if submission_schema := self._schema.get_submission():
            context["title"] = submission_schema.get("title") or lazy_gettext(
                "Check your answers and submit"
            )
            context["submit_button"] = submission_schema.get("button") or lazy_gettext(
                "Submit answers"
            )
            context["guidance"] = submission_schema.get("guidance") or lazy_gettext(
                "Please submit this survey to complete it"
            )
            context["warning"] = submission_schema.get("warning") or None
        else:
            context["title"] = lazy_gettext("Check your answers and submit")
            context["submit_button"] = lazy_gettext("Submit answers")
            context["guidance"] = lazy_gettext(
                "Please submit this survey to complete it"
            )
            context["warning"] = None

        return context
