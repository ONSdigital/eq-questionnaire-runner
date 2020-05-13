from typing import List, Mapping, Union

from flask import url_for
from flask_babel import lazy_gettext

from app.data_model.progress_store import CompletionStatus

from app.views.contexts.context import Context


class HubContext(Context):

    SECTION_CONTENT_STATES = {
        CompletionStatus.COMPLETED: {
            "text": lazy_gettext("Completed"),
            "link": {
                "text": lazy_gettext("View answers"),
                "aria_label": lazy_gettext("View answers for {section_name}"),
            },
        },
        CompletionStatus.IN_PROGRESS: {
            "text": lazy_gettext("Partially completed"),
            "link": {
                "text": lazy_gettext("Continue with section"),
                "aria_label": lazy_gettext("Continue with {section_name} section"),
            },
        },
        CompletionStatus.NOT_STARTED: {
            "text": lazy_gettext("Not started"),
            "link": {
                "text": lazy_gettext("Start section"),
                "aria_label": lazy_gettext("Start {section_name} section"),
            },
        },
    }

    def get_context(self, survey_complete, enabled_section_ids) -> Mapping:
        hub_schema = self._schema.get_hub()
        rows = self._get_rows(enabled_section_ids)
        custom_text = hub_schema.get(
            "complete" if survey_complete else "incomplete", {}
        )

        if survey_complete:
            title = custom_text.get("title") or lazy_gettext("Submit survey")
            guidance = custom_text.get("guidance") or lazy_gettext(
                "Please submit this survey to complete it"
            )

            submit_button = hub_schema.get("submission", {}).get(
                "button"
            ) or lazy_gettext("Submit survey")

        else:
            title = lazy_gettext("Choose another section to complete")
            guidance = custom_text.get("guidance") or lazy_gettext(
                "You must complete all sections in order to submit this survey"
            )
            submit_button = lazy_gettext("Continue")

        return {
            "title": title,
            "guidance": guidance,
            "submit_button": submit_button,
            "rows": rows,
        }

    def get_row_context_for_section(
        self, section_name: str, section_status: str, section_url: str
    ) -> Mapping[str, Union[str, List]]:

        section_content = self.SECTION_CONTENT_STATES[section_status]
        context: Mapping = {
            "rowTitle": section_name,
            "rowItems": [
                {
                    "valueList": [{"text": section_content["text"]}],
                    "actions": [
                        {
                            "text": section_content["link"]["text"],
                            "ariaLabel": section_content["link"]["aria_label"].format(
                                section_name=section_name
                            ),
                            "url": section_url,
                        }
                    ],
                }
            ],
        }

        if section_status == CompletionStatus.COMPLETED:
            context["rowItems"][0]["icon"] = "check-green"

        return context

    @staticmethod
    def get_section_url(section_id, list_item_id) -> str:
        if list_item_id:
            return url_for(
                "questionnaire.get_section",
                section_id=section_id,
                list_item_id=list_item_id,
            )

        return url_for("questionnaire.get_section", section_id=section_id)

    def _get_row_for_repeating_section(self, section_id, list_item_id):
        repeating_title = self._schema.get_repeating_title_for_section(section_id)

        title = self._placeholder_renderer.render_placeholder(
            repeating_title, list_item_id
        )

        return self._get_row_for_section(title, section_id, list_item_id)

    def _get_row_for_section(self, section_title, section_id, list_item_id=None):
        section_status = self._progress_store.get_section_status(
            section_id, list_item_id
        )

        return self.get_row_context_for_section(
            section_title,
            section_status,
            self.get_section_url(section_id, list_item_id),
        )

    def _get_rows(self, enabled_section_ids) -> List[Mapping[str, Union[str, List]]]:
        rows = []

        for section_id in enabled_section_ids:
            show_on_hub = self._schema.get_show_on_hub_for_section(section_id)

            if show_on_hub:
                section_title = self._schema.get_title_for_section(section_id)
                repeating_list = self._schema.get_repeating_list_for_section(section_id)

                if repeating_list:
                    for list_item_id in self._list_store[repeating_list].items:
                        rows.append(
                            self._get_row_for_repeating_section(
                                section_id, list_item_id
                            )
                        )
                else:
                    rows.append(self._get_row_for_section(section_title, section_id))

        return rows
