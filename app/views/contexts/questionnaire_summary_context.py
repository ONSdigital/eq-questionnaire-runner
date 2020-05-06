from app.questionnaire.location import Location
from .context import Context
from .summary import Group


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
        for section_id in self._router.enabled_section_ids:
            section = self._schema.get_section(section_id)
            if section.get("summary", {}).get("items"):
                break

            for group in section["groups"]:
                location = Location(section_id=section_id)

                routing_path = self._router.routing_path(
                    location.section_id, location.list_item_id
                )

                yield Group(
                    group,
                    routing_path,
                    self._answer_store,
                    self._list_store,
                    self._metadata,
                    self._schema,
                    location,
                    self._language,
                ).serialize()
