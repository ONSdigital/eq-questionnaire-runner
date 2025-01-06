from functools import cached_property
from typing import Any, Iterable, Mapping, Optional, Union

from flask import url_for
from flask_babel import lazy_gettext
from werkzeug.datastructures import ImmutableDict

from app.data_models import CompletionStatus
from app.questionnaire.location import SectionKey
from app.views.contexts import Context  # pylint: disable=cyclic-import

# Removing Pylint disable causes linting fail in GHA but not locally this issue has been raised here: https://github.com/pylint-dev/pylint/issues/9168


class HubContext(Context):
    SECTION_CONTENT_STATES = {
        CompletionStatus.COMPLETED: {
            "text": lazy_gettext("Completed"),
            "link": {
                "text": lazy_gettext("View answers"),
                "aria_label": lazy_gettext("View answers: {section_name}"),
            },
        },
        CompletionStatus.IN_PROGRESS: {
            "text": lazy_gettext("Partially completed"),
            "link": {
                "text": lazy_gettext("Continue with section"),
                "aria_label": lazy_gettext("Continue with section: {section_name}"),
            },
        },
        CompletionStatus.NOT_STARTED: {
            "text": lazy_gettext("Not started"),
            "link": {
                "text": lazy_gettext("Start section"),
                "aria_label": lazy_gettext("Start section: {section_name}"),
            },
        },
    }

    def __call__(
        self, survey_complete: bool, enabled_section_ids: Iterable[str]
    ) -> dict[str, Any]:
        rows = self._get_rows(enabled_section_ids)

        if survey_complete:
            submission_schema: Mapping = self._schema.get_submission()
            title = submission_schema.get("title") or lazy_gettext("Submit survey")
            submit_button = submission_schema.get("button") or lazy_gettext(
                "Submit survey"
            )
            guidance = submission_schema.get("guidance")
            warning = submission_schema.get("warning") or lazy_gettext(
                "You must submit this survey to complete it"
            )

        else:
            title = lazy_gettext("Choose another section to complete")
            submit_button = lazy_gettext("Continue")
            guidance = None
            warning = None

        return {
            "guidance": guidance,
            "rows": rows,
            "submit_button": submit_button,
            "title": title,
            "warning": warning,
        }

    def get_row_context_for_section(
        self,
        section_name: Optional[str],
        section_status: CompletionStatus,
        section_url: str,
        row_id: str,
    ) -> dict[str, Union[str, list]]:
        section_content = self.SECTION_CONTENT_STATES[section_status]
        context: dict = {
            "rowItems": [
                {
                    "rowTitle": section_name,
                    "rowTitleAttributes": {"data-qa": f"hub-row-{row_id}-title"},
                    "attributes": {"data-qa": f"hub-row-{row_id}-state"},
                    "valueList": [{"text": section_content["text"]}],
                    "actions": [
                        {
                            "text": section_content["link"]["text"],
                            "visuallyHiddenText": section_content["link"][
                                "aria_label"
                            ].format(section_name=section_name),
                            "url": section_url,
                            "attributes": {"data-qa": f"hub-row-{row_id}-link"},
                        }
                    ],
                }
            ]
        }

        if section_status in (CompletionStatus.COMPLETED,):
            context["rowItems"][0]["iconType"] = "check"

        return context

    @staticmethod
    def get_section_url(
        section_id: str, list_item_id: Optional[str], section_status: CompletionStatus
    ) -> str:
        if list_item_id:
            return url_for(
                "questionnaire.get_section",
                section_id=section_id,
                list_item_id=list_item_id,
            )

        return url_for("questionnaire.get_section", section_id=section_id)

    def _get_row_for_repeating_section(
        self, section_id: str, list_item_id: str, list_item_index: Optional[int]
    ) -> dict[str, Union[str, list]]:
        # Type ignore: section id will be valid and repeat will be present at this stage
        repeating_title: ImmutableDict = self._schema.get_repeating_title_for_section(section_id)  # type: ignore

        title: str = self._placeholder_renderer.render_placeholder(
            repeating_title,
            list_item_id,
        )

        return self._get_row_for_section(
            title, section_id, list_item_id, list_item_index
        )

    def _get_row_for_section(
        self,
        section_title: Optional[str],
        section_id: str,
        list_item_id: Optional[str] = None,
        list_item_index: Optional[int] = None,
    ) -> dict[str, Union[str, list]]:
        row_id = f"{section_id}-{list_item_index}" if list_item_index else section_id

        section_status = self._data_stores.progress_store.get_section_status(
            SectionKey(section_id, list_item_id)
        )

        return self.get_row_context_for_section(
            section_title,
            section_status,
            self.get_section_url(section_id, list_item_id, section_status),
            row_id,
        )

    def _get_rows(
        self, enabled_section_ids: Iterable[str]
    ) -> list[dict[str, Union[str, list]]]:
        rows: list[dict] = []

        for section_id in enabled_section_ids:
            show_on_hub = self._schema.get_show_on_hub_for_section(section_id)

            if show_on_hub:
                section_title = self._schema.get_title_for_section(section_id)
                repeating_list = self._schema.get_repeating_list_for_section(section_id)

                if repeating_list:
                    for list_item_index, list_item_id in enumerate(
                        self._data_stores.list_store[repeating_list].items, start=1
                    ):
                        rows.append(
                            self._get_row_for_repeating_section(
                                section_id, list_item_id, list_item_index
                            )
                        )
                else:
                    rows.append(self._get_row_for_section(section_title, section_id))

        return rows
