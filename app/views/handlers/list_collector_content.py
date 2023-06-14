from app.views.contexts import ListContext
from app.views.handlers.question import Question


class ListCollectorContent(Question):
    def __init__(self, *args):
        self._is_adding = False
        super().__init__(*args)

    def get_context(self):
        list_context = ListContext(
            self._language,
            self._schema,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.progress_store,
            self._questionnaire_store.metadata,
            self._questionnaire_store.response_metadata,
        )

        return {
            **list_context(
                self.rendered_block["summary"],
                for_list=self.rendered_block["for_list"],
                return_to=self._return_to,
            ),
        }

    def get_next_location_url(self):
        return self.router.get_next_location_url(
            self._current_location,
            self._routing_path,
            self._return_to,
            self._return_to_answer_id,
            self._return_to_block_id,
        )

    def handle_post(self):
        self._set_started_at_metadata()
        self.questionnaire_store_updater.add_completed_location()
        self._update_section_completeness()
        self.questionnaire_store_updater.update_progress_for_dependent_sections()
        self.questionnaire_store_updater.save()
