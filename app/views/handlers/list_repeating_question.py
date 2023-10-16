from flask import url_for

from app.views.handlers.list_edit_question import ListEditQuestion


class ListRepeatingQuestion(ListEditQuestion):
    def get_previous_location_url(self) -> str:
        """
        return to previous location, or when return to is None, navigate to the previous repeating block
        unless this is the first repeating block, in which case, route back to the edit block
        """
        if url := self.get_section_or_final_summary_url():
            return url

        # the locations list_item_id is referring to where to return to within the context of a repeating section
        # since the list collector won't be in a repeating section, use the parent location which doesn't have a list item id
        if url := self.router.get_return_to_location_url(
            location=self.parent_location,
            return_location=self.return_location,
            routing_path=self._routing_path,
            is_for_previous=True,
        ):
            return url

        repeating_block_index = self.repeating_block_ids.index(
            # Type ignore: block_id will exist at this point
            self.current_location.block_id  # type: ignore
        )
        if repeating_block_index != 0:
            previous_repeating_block_id = self.repeating_block_ids[
                repeating_block_index - 1
            ]
            return url_for(
                "questionnaire.block",
                list_name=self.current_location.list_name,
                list_item_id=self.current_location.list_item_id,
                block_id=previous_repeating_block_id,
                **self.return_location.to_dict(),
            )

        if edit_block := self._schema.get_edit_block_for_list_collector(
            self.parent_block["id"]
        ):
            return url_for(
                "questionnaire.block",
                list_name=self.current_location.list_name,
                list_item_id=self.current_location.list_item_id,
                block_id=edit_block["id"],
                **self.return_location.to_dict(),
            )

        return self.parent_location.url(
            **self.return_location.to_dict(),
        )

    def handle_post(self) -> None:
        self.questionnaire_store_updater.add_completed_location(self.current_location)
        if not self.get_first_incomplete_list_repeating_block_location_for_list_item(
            repeating_block_ids=self.repeating_block_ids,
            section_key=self.current_location.section_key,
            # Type ignore: list_name will always exist at this point
            list_name=self.current_location.list_name,  # type: ignore
        ):
            self.questionnaire_store_updater.update_section_status(
                is_complete=True, section_key=self.current_location.section_key
            )

        super().handle_post()
