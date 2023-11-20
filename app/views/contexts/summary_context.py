from app.data_models.data_stores import DataStores
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.views.contexts.context import Context
from app.views.contexts.section_summary_context import SectionSummaryContext


class SummaryContext(Context):
    def __init__(
        self,
        language: str,
        schema: QuestionnaireSchema,
        data_stores: DataStores,
        view_submitted_response: bool,
    ) -> None:
        super().__init__(
            language,
            schema,
            data_stores,
        )
        self.view_submitted_response = view_submitted_response
        self.summaries: list[dict] = []

    def __call__(
        self, answers_are_editable: bool = False, return_to: str | None = None
    ) -> dict[str, dict | str | list | bool]:
        self._build_all_groups(return_to)
        summary_options = self._schema.get_summary_options()
        collapsible = summary_options.get("collapsible", False)
        self.set_unique_group_ids()

        return {
            "sections": self.summaries,
            "answers_are_editable": answers_are_editable,
            "collapsible": collapsible,
            "summary_type": "Summary",
            "view_submitted_response": self.view_submitted_response,
        }

    def _build_all_groups(self, return_to: str | None) -> None:
        for section_id in self._router.enabled_section_ids:
            if repeat := self._schema.get_repeat_for_section(section_id):
                for_repeat = self._data_stores.list_store[repeat["for_list"]]

                if for_repeat.count > 0:
                    for item in for_repeat.items:
                        self.build_summary_item(
                            section_id=section_id,
                            return_to=return_to,
                            list_item_id=item,
                            list_name=for_repeat.name,
                        )
            else:
                self.build_summary_item(section_id=section_id, return_to=return_to)

    def build_summary_item(
        self,
        section_id: str,
        return_to: str | None,
        list_name: str | None = None,
        list_item_id: str | None = None,
    ) -> None:
        location = Location(
            section_id=section_id, list_name=list_name, list_item_id=list_item_id
        )
        section_summary_context = SectionSummaryContext(
            language=self._language,
            schema=self._schema,
            data_stores=self._data_stores,
            current_location=location,
            routing_path=self._router.routing_path(location.section_key),
        )

        summary = section_summary_context(
            view_submitted_response=self.view_submitted_response, return_to=return_to
        )["summary"]

        for section in summary.get("sections", []):
            if any(group["blocks"] for group in section["groups"]):
                self.summaries.extend(summary["sections"])

    def set_unique_group_ids(self) -> None:
        checked_ids = set()
        id_value = 0

        for section in self.summaries:
            if groups := section.get("groups"):
                for group in groups:
                    group_id = group["id"]
                    if group_id in checked_ids:
                        id_value += 1
                        group["id"] = f"{group_id}-{id_value}"
                    checked_ids.add(group_id)
