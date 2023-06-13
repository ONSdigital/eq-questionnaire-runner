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
