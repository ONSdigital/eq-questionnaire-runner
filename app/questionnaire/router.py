from typing import Generator, Mapping, Optional, Union

from flask import url_for

from app.data_models import AnswerStore, ListStore, ProgressStore
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.questionnaire.when_rules import evaluate_when_rules


class Router:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: Mapping[str, Union[str, int, list]],
        response_metadata: Mapping,
    ):
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata
        self._response_metadata = response_metadata

        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
        )

    @property
    def enabled_section_ids(self) -> list[str]:
        return [
            section["id"]
            for section in self._schema.get_sections()
            if self._is_section_enabled(section=section)
        ]

    @property
    def is_questionnaire_complete(self) -> bool:
        first_incomplete_section_key = self._get_first_incomplete_section_key()
        return not first_incomplete_section_key

    def get_first_incomplete_location_in_questionnaire_url(self) -> str:
        first_incomplete_section_key = self._get_first_incomplete_section_key()

        if first_incomplete_section_key:
            section_id, list_item_id = first_incomplete_section_key

            section_routing_path = self._path_finder.routing_path(
                section_id=section_id, list_item_id=list_item_id
            )
            return self.get_section_resume_url(section_routing_path)

        return self.get_next_location_url_for_end_of_section()

    def get_last_location_in_questionnaire_url(self) -> str:
        routing_path = self.routing_path(*self._get_last_complete_section_key())
        return self.get_last_location_in_section(routing_path).url()

    def is_list_item_in_list_store(self, list_item_id: str, list_name: str) -> bool:
        return list_item_id in self._list_store[list_name]

    def can_access_location(
        self, location: Location, routing_path: RoutingPath
    ) -> bool:
        """
        Checks whether the location is valid and accessible.
        :return: boolean
        """
        if location.section_id not in self.enabled_section_ids:
            return False

        if (
            location.list_item_id
            and location.list_name
            and not self.is_list_item_in_list_store(
                location.list_item_id, location.list_name
            )
        ):
            return False

        return location.block_id in self._get_allowable_path(routing_path)

    def can_access_hub(self) -> bool:
        return self._schema.is_flow_hub and all(
            self._progress_store.is_section_complete(section_id)
            for section_id in self._schema.get_section_ids_required_for_hub()
            if section_id in self.enabled_section_ids
        )

    def can_display_section_summary(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> bool:
        return bool(
            self._schema.get_summary_for_section(section_id)
        ) and self._progress_store.is_section_complete(section_id, list_item_id)

    def routing_path(
        self, section_id: str, list_item_id: Optional[str] = None
    ) -> RoutingPath:
        return self._path_finder.routing_path(section_id, list_item_id)

    def get_next_location_url(
        self,
        location: Location,
        routing_path: RoutingPath,
        return_to: Optional[str] = None,
    ) -> str:
        """
        Get the next location in the section. If the section is complete, determine where to go next,
        whether it be a summary, the hub or the next incomplete location.
        """
        is_last_block_in_section = routing_path[-1] == location.block_id
        if self._progress_store.is_section_complete(
            location.section_id, location.list_item_id
        ):
            if return_to and (
                return_to_url := self._get_return_to_location_url(location, return_to)
            ):
                return return_to_url

            if is_last_block_in_section:
                return self._get_next_location_url_for_last_block_in_section(location)

        # Due to backwards routing, you can be on the last block without the section being complete
        if is_last_block_in_section:
            return self._get_first_incomplete_location_in_section(routing_path).url()

        return self.get_next_block_url(location, routing_path)

    def _get_next_location_url_for_last_block_in_section(
        self, location: Location
    ) -> str:
        if self._schema.show_summary_on_completion_for_section(location.section_id):
            return self._get_section_url(location)

        return self.get_next_location_url_for_end_of_section()

    def get_previous_location_url(
        self,
        location: Location,
        routing_path: RoutingPath,
        return_to: Optional[str] = None,
    ) -> Optional[str]:
        """
        Returns the previous 'location' to visit given a set of user answers or returns to the summary if
        the `return_to` var is set and the section is complete.
        """

        if return_to and (
            self._progress_store.is_section_complete(
                location.section_id, location.list_item_id
            )
            and (return_to_url := self._get_return_to_location_url(location, return_to))
        ):
            return return_to_url

        block_id_index = routing_path.index(location.block_id)

        if block_id_index != 0:
            previous_block_id = routing_path[block_id_index - 1]
            previous_block = self._schema.get_block(previous_block_id)
            if previous_block and previous_block["type"] == "RelationshipCollector":
                return url_for(
                    "questionnaire.relationships",
                    last=True,
                )
            return url_for(
                "questionnaire.block",
                block_id=previous_block_id,
                list_name=routing_path.list_name,
                list_item_id=routing_path.list_item_id,
            )

        if self.can_access_hub():
            return url_for("questionnaire.get_questionnaire")

        return None

    def _get_return_to_location_url(
        self, location: Location, return_to: str
    ) -> Optional[str]:
        if return_to == "section-summary":
            return self._get_section_url(location)

        if return_to == "final-summary" and self.is_questionnaire_complete:
            return url_for("questionnaire.submit_questionnaire")

    def get_next_location_url_for_end_of_section(self) -> str:
        if self._schema.is_flow_hub and self.can_access_hub():
            return url_for("questionnaire.get_questionnaire")

        if self._schema.is_flow_linear and self.is_questionnaire_complete:
            return url_for("questionnaire.submit_questionnaire")

        return self.get_first_incomplete_location_in_questionnaire_url()

    def get_section_resume_url(self, routing_path: RoutingPath) -> str:
        section_key = (routing_path.section_id, routing_path.list_item_id)

        if section_key in self._progress_store:
            location = self._get_first_incomplete_location_in_section(routing_path)
            if location:
                return location.url(resume=True)

        return self.get_first_location_in_section(routing_path).url()

    def is_path_complete(self, routing_path: RoutingPath) -> bool:
        return not bool(self._get_first_incomplete_location_in_section(routing_path))

    @staticmethod
    def get_first_location_in_section(routing_path: RoutingPath) -> Location:
        return Location(
            block_id=routing_path[0],
            section_id=routing_path.section_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    @staticmethod
    def get_last_location_in_section(routing_path: RoutingPath) -> Location:
        return Location(
            block_id=routing_path[-1],
            section_id=routing_path.section_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    def full_routing_path(self) -> list[RoutingPath]:
        full_routing_path = []
        for section_id in self.enabled_section_ids:
            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list]:
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

    def _is_block_complete(
        self, block_id: str, section_id: str, list_item_id: str
    ) -> bool:
        return block_id in self._progress_store.get_completed_block_ids(
            section_id, list_item_id
        )

    def _get_first_incomplete_location_in_section(
        self, routing_path: RoutingPath
    ) -> Location:
        for block_id in routing_path:
            if not self._is_block_complete(
                block_id, routing_path.section_id, routing_path.list_item_id
            ):
                return Location(
                    block_id=block_id,
                    section_id=routing_path.section_id,
                    list_item_id=routing_path.list_item_id,
                    list_name=routing_path.list_name,
                )

    def _get_allowable_path(self, routing_path: RoutingPath) -> list[str]:
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

    def get_enabled_section_keys(
        self,
    ) -> Generator[tuple[str, Optional[str]], None, None]:
        for section_id in self.enabled_section_ids:
            repeating_list = self._schema.get_repeating_list_for_section(section_id)

            if repeating_list:
                for list_item_id in self._list_store[repeating_list]:
                    section_key = (section_id, list_item_id)
                    yield section_key
            else:
                section_key = (section_id, None)
                yield section_key

    def _get_first_incomplete_section_key(self) -> tuple[str, Optional[str]]:
        for section_id, list_item_id in self.get_enabled_section_keys():
            if not self._progress_store.is_section_complete(section_id, list_item_id):
                return section_id, list_item_id

    def _get_last_complete_section_key(self) -> tuple[str, Optional[str]]:
        for section_id, list_item_id in list(self.get_enabled_section_keys())[::-1]:
            if self._progress_store.is_section_complete(section_id, list_item_id):
                return section_id, list_item_id

    def _is_section_enabled(self, section: Mapping) -> bool:
        if "enabled" not in section:
            return True

        enabled = section["enabled"]
        if isinstance(enabled, dict):
            when_rule_evaluator = RuleEvaluator(
                self._schema,
                self._answer_store,
                self._list_store,
                self._metadata,
                self._response_metadata,
                location=None,
                routing_path_block_ids=None,
            )

            return bool(when_rule_evaluator.evaluate(enabled["when"]))

        return any(
            evaluate_when_rules(
                condition["when"],
                self._schema,
                self._metadata,
                self._answer_store,
                self._list_store,
            )
            for condition in enabled
        )

    @staticmethod
    def get_next_block_url(location: Location, routing_path: RoutingPath) -> str:
        next_block_id = routing_path[routing_path.index(location.block_id) + 1]
        return url_for(
            "questionnaire.block",
            block_id=next_block_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
        )

    @staticmethod
    def _get_section_url(location: Location) -> str:
        return url_for(
            "questionnaire.get_section",
            section_id=location.section_id,
            list_item_id=location.list_item_id,
        )
