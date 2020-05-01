from app.questionnaire.location import Location
from .context import Context
from .section_summary_context import SectionSummaryContext


class QuestionnaireSummaryContext(Context):
    def __call__(self, collapsible=True, answers_are_editable=True):
        groups = list(self._build_all_groups())

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": answers_are_editable,
                "collapsible": collapsible,
                "summary_type": "Summary",
            }
        }
        return context

    def _build_all_groups(self):
        """ NB: Does not support repeating sections """
        section_summary_context = SectionSummaryContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )

        section_ids = [
            section_id
            for section_id in self._router.enabled_section_ids
            if not self._schema.get_summary_for_section(section_id)
        ]

        for section_id in section_ids:
            for group in section_summary_context(Location(section_id=section_id))[
                "summary"
            ]["groups"]:
                yield group
