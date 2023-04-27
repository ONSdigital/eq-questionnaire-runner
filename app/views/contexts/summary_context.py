from typing import Any, Generator, Mapping, Optional, Union

from app.questionnaire.location import Location

from ...data_models import AnswerStore, ListStore, ProgressStore
from ...data_models.metadata_proxy import MetadataProxy
from ...questionnaire import QuestionnaireSchema
from .context import Context
from .section_summary_context import SectionSummaryContext


class SummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Optional[MetadataProxy],
        response_metadata: Mapping,
        view_submitted_response: bool,
    ) -> None:
        super().__init__(
            language,
            schema,
            answer_store,
            list_store,
            progress_store,
            metadata,
            response_metadata,
        )
        self.view_submitted_response = view_submitted_response

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
            "view_submitted_response": self.view_submitted_response,
        }

    def _build_all_groups(
        self, return_to: Optional[str]
    ) -> Generator[dict[str, Any], None, None]:
        for section_id in self._router.enabled_section_ids:
            if repeat := self._schema.get_repeat_for_section(section_id):
                for_repeat = self._list_store[repeat["for_list"]]

                if for_repeat.count > 0:
                    for item in for_repeat.items:
                        yield from self.build_summary_item(
                            section_id=section_id,
                            return_to=return_to,
                            list_item_id=item,
                            list_name=for_repeat.name,
                        )
            else:
                yield from self.build_summary_item(
                    section_id=section_id, return_to=return_to
                )

    def build_summary_item(
        self,
        section_id: str,
        return_to: str | None,
        list_name: str | None = None,
        list_item_id: str | None = None,
    ) -> list[dict[str, Any]]:
        location = Location(
            section_id=section_id, list_name=list_name, list_item_id=list_item_id
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
            routing_path=self._router.routing_path(section_id),
        )

        return section_summary_context.build_summary(
            return_to=return_to,
            view_submitted_response=self.view_submitted_response,
        ).get("groups", [])


def set_unique_group_ids(groups: list[dict]) -> list[dict]:
    checked_ids = set()
    id_value = 0

    for group in groups:
        group_id = group["id"]
        if group_id in checked_ids:
            id_value += 1
            group["id"] = f"{group_id}-{id_value}"
        checked_ids.add(group_id)

    return groups
