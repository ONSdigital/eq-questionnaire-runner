from typing import Generator, Mapping, Union

from app.questionnaire.location import Location

from .context import Context
from .section_summary_context import SectionSummaryContext


class SummaryContext(Context):
    def __call__(
        self, answers_are_editable: bool = True, summary_type: str = "final"
    ) -> dict[str, Union[str, list, bool]]:

        groups = list(self._build_all_groups(summary_type))
        summary_options = self._schema.get_summary_options()
        collapsible = summary_options.get("collapsible", False)
        return {
            "groups": groups,
            "answers_are_editable": answers_are_editable,
            "collapsible": collapsible,
            "summary_type": "Summary",
        }

    def _build_all_groups(self, summary_type: str) -> Generator[dict, None, None]:
        """ NB: Does not support repeating sections """

        for section_id in self._router.enabled_section_ids:
            location = Location(section_id=section_id)
            section_summary_context = SectionSummaryContext(
                language=self._language,
                schema=self._schema,
                answer_store=self._answer_store,
                list_store=self._list_store,
                progress_store=self._progress_store,
                metadata=self._metadata,
                current_location=location,
                return_to="final-summary" if summary_type == "final" else None,
                routing_path=self._router.routing_path(section_id),
            )
            section: Mapping = self._schema.get_section(section_id) or {}
            if section.get("summary", {}).get("items"):
                break

            for group in section_summary_context()["summary"]["groups"]:
                yield group
