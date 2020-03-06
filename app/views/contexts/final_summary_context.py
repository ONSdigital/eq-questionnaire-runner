from app.questionnaire.location import Location
from .context import Context
from .section_summary_context import SectionSummaryContext


class FinalSummaryContext(Context):
    def __call__(
        self,
        collapsible=True,
        answers_are_editable=True,
        is_view_submission_response_enabled=False,
    ):
        section_summary_context = SectionSummaryContext(
            self._language,
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )
        groups = list(self._build_all_groups(section_summary_context))

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": answers_are_editable,
                "collapsible": collapsible,
                "is_view_submission_response_enabled": is_view_submission_response_enabled,
                "summary_type": "Summary",
            }
        }
        return context

    def _build_all_groups(self, section_summary_context):
        """ NB: Does not support repeating sections """
        for section_id in self._router.enabled_section_ids:
            for group in section_summary_context(Location(section_id=section_id))[
                "summary"
            ]["groups"]:
                yield group
