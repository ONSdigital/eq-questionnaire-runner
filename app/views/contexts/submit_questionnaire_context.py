from typing import Mapping, Union

from flask_babel import lazy_gettext

from .context import Context
from .summary_context import SummaryContext


class SubmitQuestionnaireContext(Context):
    def __call__(self) -> dict[str, Union[str, dict]]:

        submission_schema: Mapping = self._schema.get_submission()

        title = submission_schema.get("title") or lazy_gettext(
            "Check your answers and submit"
        )
        submit_button = submission_schema.get("button") or lazy_gettext(
            "Submit answers"
        )
        guidance = submission_schema.get("guidance") or lazy_gettext(
            "Please submit this survey to complete it"
        )

        warning = submission_schema.get("warning") or None

        context = {
            "title": title,
            "guidance": guidance,
            "warning": warning,
            "submit_button": submit_button,
        }
        summary_options = self._schema.get_summary_options()

        if summary_options:
            summary_context = SummaryContext(
                language=self._language,
                schema=self._schema,
                answer_store=self._answer_store,
                list_store=self._list_store,
                progress_store=self._progress_store,
                metadata=self._metadata,
                response_metadata=self._response_metadata,
            )
            context["summary"] = summary_context(
                answers_are_editable=True, return_to="final-summary"
            )

        return context
