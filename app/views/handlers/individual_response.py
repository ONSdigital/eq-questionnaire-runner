from functools import cached_property
from typing import List, Mapping

from flask import redirect
from flask.helpers import url_for
from flask_babel import lazy_gettext
from werkzeug.exceptions import NotFound

from app.data_model.progress_store import CompletionStatus
from app.forms.questionnaire_form import generate_form
from app.helpers.template_helper import render_template
from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.questionnaire.router import Router
from app.views.contexts.question import build_question_context


class IndividualResponseHandler:
    _person_name_placeholder: List[Mapping] = [
        {
            "placeholder": "person_name",
            "transforms": [
                {
                    "arguments": {
                        "delimiter": " ",
                        "list_to_concatenate": {
                            "identifier": ["first-name", "last-name"],
                            "source": "answers",
                        },
                    },
                    "transform": "concatenate_list",
                }
            ],
        }
    ]

    def __init__(
        self,
        block_definition,
        schema,
        questionnaire_store,
        language,
        form_data,
        list_item_id,
    ):
        self._block_definition = block_definition
        self._schema = schema
        self._questionnaire_store = questionnaire_store
        self._language = language
        self._form_data = form_data
        self._list_item_id = list_item_id

        self.page_title = None

        if not self._is_location_valid():
            raise NotFound

    def _is_location_valid(self):
        if not self.router.can_access_hub():
            return False

        self._list_name = self._schema.json.get("individual_response", {}).get(
            "for_list"
        )
        list_model = self._questionnaire_store.list_store[self._list_name]

        if not list_model:
            return False

        if self._list_item_id:
            if self._list_item_id not in list_model:
                return False

            if self._list_item_id == list_model.primary_person:
                return False

        return True

    @cached_property
    def rendered_block(self) -> Mapping:
        return self._render_block()

    @cached_property
    def placeholder_renderer(self):
        return PlaceholderRenderer(
            language=self._language,
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            metadata=self._questionnaire_store.metadata,
            location=None,
            list_store=self._questionnaire_store.list_store,
        )

    @cached_property
    def router(self):
        return Router(
            schema=self._schema,
            answer_store=self._questionnaire_store.answer_store,
            list_store=self._questionnaire_store.list_store,
            progress_store=self._questionnaire_store.progress_store,
            metadata=self._questionnaire_store.metadata,
        )

    @cached_property
    def individual_section_id(self):
        return self._schema.json.get("individual_response", {}).get(
            "individual_section_id"
        )

    @cached_property
    def form(self):
        return generate_form(
            schema=self._schema,
            question_schema=self.rendered_block["question"],
            answer_store=None,
            metadata=self._questionnaire_store.metadata,
            form_data=self._form_data,
        )

    def get_context(self):
        return build_question_context(self.rendered_block, self.form)

    def handle_get(self):
        individual_section_first_block_id = self._schema.get_first_block_id_for_section(
            self.individual_section_id
        )

        if self._list_item_id:
            previous_location_url = url_for(
                "questionnaire.block",
                list_name=self._list_name,
                list_item_id=self._list_item_id,
                block_id=individual_section_first_block_id,
            )
        else:
            previous_location_url = url_for("questionnaire.get_questionnaire")

        return render_template(
            template="individual_response/interstitial",
            language=self._language,
            previous_location_url=previous_location_url,
        )

    def _render_block(self):
        return self.placeholder_renderer.render(
            self._block_definition, self._list_item_id
        )


class IndividualResponseHowHandler(IndividualResponseHandler):
    block_definition: Mapping = {
        "type": "IndividualResponse",
        "id": "individual-response",
        "question": {
            "type": "Question",
            "id": "individual-response-how",
            "title": {
                "text": lazy_gettext(
                    "How would you like <em>{person_name}</em> to receive a separate census?"
                ),
                "placeholders": IndividualResponseHandler._person_name_placeholder,
            },
            "description": lazy_gettext(
                "<p>For someone to complete a separate census, we need to send them an individual access code.</p><p>Select how to send access code</p>"
            ),
            "answers": [
                {
                    "type": "Radio",
                    "id": "individual-response-how-answer",
                    "mandatory": False,
                    "default": "Post",
                    "options": [
                        {
                            "label": lazy_gettext("Post"),
                            "value": "Post",
                            "description": lazy_gettext(
                                "We can only send this to an unnamed resident at the registered household address"
                            ),
                        }
                    ],
                }
            ],
        },
    }

    def __init__(self, schema, questionnaire_store, language, form_data, list_item_id):
        super().__init__(
            self.block_definition,
            schema,
            questionnaire_store,
            language,
            form_data,
            list_item_id,
        )

    def handle_get(self):
        previous_location_url = url_for(
            "individual_response.request_individual_response",
            list_item_id=self._list_item_id,
        )

        return render_template(
            "individual_response/how",
            language=self._language,
            content=self.get_context(),
            previous_location_url=previous_location_url,
        )


class IndividualResponsePostAddressConfirmHandler(IndividualResponseHandler):
    block_definition: Mapping = {
        "type": "IndividualResponse",
        "question": {
            "type": "Question",
            "id": "individual-response-post-confirm",
            "title": {
                "text": lazy_gettext(
                    "Do you want to send an individual access code for {person_name} by post?"
                ),
                "placeholders": IndividualResponseHandler._person_name_placeholder,
            },
            "description": lazy_gettext(
                "A letter with an individual access code will be sent to your registered household address"
            ),
            "guidance": {
                "contents": [
                    {
                        "description": lazy_gettext(
                            "The letter will be addressed to <strong>Individual Resident</strong> instead of the name provided"
                        )
                    }
                ]
            },
            "answers": [
                {
                    "type": "Radio",
                    "id": "individual-response-post-confirm-answer",
                    "mandatory": True,
                    "options": [
                        {
                            "label": lazy_gettext("Yes, send the access code by post"),
                            "value": "Yes, send the access code by post",
                        },
                        {
                            "label": lazy_gettext("No, send it another way"),
                            "value": "No, send it another way",
                        },
                    ],
                }
            ],
        },
    }

    def __init__(self, schema, questionnaire_store, language, form_data, list_item_id):
        super().__init__(
            self.block_definition,
            schema,
            questionnaire_store,
            language,
            form_data,
            list_item_id,
        )

    @cached_property
    def answer_id(self):
        return self.rendered_block["question"]["answers"][0]["id"]

    @cached_property
    def confirm_option(self):
        return self.rendered_block["question"]["answers"][0]["options"][0]["value"]

    @cached_property
    def selected_option(self):
        return self.form.get_data(self.answer_id)

    def handle_get(self):
        previous_location_url = url_for(
            "individual_response.get_individual_response_how",
            list_item_id=self._list_item_id,
        )

        return render_template(
            "individual_response/question",
            language=self._language,
            content=self.get_context(),
            previous_location_url=previous_location_url,
        )

    def handle_post(self):
        if self.selected_option == self.confirm_option:
            self._questionnaire_store.progress_store.update_section_status(
                CompletionStatus.INDIVIDUAL_RESPONSE_REQUESTED,
                self._schema.json["individual_response"]["individual_section_id"],
                self._list_item_id,
            )
            if self._questionnaire_store.progress_store.is_dirty:
                self._questionnaire_store.save()

            return redirect(
                url_for(
                    "individual_response.get_individual_response_post_address_confirmation"
                )
            )

        return redirect(
            url_for(
                "individual_response.get_individual_response_how",
                list_item_id=self._list_item_id,
            )
        )
