from . import Context
from .summary import Group


class SummaryContext(Context):
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

