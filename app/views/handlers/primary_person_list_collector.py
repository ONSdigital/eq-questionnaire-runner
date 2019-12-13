from flask import url_for

from app.views.handlers.question import Question
from app.views.contexts.question import build_question_context


class PrimaryPersonListCollector(Question):
    def __init__(self, *args):
        self._is_adding = False
        self._primary_person_id = None
        super().__init__(*args)

    def get_next_location_url(self):
        if self._is_adding:
            add_or_edit_url = url_for(
                'questionnaire.block',
                list_name=self.rendered_block['for_list'],
                block_id=self.rendered_block['add_or_edit_block']['id'],
                list_item_id=self._primary_person_id,
            )
            return add_or_edit_url

        return super().get_next_location_url()

    def get_context(self):
        return build_question_context(self.rendered_block, self.form)

    def handle_post(self):
        list_name = self.rendered_block['for_list']

        if (
            self.form.data[self.rendered_block['add_or_edit_answer']['id']]
            == self.rendered_block['add_or_edit_answer']['value']
        ):
            self._is_adding = True
            self.questionnaire_store_updater.update_answers(self.form)
            self._primary_person_id = self.questionnaire_store_updater.add_primary_person(
                list_name
            )

        else:
            self.questionnaire_store_updater.remove_primary_person(list_name)
            super().handle_post()

        if self.questionnaire_store_updater.is_dirty:
            self.evaluate_and_update_section_status_on_list_change(list_name)
            self.questionnaire_store_updater.save()
