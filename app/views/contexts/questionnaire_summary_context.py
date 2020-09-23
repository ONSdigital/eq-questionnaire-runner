from flask_babel import lazy_gettext

from app.questionnaire.location import Location

from .context import Context
from .section_summary_context import SectionSummaryContext


class QuestionnaireSummaryContext(Context):
    def __call__(self, collapsible=True, answers_are_editable=True):
        groups = list(self._build_all_groups())

        submission_schema = self._schema.get_submission()

        title = submission_schema.get("title") or lazy_gettext(
            "Check your answers and submit"
        )
        submit_button = submission_schema.get("button") or lazy_gettext(
            "Submit answers"
        )
        guidance = submission_schema.get("guidance") or lazy_gettext(
            "Please submit this survey to complete it")

        warning = submission_schema.get("warning") or None

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": answers_are_editable,
                "collapsible": collapsible,
                "summary_type": "Summary",
            },
                "title": title,
                "guidance": guidance,
                "warning": warning,
                "submit_button": submit_button
            }

        return context

    def _build_all_groups(self):
        """ NB: Does not support repeating sections """
        section_summary_context = SectionSummaryContext(
            language=self._language,
            schema=self._schema,
            answer_store=self._answer_store,
            list_store=self._list_store,
            progress_store=self._progress_store,
            metadata=self._metadata,
        )

        for section_id in self._router.enabled_section_ids:
            section = self._schema.get_section(section_id)
            if section.get("summary", {}).get("items"):
                break

            location = Location(section_id=section_id)
            for group in section_summary_context(location, return_to="final-summary")[
                "summary"
            ]["groups"]:
                yield group
