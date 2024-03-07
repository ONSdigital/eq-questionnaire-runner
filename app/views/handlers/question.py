from functools import cached_property
from typing import Mapping, Sequence

from flask import url_for
from flask_babel import gettext

from app.forms.questionnaire_form import QuestionnaireForm, generate_form
from app.helpers import get_address_lookup_api_auth_token
from app.questionnaire.location import Location, SectionKey
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.variants import transform_variants
from app.views.contexts import ListContext
from app.views.contexts.question import build_question_context
from app.views.handlers.block import BlockHandler


class Question(BlockHandler):
    @staticmethod
    def _has_redirect_to_list_add_action(answer_action: Mapping | None) -> bool:
        return bool(answer_action and answer_action["type"] == "RedirectToListAddBlock")

    @cached_property
    def form(self) -> QuestionnaireForm:
        question_json = self.rendered_block.get("question", {})

        if self._form_data:
            return generate_form(
                schema=self._schema,
                question_schema=question_json,
                data_stores=self._questionnaire_store.data_stores,
                location=self._current_location,
                form_data=self._form_data,
            )

        answers = self._get_answers_for_question(question_json)
        return generate_form(
            schema=self._schema,
            question_schema=question_json,
            data_stores=self._questionnaire_store.data_stores,
            location=self._current_location,
            data=answers,
        )

    @cached_property
    def questionnaire_store_updater(self) -> QuestionnaireStoreUpdater:
        return QuestionnaireStoreUpdater(
            self._current_location,
            self._schema,
            self._questionnaire_store,
            self.router,
            self.rendered_block.get("question"),
        )

    @cached_property
    def rendered_block(self) -> dict:
        transformed_block = transform_variants(
            self.block,
            self._schema,
            self._questionnaire_store.data_stores,
            self._current_location,
        )
        page_title = transformed_block.get("page_title") or self._get_safe_page_title(
            transformed_block["question"]["title"]
        )

        self._set_page_title(page_title)

        # We inherit from question in list collector content block which doesn't have "question" sub-block
        if not transformed_block.get("question"):
            return transformed_block

        rendered_question = self.placeholder_renderer.render(
            data_to_render=transformed_block["question"],
            list_item_id=self._current_location.list_item_id,
        )
        return {
            **transformed_block,
            **{"question": rendered_question},
        }

    @cached_property
    def list_context(self) -> ListContext:
        return ListContext(
            language=self._language,
            schema=self._schema,
            data_stores=self._questionnaire_store.data_stores,
        )

    def get_next_location_url(self) -> str:
        answer_action = self._get_answer_action()
        if self._has_redirect_to_list_add_action(answer_action):
            # Type ignore: this is only called if answer_action is not none.
            location_url = self._get_list_add_question_url(answer_action["params"])  # type: ignore

            if location_url:
                return location_url

        return self.router.get_next_location_url(
            self._current_location, self._routing_path, self._return_location
        )

    def _get_answers_for_question(self, question_json: Mapping) -> dict:
        answers_by_answer_id = self._schema.get_answers_for_question_by_id(
            question_json
        )
        answer_value_by_answer_id = {}

        for answer_id, resolved_answer in answers_by_answer_id.items():
            list_item_id = (
                resolved_answer.get("list_item_id")
                or self._current_location.list_item_id
            )
            answer_id_to_use = resolved_answer.get("original_answer_id") or answer_id
            if answer := self._questionnaire_store.data_stores.answer_store.get_answer(
                answer_id=answer_id_to_use, list_item_id=list_item_id
            ):
                answer_value_by_answer_id[answer_id] = answer.value

        return answer_value_by_answer_id

    def _get_list_add_question_url(self, params: dict) -> str | None:
        block_id = params["block_id"]
        list_name = params["list_name"]
        list_items = self._questionnaire_store.data_stores.list_store[list_name].items
        section_id = self._schema.get_section_id_for_block_id(block_id)

        if self._is_list_just_primary(list_items, list_name) or not list_items:
            return Location(
                # Type ignore: section_id is always valid when this is called
                section_id=section_id,  # type: ignore
                block_id=block_id,
                list_name=list_name,
            ).url(previous=self.current_location.block_id)

    def _is_list_just_primary(self, list_items: list[str], list_name: str) -> bool:
        return (
            len(list_items) == 1
            and list_items[0]
            == self._questionnaire_store.data_stores.list_store[
                list_name
            ].primary_person
        )

    def _get_answer_action(self) -> dict | None:
        # When used by list collector content class rendered block we won't have "question" sub-block
        if not self.rendered_block.get("question"):
            return None

        answers = self.rendered_block["question"]["answers"]

        for answer in answers:
            submitted_answer = self.form.data[answer["id"]]

            for option in answer.get("options", {}):
                action: dict | None = option.get("action")

                if action and (
                    option["value"] == submitted_answer
                    or option["value"] in submitted_answer
                ):
                    return action

    def get_context(self) -> dict[str, dict]:
        context = build_question_context(self.rendered_block, self.form)
        context["return_to_hub_url"] = self.get_return_to_hub_url()
        context["last_viewed_question_guidance"] = (
            self.get_last_viewed_question_guidance_context()
        )

        if "list_summary" in self.rendered_block:
            context.update(self.get_list_summary_context())
        if self.form.errors or self.form.question_errors:
            self.page_title = gettext("Error: {page_title}").format(
                page_title=self.page_title
            )

        if self._schema.has_address_lookup_answer(self.rendered_block["question"]) and (
            address_lookup_api_auth_token := get_address_lookup_api_auth_token()
        ):
            context["address_lookup_api_auth_token"] = address_lookup_api_auth_token

        return context

    def get_last_viewed_question_guidance_context(self) -> dict | bool | None:
        if self.resume:
            first_location_in_section_url = self.router.get_first_location_in_section(
                self._routing_path
            ).url()
            return {"first_location_in_section_url": first_location_in_section_url}

    def get_list_summary_context(self) -> dict:
        return self.list_context(
            summary_definition=self.rendered_block["list_summary"]["summary"],
            for_list=self.rendered_block["list_summary"]["for_list"],
            section_id=self.current_location.section_id,
            has_repeating_blocks=bool(self.rendered_block.get("repeating_blocks")),
        )

    def handle_post(self) -> None:
        self.questionnaire_store_updater.update_answers(self.form.data)
        if self.questionnaire_store_updater.is_dirty():
            # We prematurely complete the block, as we need it completed to build the routing path
            # In order to support progress value source references of the previous block
            self.questionnaire_store_updater.add_completed_location(
                self.current_location
            )
            self._routing_path = self.router.routing_path(
                self._current_location.section_key
            )
        super().handle_post()

    def get_return_to_hub_url(self) -> str | None:
        if (
            self.rendered_block["type"] in ["Question", "ConfirmationQuestion"]
            and self.router.can_access_hub()
        ):
            return url_for(".get_questionnaire")

    def clear_radio_answers(self) -> None:
        answer_ids_to_remove = []
        for answer in self.rendered_block["question"]["answers"]:
            if answer["type"] == "Radio":
                answer_ids_to_remove.append(answer["id"])

        if answer_ids_to_remove:
            self.questionnaire_store_updater.remove_answers(
                answer_ids_to_remove, self.current_location.list_item_id
            )
            self.questionnaire_store_updater.save()

    def get_first_incomplete_list_repeating_block_location(
        self, *, repeating_block_ids: Sequence[str], section_id: str, list_name: str
    ) -> Location | None:
        if not repeating_block_ids:
            return None

        list_model = self._questionnaire_store.data_stores.list_store.get(list_name)
        for list_item_id in list_model.items:
            if incomplete_location := self.get_first_incomplete_list_repeating_block_location_for_list_item(
                repeating_block_ids=repeating_block_ids,
                section_key=SectionKey(section_id, list_item_id),
                list_name=list_name,
            ):
                return incomplete_location

    def get_first_incomplete_list_repeating_block_location_for_list_item(
        self,
        *,
        repeating_block_ids: Sequence[str],
        section_key: SectionKey,
        list_name: str,
    ) -> Location | None:
        if self._questionnaire_store.data_stores.progress_store.is_section_complete(
            section_key
        ):
            return None

        for repeating_block_id in repeating_block_ids:
            if not self._questionnaire_store.data_stores.progress_store.is_block_complete(
                block_id=repeating_block_id,
                section_key=section_key,
            ):
                return Location(
                    block_id=repeating_block_id,
                    list_name=list_name,
                    **section_key.to_dict(),
                )
