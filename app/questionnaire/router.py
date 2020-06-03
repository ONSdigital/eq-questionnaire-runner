from flask import url_for

from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.relationship_router import RelationshipRouter
from app.questionnaire.rules import evaluate_when_rules


class Router:
    def __init__(self, schema, answer_store, list_store, progress_store, metadata):
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata

        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
        )

    @property
    def enabled_section_ids(self):
        return [
            section["id"]
            for section in self._schema.get_sections()
            if self._is_section_enabled(section=section)
        ]

    def can_access_location(self, location: Location, routing_path):
        """
        Checks whether the location is valid and accessible.
        :return: boolean
        """
        if location.section_id not in self.enabled_section_ids:
            return False

        if (
            location.list_item_id
            and location.list_item_id not in self._list_store[location.list_name].items
        ):
            return False

        allowable_path = self._get_allowable_path(routing_path)
        if location.block_id in allowable_path:
            block = self._schema.get_block(location.block_id)
            if (
                block["type"] in ["Confirmation", "Summary"]
                and not self.is_survey_complete()
            ):
                return False

            return True
        return False

    def can_access_hub(self):
        return self._schema.is_hub_enabled() and all(
            self._progress_store.is_section_complete(section_id)
            for section_id in self._schema.get_section_ids_required_for_hub()
            if section_id in self.enabled_section_ids
        )

    def routing_path(self, section_id, list_item_id=None):
        return self._path_finder.routing_path(section_id, list_item_id)

    def get_next_location_url(self, location, routing_path, return_to_summary=False):
        """
        Get the next location in the section. If the section is complete, determine where to go next,
        whether it be a summary, the hub or the next incomplete location.
        """

        is_section_complete = self._progress_store.is_section_complete(
            location.section_id, location.list_item_id
        )

        is_last_block_in_section = routing_path[-1] == location.block_id

        if is_section_complete and (return_to_summary or is_last_block_in_section):
            show_summary_on_completion = self._schema.show_summary_on_completion_for_section(
                location.section_id
            )

            if show_summary_on_completion:
                return url_for(
                    "questionnaire.get_section",
                    section_id=location.section_id,
                    list_item_id=location.list_item_id,
                )
            if self._schema.is_hub_enabled():
                return url_for(".get_questionnaire")

            return self.get_first_incomplete_location_in_survey_url()

        return self.get_next_block_url(location, routing_path)

    def get_previous_location_url(self, location, routing_path):
        """
        Returns the previous 'location' to visit given a set of user answers
        """
        block_id_index = routing_path.index(location.block_id)

        if block_id_index != 0:
            previous_block_id = routing_path[block_id_index - 1]
            previous_block = self._schema.get_block(previous_block_id)
            if previous_block["type"] == "RelationshipCollector":
                list_items = self._list_store.get(previous_block["for_list"]).items
                relationship_router = RelationshipRouter(
                    section_id=routing_path.section_id,
                    block_id=previous_block["id"],
                    list_item_ids=list_items,
                )
                return relationship_router.get_last_location_url()
            return url_for(
                "questionnaire.block",
                block_id=previous_block_id,
                list_name=routing_path.list_name,
                list_item_id=routing_path.list_item_id,
            )

        if self.can_access_hub():
            return url_for("questionnaire.get_questionnaire")

        return None

    def get_first_incomplete_location_in_survey_url(self):
        first_incomplete_section_key = self._get_first_incomplete_section_key()

        if first_incomplete_section_key:
            section_id, list_item_id = first_incomplete_section_key

            section_routing_path = self._path_finder.routing_path(
                section_id=section_id, list_item_id=list_item_id
            )
            return self.get_section_resume_url(section_routing_path)

        return self.get_last_location_in_survey().url()

    def get_section_resume_url(self, routing_path):
        section_key = (routing_path.section_id, routing_path.list_item_id)

        if section_key in self._progress_store:
            location = self._get_first_incomplete_location_in_section(routing_path)
            if location:
                return location.url(resume=True)

        return self.get_first_location_in_section(routing_path).url()

    def is_survey_complete(self):
        first_incomplete_section_key = self._get_first_incomplete_section_key()
        if first_incomplete_section_key:
            section_id = first_incomplete_section_key[0]
            if self._does_section_only_contain_summary(section_id):
                return True
            return False

        return True

    def is_path_complete(self, routing_path):
        return not bool(self._get_first_incomplete_location_in_section(routing_path))

    @staticmethod
    def get_first_location_in_section(routing_path) -> Location:
        return Location(
            block_id=routing_path[0],
            section_id=routing_path.section_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    @staticmethod
    def get_last_location_in_section(routing_path) -> Location:
        return Location(
            block_id=routing_path[-1],
            section_id=routing_path.section_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    def full_routing_path(self):
        full_routing_path = []
        for section_id in self.enabled_section_ids:
            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list].items:
                    full_routing_path.append(
                        self._path_finder.routing_path(
                            section_id=section_id, list_item_id=list_item_id
                        )
                    )
            else:
                full_routing_path.append(
                    self._path_finder.routing_path(section_id=section_id)
                )
        return full_routing_path

    def _is_block_complete(self, block_id, section_id, list_item_id):
        completed_block_ids = self._progress_store.get_completed_block_ids(
            section_id, list_item_id
        )

        return block_id in completed_block_ids

    def _get_first_incomplete_location_in_section(self, routing_path):
        for block_id in routing_path:
            block = self._schema.get_block(block_id)
            block_type = block.get("type")

            if not self._is_block_complete(
                block_id, routing_path.section_id, routing_path.list_item_id
            ) and block_type not in {"Summary", "Confirmation"}:
                return Location(
                    block_id=block_id,
                    section_id=routing_path.section_id,
                    list_item_id=routing_path.list_item_id,
                    list_name=routing_path.list_name,
                )

    def _get_allowable_path(self, routing_path):
        """
        The allowable path is the completed path plus the next location
        """
        allowable_path = []

        if routing_path:
            for block_id in routing_path:
                allowable_path.append(block_id)

                if not self._is_block_complete(
                    block_id, routing_path.section_id, routing_path.list_item_id
                ):
                    return allowable_path

        return allowable_path

    def get_enabled_section_keys(self):
        enabled_section_keys = []

        for section_id in self.enabled_section_ids:
            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list].items:
                    section_key = (section_id, list_item_id)
                    enabled_section_keys.append(section_key)
            else:
                section_key = (section_id, None)
                enabled_section_keys.append(section_key)

        return enabled_section_keys

    def _get_first_incomplete_section_key(self):
        enabled_section_keys = self.get_enabled_section_keys()

        for section_id, list_item_id in enabled_section_keys:
            if not self._progress_store.is_section_complete(section_id, list_item_id):
                return section_id, list_item_id

    # This is horrible and only necessary as currently a section can be defined that only
    # contains a Summary or Confirmation. The ideal solution is to move Summary/Confirmation
    # blocks from sections and into the top level of the schema. Once that's done this can be
    # removed.
    def _does_section_only_contain_summary(self, section_id):
        section = self._schema.get_section(section_id)
        groups = section.get("groups")
        if len(groups) == 1:
            blocks = groups[0].get("blocks")
            if len(blocks) == 1:
                block_type = blocks[0].get("type")
                if block_type in {"Summary", "Confirmation"}:
                    return True
        return False

    def _is_section_enabled(self, section):
        if "enabled" not in section:
            return True

        for condition in section["enabled"]:
            if evaluate_when_rules(
                condition["when"],
                self._schema,
                self._metadata,
                self._answer_store,
                self._list_store,
            ):
                return True
        return False

    @staticmethod
    def get_next_block_url(location, routing_path):
        next_block_id = routing_path[routing_path.index(location.block_id) + 1]
        return url_for(
            "questionnaire.block",
            block_id=next_block_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    def get_last_location_in_survey(self):
        last_section_id = self._schema.get_section_ids()[-1]
        last_block_id = self._schema.get_last_block_id_for_section(last_section_id)
        return Location(section_id=last_section_id, block_id=last_block_id)
