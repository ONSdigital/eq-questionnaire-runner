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
    def path_finder(self):
        return self._path_finder

    @property
    def enabled_section_ids(self):
        all_sections = self._schema.get_sections()

        return [
            section['id']
            for section in all_sections
            if self._is_section_enabled(section=section)
        ]

    def _is_section_enabled(self, section):
        section_enabled_conditions = section.get('enabled', [])
        if not section_enabled_conditions:
            return True

        for condition in section_enabled_conditions:
            if evaluate_when_rules(
                condition['when'],
                self._schema,
                self._metadata,
                self._answer_store,
                self._list_store,
            ):
                return True
        return False

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

        if location in allowable_path:
            block = self._schema.get_block(location.block_id)
            if (
                block['type'] in ['Confirmation', 'Summary']
                and not self.is_survey_complete()
            ):
                return False

            return True

        return False

    def can_access_hub(self):
        return self._schema.is_hub_enabled() and all(
            self._progress_store.is_section_complete(section_id)
            for section_id in self._schema.get_section_ids_required_for_hub()
        )

    def get_next_location_url(self, location, routing_path):
        """
        Get the first incomplete block in section/survey if trying to access the section/survey end,
        and the section/survey is incomplete or gets the next default location if the above is false.
        """
        current_block_type = self._schema.get_block(location.block_id)['type']
        last_block_location = routing_path[-1]
        last_block_type = self._schema.get_block(last_block_location.block_id)['type']
        hub_enabled = self._schema.is_hub_enabled()

        # A section summary doesn't always have to be the last block
        if (
            hub_enabled
            and (
                location.block_id == last_block_location.block_id
                or current_block_type == 'SectionSummary'
            )
            and self._progress_store.is_section_complete(
                location.section_id, location.list_item_id
            )
        ):
            return url_for('.get_questionnaire')

        # If the section is complete and contains a SectionSummary, return the SectionSummary location
        if (
            last_block_type == 'SectionSummary'
            and current_block_type != last_block_type
            and self._progress_store.is_section_complete(
                location.section_id, location.list_item_id
            )
        ):
            return last_block_location.url()

        if self.is_survey_complete() and not hub_enabled:
            last_section_id = self._schema.get_section_ids()[-1]
            last_block_id = self._schema.get_last_block_id_for_section(last_section_id)
            return Location(section_id=last_section_id, block_id=last_block_id).url()

        location_index = routing_path.index(location)
        # At end of routing path, so go to next incomplete location
        if location_index == len(routing_path) - 1:
            return self.get_first_incomplete_location_in_survey().url()

        next_location = routing_path[location_index + 1]
        return next_location.url()

    def get_previous_location_url(self, location, routing_path):
        """
        Returns the previous 'location' to visit given a set of user answers
        """
        location_index = routing_path.index(location)

        if location_index != 0:
            previous_location = routing_path[location_index - 1]
            previous_block = self._schema.get_block(previous_location.block_id)
            if previous_block['type'] == 'RelationshipCollector':
                list_items = self._list_store.get(previous_block['for_list']).items
                relationship_router = RelationshipRouter(
                    section_id=location.section_id,
                    block_id=previous_block['id'],
                    list_item_ids=list_items,
                )
                return relationship_router.get_last_location_url()

            return previous_location.url()

        if self.can_access_hub():
            return url_for('questionnaire.get_questionnaire')

        return None

    def get_first_incomplete_location_in_survey(self):
        incomplete_section_keys = self._get_incomplete_section_keys()

        if incomplete_section_keys:
            section_id, list_item_id = incomplete_section_keys[0]

            section_routing_path = self._path_finder.routing_path(
                section_id=section_id, list_item_id=list_item_id
            )
            location = self._path_finder.get_first_incomplete_location(
                section_routing_path
            )

            if location:
                return location

        last_section_id = self._schema.get_section_ids()[-1]
        last_block_id = self._schema.get_last_block_id_for_section(last_section_id)

        return Location(section_id=last_section_id, block_id=last_block_id)

    def get_first_incomplete_location_for_section(
        self, routing_path, section_id, list_item_id=None
    ):
        section_key = (section_id, list_item_id)

        if section_key in self._progress_store:
            for location in routing_path:
                if (
                    location.block_id
                    not in self._progress_store.get_completed_block_ids(
                        section_id=section_id, list_item_id=list_item_id
                    )
                ):
                    return location

        return routing_path[0]

    def get_last_complete_location_for_section(
        self, routing_path, section_id, list_item_id=None
    ):
        section_key = (section_id, list_item_id)

        if section_key in self._progress_store:
            for location in routing_path[::-1]:
                if location.block_id in self._progress_store.get_completed_block_ids(
                    section_id=section_id, list_item_id=list_item_id
                ):
                    return location

    def is_survey_complete(self):
        incomplete_section_keys = self._get_incomplete_section_keys()

        if incomplete_section_keys:
            if len(incomplete_section_keys) > 1:
                return False

            section_id = incomplete_section_keys[0][0]
            if self._does_section_only_contain_summary(section_id):
                return True
            return False

        return True

    def get_section_return_location_when_section_complete(
        self, routing_path
    ) -> Location:
        return self._get_location_of_section_summary(routing_path) or routing_path[0]

    def full_routing_path(self):
        path = []
        for section_id in self.enabled_section_ids:

            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list].items:
                    path = path + list(
                        self._path_finder.routing_path(
                            section_id=section_id, list_item_id=list_item_id
                        )
                    )
            else:
                path = path + list(
                    self._path_finder.routing_path(section_id=section_id)
                )

        return path

    def _get_allowable_path(self, routing_path):
        """
        The allowable path is the completed path plus the next location
        """
        allowable_path = []

        if routing_path:
            for location in routing_path:
                allowable_path.append(location)

                if (
                    location.block_id
                    not in self._progress_store.get_completed_block_ids(
                        section_id=location.section_id,
                        list_item_id=location.list_item_id,
                    )
                ):
                    return allowable_path

        return allowable_path

    def _get_incomplete_section_keys(self):
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

        incomplete_section_keys = [
            (section_id, list_item_id)
            for section_id, list_item_id in enabled_section_keys
            if not self._progress_store.is_section_complete(section_id, list_item_id)
        ]

        return incomplete_section_keys

    # This is horrible and only necessary as currently a section can be defined that only
    # contains a Summary or Confirmation. The ideal solution is to move Summary/Confirmation
    # blocks from sections and into the top level of the schema. Once that's done this can be
    # removed.
    def _does_section_only_contain_summary(self, section_id):
        section = self._schema.get_section(section_id)
        groups = section.get('groups')
        if len(groups) == 1:
            blocks = groups[0].get('blocks')
            if len(blocks) == 1:
                block_type = blocks[0].get('type')
                if block_type in ['Summary', 'Confirmation']:
                    return True
        return False

    def _get_location_of_section_summary(self, routing_path):
        for location in routing_path[::-1]:
            block = self._schema.get_block(location.block_id)
            if block['type'] == 'SectionSummary':
                return location
