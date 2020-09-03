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
