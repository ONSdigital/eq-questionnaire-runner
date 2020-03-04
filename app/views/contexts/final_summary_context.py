from app.questionnaire.location import Location
from app.views.contexts import Context
from app.views.contexts.summary.group import Group


class FinalSummaryContext(Context):
    def __call__(self, collapsible):
        groups = self.build_all_groups()

        context = {
            "summary": {
                "groups": groups,
                "answers_are_editable": True,
                "collapsible": collapsible,
                "summary_type": "Summary",
            }
        }
        return context

    def build_groups_for_location(self, location):
        """
        Build a groups context for a particular location.

        Does not support generating multiple sections at a time (i.e. passing no list_item_id for repeating section).
        """
        section = self._schema.get_section(location.section_id)
        routing_path = self._router.routing_path(
            location.section_id, location.list_item_id
        )

        return [
            Group(
                group,
                routing_path,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._schema,
                location,
                self._language,
            ).serialize()
            for group in section["groups"]
        ]

    def build_all_groups(self):
        """ NB: Does not support repeating sections """
        all_groups = []

        for section_id in self._router.enabled_section_ids:
            all_groups.extend(
                self.build_groups_for_location(Location(section_id=section_id))
            )

        return all_groups

    def _section_summary_context(self, current_location):
        section_id = self._schema.get_section_id_for_block_id(current_location.block_id)
        section = self._schema.get_section(section_id)
        block = self._schema.get_block(current_location.block_id)

        summary_context = {
            "summary": {
                "title": self._title_for_location(current_location),
                "summary_type": "SectionSummary",
                "answers_are_editable": True,
                "collapsible": block.get("collapsible", False),
            }
        }

        return summary_context, section

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
