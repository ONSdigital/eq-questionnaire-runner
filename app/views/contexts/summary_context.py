from typing import Any, Generator, Optional, Union

from werkzeug.datastructures import ImmutableDict

from app.questionnaire.location import Location

from .context import Context
from .section_summary_context import SectionSummaryContext


class SummaryContext(Context):
    def __call__(
        self, answers_are_editable: bool = False, return_to: Optional[str] = None
    ) -> dict[str, Union[str, list, bool]]:
        groups = list(self._build_all_groups(return_to))
        summary_options = self._schema.get_summary_options()
        collapsible = summary_options.get("collapsible", False)

        refactored_groups = set_unique_group_ids(groups)

        return {
            "groups": refactored_groups,
            "answers_are_editable": answers_are_editable,
            "collapsible": collapsible,
            "summary_type": "Summary",
        }

    def _build_all_groups(
        self, return_to: Optional[str]
    ) -> Generator[ImmutableDict[str, Any], None, None]:
        for section_id in self._router.enabled_section_ids:
            if repeat := self._schema.get_repeat_for_section(section_id):
                for_repeat = self._list_store[repeat["for_list"]]

                if for_repeat.count > 0:
                    for item in for_repeat.items:
                        location = Location(
                            section_id=section_id,
                            list_name=for_repeat.name,
                            list_item_id=item,
                        )
                        section_summary_context = SectionSummaryContext(
                            language=self._language,
                            schema=self._schema,
                            answer_store=self._answer_store,
                            list_store=self._list_store,
                            progress_store=self._progress_store,
                            metadata=self._metadata,
                            response_metadata=self._response_metadata,
                            current_location=location,
                            routing_path=self._router.routing_path(
                                section_id=section_id, list_item_id=item
                            ),
                        )

                        yield from section_summary_context.build_summary(
                            return_to=return_to, get_refactored_groups=False
                        ).get("groups", [])
            else:
                location = Location(section_id=section_id, list_item_id=None)
                section_summary_context = SectionSummaryContext(
                    language=self._language,
                    schema=self._schema,
                    answer_store=self._answer_store,
                    list_store=self._list_store,
                    progress_store=self._progress_store,
                    metadata=self._metadata,
                    response_metadata=self._response_metadata,
                    current_location=location,
                    routing_path=self._router.routing_path(section_id),
                )

                yield from section_summary_context.build_summary(
                    return_to=return_to, get_refactored_groups=False
                ).get("groups", [])


def set_unique_group_ids(groups: list[ImmutableDict]) -> list[ImmutableDict]:
    checked_ids = set()
    id_value = 0

    for group in groups:
        if "id" in group:
            group_id = group["id"]
            if group_id in checked_ids:
                id_value += 1
            checked_ids.add(group_id)
            group["id"] = f"{group_id}-{id_value}"

    return groups
