from typing import Generator, Mapping, MutableMapping

from flask import url_for

from app.data_models import (
    AnswerStore,
    ListStore,
    ProgressStore,
    SupplementaryDataStore,
)
from app.data_models.metadata_proxy import MetadataProxy
from app.questionnaire import QuestionnaireSchema
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.rules.rule_evaluator import RuleEvaluator
from app.utilities.types import LocationType, SectionKey


class Router:
    def __init__(
        self,
        schema: QuestionnaireSchema,
        answer_store: AnswerStore,
        list_store: ListStore,
        progress_store: ProgressStore,
        metadata: MetadataProxy | None,
        response_metadata: MutableMapping,
        supplementary_data_store: SupplementaryDataStore,
    ):
        self._schema = schema
        self._answer_store = answer_store
        self._list_store = list_store
        self._progress_store = progress_store
        self._metadata = metadata
        self._response_metadata = response_metadata
        self._supplementary_data_store = supplementary_data_store

        self._path_finder = PathFinder(
            self._schema,
            self._answer_store,
            self._list_store,
            self._progress_store,
            self._metadata,
            self._response_metadata,
            self._supplementary_data_store,
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

    def get_last_location_in_questionnaire_url(self) -> str | None:
        section_key = self._get_last_complete_section_key()
        if section_key:
            routing_path = self.routing_path(*section_key)
            return self.get_last_location_in_section(routing_path).url()

    def is_list_item_in_list_store(self, list_item_id: str, list_name: str) -> bool:
        return list_item_id in self._list_store[list_name]

    def can_access_location(
        self, location: LocationType, routing_path: RoutingPath
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
            self._progress_store.is_section_or_repeating_blocks_progress_complete(
                section_id
            )
            for section_id in self._schema.get_section_ids_required_for_hub()
            if section_id in self.enabled_section_ids
        )

    def can_display_section_summary(
        self, section_id: str, list_item_id: str | None = None
    ) -> bool:
        return bool(
            self._schema.get_summary_for_section(section_id)
        ) and self._progress_store.is_section_or_repeating_blocks_progress_complete(
            section_id, list_item_id
        )

    def routing_path(
        self, section_id: str, list_item_id: str | None = None
    ) -> RoutingPath:
        return self._path_finder.routing_path(section_id, list_item_id)

    def get_next_location_url(
        self,
        location: LocationType,
        routing_path: RoutingPath,
        return_to: str | None = None,
        return_to_answer_id: str | None = None,
        return_to_block_id: str | None = None,
    ) -> str:
        """
        Get the next location in the section. If the section is complete, determine where to go next,
        whether it be a summary, the hub or the next incomplete location.
        """
        is_section_complete = (
            self._progress_store.is_section_or_repeating_blocks_progress_complete(
                location.section_id, location.list_item_id
            )
        )

        if return_to_url := self._get_return_to_location_url(
            location,
            return_to,
            routing_path,
            is_for_previous=False,
            is_section_complete=is_section_complete,
            return_to_answer_id=return_to_answer_id,
            return_to_block_id=return_to_block_id,
        ):
            return return_to_url

        if is_section_complete:
            return self._get_next_location_url_for_complete_section(location)

        # Due to backwards routing you can be on the last block of the path but with an in_progress section
        is_last_block_on_path = routing_path[-1] == location.block_id
        if is_last_block_on_path:
            # Type ignore: The section is not complete therefore we must have a location
            next_location: Location = self._get_first_incomplete_location_in_section(routing_path)  # type: ignore
            return next_location.url()

        return self.get_next_block_url(
            location,
            routing_path,
            return_to=return_to,
            return_to_answer_id=return_to_answer_id,
            return_to_block_id=return_to_block_id,
        )

    def _get_next_location_url_for_complete_section(
        self, location: LocationType
    ) -> str:
        if self._schema.show_summary_on_completion_for_section(location.section_id):
            return self._get_section_url(location)

        return self.get_next_location_url_for_end_of_section()

    def get_previous_location_url(
        self,
        location: LocationType,
        routing_path: RoutingPath,
        return_to: str | None = None,
        return_to_answer_id: str | None = None,
        return_to_block_id: str | None = None,
    ) -> str | None:
        """
        Returns the previous 'location' to visit given a set of user answers or returns to the summary if
        the `return_to` var is set and the section is complete.
        """
        if return_to_url := self._get_return_to_location_url(
            location,
            return_to,
            routing_path,
            is_for_previous=True,
            return_to_answer_id=return_to_answer_id,
            return_to_block_id=return_to_block_id,
        ):
            return return_to_url

        # Type ignore: the location will have a block id at this point
        block_id_index = routing_path.index(location.block_id)  # type: ignore

        if block_id_index != 0:
            previous_block_id = routing_path[block_id_index - 1]
            previous_block = self._schema.get_block(previous_block_id)
            if previous_block and previous_block["type"] == "RelationshipCollector":
                return url_for(
                    "questionnaire.relationships",
                    last=True,
                    return_to=return_to,
                    _anchor=return_to_answer_id,
                )
            return url_for(
                "questionnaire.block",
                block_id=previous_block_id,
                list_name=routing_path.list_name,
                list_item_id=routing_path.list_item_id,
                return_to=return_to,
                return_to_block_id=return_to_block_id,
                _anchor=return_to_answer_id,
            )

        if self.can_access_hub():
            return url_for("questionnaire.get_questionnaire")

        return None

    def _get_return_to_location_url(
        self,
        location: LocationType,
        return_to: str | None,
        routing_path: RoutingPath,
        is_for_previous: bool,
        is_section_complete: bool | None = None,
        return_to_answer_id: str | None = None,
        return_to_block_id: str | None = None,
    ) -> str | None:
        if not return_to:
            return None

        if return_to == "grand-calculated-summary" and (
            url := self._get_return_to_for_grand_calculated_summary(
                return_to=return_to,
                return_to_block_id=return_to_block_id,
                location=location,
                routing_path=routing_path,
                is_for_previous=is_for_previous,
                return_to_answer_id=return_to_answer_id,
            )
        ):
            return url

        if return_to.startswith("calculated-summary") and (
            url := self._get_return_to_for_calculated_summary(
                return_to=return_to,
                return_to_block_id=return_to_block_id,
                location=location,
                routing_path=routing_path,
                is_for_previous=is_for_previous,
                return_to_answer_id=return_to_answer_id,
            )
        ):
            return url

        if is_section_complete is None:
            is_section_complete = (
                self._progress_store.is_section_or_repeating_blocks_progress_complete(
                    location.section_id, location.list_item_id
                )
            )

        if not is_section_complete:
            return None

        if return_to == "section-summary":
            return self._get_section_url(
                location, return_to_answer_id=return_to_answer_id
            )
        if return_to == "final-summary" and self.is_questionnaire_complete:
            return url_for(
                "questionnaire.submit_questionnaire", _anchor=return_to_answer_id
            )

    def _get_return_to_for_grand_calculated_summary(
        self,
        *,
        return_to: str | None,
        return_to_block_id: str | None,
        location: LocationType,
        routing_path: RoutingPath,
        is_for_previous: bool,
        return_to_answer_id: str | None = None,
    ) -> str | None:
        """
        Builds the return url for a grand calculated summary,
        and accounts for it possibly being in a different section to the calculated summaries it references
        """
        if not (return_to_block_id and self._schema.is_block_valid(return_to_block_id)):
            return None

        # Type ignore: if the block is valid, then we'll be able to find a section for it
        grand_calculated_summary_section: str = (
            self._schema.get_section_id_for_block_id(return_to_block_id)  # type: ignore
        )
        if grand_calculated_summary_section != location.section_id:
            # the grand calculated summary is in a different section which will have a different routing path
            # but don't go to it unless the current section is complete
            if not self._progress_store.is_section_or_repeating_blocks_progress_complete(
                location.section_id
            ):
                return self._get_return_url_for_inaccessible_location(
                    is_for_previous=is_for_previous,
                    return_to_block_id=return_to_block_id,
                    return_to=return_to,
                    routing_path=routing_path,
                )

            routing_path = self._path_finder.routing_path(
                section_id=grand_calculated_summary_section
            )
        if self.can_access_location(
            # grand calculated summaries do not yet support repeating sections, when they do, this will need to make use of list item id as well
            Location(
                block_id=return_to_block_id,
                section_id=grand_calculated_summary_section,
            ),
            routing_path,
        ):
            return url_for(
                "questionnaire.block",
                block_id=return_to_block_id,
                return_to=return_to,
                _anchor=return_to_answer_id,
            )
        return self._get_return_url_for_inaccessible_location(
            is_for_previous=is_for_previous,
            return_to_block_id=return_to_block_id,
            return_to=return_to,
            routing_path=routing_path,
        )

    def _get_return_to_for_calculated_summary(
        self,
        *,
        return_to: str,
        return_to_block_id: str | None,
        location: LocationType,
        routing_path: RoutingPath,
        is_for_previous: bool,
        return_to_answer_id: str | None = None,
    ) -> str | None:
        """
        The return url for a calculated summary varies based on whether it's standalone or part of a grand calculated summary

        If the user goes from GrandCalculatedSummary -> CalculatedSummary -> Question, then return_to_block_ids needs to be a list
        so that both the calculated summary id and the grand calculated summary ids are stored.
        """
        block_id = None
        remaining: list[str] = []
        # for a calculated summary this might have multiple items, e.g. a calculated summary to go to and then a grand calculated one
        if return_to_block_id:
            # the first item is the block id to route to (e.g. a calculated summary to go back to first)
            # anything remaining forms where to go next (e.g. a grand calculated summary)
            block_id, *remaining = return_to_block_id.split(",")

        if self.can_access_location(
            Location(
                block_id=block_id,
                section_id=location.section_id,
                list_item_id=location.list_item_id,
            ),
            routing_path,
        ):
            # if the next location is valid, the new url is that location, and the new 'return to block id' is just what remains
            return_to_block_id = ",".join(remaining) if remaining else None
            # if return_to is a list, return all but the first item, but if it's a single item then leave as is
            return_to = return_to[return_to.find(",") + 1 :]

            return url_for(
                "questionnaire.block",
                block_id=block_id,
                list_name=location.list_name,
                list_item_id=location.list_item_id,
                return_to=return_to,
                return_to_block_id=return_to_block_id,
                _anchor=return_to_answer_id,
            )

        return self._get_return_url_for_inaccessible_location(
            is_for_previous=is_for_previous,
            return_to_block_id=return_to_block_id,
            return_to=return_to,
            routing_path=routing_path,
        )

    def _get_return_url_for_inaccessible_location(
        self,
        *,
        is_for_previous: bool,
        return_to_block_id: str | None,
        return_to: str | None,
        routing_path: RoutingPath,
    ) -> str | None:
        """
        Routes to the next incomplete block in the section and preserves return to parameters
        but only when routing forwards, returns None in the case of the previous link
        """
        if (
            not is_for_previous
            and return_to_block_id
            and (
                next_incomplete_location := self._get_first_incomplete_location_in_section(
                    routing_path
                )
            )
        ):
            return next_incomplete_location.url(
                return_to=return_to,
                return_to_block_id=return_to_block_id,
            )

    def get_next_location_url_for_end_of_section(self) -> str:
        if self._schema.is_flow_hub and self.can_access_hub():
            return url_for("questionnaire.get_questionnaire")

        if self._schema.is_flow_linear and self.is_questionnaire_complete:
            return url_for("questionnaire.submit_questionnaire")

        return self.get_first_incomplete_location_in_questionnaire_url()

    def get_section_resume_url(self, routing_path: RoutingPath) -> str:
        section_key = SectionKey(routing_path.section_id, routing_path.list_item_id)

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

    def is_block_complete(
        self, *, block_id: str, section_id: str, list_item_id: str | None
    ) -> bool:
        return block_id in self._progress_store.get_completed_block_ids(
            section_id=section_id, list_item_id=list_item_id
        )

    def _get_first_incomplete_location_in_section(
        self, routing_path: RoutingPath
    ) -> Location | None:
        for block_id in routing_path:
            if not self.is_block_complete(
                block_id=block_id,
                section_id=routing_path.section_id,
                list_item_id=routing_path.list_item_id,
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
        allowable_path: list[str] = []

        if routing_path:
            for block_id in routing_path:
                allowable_path.append(block_id)

                if not self.is_block_complete(
                    block_id=block_id,
                    section_id=routing_path.section_id,
                    list_item_id=routing_path.list_item_id,
                ):
                    return allowable_path

        return allowable_path

    def get_enabled_section_keys(
        self,
    ) -> Generator[SectionKey, None, None]:
        for section_id in self.enabled_section_ids:
            if repeating_list := self._schema.get_repeating_list_for_section(
                section_id
            ):
                for list_item_id in self._list_store[repeating_list]:
                    section_key = SectionKey(section_id, list_item_id)
                    yield section_key
            else:
                section_key = SectionKey(section_id, None)
                yield section_key

    def _get_first_incomplete_section_key(self) -> tuple[str, str | None] | None:
        for section_id, list_item_id in self.get_enabled_section_keys():
            if not self._progress_store.is_section_or_repeating_blocks_progress_complete(
                section_id, list_item_id
            ):
                return section_id, list_item_id

    def _get_last_complete_section_key(self) -> tuple[str, str | None] | None:
        for section_id, list_item_id in list(self.get_enabled_section_keys())[::-1]:
            if self._progress_store.is_section_or_repeating_blocks_progress_complete(
                section_id, list_item_id
            ):
                return section_id, list_item_id

    def _is_section_enabled(self, section: Mapping) -> bool:
        if "enabled" not in section:
            return True

        enabled = section["enabled"]
        section_id = section["id"]

        routing_path_block_ids = self._path_finder.get_when_rules_block_dependencies(
            section_id
        )

        when_rule_evaluator = RuleEvaluator(
            schema=self._schema,
            answer_store=self._answer_store,
            list_store=self._list_store,
            metadata=self._metadata,
            response_metadata=self._response_metadata,
            progress_store=self._progress_store,
            location=Location(section_id=section_id),
            routing_path_block_ids=routing_path_block_ids,
            supplementary_data_store=self._supplementary_data_store,
        )

        return bool(when_rule_evaluator.evaluate(enabled["when"]))

    @staticmethod
    def get_next_block_url(
        location: LocationType,
        routing_path: RoutingPath,
        **kwargs: str | None,
    ) -> str:
        # Type ignore: the location will have a block
        next_block_id = routing_path[routing_path.index(location.block_id) + 1]  # type: ignore
        return url_for(
            "questionnaire.block",
            block_id=next_block_id,
            list_name=routing_path.list_name,
            list_item_id=routing_path.list_item_id,
            _external=False,
            **kwargs,
        )

    @staticmethod
    def _get_section_url(
        location: LocationType,
        return_to_answer_id: str | None = None,
    ) -> str:
        return url_for(
            "questionnaire.get_section",
            section_id=location.section_id,
            list_item_id=location.list_item_id,
            _anchor=return_to_answer_id,
        )
