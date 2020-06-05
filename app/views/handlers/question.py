from flask import url_for
from werkzeug.utils import cached_property
from app.helpers.template_helper import safe_content

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
    def rendered_block(self):
        return self._render_block(self.block["id"])

    def get_next_location_url(self):
        answer_action = self._get_answer_action()
        if self._has_redirect_to_list_add_action(answer_action):
            location_url = self._get_list_add_question_url(answer_action["params"])

            if location_url:
                return location_url

        return self.router.get_next_location_url(
            self._current_location, self._routing_path, self._return_to_summary
        )

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

        return context

    def get_last_viewed_question_guidance_context(self):
        if self.resume:
            first_location_in_section_url = self._router.get_first_location_in_section(
                self._routing_path
            ).url()
            return {"first_location_in_section_url": first_location_in_section_url}

    def handle_post(self):
        self.questionnaire_store_updater.update_answers(self.form)

        self.questionnaire_store_updater.add_completed_location()

        # pylint: disable=using-constant-test
        if self.questionnaire_store_updater.is_dirty:
            self._routing_path = self.router.routing_path(
                section_id=self._current_location.section_id,
                list_item_id=self._current_location.list_item_id,
            )

        self._update_section_completeness()

        self.questionnaire_store_updater.save()

    @cached_property
    def questionnaire_store_updater(self):
        if not self._questionnaire_store_updater:
            self._questionnaire_store_updater = QuestionnaireStoreUpdater(
                self._current_location,
                self._schema,
                self._questionnaire_store,
                self.rendered_block.get("question"),
            )
        return self._questionnaire_store_updater

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
            self.page_title = self._get_page_title(variant_block["question"])

        return {**variant_block, **{"question": rendered_question}}

    def get_return_to_hub_url(self):
        if (
            self.rendered_block["type"] in ["Question", "ConfirmationQuestion"]
            and self._router.can_access_hub()
        ):
            return url_for(".get_questionnaire")

    def _get_page_title(self, question):
        if isinstance(question["title"], str):
            question_title = question["title"]
        elif "text_plural" in question["title"]:
            question_title = question["title"]["text_plural"]["forms"]["other"]
        else:
            question_title = question["title"]["text"]

        return safe_content(f'{question_title} - {self._schema.json["title"]}')

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
