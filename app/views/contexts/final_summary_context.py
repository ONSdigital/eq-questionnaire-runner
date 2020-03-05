from app.questionnaire.location import Location
from .summary_context import SummaryContext


class FinalSummaryContext(SummaryContext):
    def __call__(
        self,
        collapsible=True,
        answers_are_editable=True,
        is_view_submission_response_enabled=False,
    ):
        groups = self.build_all_groups()

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

    def build_all_groups(self):
        """ NB: Does not support repeating sections """
        all_groups = []

        for section_id in self._router.enabled_section_ids:
            all_groups.extend(
                self.build_groups_for_location(Location(section_id=section_id))
            )

        return all_groups

    def _title_for_location(self, location):
        title = self._schema.get_block(location.block_id).get("title")

        if location.list_item_id:
            repeating_title = self._schema.get_repeating_title_for_section(
                location.section_id
            )
            if repeating_title:
                title = self._placeholder_renderer.render_placeholder(
                    repeating_title, location.list_item_id
                )
        return title
