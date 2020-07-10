from functools import cached_property

from flask_babel import gettext
from flask import url_for

from app.forms.questionnaire_form import generate_form
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.schema_utils import transform_variants
from app.views.contexts import ListContext
from app.views.contexts.question import build_question_context
from app.views.handlers.block import BlockHandler


class Question(BlockHandler):
    @staticmethod
    def _has_redirect_to_list_add_action(answer_action):
        return answer_action and answer_action["type"] == "RedirectToListAddQuestion"

    @cached_property
    def form(self):
        question_json = self.rendered_block.get("question")
        if self._form_data:
            return generate_form(
                self._schema,
                question_json,
                self._questionnaire_store.answer_store,
                self._questionnaire_store.metadata,
                self._current_location,
                form_data=self._form_data,
            )

        answer_ids = self._schema.get_answer_ids_for_question(question_json)
        answers = self._get_answers_from_answer_store(answer_ids)
        return generate_form(
            self._schema,
            question_json,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.metadata,
            self._current_location,
            data=answers,
        )

    @cached_property
    def rendered_block(self):
        return self._render_block(self.block["id"])

    @cached_property
    def questionnaire_store_updater(self):
        return QuestionnaireStoreUpdater(
            self._current_location,
            self._schema,
            self._questionnaire_store,
            self.rendered_block.get("question"),
        )

    def get_next_location_url(self):
        answer_action = self._get_answer_action()
        if self._has_redirect_to_list_add_action(answer_action):
            location_url = self._get_list_add_question_url(answer_action["params"])

            if location_url:
                return location_url

        return self.router.get_next_location_url(
            self._current_location, self._routing_path, self._return_to_summary
        )

    def _get_answers_from_answer_store(self, answer_ids):
        answers = self._questionnaire_store.answer_store.get_answers_by_answer_id(
            answer_ids=answer_ids, list_item_id=self._current_location.list_item_id
        )
        return {answer.answer_id: answer.value for answer in answers if answer}

    def _get_list_add_question_url(self, params):
        block_id = params["block_id"]
        list_name = params["list_name"]
        list_items = self._questionnaire_store.list_store[list_name].items
        section_id = self._schema.get_section_id_for_block_id(block_id)

        if self._is_list_just_primary(list_items, list_name) or not list_items:
            return Location(
                section_id=section_id, block_id=block_id, list_name=list_name
            ).url(previous=self.current_location.block_id)

    def _is_list_just_primary(self, list_items, list_name):
        return (
            len(list_items) == 1
            and list_items[0]
            == self._questionnaire_store.list_store[list_name].primary_person
        )

    def _get_answer_action(self):
        answers = self.rendered_block["question"]["answers"]

        for answer in answers:
            submitted_answer = self.form.data[answer["id"]]

            for option in answer.get("options", {}):
                action = option.get("action")

                if action and (
                    option["value"] == submitted_answer
                    or option["value"] in submitted_answer
                ):
                    return action

    def get_context(self):
        context = build_question_context(self.rendered_block, self.form)
        context["return_to_hub_url"] = self.get_return_to_hub_url()
        context[
            "last_viewed_question_guidance"
        ] = self.get_last_viewed_question_guidance_context()

        if "list_summary" in self.rendered_block:
            list_context = ListContext(
                self._language,
                self._schema,
                self._questionnaire_store.answer_store,
                self._questionnaire_store.list_store,
                self._questionnaire_store.progress_store,
                self._questionnaire_store.metadata,
            )

            context.update(
                list_context(
                    self.rendered_block["list_summary"]["summary"],
                    self.rendered_block["list_summary"]["for_list"],
                )
            )

        if self.form.errors or self.form.question_errors:
            self.page_title = gettext("Error: {page_title}").format(page_title=self.page_title)

        return context

    def get_last_viewed_question_guidance_context(self):
        if self.resume:
            first_location_in_section_url = self.router.get_first_location_in_section(
                self._routing_path
            ).url()
            return {"first_location_in_section_url": first_location_in_section_url}

    def handle_post(self):
        self.questionnaire_store_updater.update_answers(self.form.data)
        if self.questionnaire_store_updater.is_dirty():
            self._routing_path = self.router.routing_path(
                section_id=self._current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )
        super().handle_post()

    def _render_block(self, block_id):
        block_schema = self._schema.get_block(block_id)

        variant_block = transform_variants(
            block_schema,
            self._schema,
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._current_location,
        )

        rendered_question = self.placeholder_renderer.render(
            variant_block["question"], self._current_location.list_item_id
        )

        if variant_block["question"]:
            self.page_title = self._get_safe_page_title(
                variant_block["question"]["title"]
            )

        return {**variant_block, **{"question": rendered_question}}

    def get_return_to_hub_url(self):
        if (
            self.rendered_block["type"] in ["Question", "ConfirmationQuestion"]
            and self.router.can_access_hub()
        ):
            return url_for(".get_questionnaire")

    def evaluate_and_update_section_status_on_list_change(self, list_name):
        section_ids = self._schema.get_section_ids_dependent_on_list(list_name)

        section_keys_to_evaluate = self.questionnaire_store_updater.started_section_keys(
            section_ids=section_ids
        )

        for section_id, list_item_id in section_keys_to_evaluate:
            path = self.router.routing_path(section_id, list_item_id)
            self.questionnaire_store_updater.update_section_status(
                is_complete=self.router.is_path_complete(path),
                section_id=section_id,
                list_item_id=list_item_id,
            )

    def clear_radio_answers(self):
        answer_ids_to_remove = []
        for answer in self.rendered_block["question"]["answers"]:
            if answer["type"] == "Radio":
                answer_ids_to_remove.append(answer["id"])

        if answer_ids_to_remove:
            self.questionnaire_store_updater.remove_answers(answer_ids_to_remove)
            self.questionnaire_store_updater.save()
