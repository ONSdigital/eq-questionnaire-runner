from .summary_context import SummaryContext


class SectionSummaryContext(SummaryContext):
    def __call__(self, current_location):
        section_summary_context = self._section_summary_context(current_location)
        section_summary_context["summary"]["groups"] = self.build_groups_for_location(
            current_location
        )
        return section_summary_context

    def _section_summary_context(self, current_location):
        block = self._schema.get_block(current_location.block_id)

        return {
            "summary": {
                "title": self._title_for_location(current_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": block.get("collapsible", False),
            }
        }

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
